"""
ESGML SDK - Batch Workshop Archive Scanner & Differential Analyzer
Scans local workshop archives, detects deleted mods vs active ones using batch Steam Web API.
Zero external dependencies.
"""

import os
import csv
import json
import time
from typing import List, Dict, Callable, Optional
from .scanner import ModScanner, ModMetadata
from .steam_checker import SteamWorkshopChecker


class BatchAnalyzer:
    """Scans thousands of workshop mods and produces categorized diffs."""

    def __init__(self, workshop_root_dir: str):
        self.workshop_root = os.path.abspath(workshop_root_dir)

    def list_mod_folders(self) -> List[str]:
        """List all valid mod subdirectories in the archive."""
        if not os.path.isdir(self.workshop_root):
            return []
        entries = []
        for d in os.listdir(self.workshop_root):
            full = os.path.join(self.workshop_root, d)
            if os.path.isdir(full) and d.isdigit():
                entries.append(full)
        return sorted(entries, key=lambda p: int(os.path.basename(p)))

    def analyze_archive(
        self,
        check_steam: bool = True,
        batch_size: int = 50,
        limit: Optional[int] = None,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> Dict[str, any]:
        """
        Scan all mods in archive and check Steam Workshop status via high-speed batch API.
        """
        folders = self.list_mod_folders()
        if limit:
            folders = folders[:limit]

        total = len(folders)
        results = []

        # 1. Local scan pass
        valid_mods_for_steam = []
        for idx, folder in enumerate(folders):
            meta = ModScanner.scan(folder)
            is_junk = (meta.total_size_bytes < 50 * 1024) and not meta.is_valid_mod

            item_id = meta.workshop_id or os.path.basename(folder)
            res = {
                "id": item_id,
                "folder": folder,
                "title": meta.title,
                "label": meta.start_label,
                "size_mb": round(meta.total_size_bytes / (1024 * 1024), 2),
                "scripts_count": len(meta.script_files),
                "assets_count": len(meta.asset_files),
                "has_rpa": len(meta.existing_rpa_files) > 0,
                "is_valid": meta.is_valid_mod,
                "is_junk": is_junk,
                "steam_status": "SKIPPED" if is_junk else "PENDING",
                "notes": "; ".join(meta.notes)
            }
            results.append(res)
            if not is_junk and item_id.isdigit():
                valid_mods_for_steam.append(item_id)

            if progress_callback and (idx % 25 == 0 or idx == total - 1):
                progress_callback(idx + 1, total, f"Сканирование локальных папок: {meta.title[:30]}")

        # 2. Batch Steam check pass
        if check_steam and valid_mods_for_steam:
            steam_dict = {}
            for i in range(0, len(valid_mods_for_steam), batch_size):
                chunk = valid_mods_for_steam[i:i + batch_size]
                chunk_res = SteamWorkshopChecker.check_batch(chunk)
                steam_dict.update(chunk_res)
                if progress_callback:
                    progress_callback(
                        min(i + batch_size, len(valid_mods_for_steam)),
                        len(valid_mods_for_steam),
                        f"Проверка в Steam API: {len(steam_dict)}/{len(valid_mods_for_steam)}"
                    )
                time.sleep(0.1)

            # Merge Steam results
            for r in results:
                if r["id"] in steam_dict:
                    st = steam_dict[r["id"]]
                    r["steam_status"] = st["status"]
                    if st.get("title") and r["title"].startswith("Workshop Mod #"):
                        r["title"] = st["title"]

        # Sort by ID
        results.sort(key=lambda x: int(x["id"]) if str(x["id"]).isdigit() else 0)

        deleted_mods = [r for r in results if r["steam_status"] in ("DELETED", "BANNED") and not r["is_junk"]]
        active_mods = [r for r in results if r["steam_status"] == "ACTIVE"]
        junk_mods = [r for r in results if r["is_junk"]]

        return {
            "total_scanned": total,
            "deleted_count": len(deleted_mods),
            "active_count": len(active_mods),
            "junk_count": len(junk_mods),
            "deleted_mods": deleted_mods,
            "active_mods": active_mods,
            "junk_mods": junk_mods,
            "all_results": results
        }

    @staticmethod
    def export_markdown_report(summary: Dict[str, any], report_path: str):
        """Export analysis report in GitHub-flavored Markdown."""
        lines = [
            "# Отчёт анализа архива модов Steam Workshop",
            f"**Дата проверки:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            "## Сводка",
            f"- **Всего проверено модов:** {summary['total_scanned']}",
            f"- **🔥 УДАЛЕНО ИЗ STEAM (Кандидаты для ESGML):** {summary['deleted_count']}",
            f"- **Доступно в Steam:** {summary['active_count']}",
            f"- **Мусорные / пустые папки:** {summary['junk_count']}\n",
            "## Список удалённых модов, сохранённых в архиве\n",
            "| Workshop ID | Название | Размер (МБ) | Стартовый лейбл | Скрипты | Ресурсы |",
            "|---|---|---|---|---|---|"
        ]

        for m in summary["deleted_mods"]:
            lines.append(
                f"| `{m['id']}` | {m['title']} | {m['size_mb']} MB | `{m['label']}` | {m['scripts_count']} | {m['assets_count']} |"
            )

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    @staticmethod
    def export_csv_report(summary: Dict[str, any], report_path: str):
        """Export analysis report in CSV format."""
        fieldnames = ["id", "title", "steam_status", "size_mb", "label", "scripts_count", "assets_count", "is_valid", "is_junk"]
        with open(report_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for row in summary["all_results"]:
                writer.writerow(row)
