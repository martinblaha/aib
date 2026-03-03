"""Unit tests for config loading and saving."""

from pathlib import Path
from unittest.mock import patch

from aib import config as cfg


def test_load_defaults_when_no_file(tmp_path: Path):
    fake_file = tmp_path / "nonexistent" / "config.toml"
    with patch.object(cfg, "CONFIG_FILE", fake_file):
        config = cfg.load()
    assert config["backend"] == "claude"
    assert config["max_results"] == 5
    assert config["timeout"] == 30


def test_load_merges_user_config(tmp_path: Path):
    config_file = tmp_path / "config.toml"
    config_file.write_text('timeout = 60\nbackend = "gemini"\n')
    with patch.object(cfg, "CONFIG_FILE", config_file):
        config = cfg.load()
    assert config["timeout"] == 60
    assert config["backend"] == "gemini"
    assert config["max_results"] == 5  # default kept


def test_save_and_load_roundtrip(tmp_path: Path):
    config_file = tmp_path / "config.toml"
    config_dir = tmp_path
    with patch.object(cfg, "CONFIG_FILE", config_file), \
         patch.object(cfg, "CONFIG_DIR", config_dir):
        cfg.save({"backend": "claude", "max_results": 3, "timeout": 15})
    with patch.object(cfg, "CONFIG_FILE", config_file):
        config = cfg.load()
    assert config["backend"] == "claude"
    assert config["max_results"] == 3
    assert config["timeout"] == 15


def test_save_escapes_special_chars(tmp_path: Path):
    config_file = tmp_path / "config.toml"
    config_dir = tmp_path
    with patch.object(cfg, "CONFIG_FILE", config_file), \
         patch.object(cfg, "CONFIG_DIR", config_dir):
        cfg.save({"name": 'hello "world"'})
    content = config_file.read_text()
    assert r'\"world\"' in content
