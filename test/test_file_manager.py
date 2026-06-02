import pytest
import logging
from pathlib import Path
from dataclasses import dataclass

from src.file_manager.file_manager import Manager 

@dataclass
class StubEmail:
    filename: str
    categories: list[str]

def test_warning_for_existing(tmp_path, monkeypatch, caplog):
    monkeypatch.setattr(Manager, "path", tmp_path)

    text = "Some new text"
    old_text = "Old text"

    source = tmp_path / "source.txt"
    source.write_text(text)

    old_file = tmp_path / "First" / "source.txt"
    old_file.parent.mkdir(parents=True, exist_ok=True)
    old_file.write_text(old_text)

    email = StubEmail(filename=str(source), categories=["First"])

    with caplog.at_level(logging.WARNING):
        Manager.put(email)

    assert caplog.text

    assert (tmp_path / "First" / "source.txt").read_text() == old_text

def test_correct_copy(tmp_path, monkeypatch):
    monkeypatch.setattr(Manager, "path", tmp_path)

    text = "Some unique text"

    source = tmp_path / "source.txt"
    source.write_text(text)

    email = StubEmail(filename=str(source), categories=["First", "Second"])

    Manager.put(email)

    assert (tmp_path / "First" / "source.txt").exists()
    assert (tmp_path / "Second" / "source.txt").exists()

    assert (tmp_path / "First" / "source.txt").read_text() == text
    assert (tmp_path / "Second" / "source.txt").read_text() == text
