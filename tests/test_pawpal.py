from pawpal_system import Task, Pet, Owner, Scheduler


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_task(name, due_time, duration=30, priority=2, category="walk"):
    return Task(name, f"{name} description", due_time, duration, priority, category)


# ── Test 1: Tasks assigned with times out of order ────────────────────────────

def test_sort_by_time_returns_chronological_order():
    scheduler = Scheduler()
    tasks = [
        make_task("Dinner", "6:00 PM"),
        make_task("Morning Walk", "8:00 AM"),
        make_task("Lunch", "12:00 PM"),
    ]
    sorted_tasks = scheduler.sort_by_time(tasks)
    due_times = [t.name for t in sorted_tasks]
    assert due_times == ["Morning Walk", "Lunch", "Dinner"]


# ── Test 2: Pet with no tasks ─────────────────────────────────────────────────

def test_generate_daily_plan_with_no_tasks():
    scheduler = Scheduler()
    owner = Owner("Alice", 120)
    pet = Pet("Buddy", "dog", 3, "Alice")
    owner.register_pet(pet)

    plan = scheduler.generate_daily_plan(owner)
    assert plan == []


# ── Test 4: Two pets with tasks at the same time (conflict detection) ─────────

def test_detect_conflicts_two_pets_same_time():
    scheduler = Scheduler()
    owner = Owner("Alice", 120)

    pet_a = Pet("Buddy", "dog", 3, "Alice")
    pet_b = Pet("Whiskers", "cat", 2, "Alice")
    pet_a.add_task(make_task("Morning Walk", "8:00 AM"))
    pet_b.add_task(make_task("Feeding", "8:00 AM"))
    owner.register_pet(pet_a)
    owner.register_pet(pet_b)

    conflicts = scheduler.detect_conflicts(owner)
    assert len(conflicts) == 1
    pa, ta, pb, tb = conflicts[0]
    assert {pa.name, pb.name} == {"Buddy", "Whiskers"}
    assert {ta.name, tb.name} == {"Morning Walk", "Feeding"}


def test_detect_conflicts_no_overlap():
    scheduler = Scheduler()
    owner = Owner("Alice", 120)

    pet_a = Pet("Buddy", "dog", 3, "Alice")
    pet_b = Pet("Whiskers", "cat", 2, "Alice")
    pet_a.add_task(make_task("Morning Walk", "8:00 AM"))
    pet_b.add_task(make_task("Feeding", "9:00 AM"))
    owner.register_pet(pet_a)
    owner.register_pet(pet_b)

    conflicts = scheduler.detect_conflicts(owner)
    assert conflicts == []


# ── Test 5: Owner time budget exhausted ───────────────────────────────────────

def test_generate_daily_plan_respects_time_budget():
    scheduler = Scheduler()
    owner = Owner("Alice", 30)  # only 30 minutes available
    pet = Pet("Buddy", "dog", 3, "Alice")

    pet.add_task(Task("Morning Walk", "Walk", "8:00 AM", 30, 1, "walk"))
    pet.add_task(Task("Grooming", "Brush coat", "9:00 AM", 20, 2, "grooming"))
    pet.add_task(Task("Playtime", "Fetch", "10:00 AM", 15, 3, "play"))
    owner.register_pet(pet)

    plan = scheduler.generate_daily_plan(owner)
    total_duration = sum(entry["duration"] for entry in plan)
    assert total_duration <= 30
    # Highest priority task (Morning Walk, priority=1) must be included
    task_names = [entry["task"] for entry in plan]
    print("Planned tasks:", task_names)
    assert "Morning Walk" in task_names

# ── Test 5: Owner time budget exhausted ───────────────────────────────────────

def test_empty_plan_when_time_budget_exhausted():
    scheduler = Scheduler()
    owner = Owner("Alice", 30)  # only 30 minutes available
    pet = Pet("Buddy", "dog", 3, "Alice")

    pet.add_task(Task("Morning Walk", "Walk", "8:00 AM", 35, 1, "walk"))
    pet.add_task(Task("Grooming", "Brush coat", "9:00 AM", 40, 2, "grooming"))
    pet.add_task(Task("Playtime", "Fetch", "10:00 AM", 60, 3, "play"))
    owner.register_pet(pet)

    plan = scheduler.generate_daily_plan(owner)
    total_duration = sum(entry["duration"] for entry in plan)
    assert total_duration <= 30
    # Highest priority task (Morning Walk, priority=1) must be included
    task_names = [entry["task"] for entry in plan]
    assert len(task_names) == 0
