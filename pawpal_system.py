from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    name: str
    duration: int  # minutes
    priority: int  # e.g. 1 (highest) to 5 (lowest)
    category: str  # e.g. "walk", "feeding", "meds", "grooming", "enrichment"


class Pet:
    def __init__(self, name: str, species: str, age: int, owner_name: str, condition: Optional[str] = None):
        self.name = name
        self.species = species
        self.age = age
        self.owner_name = owner_name
        self.condition = condition
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_name: str) -> None:
        pass

    def edit_task(self, task_name: str, **updates) -> None:
        pass


class Owner:
    def __init__(self, name: str, time_available: int, preferences: Optional[dict] = None):
        self.name = name
        self.time_available = time_available  # minutes per day
        self.preferences = preferences or {}
        self.pets: list[Pet] = []

    def register_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_name: str) -> None:
        pass


class Scheduler:
    def generate_daily(self, owner: Owner, pet: Pet) -> list[Task]:
        pass

    def _is_feasible(self, tasks: list[Task], time_available: int) -> bool:
        pass

    def _fit_to_time(self, tasks: list[Task], time_available: int) -> list[Task]:
        pass
