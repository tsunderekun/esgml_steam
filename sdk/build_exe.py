#!/usr/bin/env python3
"""
ESGML SDK - PyInstaller Build Script
Builds standalone .exe binaries for GUI and CLI tools.
Zero manual configuration needed.
"""

import sys
import os
import subprocess
import shutil

SDK_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SDK_DIR)
DIST_DIR = os.path.join(REPO_ROOT, "dist_bin")


def build_gui():
    print("[*] Сборка GUI приложения (esgml_gui.exe)...")
    gui_script = os.path.join(SDK_DIR, "esgml_gui.py")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "ESGML_Tool_GUI",
        "--distpath", DIST_DIR,
        "--workpath", os.path.join(DIST_DIR, "build_gui"),
        gui_script
    ]
    subprocess.check_call(cmd, cwd=REPO_ROOT)
    print("[+] GUI приложение успешно собрано в:", os.path.join(DIST_DIR, "ESGML_Tool_GUI"))


def build_cli():
    print("[*] Сборка CLI утилиты (esgml_cli.exe)...")
    cli_script = os.path.join(SDK_DIR, "esgml_cli.py")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--console",
        "--name", "esgml_cli",
        "--distpath", DIST_DIR,
        "--workpath", os.path.join(DIST_DIR, "build_cli"),
        cli_script
    ]
    subprocess.check_call(cmd, cwd=REPO_ROOT)
    print("[+] CLI утилита успешно собрана в:", os.path.join(DIST_DIR, "esgml_cli.exe"))


def main():
    os.makedirs(DIST_DIR, exist_ok=True)
    build_cli()
    build_gui()
    print("\n[+] ВСЕ БИНАРНИКИ УСПЕШНО СОБРАНЫ В ПАПКУ:", DIST_DIR)


if __name__ == "__main__":
    main()
