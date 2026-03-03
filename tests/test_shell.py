"""Unit tests for shell integration generator."""

from aib.shell import get_integration


def test_bash_integration():
    code = get_integration("bash")
    assert "__aib_widget__" in code
    assert "bind -x" in code
    assert "aib()" in code
    assert "read -e -i" in code


def test_bash_from_full_path():
    code = get_integration("/bin/bash")
    assert "bind -x" in code


def test_zsh_integration():
    code = get_integration("zsh")
    assert "print -z" in code


def test_zsh_from_full_path():
    code = get_integration("/usr/bin/zsh")
    assert "print -z" in code


def test_fish_integration():
    code = get_integration("fish")
    assert "commandline" in code
    assert "or return" in code


def test_unknown_shell_defaults_to_bash():
    code = get_integration("unknown")
    assert "bind -x" in code
