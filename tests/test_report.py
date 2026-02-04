from youtube_automation.report import render_report
from youtube_automation.state import State, VideoEvent


def test_report_includes_events():
    state = State(
        uploads=[VideoEvent(video_id="abc", title="Upload", timestamp="2024-01-01T00:00:00+00:00")],
        downloads=[VideoEvent(video_id="abc", title="Download", timestamp="2024-01-01T01:00:00+00:00")],
        last_report_at="",
    )
    report = render_report(state)
    assert "Upload" in report
    assert "Download" in report
