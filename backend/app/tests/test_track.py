from collections.abc import Mapping
from typing import Callable, Dict


def test_create_track(
    test_user: Mapping[str, str],
    habit_factory: Callable[[int, str], Dict[str, str]],
    track_factory: Callable[[int, int], Dict[str, str]],
):
    habit = habit_factory(int(test_user["id"]), "Jogging")
    track = track_factory(int(test_user["id"]), int(habit["id"]))

    assert track["habit_id"] == habit["id"]
    assert track["user_id"] == test_user["id"]
    assert "timestamp" in track
