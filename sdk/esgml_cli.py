#!/usr/bin/env python3
"""
ESGML SDK - Command Line Interface (CLI)
Zero external dependencies.
Usage:
    python esgml_cli.py adapt <path_to_mod> [--alias <name>] [--out <dir>]
    python esgml_cli.py rpa-pack <folder> <output.rpa>
    python esgml_cli.py rpa-unpack <archive.rpa> <output_dir>
    python esgml_cli.py batch-scan <workshop_dir> [--check-steam] [--limit 50]
"""

import sys
import os
import argparse

# Add repository root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk.core.rpa import RPAArchive
from sdk.core.rpyc import RPYCTool
from sdk.core.scanner import ModScanner
from sdk.core.adapter import ModAdapter
from sdk.core.steam_checker import SteamWorkshopChecker
from sdk.core.batch import BatchAnalyzer


def cmd_adapt(args):
    adapter = ModAdapter()
    print(f"[*] Адаптация мода: {args.path}")
    print(f"[*] Выходная папка: {args.out}")

    def on_progress(msg, pct):
        print(f"    [{int(pct*100):3d}%] {msg}")

    success, info = adapter.adapt(
        mod_source_path=args.path,
        output_dir=args.out,
        alias=args.alias,
        custom_title=args.title,
        custom_desc=args.desc,
        progress_callback=on_progress
    )

    if success:
        print("\n[+] УСПЕШНО АДАПТИРОВАНО!")
        print(f"    Алиас:        {info['alias']}")
        print(f"    Название:     {info['title']}")
        print(f"    RPA архив:    {info['rpa_file']}")
        print(f"    Скрипт базы:  {info['base_rpyc']}")
        print(f"    Превью:       {', '.join(info['previews'])}")
        print("\n--- Блок для вставки в git_default_repo.rpy ---")
        print(info['repo_snippet'])
        print("------------------------------------------------\n")
    else:
        print(f"\n[-] ОШИБКА: {info.get('error', 'Неизвестная ошибка')}")
        sys.exit(1)


def cmd_rpa_pack(args):
    archive = RPAArchive(key=int(args.key, 16) if args.key else 0xDEADBEEF, version=args.ver)
    print(f"[*] Упаковка '{args.folder}' в '{args.output}' (RPA v{args.ver})...")
    count = archive.pack(args.folder, args.output, verbose=args.verbose)
    print(f"[+] Упаковано {count} файлов в {args.output}")


def cmd_rpa_unpack(args):
    archive = RPAArchive()
    print(f"[*] Распаковка '{args.archive}' в '{args.output}'...")
    count = archive.unpack(args.archive, args.output, verbose=args.verbose)
    print(f"[+] Распаковано {count} файлов в {args.output}")


def cmd_rpa_list(args):
    archive = RPAArchive()
    files = archive.list_files(args.archive)
    print(f"[*] Файлы в архиве '{args.archive}' ({len(files)} шт.):")
    for f in files:
        print(f"    {f}")


def cmd_rpyc_info(args):
    tool = RPYCTool()
    info = tool.extract_strings_and_code(args.file)
    print(f"[*] Анализ файла: {args.file}")
    if info["mods"]:
        print("\n[+] Найдена регистрация в меню модов:")
        for k, v in info["mods"].items():
            print(f"    mods['{k}'] = {v}")
    if info["labels"]:
        print(f"\n[+] Найденные лейблы ({len(info['labels'])} шт.):")
        for lbl in info["labels"]:
            print(f"    label {lbl}:")


def cmd_rpyc_decompile(args):
    tool = RPYCTool()
    out = args.out or os.path.splitext(args.file)[0] + ".rpy"
    print(f"[*] Декомпиляция '{args.file}' -> '{out}'...")
    ok, msg = tool.decompile(args.file, out)
    if ok:
        print(f"[+] {msg}")
    else:
        print(f"[-] {msg}")


def cmd_steam_check(args):
    print(f"[*] Проверка Steam Workshop ID: {args.id}...")
    res = SteamWorkshopChecker.check_item(args.id)
    print(f"    Статус:  {res['status']}")
    if res['title']:
        print(f"    Название: {res['title']}")
    if res['error']:
        print(f"    Инфо:     {res['error']}")


def cmd_batch_scan(args):
    print(f"[*] Запуск массового анализа архива: {args.dir}")
    analyzer = BatchAnalyzer(args.dir)

    def on_progress(done, total, title):
        if done % 10 == 0 or done == total:
            print(f"    [{done}/{total}] Обработано... ({title[:30]})")

    summary = analyzer.analyze_archive(
        check_steam=args.check_steam,
        max_workers=args.workers,
        limit=args.limit,
        progress_callback=on_progress
    )

    print("\n" + "="*50)
    print(f"ИТОГИ АНАЛИЗА:")
    print(f"Всего проверено модов: {summary['total_scanned']}")
    print(f"🔥 УДАЛЕНО ИЗ STEAM:    {summary['deleted_count']}")
    print(f"Доступно в Steam:      {summary['active_count']}")
    print(f"Мусор / пустые:        {summary['junk_count']}")
    print("="*50 + "\n")

    if args.out_md:
        analyzer.export_markdown_report(summary, args.out_md)
        print(f"[+] Markdown отчёт сохранён: {args.out_md}")

    if args.out_csv:
        analyzer.export_csv_report(summary, args.out_csv)
        print(f"[+] CSV отчёт сохранён: {args.out_csv}")


def main():
    parser = argparse.ArgumentParser(description="ESGML SDK - Мощный набор инструментов для портирования модов 'Бесконечного лета'")
    subparsers = parser.add_subparsers(dest="command", help="Команда для выполнения")

    # adapt
    p_adapt = subparsers.add_parser("adapt", help="Полное портирование мода под ESGML (RPA + скрипт + превью)")
    p_adapt.add_argument("path", help="Путь к папке мода (Workshop ID или распакованный мод)")
    p_adapt.add_argument("--out", default="output", help="Выходная папка для готового пакета (по умолчанию: output)")
    p_adapt.add_argument("--alias", help="Уникальный идентификатор мода (латиница)")
    p_adapt.add_argument("--title", help="Название мода (если нужно переопределить)")
    p_adapt.add_argument("--desc", help="Описание мода")

    # rpa-pack
    p_pack = subparsers.add_parser("rpa-pack", help="Упаковать папку в RPA архив")
    p_pack.add_argument("folder", help="Входная папка с файлами")
    p_pack.add_argument("output", help="Выходной файл .rpa")
    p_pack.add_argument("--key", default="DEADBEEF", help="HEX-ключ шифрования (по умолчанию: DEADBEEF)")
    p_pack.add_argument("--ver", type=int, choices=[2, 3], default=3, help="Версия RPA (2 или 3)")
    p_pack.add_argument("-v", "--verbose", action="store_true", help="Подробный вывод")

    # rpa-unpack
    p_unpack = subparsers.add_parser("rpa-unpack", help="Распаковать RPA архив")
    p_unpack.add_argument("archive", help="Файл .rpa")
    p_unpack.add_argument("output", help="Папка назначения")
    p_unpack.add_argument("-v", "--verbose", action="store_true", help="Подробный вывод")

    # rpa-list
    p_list = subparsers.add_parser("rpa-list", help="Показать список файлов в RPA архиве")
    p_list.add_argument("archive", help="Файл .rpa")

    # rpyc-info
    p_rpyc_info = subparsers.add_parser("rpyc-info", help="Просмотреть метаданные и структуру .rpyc файла")
    p_rpyc_info.add_argument("file", help="Файл .rpyc")

    # rpyc-decompile
    p_rpyc_dec = subparsers.add_parser("rpyc-decompile", help="Декомпилировать .rpyc файл в .rpy")
    p_rpyc_dec.add_argument("file", help="Файл .rpyc")
    p_rpyc_dec.add_argument("--out", help="Выходной .rpy файл")

    # steam-check
    p_st = subparsers.add_parser("steam-check", help="Проверить статус предмета в Мастерской Steam")
    p_st.add_argument("id", help="Steam Workshop ID")

    # batch-scan
    p_batch = subparsers.add_parser("batch-scan", help="Массовый анализ локального архива Workshop с детектированием удалённых модов")
    p_batch.add_argument("dir", help="Корневая папка архива (содержащая цифровые папки ID)")
    p_batch.add_argument("--check-steam", action="store_true", help="Выполнять HTTP-проверку доступности в Steam")
    p_batch.add_argument("--limit", type=int, help="Ограничить количество проверяемых модов")
    p_batch.add_argument("--workers", type=int, default=6, help="Количество потоков для проверки")
    p_batch.add_argument("--out-md", default="workshop_report.md", help="Путь для Markdown отчёта")
    p_batch.add_argument("--out-csv", default="workshop_report.csv", help="Путь для CSV отчёта")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "adapt": cmd_adapt,
        "rpa-pack": cmd_rpa_pack,
        "rpa-unpack": cmd_rpa_unpack,
        "rpa-list": cmd_rpa_list,
        "rpyc-info": cmd_rpyc_info,
        "rpyc-decompile": cmd_rpyc_decompile,
        "steam-check": cmd_steam_check,
        "batch-scan": cmd_batch_scan
    }

    dispatch[args.command](args)


if __name__ == "__main__":
    main()
