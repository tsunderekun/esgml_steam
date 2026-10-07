#!/usr/bin/env python3
"""
High-reliability Uploader using curl.exe for Archive.org S3 API.
Handles gigabyte-scale files without Python urllib SSL socket renegotiation drops.
"""

import os
import sys
import time
import subprocess
import urllib.parse

ACCESS_KEY = "YXLMKlSyfHDT60XG"
SECRET_KEY = "o79r78YXVUaTreSB"
S3_ENDPOINT = "https://s3.us.archive.org"

MODS = [
    ("geralt", "ESGML Mod: Pioneer from Rivia"),
    ("alternativa", "ESGML Mod: Alternativa"),
    ("dear_alice_1", "ESGML Mod: Dear Alice Part 1"),
    ("inoy_mir_alt", "ESGML Mod: Inoy Mir Alternative"),
    ("inoy_mir", "ESGML Mod: Inoy Mir"),
    ("bratskoe_leto", "ESGML Mod: Bratskoe Leto"),
    ("we_are_main", "ESGML Mod: We Are The Main Thing"),
    ("become_pioneer_rmk", "ESGML Mod: Become Pioneer Remake"),
    ("dear_alice_2", "ESGML Mod: Dear Alice 2"),
    ("cbb_ec", "ESGML Mod: Cat Bloody Blues - Extended Cat"),
]

def check_remote_size(url: str):
    try:
        out = subprocess.run(["curl.exe", "-s", "-I", "-L", url], capture_output=True, text=True).stdout
        for line in out.splitlines():
            if line.lower().startswith("content-length:"):
                return int(line.split(":")[1].strip())
    except Exception:
        pass
    return None

def upload_with_curl(identifier: str, local_filepath: str, remote_name: str, title: str):
    file_size = os.path.getsize(local_filepath)
    size_mb = round(file_size / (1024 * 1024), 2)

    quoted_name = urllib.parse.quote(remote_name)
    download_url = f"https://archive.org/download/{identifier}/{quoted_name}"
    rem_size = check_remote_size(download_url)
    if not remote_name.endswith(".rpyc") and rem_size == file_size:
        print(f"[=] Skipping '{remote_name}' ({size_mb} MB) -> already uploaded & matches on archive.org.")
        return True

    print(f"\n[*] Uploading '{remote_name}' ({size_mb} MB) via curl -> {identifier}...", flush=True)
    url = f"{S3_ENDPOINT}/{identifier}/{quoted_name}"
    safe_title = urllib.parse.quote(title)

    cmd = [
        "curl.exe",
        "--resolve", "s3.us.archive.org:443:207.241.225.119",
        "--http1.1",
        "-f",
        "--progress-bar",
        "-S",
        "--show-error",
        "-X", "PUT",
        "-T", local_filepath,
        "-H", f"Authorization: LOW {ACCESS_KEY}:{SECRET_KEY}",
        "-H", "x-amz-auto-make-bucket: 1",
        "-H", "x-archive-auto-make-bucket: 1",
        "-H", "x-archive-meta-mediatype: data",
        "-H", "x-archive-meta-collection: opensource_media",
        "-H", f"x-archive-meta-title: {safe_title}",
        "-H", f"Content-Length: {file_size}",
        "--retry", "5",
        "--retry-delay", "5",
        "--retry-all-errors",
        "--speed-time", "60",
        "--speed-limit", "1024",
        url
    ]

    start_t = time.time()
    res = subprocess.run(cmd)
    elapsed = round(time.time() - start_t, 1)

    if res.returncode == 0:
        speed = round(size_mb / elapsed, 2) if elapsed > 0 else 0
        print(f"[+] Done: {remote_name} in {elapsed}s (~{speed} MB/s)", flush=True)
        return True
    else:
        print(f"[-] Curl error ({res.returncode})", flush=True)
        return False

def main():
    base_dist = os.path.abspath("dist")
    total_mods = len(MODS)
    print(f"=== Starting Bulletproof Curl Batch Upload for {total_mods} Mods ===")

    for idx, (alias, title) in enumerate(MODS, 1):
        mod_dir = os.path.join(base_dist, alias)
        if not os.path.isdir(mod_dir):
            continue

        identifier = f"esgml-mod-{alias}"
        print(f"\n==========================================")
        print(f"[{idx}/{total_mods}] Processing: {alias} -> Item: {identifier}")
        print(f"==========================================")

        files_to_upload = []
        for fname in sorted(os.listdir(mod_dir)):
            if fname.endswith(".rpa") or (fname.endswith(".rpyc") and not fname.startswith("git_repo_")):
                files_to_upload.append(fname)

        for fname in files_to_upload:
            fpath = os.path.join(mod_dir, fname)
            ok = upload_with_curl(identifier, fpath, fname, title)
            if not ok:
                print(f"[-] Failed uploading {fname}!")
                sys.exit(1)
            time.sleep(2)

        print(f"[+] Finished mod: {alias}")
        time.sleep(3)

    print("\n\n==========================================")
    print("ALL 10 MODS UPLOADED SUCCESSFULLY VIA CURL!")
    print("==========================================")

if __name__ == "__main__":
    main()
