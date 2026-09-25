from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


class ReportStore:
    def __init__(self, directory: Path):
        self.directory = directory
        self.events: list[dict] = []

    def add(self, category: str, payload: object) -> None:
        self.events.append({
            "time_utc": datetime.now(timezone.utc).isoformat(),
            "category": category,
            "payload": payload,
        })

    def write(self) -> tuple[Path, Path]:
        self.directory.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        js = self.directory / f"scorpion-{stamp}.json"
        md = self.directory / f"scorpion-{stamp}.md"

        data = {
            "project": "OBT SCORPION",
            "author": "OMAR BEN TALEB",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "events": self.events,
        }
        js.write_text(json.dumps(data, indent=2, ensure_ascii=False))

        lines = [
            "# OBT SCORPION Evidence Report",
            "",
            "**Author:** OMAR BEN TALEB",
            f"**Generated:** {data['generated_utc']}",
            "",
        ]
        for idx, event in enumerate(self.events, 1):
            lines += [
                f"## {idx}. {event['category']}",
                "",
                f"Time: `{event['time_utc']}`",
                "",
                "```json",
                json.dumps(event["payload"], indent=2, ensure_ascii=False),
                "```",
                "",
            ]
        md.write_text("\n".join(lines))
        return md, js
