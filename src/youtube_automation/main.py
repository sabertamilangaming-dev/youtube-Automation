import logging
import sys
from typing import List

from youtube_automation.config import load_settings
from youtube_automation.downloader import Downloader
from youtube_automation.logger import configure_logging
from youtube_automation.report import render_report, write_report
from youtube_automation.scheduler import Scheduler
from youtube_automation.state import StateStore, VideoEvent
from youtube_automation.youtube_api import YouTubeApi

logger = logging.getLogger(__name__)


def handle_video_updates(
    api: YouTubeApi,
    channel_id: str,
    downloader: Downloader,
    state_store: StateStore,
) -> None:
    state = state_store.load()
    uploads_playlist_id = api.get_uploads_playlist_id(channel_id)
    videos = api.list_latest_videos(uploads_playlist_id)

    new_uploads: List[VideoEvent] = []
    for video in videos:
        video_id = video.get("video_id", "")
        if not video_id:
            continue
        if video_id not in state.downloaded_ids:
            new_uploads.append(
                VideoEvent(
                    video_id=video_id,
                    title=video.get("title", ""),
                    timestamp=video.get("published_at", ""),
                )
            )

    for upload in new_uploads:
        state.uploads.append(upload)
        if upload.video_id in state.downloaded_ids:
            continue
        path = downloader.download(upload.video_id)
        if path:
            state.downloaded_ids.append(upload.video_id)
            state.downloads.append(
                VideoEvent(
                    video_id=upload.video_id,
                    title=upload.title,
                    timestamp=StateStore.now_iso(),
                )
            )
    state_store.save(state)
    logger.info("Update cycle complete. New uploads: %s", len(new_uploads))


def generate_weekly_report(state_store: StateStore, report_dir: str) -> None:
    state = state_store.load()
    report_content = render_report(state)
    report_path = write_report(report_dir, report_content)
    state.last_report_at = StateStore.now_iso()
    state_store.save(state)
    logger.info("Weekly report written to %s", report_path)


def main() -> None:
    try:
        settings = load_settings()
    except ValueError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(1)

    configure_logging(settings.log_file)
    logger.info("Starting YouTube automation tool")

    api = YouTubeApi(settings.youtube_api_key)
    downloader = Downloader(settings.download_dir)
    state_store = StateStore(settings.state_file)

    scheduler = Scheduler(
        check_interval_minutes=settings.check_interval_minutes,
        report_day=settings.report_day,
        report_time_utc=settings.report_time_utc,
    )

    def check_job() -> None:
        try:
            handle_video_updates(api, settings.youtube_channel_id, downloader, state_store)
        except Exception as exc:
            logger.exception("Error during update cycle: %s", exc)

    def report_job() -> None:
        try:
            generate_weekly_report(state_store, settings.report_dir)
        except Exception as exc:
            logger.exception("Error during report generation: %s", exc)

    scheduler.setup(check_job, report_job)
    check_job()
    scheduler.run_forever()


if __name__ == "__main__":
    main()
