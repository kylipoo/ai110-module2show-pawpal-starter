class Task:
    def __init__(self, name: str, description: str, due_time: str, duration: int, priority: int, category: str):
        self.name = name
        self.description = description   # human-readable details about the task
        self.due_time = due_time         # e.g. "8:00 AM"
        self.duration = duration         # in minutes
        self.priority = priority         # 1 (highest) to 5 (lowest)
        self.category = category         # e.g. "walk", "feed", "medication"
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def __repr__(self):
        status = "done" if self.completed else "pending"
        return f"Task({self.name!r}, due={self.due_time}, {self.duration}min, priority={self.priority}, [{status}])"


class Pet:
    def __init__(self, name: str, species: str, age: int, owner_name: str, condition: list[str] = None):
        self.name = name
        self.species = species
        self.age = age
        self.owner_name = owner_name
        self.condition = condition if condition is not None else ["healthy"]
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task: Task):
        if task in self.tasks:
            self.tasks.remove(task)

    def edit_task(self, task: Task, duration: int = None, priority: int = None):
        for t in self.tasks:
            if t is task:
                if duration is not None:
                    t.duration = duration
                if priority is not None:
                    t.priority = priority
                return
        raise ValueError(f"Task {task.name!r} not found in {self.name}'s task list.")

    def get_all_tasks(self) -> list[Task]:
        return list(self.tasks)

    def __repr__(self):
        return f"Pet({self.name!r}, {self.species}, age={self.age}, conditions={self.condition})"


class Owner:
    def __init__(self, name: str, time_available: int, preferences: dict = None):
        self.name = name
        self.time_available = time_available  # total minutes available per day
        self.preferences = preferences or {}  # e.g. {"avoid_category": "walk", "max_priority": 3}
        self.pets: list[Pet] = []

    def register_pet(self, pet: Pet):
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Returns all (pet, task) pairs across every pet this owner has."""
        result = []
        for pet in self.pets:
            for task in pet.get_all_tasks():
                result.append((pet, task))
        return result

    def __repr__(self):
        return f"Owner({self.name!r}, time_available={self.time_available}min, pets={len(self.pets)})"


class Scheduler:
    def __init__(self):
        self.remaining_time = 0

    def generate_daily_plan(self, owner: Owner) -> list[dict]:
        """
        Collect all incomplete, feasible tasks across owner's pets,
        sort by priority, then fit within the owner's available time.
        Returns a list of dicts describing the scheduled tasks.
        """
        self.remaining_time = owner.time_available

        all_pairs = owner.get_all_tasks()

        # Filter to incomplete and feasible tasks only
        candidates = [
            (pet, task) for pet, task in all_pairs
            if not task.completed and self._is_feasible(task, pet, owner)
        ]

        # Sort by priority ascending (1 = highest priority first)
        candidates.sort(key=lambda pair: pair[1].priority)

        scheduled = self._fit_to_time(candidates, owner.time_available)

        plan = []
        for pet, task in scheduled:
            plan.append({
                "pet": pet.name,
                "task": task.name,
                "description": task.description,
                "due_time": task.due_time,
                "category": task.category,
                "duration": task.duration,
                "priority": task.priority,
            })
        return plan

    def _is_feasible(self, task: Task, pet: Pet, owner: Owner) -> bool:
        """
        Returns False if the owner's preferences exclude this task or pet condition
        makes it inappropriate.
        """
        avoid = owner.preferences.get("avoid_category")
        if avoid and task.category == avoid:
            return False

        max_priority = owner.preferences.get("max_priority")
        if max_priority and task.priority > max_priority:
            return False

        # Example condition rule: skip walks for injured pets
        if "injured" in pet.condition and task.category == "walk":
            return False

        return True

    def _fit_to_time(self, candidates: list[tuple[Pet, Task]], time_available: int) -> list[tuple[Pet, Task]]:
        """
        Greedily select tasks from the (already sorted) candidate list
        until the owner's available time is exhausted.
        """
        scheduled = []
        remaining = time_available
        for pet, task in candidates:
            if task.duration <= remaining:
                scheduled.append((pet, task))
                remaining -= task.duration
        self.remaining_time = remaining
        return scheduled
