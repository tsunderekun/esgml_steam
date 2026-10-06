"""
ESGML SDK - Pure Python RPA v2/v3 Packer & Unpacker
Zero external dependencies. Compatible with Python 2.7 and Python 3.x.
"""

import os
import sys
import zlib
import io
import struct

# Python 2/3 compatibility for pickle
try:
    import cPickle as pickle
except ImportError:
    import pickle


class RPAArchive:
    """Handles reading, unpacking, and creating Ren'Py RPA archives (v2.0 and v3.0)."""

    def __init__(self, key=0xDEADBEEF, version=3):
        self.key = key
        self.version = version

    @staticmethod
    def is_rpa(filepath):
        """Check if file is a valid RPA archive."""
        if not os.path.isfile(filepath):
            return False
        try:
            with open(filepath, "rb") as f:
                header = f.readline()
                return header.startswith(b"RPA-2.0") or header.startswith(b"RPA-3.0")
        except Exception:
            return False

    def list_files(self, rpa_path):
        """List all files in an RPA archive."""
        index, _ = self._read_index(rpa_path)
        return sorted(list(index.keys()))

    def extract_file(self, rpa_path, filename, output_path=None):
        """Extract a single file from the archive and return its bytes."""
        index, key = self._read_index(rpa_path)
        if filename not in index:
            raise KeyError("File '{}' not found in archive.".format(filename))

        segments = index[filename]
        data = bytearray()

        with open(rpa_path, "rb") as f:
            for seg in segments:
                if len(seg) == 3:
                    offset, length, prefix = seg
                    offset ^= key
                    length ^= key
                    f.seek(offset)
                    chunk = f.read(length)
                    if prefix:
                        data.extend(prefix)
                        data.extend(chunk[len(prefix):])
                    else:
                        data.extend(chunk)
                else:
                    offset, length = seg[:2]
                    offset ^= key
                    length ^= key
                    f.seek(offset)
                    data.extend(f.read(length))

        data_bytes = bytes(data)
        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            with open(output_path, "wb") as out_f:
                out_f.write(data_bytes)

        return data_bytes

    def unpack(self, rpa_path, output_dir, verbose=False, progress_callback=None):
        """Unpack all files from RPA archive into output directory."""
        index, key = self._read_index(rpa_path)
        total = len(index)
        extracted = 0

        with open(rpa_path, "rb") as f:
            for idx, (filename, segments) in enumerate(sorted(index.items())):
                # Normalize path for operating system
                norm_rel = os.path.normpath(filename.replace("/", os.sep))
                target_path = os.path.join(output_dir, norm_rel)
                target_dir = os.path.dirname(target_path)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)

                data = bytearray()
                for seg in segments:
                    if len(seg) == 3:
                        offset, length, prefix = seg
                        offset ^= key
                        length ^= key
                        f.seek(offset)
                        chunk = f.read(length)
                        if prefix:
                            data.extend(prefix)
                            data.extend(chunk[len(prefix):])
                        else:
                            data.extend(chunk)
                    else:
                        offset, length = seg[:2]
                        offset ^= key
                        length ^= key
                        f.seek(offset)
                        data.extend(f.read(length))

                with open(target_path, "wb") as out_f:
                    out_f.write(bytes(data))

                extracted += 1
                if progress_callback:
                    progress_callback(extracted, total, filename)
                elif verbose:
                    print("  [+] Extracted: {} ({} bytes)".format(filename, len(data)))

        return extracted

    def pack(self, input_dir, output_rpa_path, key=None, version=3, verbose=False, progress_callback=None, filter_ext=None):
        """
        Pack directory into RPA archive.
        filter_ext: optional set/list of extensions to include, or None for all.
        """
        if key is None:
            key = self.key

        input_dir = os.path.abspath(input_dir)
        files_to_pack = []

        for root, _, files in os.walk(input_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, input_dir).replace("\\", "/")
                if filter_ext:
                    _, ext = os.path.splitext(file)
                    if ext.lower() not in filter_ext:
                        continue
                files_to_pack.append((rel_path, full_path))

        files_to_pack.sort(key=lambda x: x[0])
        total = len(files_to_pack)

        os.makedirs(os.path.dirname(os.path.abspath(output_rpa_path)), exist_ok=True)

        # Temporary file while writing
        temp_rpa = output_rpa_path + ".tmp"
        index = {}

        with open(temp_rpa, "wb") as f:
            # Reserve space for header
            header_format = "RPA-{}.0 0000000000000000 {:08x}\n".format(version, key)
            header_bytes = header_format.encode("latin1")
            f.write(header_bytes)

            for idx, (rel_path, full_path) in enumerate(files_to_pack):
                offset = f.tell()
                with open(full_path, "rb") as in_f:
                    file_data = in_f.read()
                f.write(file_data)
                length = len(file_data)

                # Store segment
                if version == 3:
                    prefix = b""
                    index[rel_path] = [(offset ^ key, length ^ key, prefix)]
                else:
                    index[rel_path] = [(offset ^ key, length ^ key)]

                if progress_callback:
                    progress_callback(idx + 1, total, rel_path)
                elif verbose:
                    print("  [+] Packed: {} ({} bytes)".format(rel_path, length))

            # Write compressed index
            index_offset = f.tell()
            pickled = pickle.dumps(index, protocol=2)
            compressed = zlib.compress(pickled, 9)
            f.write(compressed)

            # Rewrite final header with true index offset
            f.seek(0)
            final_header = "RPA-{}.0 {:016x} {:08x}\n".format(version, index_offset, key)
            f.write(final_header.encode("latin1"))

        if os.path.exists(output_rpa_path):
            os.remove(output_rpa_path)
        os.rename(temp_rpa, output_rpa_path)

        return len(files_to_pack)

    def _read_index(self, rpa_path):
        """Read and decrypt the index from an RPA file."""
        with open(rpa_path, "rb") as f:
            header = f.readline()
            if not (header.startswith(b"RPA-2.0") or header.startswith(b"RPA-3.0")):
                raise ValueError("Not a supported RPA archive: {}".format(rpa_path))

            parts = header.split()
            if len(parts) < 3:
                raise ValueError("Malformed RPA header: {}".format(header))

            offset = int(parts[1], 16)
            key = int(parts[2], 16)

            f.seek(offset)
            compressed_index = f.read()
            raw_index = zlib.decompress(compressed_index)
            index = pickle.loads(raw_index)

        return index, key
