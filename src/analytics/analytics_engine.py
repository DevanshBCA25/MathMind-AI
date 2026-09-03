from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.config.settings import LOG_DIR


ANALYTICS_FILE = (
    Path(LOG_DIR)
    / "analytics_events.json"
)


class AnalyticsEngine:
    """
    Lightweight analytics engine for MathMind AI.

    Stores application events locally in JSON format.
    No external analytics service is required.
    """

    def __init__(
        self,
        storage_path: Optional[
            str | Path
        ] = None,
    ):

        self.storage_path = Path(
            storage_path
            if storage_path
            else ANALYTICS_FILE
        )

        self.storage_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._ensure_storage()

    # ========================================================
    # STORAGE
    # ========================================================

    def _ensure_storage(self) -> None:

        if not self.storage_path.exists():

            self.storage_path.write_text(
                "[]",
                encoding="utf-8",
            )

    def _load_events(self) -> List[Dict[str, Any]]:

        try:

            content = (
                self.storage_path.read_text(
                    encoding="utf-8"
                )
            )

            if not content.strip():

                return []

            data = json.loads(
                content
            )

            if not isinstance(
                data,
                list,
            ):

                return []

            return data

        except (
            json.JSONDecodeError,
            OSError,
        ):

            return []

    def _save_events(
        self,
        events: List[Dict[str, Any]],
    ) -> None:

        self.storage_path.write_text(
            json.dumps(
                events,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

    # ========================================================
    # EVENT TRACKING
    # ========================================================

    def track_event(
        self,
        event_type: str,
        module: str = "unknown",
        status: str = "SUCCESS",
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:

        event = {
            "timestamp": (
                datetime.now().isoformat()
            ),
            "event_type": str(
                event_type
            ),
            "module": str(
                module
            ),
            "status": str(
                status
            ),
            "metadata": (
                metadata
                if metadata
                else {}
            ),
        }

        events = self._load_events()

        events.append(
            event
        )

        self._save_events(
            events
        )

        return event

    # ========================================================
    # QUERY
    # ========================================================

    def get_events(
        self,
    ) -> List[Dict[str, Any]]:

        return self._load_events()

    # ========================================================
    # SUMMARY
    # ========================================================

    def get_summary(
        self,
    ) -> Dict[str, Any]:

        events = self._load_events()

        total = len(events)

        success = sum(
            1
            for event in events
            if str(
                event.get(
                    "status",
                    "",
                )
            ).upper()
            == "SUCCESS"
        )

        errors = sum(
            1
            for event in events
            if str(
                event.get(
                    "status",
                    "",
                )
            ).upper()
            in {
                "ERROR",
                "FAILED",
                "FAILURE",
            }
        )

        api_errors = sum(
            1
            for event in events
            if str(
                event.get(
                    "status",
                    "",
                )
            ).upper()
            == "API_ERROR"
        )

        success_rate = (
            (success / total) * 100
            if total
            else 0.0
        )

        return {
            "total_events": total,
            "successful_events": success,
            "error_events": errors,
            "api_errors": api_errors,
            "success_rate": round(
                success_rate,
                2,
            ),
        }

    # ========================================================
    # MODULE STATISTICS
    # ========================================================

    def module_statistics(
        self,
    ) -> Dict[str, int]:

        events = self._load_events()

        counter = Counter()

        for event in events:

            module = event.get(
                "module",
                "unknown",
            )

            counter[
                str(module)
            ] += 1

        return dict(
            counter
        )

    # ========================================================
    # STATUS STATISTICS
    # ========================================================

    def status_statistics(
        self,
    ) -> Dict[str, int]:

        events = self._load_events()

        counter = Counter()

        for event in events:

            status = event.get(
                "status",
                "UNKNOWN",
            )

            counter[
                str(status).upper()
            ] += 1

        return dict(
            counter
        )

    # ========================================================
    # EVENT STATISTICS
    # ========================================================

    def event_statistics(
        self,
    ) -> Dict[str, int]:

        events = self._load_events()

        counter = Counter()

        for event in events:

            event_type = event.get(
                "event_type",
                "unknown",
            )

            counter[
                str(event_type)
            ] += 1

        return dict(
            counter
        )

    # ========================================================
    # CLEAR
    # ========================================================

    def clear_events(self) -> None:

        self._save_events(
            []
        )