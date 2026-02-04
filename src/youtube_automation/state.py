import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class VideoEvent:
    video_id: str
    title: str
    timestamp: str


@dataclass
class State:
    downloaded_ids: List[str] = field(default_factory=list)
    uploads: List[VideoEvent] = field(default_factory=list)
    downloads: List[VideoEvent] = field(default_factory=list)
    last_report_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "downloaded_ids": self.downloaded_ids,
            "uploads": [event.__dict__ for event in self.uploads],
            "downloads": [event.__dict__ for event in self.downloads],
            "last_report_at": self.last_report_at,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "State":
        uploads = [VideoEvent(**item) for item in payload.get("uploads", [])]
        downloads = [VideoEvent(**item) for item in payload.get("downloads", [])]
        return cls(
            downloaded_ids=payload.get("downloaded_ids", []),
            uploads=uploads,
            downloads=downloads,
            last_report_at=payload.get("last_report_at", ""),
        )


class StateStore:
    def __init__(self, path: str):
        self.path = Path(path)

    def load(self) -> State:
        if not self.path.exists():
            return State()
        with self.path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return State.from_dict(payload)

    def save(self, state: State) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(state.to_dict(), handle, indent=2, sort_keys=True)

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()
