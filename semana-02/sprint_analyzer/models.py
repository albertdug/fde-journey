from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Story:
    id: str
    title: str
    points: int
    status: str  # "done", "in_progress", "not_started"

@dataclass
class Sprint:
    number: int
    team_name: str
    start_date: datetime
    end_date: datetime
    committed_points: int
    stories: list[Story] = field(default_factory=list)

    @property
    def completed_points(self) -> int:
        return sum(s.points for s in self.stories if s.status == "done")

    @property
    def completion_rate(self) -> float:
        if self.committed_points == 0:
            return 0.0
        return round(self.completed_points / self.committed_points * 100, 1)

    def summary(self) -> str:
        return (
            f"Sprint {self.number} — {self.team_name}\n"
            f"  Comprometidos: {self.committed_points} pts\n"
            f"  Completados:   {self.completed_points} pts\n"
            f"  Completion:    {self.completion_rate}%\n"
            f"  Stories:       {len(self.stories)}"
        )