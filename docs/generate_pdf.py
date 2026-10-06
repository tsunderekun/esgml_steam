#!/usr/bin/env python3
"""
ESGML SDK - Markdown to PDF Converter
Zero external python libraries required. Uses Windows built-in rendering engine.
Generates a beautifully styled, print-ready PDF from ESGML_GUIDE.md.
"""

import os
import sys
import subprocess
import html
import re

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(DOCS_DIR, "ESGML_GUIDE.md")
PDF_PATH = os.path.join(DOCS_DIR, "ESGML_GUIDE.pdf")
HTML_PATH = os.path.join(DOCS_DIR, "ESGML_GUIDE.tmp.html")


def find_browser_engine():
    """Locate headless browser on Windows."""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def markdown_to_html(md_text):
    """Simple, clean Markdown to HTML parser for documentation."""
    lines = md_text.splitlines()
    html_lines = []
    in_code_block = False
    in_table = False
    in_list = False

    for line in lines:
        # Code blocks
        if line.startswith("```"):
            if in_code_block:
                html_lines.append("</code></pre>")
                in_code_block = False
            else:
                lang = line[3:].strip()
                html_lines.append(f'<pre><code class="language-{lang}">')
                in_code_block = True
            continue

        if in_code_block:
            html_lines.append(html.escape(line))
            continue

        # Close list if not a list item
        if in_list and not line.strip().startswith(("-", "*", "1.", "2.", "3.", "4.", "5.")):
            html_lines.append("</ul>")
            in_list = False

        # Close table if not a table row
        if in_table and not line.strip().startswith("|"):
            html_lines.append("</table>")
            in_table = False

        # Headers
        if line.startswith("# "):
            html_lines.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("#### "):
            html_lines.append(f"<h4>{html.escape(line[5:])}</h4>")
        elif line.startswith("---"):
            html_lines.append("<hr/>")
        # Table
        elif line.strip().startswith("|"):
            parts = [p.strip() for p in line.strip().split("|")[1:-1]]
            if all(set(p) <= {"-", ":"} for p in parts if p):
                continue # Skip divider
            if not in_table:
                html_lines.append('<table border="1" cellspacing="0" cellpadding="6">')
                in_table = True
                cells = "".join(f"<th>{html.escape(p)}</th>" for p in parts)
                html_lines.append(f"<tr>{cells}</tr>")
            else:
                cells = "".join(f"<td>{html.escape(p)}</td>" for p in parts)
                html_lines.append(f"<tr>{cells}</tr>")
        # Lists
        elif line.strip().startswith(("- ", "* ")):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            item = line.strip()[2:]
            # inline formatting
            item = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', item)
            item = re.sub(r'`([^`]+)`', r'<code>\1</code>', item)
            html_lines.append(f"<li>{item}</li>")
        elif re.match(r'^\d+\.\s+', line.strip()):
            if not in_list:
                html_lines.append("<ol>")
                in_list = True
            item = re.sub(r'^\d+\.\s+', '', line.strip())
            item = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', item)
            item = re.sub(r'`([^`]+)`', r'<code>\1</code>', item)
            html_lines.append(f"<li>{item}</li>")
        elif line.strip():
            # Paragraph
            p = line.strip()
            p = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', p)
            p = re.sub(r'`([^`]+)`', r'<code>\1</code>', p)
            html_lines.append(f"<p>{p}</p>")

    if in_code_block:
        html_lines.append("</code></pre>")
    if in_list:
        html_lines.append("</ul>")
    if in_table:
        html_lines.append("</table>")

    body_content = "\n".join(html_lines)

    template = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>ESGML v4.1 Guide</title>
<style>
    @page {{
        size: A4;
        margin: 20mm;
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: #24292e;
        max-width: 900px;
        margin: auto;
    }}
    h1 {{
        color: #0366d6;
        border-bottom: 2px solid #eaecef;
        padding-bottom: 0.3em;
        font-size: 26px;
    }}
    h2 {{
        color: #2f363d;
        border-bottom: 1px solid #eaecef;
        padding-bottom: 0.3em;
        margin-top: 24px;
        font-size: 20px;
    }}
    h3 {{
        color: #444d56;
        margin-top: 18px;
        font-size: 16px;
    }}
    pre {{
        background-color: #f6f8fa;
        border: 1px solid #e1e4e8;
        border-radius: 6px;
        padding: 12px;
        overflow: auto;
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
        font-size: 12px;
    }}
    code {{
        background-color: #f0f3f6;
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-family: Consolas, monospace;
        font-size: 12px;
    }}
    pre code {{
        background: transparent;
        padding: 0;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        font-size: 13px;
    }}
    th, td {{
        border: 1px solid #dfe2e5;
        padding: 8px 12px;
        text-align: left;
    }}
    th {{
        background-color: #f6f8fa;
        font-weight: 600;
    }}
    tr:nth-child(even) {{
        background-color: #fafbfc;
    }}
    hr {{
        height: 0.25em;
        padding: 0;
        margin: 24px 0;
        background-color: #e1e4e8;
        border: 0;
    }}
    ul, ol {{
        padding-left: 2em;
    }}
    li {{
        margin: 4px 0;
    }}
</style>
</head>
<body>
{body_content}
</body>
</html>"""
    return template


def generate_pdf():
    print(f"[*] Чтение {MD_PATH}...")
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    print("[*] Генерация HTML разметки...")
    html_content = markdown_to_html(md_text)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    browser = find_browser_engine()
    if not browser:
        print("[-] Ошибка: Браузер для PDF рендеринга (Edge/Chrome) не найден.")
        return False

    print(f"[*] Рендеринг PDF через {os.path.basename(browser)}...")
    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={PDF_PATH}",
        f"file:///{HTML_PATH.replace(os.sep, '/')}"
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        if os.path.exists(PDF_PATH) and os.path.getsize(PDF_PATH) > 0:
            print(f"[+] PDF УСПЕШНО СОЗДАН: {PDF_PATH} ({os.path.getsize(PDF_PATH)} байт)")
            return True
    except Exception as e:
        print(f"[-] Сбой генерации PDF: {e}")
    finally:
        if os.path.exists(HTML_PATH):
            try:
                os.remove(HTML_PATH)
            except Exception:
                pass

    return False


if __name__ == "__main__":
    generate_pdf()
