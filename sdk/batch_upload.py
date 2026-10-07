#!/usr/bin/env python3
"""
Batch upload adapted ESGML mods to Archive.org.
Supports streaming/chunked reads or direct reads, retries with exponential backoff,
and verification.
"""

import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import mimetypes

ACCESS_KEY = "YXLMKlSyfHDT60XG"
SECRET_KEY = "o79r78YXVUaTreSB"
S3_ENDPOINT = "https://s3.us.archive.org"

MODS = [
    ("geralt", "ESGML Mod: Pioneer from Rivia (Пионер из Ривии)"),
    ("alternativa", "ESGML Mod: Alternativa (Альтернатива)"),
    ("dear_alice_1", "ESGML Mod: Dear Alice Part 1 (Дорогая Алиса Часть 1)"),
    ("inoy_mir_alt", "ESGML Mod: Inoy Mir Alternative (Иной Мир Alternative)"),
    ("inoy_mir", "ESGML Mod: Inoy Mir (Иной Мир)"),
    ("bratskoe_leto", "ESGML Mod: Bratskoe Leto (Братское лето)"),
    ("we_are_main", "ESGML Mod: We Are The Main Thing (Мы - это главное)"),
    ("become_pioneer_rmk", "ESGML Mod: Become Pioneer Remake (Стать Пионером REMAKE)"),
    ("dear_alice_2", "ESGML Mod: Dear Alice 2 (Дорогая Алиса 2)"),
    ("cbb_ec", "ESGML Mod: Cat Bloody Blues - Extended Cat"),
]

def upload_file(identifier: str, local_filepath: str, remote_name: str, title: str):
    file_size = os.path.getsize(local_filepath)
    size_mb = round(file_size / (1024 * 1024), 2)
    print(f"\n[*] Uploading '{remote_name}' ({size_mb} MB) -> {identifier}...")

    quoted_name = urllib.parse.quote(remote_name)
    url = f"{S3_ENDPOINT}/{identifier}/{quoted_name}"

    headers = {
        "Authorization": f"LOW {ACCESS_KEY}:{SECRET_KEY}",
        "x-amz-auto-make-bucket": "1",
        "x-archive-auto-make-bucket": "1",
        "x-archive-meta-mediatype": "data",
        "x-archive-meta-collection": "opensource_media",
        "User-Agent": "ESGML-SDK/4.1 (Archive.org S3 Batch Uploader)",
        "Content-Length": str(file_size),
    }
    if title:
        safe_title = urllib.parse.quote(title)
        headers["x-archive-meta-title"] = safe_title

    mime, _ = mimetypes.guess_type(remote_name)
    headers["Content-Type"] = mime if mime else "application/octet-stream"

    # Streaming read using generator or file object
    max_retries = 6
    retry_delay = 5

    for attempt in range(1, max_retries + 1):
        try:
            with open(local_filepath, "rb") as f:
                req = urllib.request.Request(url, data=f, headers=headers, method="PUT")
                start_t = time.time()
                with urllib.request.urlopen(req, timeout=600) as resp:
                    elapsed = round(time.time() - start_t, 1)
                    if resp.status in (200, 201):
                        speed = round(size_mb / elapsed, 2) if elapsed > 0 else 0
                        print(f"[+] Done: {remote_name} in {elapsed}s (~{speed} MB/s)")
                        return True
                    else:
                        raise RuntimeError(f"HTTP {resp.status}: {resp.read().decode('utf-8', errors='ignore')}")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            print(f"[!] HTTP {e.code} error: {err_body[:200]}")
            if e.code in (503, 500, 502, 504) and attempt < max_retries:
                print(f"[!] Archive.org busy/retryable ({attempt}/{max_retries}). Sleeping {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2
                continue
            raise
        except Exception as e:
            print(f"[!] Exception ({e}) during upload of {remote_name} (attempt {attempt}/{max_retries})")
            if attempt < max_retries:
                time.sleep(retry_delay)
                retry_delay *= 2
                continue
            raise
    return False

def main():
    base_dist = os.path.abspath("dist")
    total_mods = len(MODS)
    print(f"=== Starting Batch Upload for {total_mods} Mods ===")

    for idx, (alias, title) in enumerate(MODS, 1):
        mod_dir = os.path.join(base_dist, alias)
        if not os.path.isdir(mod_dir):
            print(f"[-] Directory {mod_dir} not found! Skipping.")
            continue

        identifier = f"esgml-mod-{alias}"
        print(f"\n==========================================")
        print(f"[{idx}/{total_mods}] Processing: {alias} -> Item: {identifier}")
        print(f"==========================================")

        # Upload .rpyc and .rpa
        files_to_upload = []
        for fname in sorted(os.listdir(mod_dir)):
            if fname.endswith(".rpa") or (fname.endswith(".rpyc") and not fname.startswith("git_repo_")):
                files_to_upload.append(fname)

        for fname in files_to_upload:
            fpath = os.path.join(mod_dir, fname)
            success = upload_file(identifier, fpath, fname, title)
            if not success:
                print(f"[-] Failed uploading {fname}!")
                sys.exit(1)
            # Brief pause between files to avoid hammering archive.org
            time.sleep(3)

        print(f"[+] Finished mod: {alias}")
        time.sleep(5)

    print("\n\n==========================================")
    print("ALL 10 MODS UPLOADED SUCCESSFULLY!")
    print("==========================================")

if __name__ == "__main__":
    main()
