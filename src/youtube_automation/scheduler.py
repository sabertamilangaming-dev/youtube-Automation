import logging
import time
from datetime import datetime, timezone
from typing import Callable

import schedule

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, check_interval_minutes: int, report_day: str, report_time_utc: str):
        self.check_interval_minutes = check_interval_minutes
        self.report_day = report_day.lower()
        self.report_time_utc = report_time_utc

    def setup(self, check_job: Callable[[], None], report_job: Callable[[], None]) -> None:
        schedule.every(self.check_interval_minutes).minutes.do(check_job)

        weekday = getattr(schedule.every(), self.report_day, None)
        if weekday is None:
            raise ValueError(f"Invalid report day: {self.report_day}")
        weekday.at(self.report_time_utc).do(report_job)

    def run_forever(self) -> None:
        logger.info("Scheduler started")
        while True:
            schedule.run_pending()
            time.sleep(1)


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()
