from pathlib import Path
from tempfile import TemporaryDirectory

from src.analytics.analytics_engine import (
    AnalyticsEngine,
)


def test_analytics_storage():

    with TemporaryDirectory() as temp_dir:

        path = (
            Path(temp_dir)
            / "analytics.json"
        )

        analytics = AnalyticsEngine(
            storage_path=path
        )

        assert path.exists()


def test_track_event():

    with TemporaryDirectory() as temp_dir:

        path = (
            Path(temp_dir)
            / "analytics.json"
        )

        analytics = AnalyticsEngine(
            storage_path=path
        )

        event = analytics.track_event(
            event_type="test",
            module="calculator",
            status="SUCCESS",
        )

        assert (
            event["event_type"]
            == "test"
        )

        assert (
            event["module"]
            == "calculator"
        )

        assert (
            event["status"]
            == "SUCCESS"
        )


def test_summary():

    with TemporaryDirectory() as temp_dir:

        path = (
            Path(temp_dir)
            / "analytics.json"
        )

        analytics = AnalyticsEngine(
            storage_path=path
        )

        analytics.track_event(
            "solve",
            "calculator",
            "SUCCESS",
        )

        analytics.track_event(
            "solve",
            "symbolic",
            "SUCCESS",
        )

        analytics.track_event(
            "solve",
            "rag",
            "ERROR",
        )

        summary = (
            analytics.get_summary()
        )

        assert (
            summary["total_events"]
            == 3
        )

        assert (
            summary[
                "successful_events"
            ]
            == 2
        )

        assert (
            summary[
                "error_events"
            ]
            == 1
        )

        assert (
            summary[
                "success_rate"
            ]
            == 66.67
        )


def test_module_statistics():

    with TemporaryDirectory() as temp_dir:

        path = (
            Path(temp_dir)
            / "analytics.json"
        )

        analytics = AnalyticsEngine(
            storage_path=path
        )

        analytics.track_event(
            "solve",
            "calculator",
        )

        analytics.track_event(
            "solve",
            "calculator",
        )

        analytics.track_event(
            "solve",
            "rag",
        )

        stats = (
            analytics.module_statistics()
        )

        assert (
            stats["calculator"]
            == 2
        )

        assert (
            stats["rag"]
            == 1
        )


def test_status_statistics():

    with TemporaryDirectory() as temp_dir:

        path = (
            Path(temp_dir)
            / "analytics.json"
        )

        analytics = AnalyticsEngine(
            storage_path=path
        )

        analytics.track_event(
            "test",
            "core",
            "SUCCESS",
        )

        analytics.track_event(
            "test",
            "core",
            "ERROR",
        )

        stats = (
            analytics.status_statistics()
        )

        assert (
            stats["SUCCESS"]
            == 1
        )

        assert (
            stats["ERROR"]
            == 1
        )


def test_clear_events():

    with TemporaryDirectory() as temp_dir:

        path = (
            Path(temp_dir)
            / "analytics.json"
        )

        analytics = AnalyticsEngine(
            storage_path=path
        )

        analytics.track_event(
            "test",
            "core",
        )

        assert len(
            analytics.get_events()
        ) == 1

        analytics.clear_events()

        assert len(
            analytics.get_events()
        ) == 0


if __name__ == "__main__":

    test_analytics_storage()

    test_track_event()

    test_summary()

    test_module_statistics()

    test_status_statistics()

    test_clear_events()

    print()
    print(
        "======================================"
    )
    print(
        "        Analytics Tests"
    )
    print(
        "======================================"
    )
    print(
        "All tests passed successfully."
    )