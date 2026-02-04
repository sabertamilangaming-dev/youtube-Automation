from youtube_automation.state import State, StateStore, VideoEvent


def test_state_round_trip(tmp_path):
    store = StateStore(str(tmp_path / "state.json"))
    state = State(
        downloaded_ids=["abc"],
        uploads=[VideoEvent(video_id="abc", title="Title", timestamp="2024-01-01T00:00:00+00:00")],
        downloads=[VideoEvent(video_id="abc", title="Title", timestamp="2024-01-01T01:00:00+00:00")],
        last_report_at="2024-01-02T00:00:00+00:00",
    )
    store.save(state)
    loaded = store.load()
    assert loaded.downloaded_ids == ["abc"]
    assert loaded.uploads[0].title == "Title"
    assert loaded.last_report_at == "2024-01-02T00:00:00+00:00"
