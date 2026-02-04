from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List

from youtube_automation.state import State, VideoEvent


def filter_events_since(events: Iterable[VideoEvent], since_iso: str) -> List[VideoEvent]:
    if not since_iso:
        return list(events)
    since = datetime.fromisoformat(since_iso)
    return [event for event in events if datetime.fromisoformat(event.timestamp) >= since]


def render_report(state: State) -> str:
    generated_at = datetime.now(timezone.utc).isoformat()
    uploads = filter_events_since(state.uploads, state.last_report_at)
    downloads = filter_events_since(state.downloads, state.last_report_at)

    lines = [
        f"# Weekly YouTube Automation Report",
        "",
        f"Generated at (UTC): {generated_at}",
        "",
        f"## New Uploads ({len(uploads)})",
    ]

    if uploads:
        for event in uploads:
            lines.append(f"- {event.title} ({event.video_id}) @ {event.timestamp}")
    else:
        lines.append("- No new uploads detected.")

    lines.extend(["", f"## Downloads ({len(downloads)})"])
    if downloads:
        for event in downloads:
            lines.append(f"- {event.title} ({event.video_id}) @ {event.timestamp}")
    else:
        lines.append("- No downloads completed.")

    return "\n".join(lines)


def write_report(report_dir: str, content: str) -> Path:
    directory = Path(report_dir)
    directory.mkdir(parents=True, exist_ok=True)
    filename = directory / f"weekly-report-{datetime.now(timezone.utc).date().isoformat()}.md"
    filename.write_text(content, encoding="utf-8")
    return filename
