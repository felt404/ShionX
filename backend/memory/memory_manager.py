from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.config import MEMORIES_DIR


class MemoryManager:
    """Simple JSON/TXT-backed memory manager for context, history, and notes."""

    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or MEMORIES_DIR
        self.context_file = self.base_dir / "context" / "current.json"
        self.history_file = self.base_dir / "history" / "history.jsonl"
        self.notes_file = self.base_dir / "notes" / "notes.txt"

        self.context_file.parent.mkdir(parents=True, exist_ok=True)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.notes_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.context_file.exists():
            self.save_context({"created_at": self._now_iso(), "items": []})
        if not self.history_file.exists():
            self.history_file.touch()
        if not self.notes_file.exists():
            self.notes_file.write_text("", encoding="utf-8")

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def load_context(self) -> dict[str, Any]:
        with self.context_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_context(self, context: dict[str, Any]) -> None:
        payload = dict(context)
        payload["updated_at"] = self._now_iso()
        with self.context_file.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def add_history(self, role: str, content: str) -> None:
        entry = {
            "timestamp": self._now_iso(),
            "role": role,
            "content": content,
        }
        with self.history_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_history(self, limit: int = 10) -> list[dict[str, Any]]:
        lines = self.history_file.read_text(encoding="utf-8").splitlines()
        if not lines:
            return []

        entries: list[dict[str, Any]] = []
        for line in lines[-max(limit, 1) :]:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return entries

    def append_note(self, note: str) -> None:
        note = note.strip()
        if not note:
            return

        with self.notes_file.open("a", encoding="utf-8") as f:
            f.write(f"[{self._now_iso()}] {note}\n")

    def get_notes(self) -> list[str]:
        content = self.notes_file.read_text(encoding="utf-8")
        return [line for line in content.splitlines() if line.strip()]
