"""
ESGML SDK - Full Mod Adaptation Pipeline
Converts a Steam Workshop or local Everlasting Summer mod into an ESGML-compliant package.
Zero mandatory dependencies.
"""

import os
import shutil
import re
from typing import Optional, Tuple, Callable
from .rpa import RPAArchive
from .rpyc import RPYCTool
from .scanner import ModScanner, ModMetadata


class ModAdapter:
    """Adapts arbitrary ES mods into ESGML format."""

    def __init__(self, renpy_python_path=None, game_dir=None):
        self.rpa = RPAArchive()
        self.rpyc = RPYCTool(renpy_python_path=renpy_python_path, game_dir=game_dir)

    def adapt(
        self,
        mod_source_path: str,
        output_dir: str,
        alias: Optional[str] = None,
        custom_title: Optional[str] = None,
        custom_desc: Optional[str] = None,
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> Tuple[bool, dict]:
        """
        Execute full adaptation pipeline.
        Returns (success, result_dict).
        """
        def report(msg, pct):
            if progress_callback:
                progress_callback(msg, pct)

        report("Сканирование структуры мода...", 0.1)
        meta = ModScanner.scan(mod_source_path)
        if not meta.is_valid_mod:
            return False, {"error": "Папка не содержит распознаваемого мода: " + "; ".join(meta.notes)}

        # Resolve alias
        if not alias:
            raw_alias = meta.start_label or os.path.basename(meta.inner_mod_dir)
            alias = re.sub(r'[^a-zA-Z0-9_]', '', raw_alias).lower()
            if not alias or alias == "mods":
                alias = "mod_" + (meta.workshop_id or "custom")

        title = custom_title or meta.title
        desc = custom_desc or meta.description

        os.makedirs(output_dir, exist_ok=True)

        rpa_filename = f"git_{alias}_res.rpa"
        rpa_out_path = os.path.join(output_dir, rpa_filename)

        base_rpy_name = f"git_{alias}_base.rpy"
        base_rpy_path = os.path.join(output_dir, base_rpy_name)
        base_rpyc_path = os.path.join(output_dir, f"git_{alias}_base.rpyc")

        # Determine whether scripts use paths prefixed with 'mods/'
        scripts_use_mods_prefix = False
        for sfile in meta.script_files:
            if sfile.endswith(".rpy"):
                try:
                    with open(sfile, "r", encoding="utf-8", errors="ignore") as f:
                        if re.search(r'["\']mods/[^"\']+', f.read()):
                            scripts_use_mods_prefix = True
                            break
                except Exception:
                    pass
            elif sfile.endswith(".rpyc"):
                try:
                    with open(sfile, "rb") as f:
                        if b'mods/' in f.read():
                            scripts_use_mods_prefix = True
                            break
                except Exception:
                    pass

        base_dir_for_assets = meta.source_dir if scripts_use_mods_prefix else meta.inner_mod_dir

        # Detect if script references 'mods/<subfolder>/...' but source directory doesn't have 'mods/' folder (e.g. 1631538437 / alternativa)
        prefix_to_prepend = ""
        if scripts_use_mods_prefix and not os.path.isdir(os.path.join(meta.source_dir, "mods")):
            for sfile in meta.script_files:
                if sfile.endswith(".rpy"):
                    try:
                        with open(sfile, "r", encoding="utf-8", errors="ignore") as f:
                            m = re.search(r'["\'](mods/[^/\'"]+)/', f.read())
                            if m:
                                prefix_to_prepend = m.group(1)
                                break
                    except Exception:
                        pass

        # 1. Pack media assets into RPA
        report("Упаковка медиа-ресурсов в RPA архив...", 0.3)
        files_to_pack = []
        for asset_path in meta.asset_files:
            rel = os.path.relpath(asset_path, base_dir_for_assets).replace("\\", "/")
            if prefix_to_prepend:
                rel = f"{prefix_to_prepend}/{rel}"
            files_to_pack.append((rel, asset_path))

        if files_to_pack:
            self.rpa.pack(output_rpa_path=rpa_out_path, files_to_pack=files_to_pack, version=3)
        else:
            if meta.existing_rpa_files:
                shutil.copy2(meta.existing_rpa_files[0], rpa_out_path)
            else:
                dummy_file = os.path.join(output_dir, ".dummy")
                with open(dummy_file, "w") as df:
                    df.write("esgml")
                self.rpa.pack(output_rpa_path=rpa_out_path, files_to_pack=[(".dummy", dummy_file)], version=3)
                try: os.remove(dummy_file)
                except Exception: pass

        # 2. Generate Loader Script (git_<alias>_base.rpy)
        report("Генерация скрипта загрузчика...", 0.6)
        rpa_archive_id = f"git_{alias}_res"
        start_label = meta.start_label or alias
        loader_header = f"""# -*- coding: utf-8 -*-
# Адаптировано для ESGML (Everlasting Summer Git Mods Loader)

init 1 python:
    rpa_check_append('{rpa_filename}', '{rpa_archive_id}')
    rpa_check_varinst('{start_label}', u'{title} ESGML', '{rpa_filename}')
    for ch in ['soundd', 'avto', 'music2', 'ambience2', 'sound2', 'movie']:
        try:
            renpy.music.register_channel(ch, 'voice' if 'ambience' in ch else 'music' if 'music' in ch else 'sound', loop=False)
        except Exception:
            pass

"""
        if alias != start_label:
            loader_header += f"""label {alias}:
    jump {start_label}

"""
        # Append existing scripts
        with open(base_rpy_path, "w", encoding="utf-8") as out_rpy:
            out_rpy.write(loader_header)

            for script_file in meta.script_files:
                if script_file.endswith(".rpy"):
                    try:
                        with open(script_file, "r", encoding="utf-8", errors="ignore") as in_s:
                            content = in_s.read().replace('\ufeff', '')
                            # Comment out original mods[...] registration to prevent duplicate conflict
                            content = re.sub(r'^[ \t]*(\$?\s*mods\[[^\]]+\]\s*=[^\r\n]*)', r'    # \1', content, flags=re.MULTILINE)

                            # Auto-fix legacy Ren'Py syntax bugs in old mods:
                            # 1. Invalid play music_list[...] -> play music music_list[...]
                            content = re.sub(r'\bplay\s+music_list\[', r'play music music_list[', content)
                            # 2. Typos in show statements: 'show mt normal pioneer cleft' -> 'show mt normal pioneer at cleft'
                            content = re.sub(r'\bshow\s+mt\s+normal\s+pioneer\s+cleft\b', r'show mt normal pioneer at cleft', content)
                            # 3. Typos in show statements: 'show un shy swim pioneer' -> 'show un shy pioneer'
                            content = re.sub(r'\bshow\s+un\s+shy\s+swim\s+pioneer\b', r'show un shy pioneer', content)
                            # 4. Typos in show statements: 'show pi smile far' -> 'show pi smile'
                            content = re.sub(r'\bshow\s+pi\s+smile\s+far\b', r'show pi smile', content)
                            # 5. Russian typo in scene: 'scene bg unyy то with' -> 'scene bg unyy with'
                            content = re.sub(r'\bscene\s+bg\s+unyy\s+то\s+with\b', r'scene bg unyy with', content)

                            out_rpy.write(f"\n# --- Source: {os.path.basename(script_file)} ---\n")
                            out_rpy.write(content)
                            out_rpy.write("\n")
                    except Exception:
                        pass
                elif script_file.endswith(".rpyc"):
                    # Copy standalone rpyc if needed or let Ren'Py compile base
                    pass

        # 3. Compile base script to .rpyc
        report("Компиляция скрипта в .rpyc...", 0.8)
        compile_ok, comp_msg = self.rpyc.compile(base_rpy_path, base_rpyc_path)
        if not os.path.exists(base_rpyc_path):
            # If engine compile didn't produce separate file, copy if auto-generated
            auto_c = base_rpy_path + "c"
            if os.path.exists(auto_c):
                shutil.move(auto_c, base_rpyc_path)

        # 4. Generate Previews (480x270)
        report("Подготовка скриншотов карточки мода...", 0.9)
        previews_generated = []
        for i in range(1, 4):
            preview_filename = f"{alias} ({i}).png"
            preview_dest = os.path.join(output_dir, preview_filename)
            self._generate_preview_image(meta.preview_image, preview_dest, i, title)
            previews_generated.append(preview_filename)

        # 5. Generate Repo Snippet and Files
        snippet = f"""    git_easyrepo(
        '{alias}',
        ("https://<ВАШ_ХОСТИНГ>/{os.path.basename(base_rpyc_path)}",
         "https://<ВАШ_ХОСТИНГ>/{rpa_filename}"),
        '{title}',
        u'''{desc}'''
    )"""

        # Python / Ren'Py entry file template (rename and edit before dropping into repos/ folder)
        rpy_repo_file = os.path.join(output_dir, f"git_repo_{alias}.rpy.example")
        with open(rpy_repo_file, "w", encoding="utf-8") as rf:
            rf.write(f"# -*- coding: utf-8 -*-\n# Файл пользовательского репозитория для ESGML (настройте ссылки и поместите в папку repos/)\n\ninit 5 python:\n{snippet}\n")

        # JSON manifest (drop directly into repos/ folder)
        import json as _json
        json_repo_file = os.path.join(output_dir, f"{alias}.json")
        json_data = [
            {
                "id": alias,
                "name": title,
                "desc": desc,
                "links": [
                    f"https://<ВАШ_ХОСТИНГ>/{os.path.basename(base_rpyc_path)}",
                    f"https://<ВАШ_ХОСТИНГ>/{rpa_filename}"
                ]
            }
        ]
        with open(json_repo_file, "w", encoding="utf-8") as jf:
            _json.dump(json_data, jf, ensure_ascii=False, indent=2)

        snippet_file = os.path.join(output_dir, "repo_entry.py")
        with open(snippet_file, "w", encoding="utf-8") as sf:
            sf.write(snippet)

        report("Адаптация успешно завершена!", 1.0)

        return True, {
            "alias": alias,
            "title": title,
            "rpa_file": rpa_out_path,
            "base_rpy": base_rpy_path,
            "base_rpyc": base_rpyc_path,
            "rpy_repo_file": rpy_repo_file,
            "json_repo_file": json_repo_file,
            "previews": previews_generated,
            "repo_snippet": snippet,
            "snippet_file": snippet_file
        }

    def _generate_preview_image(self, src_img_path, dest_img_path, index, title):
        """Create a 480x270 PNG preview image."""
        try:
            import cv2
            if src_img_path and os.path.isfile(src_img_path):
                img = cv2.imread(src_img_path)
                if img is not None:
                    resized = cv2.resize(img, (480, 270), interpolation=cv2.INTER_AREA)
                    cv2.imwrite(dest_img_path, resized)
                    return
        except Exception:
            pass

        # Zero-dependency fallback: create clean minimalist 480x270 BMP/PNG
        # Let's create an uncompressed 24-bit BMP (Ren'Py supports BMP/PNG natively)
        self._write_solid_bmp(dest_img_path, 480, 270, (40 + index * 15, 30 + index * 10, 50))

    @staticmethod
    def _write_solid_bmp(filepath, width, height, color_rgb):
        """Writes a simple 24-bit uncompressed BMP image without external libraries."""
        r, g, b = color_rgb
        row_size = (width * 3 + 3) & ~3
        image_size = row_size * height
        file_size = 54 + image_size

        # BMP Header
        header = bytearray(54)
        header[0:2] = b'BM'
        header[2:6] = file_size.to_bytes(4, 'little')
        header[10:14] = (54).to_bytes(4, 'little') # pixel data offset
        header[14:18] = (40).to_bytes(4, 'little') # DIB header size
        header[18:22] = width.to_bytes(4, 'little')
        header[22:26] = height.to_bytes(4, 'little')
        header[26:28] = (1).to_bytes(2, 'little')  # color planes
        header[28:30] = (24).to_bytes(2, 'little') # bits per pixel
        header[34:38] = image_size.to_bytes(4, 'little')

        row = bytearray(row_size)
        for x in range(width):
            row[x * 3] = b
            row[x * 3 + 1] = g
            row[x * 3 + 2] = r

        with open(filepath, "wb") as f:
            f.write(header)
            for _ in range(height):
                f.write(row)
