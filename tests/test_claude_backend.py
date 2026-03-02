"""Unit tests for backend response parsing."""

import pytest
from aib.backend.base import BackendResult, BaseBackend


# Concrete subclass for testing parse()
class _TestBackend(BaseBackend):
    def query(self, user_input: str) -> BackendResult:
        raise NotImplementedError


BACKEND = _TestBackend()


def test_parse_valid_response():
    raw = """\
EXPLANATION: Lists PDF files modified in the last 7 days.
COMMANDS:
find . -name "*.pdf" -mtime -7
fd --extension pdf --changed-within 7d
find . -name "*.pdf" -newer $(date -d "7 days ago" +%Y-%m-%d)
"""
    result = BACKEND.parse(raw)
    assert result.explanation == "Lists PDF files modified in the last 7 days."
    assert len(result.commands) == 3
    assert result.commands[0] == 'find . -name "*.pdf" -mtime -7'
    assert result.is_valid()


def test_parse_minimal_response():
    raw = """\
EXPLANATION: Kill the process on port 8080.
COMMANDS:
lsof -ti:8080 | xargs kill -9
"""
    result = BACKEND.parse(raw)
    assert result.explanation == "Kill the process on port 8080."
    assert result.commands == ["lsof -ti:8080 | xargs kill -9"]
    assert result.is_valid()


def test_parse_empty_response():
    result = BACKEND.parse("")
    assert result.explanation == ""
    assert result.commands == []
    assert not result.is_valid()


def test_parse_missing_explanation():
    raw = """\
COMMANDS:
ls -la
"""
    result = BACKEND.parse(raw)
    assert result.explanation == ""
    assert result.commands == ["ls -la"]
    assert not result.is_valid()


def test_parse_missing_commands():
    raw = "EXPLANATION: Does something.\n"
    result = BACKEND.parse(raw)
    assert result.explanation == "Does something."
    assert result.commands == []
    assert not result.is_valid()


def test_parse_ignores_extra_whitespace():
    raw = """\

EXPLANATION:   Show disk usage.
COMMANDS:
  du -sh *
  df -h
"""
    result = BACKEND.parse(raw)
    assert result.explanation == "Show disk usage."
    assert result.commands == ["du -sh *", "df -h"]


def test_parse_stores_raw():
    raw = "EXPLANATION: Test.\nCOMMANDS:\necho hello\n"
    result = BACKEND.parse(raw)
    assert result.raw == raw


def test_backend_result_valid():
    r = BackendResult(explanation="test", commands=["echo hi"])
    assert r.is_valid()


def test_backend_result_invalid_no_commands():
    r = BackendResult(explanation="test", commands=[])
    assert not r.is_valid()


def test_backend_result_invalid_no_explanation():
    r = BackendResult(explanation="", commands=["echo hi"])
    assert not r.is_valid()
