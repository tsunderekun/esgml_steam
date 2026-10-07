#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.abspath('sdk'))
from core.adapter import ModAdapter

BATCH = [
    ('2396824933', 'cbb_ec'),
    ('3008278992', 'dear_alice_2'),
    ('1270311946', 'inoy_mir'),
    ('743161904',  'we_are_main'),
    ('1795592911', 'geralt'),
    ('1419916523', 'inoy_mir_alt'),
    ('1631538437', 'alternativa'),
    ('2801507628', 'become_pioneer_rmk'),
    ('2520468168', 'bratskoe_leto'),
    ('2682369965', 'dear_alice_1'),
]

adapter = ModAdapter()
base_src = r'E:\ANALGAYPORNSTEAM\steamapps\workshop\content\331470'
print("=== Starting Re-adaptation of All 10 Mods with Video/Case/Syntax Fixes ===")

for wid, alias in BATCH:
    src_dir = os.path.join(base_src, wid)
    out_dir = os.path.join('dist', alias)
    print(f"\n[*] Processing: {alias} (Workshop ID: {wid})...")
    ok, res = adapter.adapt(src_dir, out_dir, alias=alias)
    if not ok:
        print(f"[-] ERROR adapting {alias}: {res}")
        sys.exit(1)
    rpa_path = res["rpa_file"]
    size_mb = round(os.path.getsize(rpa_path) / (1024 * 1024), 2)
    print(f"[+] SUCCESS {alias}: RPA = {os.path.basename(rpa_path)} ({size_mb} MB)")

print("\n\n==========================================")
print("ALL 10 MODS ADAPTED SUCCESSFULLY WITH ALL FIXES!")
print("==========================================")
