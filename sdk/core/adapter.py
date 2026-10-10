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
        custom_start_label: Optional[str] = None,
        custom_preview_image: Optional[str] = None,
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

        if custom_preview_image and os.path.isfile(custom_preview_image):
            meta.preview_image = custom_preview_image

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

        # Pack compiled .rpyc files that do not have .rpy sources (e.g. standalone bytecode mods)
        for sfile in meta.script_files:
            if sfile.endswith(".rpyc"):
                base_no_ext = sfile[:-1]
                if not os.path.exists(base_no_ext):
                    rel = os.path.relpath(sfile, base_dir_for_assets).replace("\\", "/")
                    if prefix_to_prepend:
                        rel = f"{prefix_to_prepend}/{rel}"
                    files_to_pack.append((rel, sfile))

        # Inject missing assets / fallbacks to prevent runtime IOError
        files_to_pack = self._inject_missing_asset_fallbacks(alias, meta, base_dir_for_assets, prefix_to_prepend, files_to_pack, output_dir)

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
        start_label = custom_start_label or meta.start_label or alias
        safe_title = title.replace('\\', '\\\\').replace("'", "\\'")
        loader_header = f"""# -*- coding: utf-8 -*-
# Адаптировано для ESGML (Everlasting Summer Git Mods Loader)

init -999 python:
    try:
        import renpy.audio.music as _r_music
        if not getattr(_r_music, '_esgml_patched', False):
            _orig_m_play = _r_music.play
            def _safe_m_play(filenames, *args, **kwargs):
                if filenames is not None and not isinstance(filenames, (basestring if 'basestring' in globals() else (str, bytes), list, tuple)):
                    return
                return _orig_m_play(filenames, *args, **kwargs)
            _r_music.play = _safe_m_play
            _r_music._esgml_patched = True
    except Exception:
        pass

    try:
        import renpy.exports as _renpy_exp
        _dis_func = getattr(_renpy_exp, 'Dissolve', None) or globals().get('Dissolve')
        if _dis_func:
            for _d_sec in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
                _d_name = 'dissolve%d' % _d_sec
                if _d_name not in globals():
                    globals()[_d_name] = _dis_func(float(_d_sec))
            if 'dissolve_fast' not in globals():
                globals()['dissolve_fast'] = _dis_func(0.2)
    except Exception:
        pass

    try:
        if 'Snow' not in globals():
            def Snow(image, max_particles=90, *args, **kwargs):
                if 'SnowBlossom' in globals():
                    return SnowBlossom(image, count=max_particles)
                elif hasattr(renpy.store, 'SnowBlossom'):
                    return renpy.store.SnowBlossom(image, count=max_particles)
                return Null()
    except Exception:
        pass

define -999 dissolve1 = Dissolve(1.0)
define -999 dissolve2 = Dissolve(2.0)
define -999 dissolve3 = Dissolve(3.0)
define -999 dissolve4 = Dissolve(4.0)
define -999 dissolve5 = Dissolve(5.0)
define -999 dissolve_fast = Dissolve(0.2)
define -999 big_dis = Dissolve(5.0)
define -999 dis = Dissolve(0.5)
define -999 diss = Dissolve(0.5)

init 1 python:
    rpa_check_append('{rpa_filename}', '{rpa_archive_id}')
    rpa_check_varinst('{start_label}', u'{safe_title} ESGML', '{rpa_filename}')
    try:
        for _d_sec in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
            _d_name = 'dissolve%d' % _d_sec
            if _d_name not in globals() and 'Dissolve' in globals():
                globals()[_d_name] = Dissolve(float(_d_sec))
        if 'dissolve_fast' not in globals() and 'Dissolve' in globals():
            globals()['dissolve_fast'] = Dissolve(0.2)
    except Exception:
        pass
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
                bname = os.path.basename(script_file)
                if script_file.endswith(".rpy") and not bname.startswith(".") and not bname.startswith("._"):
                    try:
                        with open(script_file, "r", encoding="utf-8", errors="ignore") as in_s:
                            content = in_s.read().replace('\ufeff', '')
                            # Comment out original mods[...] registration to prevent duplicate conflict, adding pass only if indented to prevent empty python blocks
                            def _comment_mods(m):
                                indent = m.group(1)
                                line = m.group(2)
                                if indent:
                                    return f"{indent}# {line}\n{indent}pass"
                                else:
                                    return f"# {line}"

                            content = re.sub(r'^([ \t]*)(\$?[ \t]*mods\s*\[[^\]]+\][ \t]*=[^\r\n]*)', _comment_mods, content, flags=re.MULTILINE)

                            # Auto-fix legacy Ren'Py syntax bugs in old mods:
                            # 1. Invalid play music_list[...] -> play music music_list[...]
                            content = re.sub(r'\bplay\s+music_list\[', r'play music music_list[', content)
                            # 2. Typos in show statements:
                            content = re.sub(r'\bshow\s+mt\s+normal\s+pioneer\s+cleft\b', r'show mt normal pioneer at cleft', content)
                            content = re.sub(r'\bshow\s+un\s+shy\s+swim\s+pioneer\b', r'show un shy pioneer', content)
                            content = re.sub(r'\bshow\s+pi\s+smile\s+far\b', r'show pi smile', content)
                            content = re.sub(r'\bscene\s+bg\s+unyy\s+то\s+with\b', r'scene bg unyy with', content)
                            # 3. Typo wuth -> with
                            content = re.sub(r'\bwuth\b', 'with', content)
                            # 4. Invalid hat attribute on mt ... panama pioneer
                            content = re.sub(r'\bshow\s+mt\s+([a-z0-9_]+)\s+panama\s+pioneer\s+hat\b', r'show mt \1 panama pioneer', content)
                            # 5. Invalid window dissolve attribute
                            content = re.sub(r'\bshow\s+sh\s+rage\s+window\s+dissolve\b', 'show sh rage with dissolve', content)
                            # 6. Trailing dots in filenames
                            content = re.sub(r'plastinki\.ogg\.', 'plastinki.ogg', content)
                            content = re.sub(r'boris_kukoba_da2\.ogg\.', 'boris_kukoba_da2.ogg', content)
                            # 7. Audio variable collisions with Character objects
                            if alias == 'dear_alice_1':
                                content = re.sub(r'(\$?\s*)miku(\s*=\s*["\']mods/dear_alice/msc-snd/miku_flute\.ogg["\'])', r'\1da_miku_flute\2', content)
                                content = re.sub(r'\bplay\s+music\s+miku\b', 'play music da_miku_flute', content)
                            elif alias == 'alternativa':
                                content = re.sub(r'(\$?\s*)stel(\s*=\s*["\']mods/kurliksukks/sound/02938\.mp3["\'])', r'\1omsk_stel\2', content)
                                content = re.sub(r'\bplay\s+sound\s+stel\b', 'play sound omsk_stel', content)
                                content = re.sub(r'mods/kurliksukks/sound/555333\.mp3', 'mods/kurliksukks/sound/555888.mp3', content)
                            elif alias == 'become_pioneer_rmk':
                                content = re.sub(r'(\$?\s*)golos(\s*=\s*["\']mods/statpionerom/image/golos\.mp3["\'])', r'\1stat_golos\2', content)
                                content = re.sub(r'\bplay\s+music\s+golos\b', 'play music stat_golos', content)
                            elif alias == 'serdcebienie':
                                if os.path.basename(script_file) == 'hb_d2.rpy':
                                    content = re.sub(r'(?m)^ {10}', '', content)

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
            import numpy as np
            if src_img_path and os.path.isfile(src_img_path):
                buf = np.fromfile(src_img_path, dtype=np.uint8)
                img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
                if img is not None:
                    resized = cv2.resize(img, (480, 270), interpolation=cv2.INTER_AREA)
                    cv2.imencode('.png', resized)[1].tofile(dest_img_path)
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

    def _inject_missing_asset_fallbacks(self, alias, meta, base_dir_for_assets, prefix_to_prepend, files_to_pack, output_dir):
        """
        Scans scripts for referenced assets that are missing on disk,
        and injects known assets (e.g. 18+ CGs) or dummy fallbacks into files_to_pack.
        """
        temp_dir = os.path.join(output_dir, "_injected_assets")
        os.makedirs(temp_dir, exist_ok=True)

        existing_norm = {rel.lower(): (rel, src) for rel, src in files_to_pack}

        # 1. 18+ CGs commonly expected by mods like inoy_mir and bratskoe_leto
        hentai_cg_dir = r"E:\ANALGAYPORNSTEAM\steamapps\workshop\content\331470\2758131977\mods\ES_18+\cg"
        if os.path.isdir(hentai_cg_dir):
            cgs = [
                ("d2_mt_undressed.jpg", "images/cg/d2_mt_undressed.jpg"),
                ("d2_mt_undressed.jpg", "cg/d2_mt_undressed.jpg"),
                ("d2_mt_undressed_2.jpg", "images/cg/d2_mt_undressed_2.jpg"),
                ("d2_mt_undressed_2.jpg", "cg/d2_mt_undressed_2.jpg"),
                ("d3_sl_bathhouse.jpg", "images/cg/d3_sl_bathhouse.jpg"),
                ("d3_sl_bathhouse.jpg", "cg/d3_sl_bathhouse.jpg"),
            ]
            for src_cg_name, target_rel in cgs:
                src_cg_path = os.path.join(hentai_cg_dir, src_cg_name)
                if os.path.isfile(src_cg_path) and target_rel.lower() not in existing_norm:
                    files_to_pack.append((target_rel, src_cg_path))
                    existing_norm[target_rel.lower()] = (target_rel, src_cg_path)

        # 2. Alternativa: 555333.mp3 was misnamed as 555888.mp3 in source
        if alias == "alternativa":
            target_rel = "mods/kurliksukks/sound/555333.mp3"
            if target_rel.lower() not in existing_norm:
                for rel, src in list(files_to_pack):
                    if "555888.mp3" in rel:
                        files_to_pack.append((target_rel, src))
                        existing_norm[target_rel.lower()] = (target_rel, src)
                        break

        # 3. Dummy fallbacks for any remaining missing referenced assets
        silence_src = r"D:\SteamLibrary\steamapps\common\Everlasting Summer\renpy\common\_dl_silence.ogg"
        has_silence = os.path.isfile(silence_src)
        dummy_png_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82'
        dummy_mp3_bytes = (b'\xff\xfb\x90\x64' + b'\x00' * 413) * 10

        referenced_assets = set()
        for sfile in meta.script_files:
            if sfile.endswith(".rpy"):
                try:
                    with open(sfile, "r", encoding="utf-8", errors="ignore") as f:
                        matches = re.findall(r'["\']((?:mods/|images/)[^"\'\r\n]+\.(?:png|jpg|jpeg|mp3|ogg|wav|webm))["\']', f.read(), re.IGNORECASE)
                        for m in matches:
                            clean_m = re.sub(r'<[^>]+>', '', m).strip().replace('\\', '/')
                            referenced_assets.add(clean_m)
                except Exception:
                    pass

        dummy_counter = 0
        for ref in referenced_assets:
            if ref.lower() not in existing_norm:
                ext = os.path.splitext(ref)[1].lower()
                dummy_counter += 1
                fallback_file = os.path.join(temp_dir, f"fallback_{dummy_counter}{ext}")
                if ext in ('.mp3',):
                    with open(fallback_file, "wb") as fb:
                        fb.write(dummy_mp3_bytes)
                elif ext in ('.ogg', '.wav'):
                    if has_silence:
                        shutil.copy2(silence_src, fallback_file)
                    else:
                        with open(fallback_file, "wb") as fb:
                            fb.write(dummy_mp3_bytes)
                elif ext in ('.png', '.jpg', '.jpeg'):
                    with open(fallback_file, "wb") as fb:
                        fb.write(dummy_png_bytes)
                else:
                    continue

                files_to_pack.append((ref, fallback_file))
                existing_norm[ref.lower()] = (ref, fallback_file)

        return files_to_pack

