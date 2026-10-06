#!/usr/bin/env python3
"""
ESGML SDK - Internet Archive (archive.org) Direct Uploader
Uploads adapted ESGML mod packages directly to archive.org via S3-compatible API.
Zero external libraries required.
"""

import os
import sys
import urllib.request
import urllib.error
import urllib.parse
import argparse
import mimetypes


class ArchiveOrgUploader:
    """Uploads files to Internet Archive (archive.org) via S3 REST API."""

    S3_ENDPOINT = "https://s3.us.archive.org"

    def __init__(self, access_key: str, secret_key: str):
        self.access_key = access_key.strip()
        self.secret_key = secret_key.strip()

    def upload_file(self, identifier: str, local_filepath: str, remote_filename: str = None, title: str = None) -> str:
        """
        Uploads a single file to archive.org item.
        Returns the direct permanent download URL.
        """
        if not os.path.isfile(local_filepath):
            raise FileNotFoundError(f"File not found: {local_filepath}")

        remote_name = remote_filename or os.path.basename(local_filepath)
        quoted_name = urllib.parse.quote(remote_name)
        url = f"{self.S3_ENDPOINT}/{identifier}/{quoted_name}"

        file_size = os.path.getsize(local_filepath)
        print(f"[*] Загрузка '{remote_name}' ({round(file_size/(1024*1024), 2)} МБ) на archive.org...")

        headers = {
            "Authorization": f"LOW {self.access_key}:{self.secret_key}",
            "x-amz-auto-make-bucket": "1",
            "x-archive-auto-make-bucket": "1",
            "x-archive-meta-mediatype": "data",
            "x-archive-meta-collection": "opensource_media",
            "User-Agent": "ESGML-SDK/4.1 (Archive.org S3 Uploader)",
        }
        if title:
            headers["x-archive-meta-title"] = title

        mime, _ = mimetypes.guess_type(remote_name)
        if mime:
            headers["Content-Type"] = mime
        else:
            headers["Content-Type"] = "application/octet-stream"

        with open(local_filepath, "rb") as f:
            data = f.read()

        max_retries = 5
        retry_delay = 5

        for attempt in range(1, max_retries + 1):
            req = urllib.request.Request(url, data=data, headers=headers, method="PUT")
            try:
                with urllib.request.urlopen(req, timeout=180) as resp:
                    if resp.status in (200, 201):
                        download_url = f"https://archive.org/download/{identifier}/{remote_name}"
                        print(f"[+] Загружено успешно: {download_url}")
                        return download_url
                    else:
                        raise RuntimeError(f"HTTP {resp.status}: {resp.read().decode('utf-8', errors='ignore')}")
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="ignore")
                if e.code == 503 and "SlowDown" in err_body and attempt < max_retries:
                    print(f"[!] Archive.org вернул 503 Slow Down (очередь перегружена). Ожидание {retry_delay} сек перед повтором ({attempt}/{max_retries})...")
                    import time
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                raise RuntimeError(f"HTTP {e.code}: {err_body}")
            except Exception as e:
                if attempt < max_retries:
                    import time
                    print(f"[!] Сбой сети ({e}). Ожидание {retry_delay} сек перед повтором ({attempt}/{max_retries})...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                raise

    def upload_mod_package(self, identifier: str, mod_dist_dir: str, title: str = None) -> dict:
        """Uploads mod assets in mod_dist_dir to archive.org and returns direct URLs."""
        results = {}
        files_to_upload = []

        # Only upload actual mod assets: .rpa packages, mod compiled .rpyc (not repo files), and previews
        for f in sorted(os.listdir(mod_dist_dir)):
            if f.endswith(".rpa") or f.endswith((".png", ".jpg")):
                files_to_upload.append(os.path.join(mod_dist_dir, f))
            elif f.endswith(".rpyc") and not f.startswith("git_repo_"):
                files_to_upload.append(os.path.join(mod_dist_dir, f))

        for fpath in files_to_upload:
            name = os.path.basename(fpath)
            url = self.upload_file(identifier, fpath, remote_filename=name, title=title)
            results[name] = url

        return results


def main():
    parser = argparse.ArgumentParser(description="Загрузка мода ESGML на archive.org")
    parser.add_argument("dist_dir", help="Папка со скомпилированным модом (dist/...)")
    parser.add_argument("--item", required=True, help="Уникальный идентификатор предмета на archive.org (латиница и дефисы, например: esgml-sim-mod)")
    parser.add_argument("--title", default="Everlasting Summer ESGML Mod", help="Название предмета")
    parser.add_argument("--access-key", help="S3 Access Key (из https://archive.org/account/s3.php)")
    parser.add_argument("--secret-key", help="S3 Secret Key (из https://archive.org/account/s3.php)")

    args = parser.parse_args()

    access_key = args.access_key or os.environ.get("IA_ACCESS_KEY")
    secret_key = args.secret_key or os.environ.get("IA_SECRET_KEY")

    if not access_key or not secret_key:
        print("[-] Ошибка: Требуются S3 ключи archive.org.")
        print("    Получите их бесплатно за 30 секунд: https://archive.org/account/s3.php")
        print("    И укажите флаги: --access-key <KEY> --secret-key <SECRET>")
        sys.exit(1)

    uploader = ArchiveOrgUploader(access_key, secret_key)
    print(f"[*] Загрузка пакета из '{args.dist_dir}' в элемент '{args.item}'...")
    res = uploader.upload_mod_package(args.item, args.dist_dir, title=args.title)

    print("\n[+] ВСЕ ФАЙЛЫ УСПЕШНО ЗАГРУЖЕНЫ НА ARCHIVE.ORG:")
    for name, url in res.items():
        print(f"    {name} -> {url}")


if __name__ == "__main__":
    main()
