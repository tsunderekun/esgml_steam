"""
ESGML SDK - Workshop & Local Mod Scanner
Analyzes mod directory structure, detects entry points, assets, and metadata.
Zero external dependencies.
"""

import os
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ModMetadata:
    source_dir: str
    inner_mod_dir: str
    workshop_id: Optional[str] = None
    title: str = "Unknown Mod"
    start_label: str = "start"
    description: str = ""
    author: str = ""
    preview_image: Optional[str] = None
    script_files: List[str] = field(default_factory=list)
    asset_files: List[str] = field(default_factory=list)
    existing_rpa_files: List[str] = field(default_factory=list)
    total_size_bytes: int = 0
    is_valid_mod: bool = False
    notes: List[str] = field(default_factory=list)


class ModScanner:
    """Scans and parses mod directories to extract metadata and categorize assets."""

    SCRIPT_EXTS = {".rpy", ".rpyc"}
    IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tga"}
    AUDIO_EXTS = {".mp3", ".ogg", ".wav", ".flac", ".opus", ".aiff"}
    VIDEO_EXTS = {".webm", ".mp4", ".ogv", ".avi", ".mkv"}
    FONT_EXTS = {".ttf", ".otf"}
    PREVIEW_NAMES = {"preview.jpg", "preview.png", "logo.jpg", "logo.png", "превью.jpg", "превью.png", "cover.jpg", "cover.png"}

    @classmethod
    def scan(cls, path: str) -> ModMetadata:
        """Scan a given path (workshop item or direct mod folder)."""
        abs_path = os.path.abspath(path)
        if not os.path.isdir(abs_path):
            return ModMetadata(
                source_dir=abs_path,
                inner_mod_dir=abs_path,
                is_valid_mod=False,
                notes=["Path does not exist or is not a directory."]
            )

        # Detect workshop ID from directory name if numeric
        dirname = os.path.basename(abs_path)
        workshop_id = dirname if dirname.isdigit() else None

        # Look for inner 'mods/<name>' folder
        inner_dir = abs_path
        mods_sub = os.path.join(abs_path, "mods")
        if os.path.isdir(mods_sub):
            rpy_in_mods = [f for f in os.listdir(mods_sub) if f.endswith(".rpy") or f.endswith(".rpyc")]
            if rpy_in_mods:
                inner_dir = mods_sub
            else:
                subs = [os.path.join(mods_sub, d) for d in os.listdir(mods_sub) if os.path.isdir(os.path.join(mods_sub, d))]
                sub_with_scripts = None
                for s in subs:
                    try:
                        if any(f.endswith(".rpy") or f.endswith(".rpyc") for f in os.listdir(s)):
                            sub_with_scripts = s
                            break
                    except Exception:
                        pass
                if sub_with_scripts:
                    inner_dir = sub_with_scripts
                elif subs:
                    inner_dir = subs[0]

        meta = ModMetadata(
            source_dir=abs_path,
            inner_mod_dir=inner_dir,
            workshop_id=workshop_id
        )

        # Gather files across entire mod source directory
        total_size = 0
        scripts = []
        assets = []
        rpas = []
        previews = []

        # Also check source_dir root for preview images
        for f in os.listdir(abs_path):
            fpath = os.path.join(abs_path, f)
            if os.path.isfile(fpath):
                f_lower = f.lower()
                if f_lower in cls.PREVIEW_NAMES:
                    previews.append(fpath)

        for root, _, files in os.walk(abs_path):
            for file in files:
                fpath = os.path.join(root, file)
                try:
                    fsize = os.path.getsize(fpath)
                except Exception:
                    fsize = 0
                total_size += fsize

                _, ext = os.path.splitext(file)
                ext = ext.lower()

                if ext in cls.SCRIPT_EXTS:
                    scripts.append(fpath)
                elif ext == ".rpa":
                    rpas.append(fpath)
                elif ext in cls.IMAGE_EXTS or ext in cls.AUDIO_EXTS or ext in cls.VIDEO_EXTS or ext in cls.FONT_EXTS:
                    assets.append(fpath)

                if file.lower() in cls.PREVIEW_NAMES and fpath not in previews:
                    previews.append(fpath)

        meta.total_size_bytes = total_size
        meta.script_files = scripts
        meta.asset_files = assets
        meta.existing_rpa_files = rpas
        if previews:
            meta.preview_image = previews[0]

        # Check validity
        if not scripts and not rpas:
            meta.is_valid_mod = False
            meta.notes.append("No scripts (.rpy/.rpyc) or .rpa archives found.")
            return meta

        meta.is_valid_mod = True

        # Extract title and start label from scripts
        cls._extract_metadata_from_scripts(meta)

        # If title is still default, try folder name or txt files
        if meta.title == "Unknown Mod":
            cls._extract_from_txt_or_folder(meta)

        return meta

    @classmethod
    def _extract_metadata_from_scripts(cls, meta: ModMetadata):
        """Parse scripts to find mods[...] registration and starting labels."""
        found_title = None
        found_label = None

        # Check .rpy files first (plaintext)
        rpy_files = [f for f in meta.script_files if f.endswith(".rpy")]
        for fpath in rpy_files:
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Search mods["..."] = ...
                # e.g.: mods["sam_start"] = u"{font=...}Саманта{/font}"
                match = re.search(r'mods\s*\[["\']([^"\']+)["\']\]\s*=\s*([^\r\n]+)', content)
                if match:
                    found_label = match.group(1).strip()
                    val = match.group(2).strip()
                    # Clean Ren'Py formatting tags: {font=...}, {color=...}, etc.
                    clean_title = re.sub(r'\{[^}]+\}', '', val)
                    clean_title = re.sub(r'^[uU]?["\']|["\']$', '', clean_title.strip())
                    if clean_title:
                        found_title = clean_title
                    break
            except Exception:
                continue

        # If not found in .rpy, search .rpyc files
        if not found_title or not found_label:
            rpyc_files = [f for f in meta.script_files if f.endswith(".rpyc")]
            for fpath in rpyc_files:
                try:
                    with open(fpath, "rb") as f:
                        raw = f.read()

                    # Find mods["..."] in bytecode strings
                    m = re.search(rb'mods\[[\'"]([a-zA-Z0-9_]+)[\'"]\]\s*=\s*([^\r\n\x00]+)', raw)
                    if m:
                        found_label = m.group(1).decode("utf-8", errors="ignore").strip()
                        raw_title = m.group(2).decode("utf-8", errors="ignore").strip()
                        clean = re.sub(r'\{[^}]+\}', '', raw_title)
                        clean = re.sub(r'^[uU]?[\'"]|[\'"]$', '', clean.strip())
                        if clean:
                            found_title = clean
                        break
                except Exception:
                    continue

        if found_title:
            meta.title = found_title
        if found_label:
            meta.start_label = found_label
        elif not meta.start_label:
            meta.start_label = os.path.basename(meta.inner_mod_dir).lower().replace(" ", "_")

    @classmethod
    def _extract_from_txt_or_folder(cls, meta: ModMetadata):
        """Fallback title extraction."""
        # Check text files in inner_dir or source_dir
        for d in (meta.inner_mod_dir, meta.source_dir):
            for f in os.listdir(d):
                if f.endswith(".txt") and not f.isdigit():
                    tpath = os.path.join(d, f)
                    try:
                        with open(tpath, "r", encoding="utf-8", errors="ignore") as tf:
                            lines = [line.strip() for line in tf if line.strip()]
                            if lines:
                                meta.title = lines[0]
                                if len(lines) > 1 and not meta.description:
                                    meta.description = "\n".join(lines[1:10])
                                return
                    except Exception:
                        pass

        # Fallback to inner folder basename
        base = os.path.basename(meta.inner_mod_dir)
        if base and base != "mods" and not base.isdigit():
            meta.title = base.replace("_", " ").title()
        elif meta.workshop_id:
            meta.title = "Workshop Mod #{}".format(meta.workshop_id)
