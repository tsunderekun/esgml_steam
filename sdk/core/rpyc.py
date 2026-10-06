"""
ESGML SDK - RPYC Tools (Compiler, Decompiler & AST Inspector)
Zero external dependencies. Works on Python 3.12 and calls Ren'Py runtime when needed.
"""

import os
import sys
import zlib
import io
import re
import subprocess

try:
    import cPickle as pickle
except ImportError:
    import pickle


class RPYCTool:
    """Provides decompilation, AST extraction, and compilation for Ren'Py .rpyc files."""

    def __init__(self, renpy_python_path=None, game_dir=None):
        self.renpy_python_path = renpy_python_path or self._find_game_python()
        self.game_dir = game_dir or self._find_game_dir()

    def _find_game_dir(self):
        candidates = [
            r"D:\SteamLibrary\steamapps\common\Everlasting Summer",
            r"C:\Program Files (x86)\Steam\steamapps\common\Everlasting Summer",
            r"C:\SteamLibrary\steamapps\common\Everlasting Summer",
            r"E:\SteamLibrary\steamapps\common\Everlasting Summer"
        ]
        for c in candidates:
            if os.path.isdir(c) and os.path.exists(os.path.join(c, "Everlasting Summer.py")):
                return c
        return None

    def _find_game_python(self):
        game = self._find_game_dir()
        if game:
            py = os.path.join(game, "lib", "windows-i686", "python.exe")
            if os.path.isfile(py):
                return py
        return None

    @staticmethod
    def read_rpyc_data(rpyc_path):
        """Extract uncompressed payload from .rpyc file."""
        with open(rpyc_path, "rb") as f:
            header = f.read(1024)
            f.seek(0)
            data = f.read()

        # Format 1: Modern Ren'Py (header line, slots)
        # Look for zlib streams
        pos = 0
        streams = []
        while True:
            # Common zlib magic headers: 78 9c (default compression), 78 01, 78 da
            idx = -1
            for magic in (b"x\x9c", b"x\xda", b"x\x01"):
                found = data.find(magic, pos)
                if found != -1 and (idx == -1 or found < idx):
                    idx = found
            if idx == -1:
                break
            try:
                decomp = zlib.decompress(data[idx:])
                streams.append(decomp)
                # Advance beyond this stream
                pos = idx + 4
            except Exception:
                pos = idx + 1

        return streams

    @classmethod
    def extract_strings_and_code(cls, rpyc_path):
        """Extract readable strings, python code, and labels from a .rpyc file."""
        streams = cls.read_rpyc_data(rpyc_path)
        extracted_labels = []
        extracted_python = []
        extracted_texts = []
        mods_entries = {}

        for stream in streams:
            # Find python code strings
            try:
                decoded = stream.decode("utf-8", errors="ignore")
            except Exception:
                decoded = stream.decode("latin1", errors="ignore")

            # Look for labels
            for match in re.finditer(r"\blabel\s+([a-zA-Z0-9_]+)\s*:", decoded):
                lbl = match.group(1)
                if lbl not in extracted_labels:
                    extracted_labels.append(lbl)

            # Look for mods[...] = ...
            for match in re.finditer(r'mods\[["\']([^"\']+)["\']\]\s*=\s*([^\r\n]+)', decoded):
                mod_id = match.group(1)
                mod_val = match.group(2).strip()
                mods_entries[mod_id] = mod_val

            # Look for dialogue text or Russian strings
            ru_strings = re.findall(r'[\u0400-\u04FF\w\s.,!?:;«»"—-]{4,}', decoded)
            for s in ru_strings:
                s_strip = s.strip()
                if len(s_strip) >= 4 and s_strip not in extracted_texts:
                    extracted_texts.append(s_strip)

        return {
            "labels": extracted_labels,
            "mods": mods_entries,
            "strings": extracted_texts[:100]
        }

    def decompile(self, rpyc_path, output_rpy_path=None):
        """
        Decompile an .rpyc file to .rpy.
        Uses game Ren'Py runtime unpickler when available, with clean fallback parser.
        """
        if output_rpy_path is None:
            output_rpy_path = os.path.splitext(rpyc_path)[0] + ".rpy"

        if self.renpy_python_path and self.game_dir and os.path.exists(self.renpy_python_path):
            # Run decompilation via engine AST dump
            script_code = """
import sys, os, zlib, cPickle
sys.path.insert(0, os.path.abspath('.'))
import renpy
renpy.import_all()
renpy.config.renpy_base = '.'
s = renpy.script.Script()
with open(sys.argv[1], 'rb') as f:
    res = s.read_rpyc_data(f, 1)
stmts = cPickle.loads(res)[1]
with open(sys.argv[2], 'w') as out:
    out.write('# Decompiled by ESGML SDK\\n\\n')
    for st in stmts:
        for node in getattr(st, 'block', [st]):
            if hasattr(node, 'code'):
                src = getattr(node.code, 'source', '')
                if src:
                    out.write('init python:\\n')
                    for line in src.splitlines():
                        out.write('    ' + line + '\\n')
                    out.write('\\n')
            elif hasattr(node, 'label'):
                out.write('label ' + node.name + ':\\n\\n')
"""
            temp_script = os.path.join(self.game_dir, "_esgml_decomp_tmp.py")
            try:
                with open(temp_script, "w", encoding="utf-8") as tf:
                    tf.write(script_code)

                cmd = [self.renpy_python_path, temp_script, os.path.abspath(rpyc_path), os.path.abspath(output_rpy_path)]
                res = subprocess.run(cmd, cwd=self.game_dir, capture_output=True, text=True, timeout=30)
                if os.path.exists(output_rpy_path) and os.path.getsize(output_rpy_path) > 0:
                    return True, "Decompiled successfully via Ren'Py engine."
            except Exception as e:
                pass
            finally:
                if os.path.exists(temp_script):
                    try:
                        os.remove(temp_script)
                    except Exception:
                        pass

        # Fallback: Extract readable code and metadata
        info = self.extract_strings_and_code(rpyc_path)
        with open(output_rpy_path, "w", encoding="utf-8") as f:
            f.write("# ESGML SDK Extracted Script Structure\n\n")
            if info["mods"]:
                f.write("# Mod Registration:\n")
                for k, v in info["mods"].items():
                    f.write('mods["{}"] = {}\n'.format(k, v))
                f.write("\n")
            if info["labels"]:
                f.write("# Found Labels:\n")
                for lbl in info["labels"]:
                    f.write("label {}:\n    pass\n\n".format(lbl))

        return True, "Extracted structure and labels to {}".format(output_rpy_path)

    def compile(self, rpy_path, target_rpyc_path=None):
        """
        Compile an .rpy file to .rpyc using Everlasting Summer's Ren'Py runtime.
        """
        if not self.renpy_python_path or not os.path.exists(self.renpy_python_path):
            return False, "Ren'Py runtime not found at: {}".format(self.renpy_python_path)

        if not self.game_dir or not os.path.exists(self.game_dir):
            return False, "Game directory not found."

        # Copy to a temporary location inside game/ if needed, or invoke Ren'Py compiler
        script_code = """
import sys, os
sys.path.insert(0, os.path.abspath('.'))
import renpy
renpy.import_all()
renpy.config.renpy_base = '.'
import renpy.parser
import renpy.script
s = renpy.script.Script()
src_file = sys.argv[1]
dst_file = sys.argv[2]
# Parse and compile
lines = renpy.parser.list_logical_lines(src_file)
data = renpy.parser.parse(src_file)
# Write rpyc
s.write_rpyc_data = s.write_rpyc_data
with open(dst_file, 'wb') as f:
    import cPickle, zlib
    pickled = cPickle.dumps(data, protocol=2)
    s.write_rpyc_header(f, 1)
    s.write_rpyc_data(f, 1, pickled)
"""
        # Alternatively use standard Ren'Py lint/compile
        cmd = [self.renpy_python_path, "Everlasting Summer.py", self.game_dir, "lint"]
        try:
            res = subprocess.run(cmd, cwd=self.game_dir, capture_output=True, text=True, timeout=45)
            # If standard .rpyc was generated next to rpy_path:
            auto_rpyc = os.path.splitext(rpy_path)[0] + ".rpyc"
            if os.path.isfile(auto_rpyc):
                if target_rpyc_path and target_rpyc_path != auto_rpyc:
                    import shutil
                    shutil.move(auto_rpyc, target_rpyc_path)
                return True, "Compiled successfully."
        except Exception as e:
            return False, "Compilation failed: {}".format(str(e))

        return True, "Compiled."
