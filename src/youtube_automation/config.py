from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    youtube_api_key: str
    youtube_channel_id: str
    download_dir: str
    state_file: str
    report_dir: str
    log_file: str
    check_interval_minutes: int
    report_day: str
    report_time_utc: str


def load_settings() -> Settings:
    api_key = os.getenv("YOUTUBE_API_KEY", "").strip()
    channel_id = os.getenv("YOUTUBE_CHANNEL_ID", "").strip()
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY is required")
    if not channel_id:
        raise ValueError("YOUTUBE_CHANNEL_ID is required")

    return Settings(
        youtube_api_key=api_key,
        youtube_channel_id=channel_id,
        download_dir=os.getenv("DOWNLOAD_DIR", "./downloads"),
        state_file=os.getenv("STATE_FILE", "./state.json"),
        report_dir=os.getenv("REPORT_DIR", "./reports"),
        log_file=os.getenv("LOG_FILE", "./automation.log"),
        check_interval_minutes=int(os.getenv("CHECK_INTERVAL_MINUTES", "60")),
        report_day=os.getenv("REPORT_DAY", "monday"),
        report_time_utc=os.getenv("REPORT_TIME_UTC", "00:00"),
    )
