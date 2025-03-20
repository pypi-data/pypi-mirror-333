import os
from deingest.exceptions import ParseError, RestoreError

def parse_digest_file(digest_path):
    if not os.path.exists(digest_path):
        raise ParseError(f"Digest file '{digest_path}' not found.")
    with open(digest_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    entries = []
    i = 0
    total = len(lines)
    while i < total:
        if lines[i].strip() == "================================================":
            i += 1
            if i < total and lines[i].strip().startswith("File:"):
                file_path = lines[i].strip()[5:].strip()
                if not file_path:
                    raise ParseError("Empty file path encountered.")
                i += 1
                if i < total and lines[i].strip() == "================================================":
                    i += 1
                    content_lines = []
                    while i < total and lines[i].strip() != "================================================":
                        content_lines.append(lines[i])
                        i += 1
                    content = "".join(content_lines).rstrip("\n")
                    entries.append((file_path, content))
                else:
                    raise ParseError("Missing separator after file header.")
            else:
                i += 1
        else:
            i += 1
    if not entries:
        raise ParseError("No valid file entries found in the digest.")
    return entries

def restore_files(entries, output_dir, overwrite=False, dry_run=False):
    restored = []
    errors = []
    for rel_path, content in entries:
        dest = os.path.join(output_dir, rel_path)
        dest_dir = os.path.dirname(dest)
        try:
            if dry_run:
                restored.append(dest)
                continue
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)
            if os.path.exists(dest) and not overwrite:
                continue
            with open(dest, "w", encoding="utf-8") as f:
                f.write(content)
            restored.append(dest)
        except Exception as e:
            errors.append((dest, str(e)))
        # End each file
    if errors:
        raise RestoreError(errors)
    return restored