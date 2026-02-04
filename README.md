# YouTube Automation Tool

A Python automation tool that monitors a YouTube channel 24/7, downloads new uploads, and generates weekly reports.

## Development Environment

This project is set up for **VS Code**. Recommended extensions:
- Python
- Pylance
- Docker

## Features

- YouTube Data API integration for channel monitoring.
- Hourly scheduled checks for new uploads.
- Automatic download of new videos with duplicate prevention.
- Weekly Markdown report of downloads and uploads.
- Dockerized for consistent deployment.
- Structured project layout for easy maintenance.

## Project Structure

```
.
├── Dockerfile
├── README.md
├── requirements.txt
├── src/
│   └── youtube_automation/
│       ├── __init__.py
│       ├── config.py
│       ├── downloader.py
│       ├── logger.py
│       ├── main.py
│       ├── report.py
│       ├── scheduler.py
│       ├── state.py
│       └── youtube_api.py
└── tests/
```

## Configuration

Set environment variables before running:

- `YOUTUBE_API_KEY`: API key for the YouTube Data API.
- `YOUTUBE_CHANNEL_ID`: Channel ID to monitor.
- `DOWNLOAD_DIR`: (Optional) Directory for video downloads. Default: `./downloads`.
- `STATE_FILE`: (Optional) Path for the state JSON. Default: `./state.json`.
- `REPORT_DIR`: (Optional) Directory for weekly reports. Default: `./reports`.
- `LOG_FILE`: (Optional) Path for logs. Default: `./automation.log`.
- `CHECK_INTERVAL_MINUTES`: (Optional) Override scheduling in minutes. Default: `60`.
- `REPORT_DAY`: (Optional) Weekly report day (`monday`..`sunday`). Default: `monday`.
- `REPORT_TIME_UTC`: (Optional) Weekly report time in `HH:MM` (24h). Default: `00:00`.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
export YOUTUBE_API_KEY=your_key
export YOUTUBE_CHANNEL_ID=your_channel_id
python -m youtube_automation.main
```

## Docker

Build:

```bash
docker build -t youtube-automation .
```

Run:

```bash
docker run -d \
  -e YOUTUBE_API_KEY=your_key \
  -e YOUTUBE_CHANNEL_ID=your_channel_id \
  -v $(pwd)/downloads:/app/downloads \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/state.json:/app/state.json \
  -v $(pwd)/automation.log:/app/automation.log \
  youtube-automation
```

## Testing

```bash
pytest
```

## Notes

- This tool uses `yt-dlp` for reliable downloading.
- Weekly reports are created in Markdown under the report directory.
