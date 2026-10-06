#!/usr/bin/env python3
"""
ESGML SDK - Graphical User Interface (GUI)
Built with native Tkinter. Zero external dependencies required.
"""

import sys
import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Add repository root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk.core.rpa import RPAArchive
from sdk.core.rpyc import RPYCTool
from sdk.core.scanner import ModScanner
from sdk.core.adapter import ModAdapter
from sdk.core.batch import BatchAnalyzer


class ESGMLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ESGML SDK v4.1 — Набор инструментов портирования модов 'Бесконечного лета'")
        self.geometry("960x680")
        self.minsize(800, 560)

        # Apply clean theme
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        self._create_widgets()

    def _create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Porting Single Mod
        self.tab_port = ttk.Frame(notebook)
        notebook.add(self.tab_port, text="🛠️ Портирование мода")
        self._build_port_tab(self.tab_port)

        # Tab 2: RPA Tool
        self.tab_rpa = ttk.Frame(notebook)
        notebook.add(self.tab_rpa, text="📦 RPA Архиватор")
        self._build_rpa_tab(self.tab_rpa)

        # Tab 3: RPYC Tool
        self.tab_rpyc = ttk.Frame(notebook)
        notebook.add(self.tab_rpyc, text="📜 RPYC Скрипты")
        self._build_rpyc_tab(self.tab_rpyc)

        # Tab 4: Workshop Analyzer
        self.tab_batch = ttk.Frame(notebook)
        notebook.add(self.tab_batch, text="📊 Анализ Workshop")
        self._build_batch_tab(self.tab_batch)

    # ---------------- TAB 1: MOD PORTING ----------------
    def _build_port_tab(self, parent):
        frame = ttk.LabelFrame(parent, text="Исходный мод", padding=12)
        frame.pack(fill=tk.X, padx=10, pady=6)

        ttk.Label(frame, text="Папка с модом (Workshop ID или распакованный):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.port_path_var = tk.StringVar()
        entry_path = ttk.Entry(frame, textvariable=self.port_path_var, width=65)
        entry_path.grid(row=1, column=0, sticky=tk.EW, padx=(0, 8), pady=2)
        ttk.Button(frame, text="Обзор...", command=self._browse_port_mod).grid(row=1, column=1)

        # Metadata fields
        meta_frame = ttk.LabelFrame(parent, text="Параметры адаптации", padding=12)
        meta_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        ttk.Label(meta_frame, text="Название мода:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.port_title_var = tk.StringVar()
        ttk.Entry(meta_frame, textvariable=self.port_title_var, width=50).grid(row=0, column=1, sticky=tk.W, pady=3)

        ttk.Label(meta_frame, text="Уникальный алиас (латиница):").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.port_alias_var = tk.StringVar()
        ttk.Entry(meta_frame, textvariable=self.port_alias_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=3)

        ttk.Label(meta_frame, text="Папка сохранения:").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.port_out_var = tk.StringVar(value=os.path.abspath("output"))
        out_box = ttk.Frame(meta_frame)
        out_box.grid(row=2, column=1, sticky=tk.EW, pady=3)
        ttk.Entry(out_box, textvariable=self.port_out_var, width=45).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        ttk.Button(out_box, text="Обзор...", command=self._browse_port_out).pack(side=tk.LEFT)

        ttk.Label(meta_frame, text="Описание мода:").grid(row=3, column=0, sticky=tk.NW, pady=3)
        self.port_desc_txt = tk.Text(meta_frame, height=4, width=55)
        self.port_desc_txt.grid(row=3, column=1, sticky=tk.EW, pady=3)

        # Progress and Action
        action_frame = ttk.Frame(parent, padding=8)
        action_frame.pack(fill=tk.X, padx=10, pady=4)

        self.port_btn = ttk.Button(action_frame, text="⚡ Адаптировать и собрать под ESGML", command=self._run_port_process)
        self.port_btn.pack(side=tk.LEFT, padx=6)

        self.port_status_lbl = ttk.Label(action_frame, text="Готов к работе", foreground="#555")
        self.port_status_lbl.pack(side=tk.LEFT, padx=10)

        # Output Log / Repo Snippet
        res_frame = ttk.LabelFrame(parent, text="Результат и строка для репозитория (git_easyrepo)", padding=10)
        res_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        self.port_snippet_txt = tk.Text(res_frame, height=7, font=("Consolas", 9))
        self.port_snippet_txt.pack(fill=tk.BOTH, expand=True)

    def _browse_port_mod(self):
        init_dir = r"E:\ANALGAYPORNSTEAM\steamapps\workshop\content\331470"
        if not os.path.exists(init_dir):
            init_dir = os.path.expanduser("~")
        path = filedialog.askdirectory(initialdir=init_dir, title="Выберите папку мода")
        if path:
            self.port_path_var.set(path)
            meta = ModScanner.scan(path)
            if meta.is_valid_mod:
                self.port_title_var.set(meta.title)
                self.port_alias_var.set(meta.start_label)
                self.port_desc_txt.delete("1.0", tk.END)
                self.port_desc_txt.insert("1.0", meta.description)
                self.port_status_lbl.config(
                    text=f"Найдено: {len(meta.script_files)} скриптов, {len(meta.asset_files)} файлов ресурсов"
                )

    def _browse_port_out(self):
        path = filedialog.askdirectory(title="Выберите папку назначения")
        if path:
            self.port_out_var.set(path)

    def _run_port_process(self):
        src = self.port_path_var.get().strip()
        if not src or not os.path.exists(src):
            messagebox.showerror("Ошибка", "Укажите существующую папку мода.")
            return

        out = self.port_out_var.get().strip()
        alias = self.port_alias_var.get().strip() or None
        title = self.port_title_var.get().strip() or None
        desc = self.port_desc_txt.get("1.0", tk.END).strip()

        self.port_btn.config(state=tk.DISABLED)
        self.port_status_lbl.config(text="Идёт адаптация...", foreground="#007acc")

        def worker():
            adapter = ModAdapter()
            def on_progress(msg, pct):
                self.port_status_lbl.config(text=f"[{int(pct*100)}%] {msg}")

            ok, res = adapter.adapt(
                mod_source_path=src,
                output_dir=out,
                alias=alias,
                custom_title=title,
                custom_desc=desc,
                progress_callback=on_progress
            )

            self.port_btn.config(state=tk.NORMAL)
            if ok:
                self.port_status_lbl.config(text="Успешно адаптировано!", foreground="#2e7d32")
                self.port_snippet_txt.delete("1.0", tk.END)
                self.port_snippet_txt.insert("1.0", res["repo_snippet"])
                messagebox.showinfo("Готово", f"Мод успешно собран в папку:\n{out}\n\nRPA: {os.path.basename(res['rpa_file'])}\nСкрипт: {os.path.basename(res['base_rpyc'])}")
            else:
                self.port_status_lbl.config(text="Ошибка адаптации", foreground="#d32f2f")
                messagebox.showerror("Ошибка", res.get("error", "Сбой адаптации"))

        threading.Thread(target=worker, daemon=True).start()

    # ---------------- TAB 2: RPA TOOL ----------------
    def _build_rpa_tab(self, parent):
        # Pack Section
        pack_frame = ttk.LabelFrame(parent, text="Упаковка папки в RPA", padding=12)
        pack_frame.pack(fill=tk.X, padx=10, pady=8)

        ttk.Label(pack_frame, text="Исходная папка с файлами:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.rpa_pack_src = tk.StringVar()
        ttk.Entry(pack_frame, textvariable=self.rpa_pack_src, width=60).grid(row=1, column=0, padx=(0, 8))
        ttk.Button(pack_frame, text="Обзор...", command=lambda: self._choose_dir(self.rpa_pack_src)).grid(row=1, column=1)

        ttk.Label(pack_frame, text="Выходной файл .rpa:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.rpa_pack_dst = tk.StringVar()
        ttk.Entry(pack_frame, textvariable=self.rpa_pack_dst, width=60).grid(row=3, column=0, padx=(0, 8))
        ttk.Button(pack_frame, text="Обзор...", command=lambda: self._choose_save_file(self.rpa_pack_dst, [("RPA Archive", "*.rpa")])).grid(row=3, column=1)

        ttk.Button(pack_frame, text="📦 Упаковать в RPA v3", command=self._run_rpa_pack).grid(row=4, column=0, sticky=tk.W, pady=8)

        # Unpack Section
        unpack_frame = ttk.LabelFrame(parent, text="Распаковка RPA архива", padding=12)
        unpack_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        ttk.Label(unpack_frame, text="Файл архива .rpa:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.rpa_unpack_src = tk.StringVar()
        ttk.Entry(unpack_frame, textvariable=self.rpa_unpack_src, width=60).grid(row=1, column=0, padx=(0, 8))
        ttk.Button(unpack_frame, text="Обзор...", command=lambda: self._choose_open_file(self.rpa_unpack_src, [("RPA Archive", "*.rpa")])).grid(row=1, column=1)

        ttk.Label(unpack_frame, text="Папка для извлечения:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.rpa_unpack_dst = tk.StringVar()
        ttk.Entry(unpack_frame, textvariable=self.rpa_unpack_dst, width=60).grid(row=3, column=0, padx=(0, 8))
        ttk.Button(unpack_frame, text="Обзор...", command=lambda: self._choose_dir(self.rpa_unpack_dst)).grid(row=3, column=1)

        btn_row = ttk.Frame(unpack_frame)
        btn_row.grid(row=4, column=0, sticky=tk.W, pady=8)
        ttk.Button(btn_row, text="📂 Распаковать всё", command=self._run_rpa_unpack).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_row, text="🔍 Показать список файлов", command=self._run_rpa_list).pack(side=tk.LEFT)

        self.rpa_list_txt = tk.Text(unpack_frame, height=8, font=("Consolas", 9))
        self.rpa_list_txt.grid(row=5, column=0, columnspan=2, sticky=tk.NSEW, pady=6)

    def _choose_dir(self, str_var):
        p = filedialog.askdirectory()
        if p:
            str_var.set(p)

    def _choose_open_file(self, str_var, types):
        p = filedialog.askopenfilename(filetypes=types)
        if p:
            str_var.set(p)

    def _choose_save_file(self, str_var, types):
        p = filedialog.asksaveasfilename(filetypes=types)
        if p:
            str_var.set(p)

    def _run_rpa_pack(self):
        src = self.rpa_pack_src.get().strip()
        dst = self.rpa_pack_dst.get().strip()
        if not src or not dst:
            messagebox.showerror("Ошибка", "Заполните пути для упаковки.")
            return
        archive = RPAArchive()
        try:
            count = archive.pack(src, dst)
            messagebox.showinfo("Успех", f"Упаковано файлов: {count}\nАрхив создан: {dst}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _run_rpa_unpack(self):
        src = self.rpa_unpack_src.get().strip()
        dst = self.rpa_unpack_dst.get().strip()
        if not src or not dst:
            messagebox.showerror("Ошибка", "Заполните пути для распаковки.")
            return
        archive = RPAArchive()
        try:
            count = archive.unpack(src, dst)
            messagebox.showinfo("Успех", f"Извлечено файлов: {count}\nПапка: {dst}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _run_rpa_list(self):
        src = self.rpa_unpack_src.get().strip()
        if not src or not os.path.isfile(src):
            messagebox.showerror("Ошибка", "Выберите существующий .rpa файл.")
            return
        archive = RPAArchive()
        try:
            files = archive.list_files(src)
            self.rpa_list_txt.delete("1.0", tk.END)
            self.rpa_list_txt.insert("1.0", f"Файлов в архиве: {len(files)}\n" + "\n".join(files))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ---------------- TAB 3: RPYC TOOL ----------------
    def _build_rpyc_tab(self, parent):
        frame = ttk.LabelFrame(parent, text="Анализ и декомпиляция .rpyc", padding=12)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        ttk.Label(frame, text="Файл .rpyc:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.rpyc_src_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.rpyc_src_var, width=65).grid(row=1, column=0, padx=(0, 8))
        ttk.Button(frame, text="Обзор...", command=lambda: self._choose_open_file(self.rpyc_src_var, [("Ren'Py Bytecode", "*.rpyc")])).grid(row=1, column=1)

        btns = ttk.Frame(frame)
        btns.grid(row=2, column=0, sticky=tk.W, pady=8)
        ttk.Button(btns, text="🔍 Анализ структуры", command=self._run_rpyc_info).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btns, text="📜 Декомпилировать в .rpy", command=self._run_rpyc_decomp).pack(side=tk.LEFT)

        self.rpyc_txt = tk.Text(frame, height=18, font=("Consolas", 9))
        self.rpyc_txt.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, pady=6)

    def _run_rpyc_info(self):
        f = self.rpyc_src_var.get().strip()
        if not f or not os.path.isfile(f):
            messagebox.showerror("Ошибка", "Выберите существующий .rpyc файл.")
            return
        tool = RPYCTool()
        info = tool.extract_strings_and_code(f)
        self.rpyc_txt.delete("1.0", tk.END)
        out = [f"=== Анализ {os.path.basename(f)} ==="]
        if info["mods"]:
            out.append("\n[Регистрация в меню модов]:")
            for k, v in info["mods"].items():
                out.append(f"  mods['{k}'] = {v}")
        if info["labels"]:
            out.append(f"\n[Найденные лейблы ({len(info['labels'])} шт.)]:")
            for lbl in info["labels"]:
                out.append(f"  label {lbl}:")
        self.rpyc_txt.insert("1.0", "\n".join(out))

    def _run_rpyc_decomp(self):
        f = self.rpyc_src_var.get().strip()
        if not f or not os.path.isfile(f):
            messagebox.showerror("Ошибка", "Выберите существующий .rpyc файл.")
            return
        tool = RPYCTool()
        out = os.path.splitext(f)[0] + "_decompiled.rpy"
        ok, msg = tool.decompile(f, out)
        if ok:
            messagebox.showinfo("Декомпиляция", f"{msg}\nСохранено в:\n{out}")
        else:
            messagebox.showerror("Ошибка", msg)

    # ---------------- TAB 4: WORKSHOP ANALYZER ----------------
    def _build_batch_tab(self, parent):
        top_frame = ttk.Frame(parent, padding=8)
        top_frame.pack(fill=tk.X, padx=10, pady=4)

        default_archive = r"E:\ANALGAYPORNSTEAM\steamapps\workshop\content\331470"
        self.batch_dir_var = tk.StringVar(value=default_archive if os.path.exists(default_archive) else "")

        ttk.Label(top_frame, text="Архив Workshop:").pack(side=tk.LEFT)
        ttk.Entry(top_frame, textvariable=self.batch_dir_var, width=50).pack(side=tk.LEFT, padx=6)
        ttk.Button(top_frame, text="Обзор...", command=lambda: self._choose_dir(self.batch_dir_var)).pack(side=tk.LEFT)

        self.batch_steam_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(top_frame, text="Проверять Steam API", variable=self.batch_steam_var).pack(side=tk.LEFT, padx=10)

        self.batch_btn = ttk.Button(top_frame, text="▶ Запустить анализ", command=self._run_batch_analysis)
        self.batch_btn.pack(side=tk.LEFT, padx=6)

        # Status and Summary Banner
        self.batch_summary_lbl = ttk.Label(parent, text="Готов к сканированию архива", font=("Segoe UI", 10, "bold"))
        self.batch_summary_lbl.pack(anchor=tk.W, padx=18, pady=4)

        # Treeview Results
        tree_frame = ttk.Frame(parent, padding=8)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        cols = ("id", "title", "status", "size_mb", "label", "scripts", "assets")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=14)
        self.tree.heading("id", text="Workshop ID")
        self.tree.heading("title", text="Название мода")
        self.tree.heading("status", text="Статус в Steam")
        self.tree.heading("size_mb", text="Размер (МБ)")
        self.tree.heading("label", text="Лейбл")
        self.tree.heading("scripts", text="Скрипты")
        self.tree.heading("assets", text="Ресурсы")

        self.tree.column("id", width=110)
        self.tree.column("title", width=280)
        self.tree.column("status", width=120)
        self.tree.column("size_mb", width=90)
        self.tree.column("label", width=120)
        self.tree.column("scripts", width=70)
        self.tree.column("assets", width=70)

        scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Export buttons
        bot_frame = ttk.Frame(parent, padding=8)
        bot_frame.pack(fill=tk.X, padx=10, pady=4)

        ttk.Button(bot_frame, text="📥 Экспорт в Markdown", command=self._export_batch_md).pack(side=tk.LEFT, padx=6)
        ttk.Button(bot_frame, text="📊 Экспорт в CSV", command=self._export_batch_csv).pack(side=tk.LEFT, padx=6)
        ttk.Button(bot_frame, text="⚡ Адаптировать выбранный мод", command=self._adapt_selected_from_tree).pack(side=tk.RIGHT, padx=6)

        self.last_summary = None

    def _run_batch_analysis(self):
        archive_dir = self.batch_dir_var.get().strip()
        if not archive_dir or not os.path.exists(archive_dir):
            messagebox.showerror("Ошибка", "Укажите существующую папку архива Workshop.")
            return

        check_steam = self.batch_steam_var.get()
        self.batch_btn.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())

        def worker():
            analyzer = BatchAnalyzer(archive_dir)
            def on_progress(done, total, msg):
                self.batch_summary_lbl.config(text=f"Обработка [{done}/{total}]: {msg}")

            summary = analyzer.analyze_archive(check_steam=check_steam, progress_callback=on_progress)
            self.last_summary = summary

            # Populate Treeview
            self.tree.delete(*self.tree.get_children())
            for item in summary["all_results"]:
                tag = ()
                if item["steam_status"] in ("DELETED", "BANNED"):
                    tag = ("deleted",)
                self.tree.insert("", tk.END, values=(
                    item["id"],
                    item["title"],
                    item["steam_status"],
                    item["size_mb"],
                    item["label"],
                    item["scripts_count"],
                    item["assets_count"]
                ), tags=tag)

            self.tree.tag_configure("deleted", foreground="#d32f2f")
            self.batch_summary_lbl.config(
                text=f"Всего: {summary['total_scanned']} | 🔥 УДАЛЕНО ИЗ STEAM: {summary['deleted_count']} | Доступно: {summary['active_count']} | Мусор: {summary['junk_count']}"
            )
            self.batch_btn.config(state=tk.NORMAL)

        threading.Thread(target=worker, daemon=True).start()

    def _export_batch_md(self):
        if not self.last_summary:
            messagebox.showinfo("Инфо", "Сначала выполните анализ архива.")
            return
        p = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown", "*.md")])
        if p:
            BatchAnalyzer.export_markdown_report(self.last_summary, p)
            messagebox.showinfo("Успех", f"Markdown отчёт сохранён:\n{p}")

    def _export_batch_csv(self):
        if not self.last_summary:
            messagebox.showinfo("Инфо", "Сначала выполните анализ архива.")
            return
        p = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if p:
            BatchAnalyzer.export_csv_report(self.last_summary, p)
            messagebox.showinfo("Успех", f"CSV отчёт сохранён:\n{p}")

    def _adapt_selected_from_tree(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Инфо", "Выберите мод из таблицы.")
            return
        item = self.tree.item(selected[0])
        mod_id = str(item["values"][0])

        archive_dir = self.batch_dir_var.get().strip()
        mod_path = os.path.join(archive_dir, mod_id)
        if os.path.exists(mod_path):
            self.port_path_var.set(mod_path)
            meta = ModScanner.scan(mod_path)
            self.port_title_var.set(meta.title)
            self.port_alias_var.set(meta.start_label)
            # Switch to first tab
            self.children['!notebook'].select(self.tab_port)


def main():
    app = ESGMLApp()
    app.mainloop()


if __name__ == "__main__":
    main()
