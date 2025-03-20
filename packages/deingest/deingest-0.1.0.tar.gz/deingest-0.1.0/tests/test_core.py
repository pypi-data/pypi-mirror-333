import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deingest')))

from deingest.core import *

SAMPLE_DIGEST = """================================================
File: sample/test.txt
================================================
Hello Test
================================================
File: readme.md
================================================
# Readme
Content.
"""

def test_parse_digest_file(tmp_path):
    digest = tmp_path / "digest.txt"
    digest.write_text(SAMPLE_DIGEST, encoding="utf-8")
    entries = parse_digest_file(str(digest))
    assert len(entries) == 2
    assert entries[0][0] == "sample/test.txt"
    assert "Hello Test" in entries[0][1]
    assert entries[1][0] == "readme.md"
    assert "# Readme" in entries[1][1]

def test_restore_files(tmp_path):
    entries = [("sample/test.txt", "Content A"), ("readme.md", "Content B")]
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    restored = restore_files(entries, str(output_dir), overwrite=False, dry_run=False)
    file1 = output_dir / "sample" / "test.txt"
    file2 = output_dir / "readme.md"
    assert file1.exists() and file1.read_text() == "Content A"
    assert file2.exists() and file2.read_text() == "Content B"
    