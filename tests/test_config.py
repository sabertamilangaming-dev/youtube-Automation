import os
import pytest

from youtube_automation.config import load_settings


def test_load_settings_requires_env(monkeypatch):
    monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)
    monkeypatch.delenv("YOUTUBE_CHANNEL_ID", raising=False)
    with pytest.raises(ValueError):
        load_settings()


def test_load_settings_reads_defaults(monkeypatch):
    monkeypatch.setenv("YOUTUBE_API_KEY", "key")
    monkeypatch.setenv("YOUTUBE_CHANNEL_ID", "channel")
    settings = load_settings()
    assert settings.download_dir == "./downloads"
    assert settings.check_interval_minutes == 60
