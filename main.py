from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Kyle", time_available=90)

buddy = Pet(name="Buddy", species="Dog", age=3, owner_name="Kyle")
whiskers = Pet(name="Whiskers", species="Cat", age=5, owner_name="Kyle")

owner.register_pet(buddy)
owner.register_pet(whiskers)

# --- Tasks for Buddy ---
buddy.add_task(Task(name="Morning Walk", description="30-min walk around the block",          due_time="9:00 AM",  duration=30, priority=1, category="walk"))
buddy.add_task(Task(name="Breakfast",    description="One cup of dry kibble",                  due_time="7:00 AM",  duration=10, priority=2, category="feed"))
buddy.add_task(Task(name="Evening Walk", description="Evening walk before sunset",             due_time="6:00 PM",  duration=30, priority=3, category="walk"))

# --- Tasks for Whiskers ---
whiskers.add_task(Task(name="Medication", description="Half-pill hidden in wet food",          due_time="9:00 AM",  duration=5,  priority=1, category="medication"))
whiskers.add_task(Task(name="Playtime",   description="Interactive wand toy session",          due_time="10:00 AM", duration=20, priority=2, category="play"))
whiskers.add_task(Task(name="Dinner",     description="Quarter-can of wet food",               due_time="5:00 PM",  duration=10, priority=2, category="feed"))
whiskers.add_task(Task(name="Grooming",   description="Brush coat to reduce shedding",         due_time="11:00 AM", duration=15, priority=3, category="clean"))

# --- Schedule ---
scheduler = Scheduler()

conflicts = scheduler.detect_conflicts(owner)
if conflicts:
    print("\n⚠ Scheduling conflicts detected:")
    for pet_a, task_a, pet_b, task_b in conflicts:
        print(f"  {pet_a.name}: '{task_a.name}' and {pet_b.name}: '{task_b.name}' both at {task_a.due_time}")
    print()

plan = scheduler.generate_daily_plan(owner)

print("=" * 40)
print("       Today's Schedule for", owner.name)
print("=" * 40)
for i, entry in enumerate(plan, start=1):
    print(f"{i}. [{entry['category'].upper()}] {entry['pet']} — {entry['task']} @ {entry['due_time']} ({entry['duration']} min, priority {entry['priority']})")
    print(f"      {entry['description']}")
print("-" * 40)
print(f"Total time used : {owner.time_available - scheduler.remaining_time} min")
print(f"Time remaining  : {scheduler.remaining_time} min")
print("=" * 40)

# --- Simulate completing some tasks ---
buddy.tasks[0].mark_complete()      # Morning Walk
whiskers.tasks[0].mark_complete()   # Medication

# --- End of day summary ---
print("\n" + "=" * 40)
print("        End of Day Summary")
print("=" * 40)
for pet in owner.pets:
    for task in scheduler.sort_by_time(pet.get_all_tasks()): # Added sort by time call here
        status = "✓ done" if task.completed else "✗ pending"
        print(f"  {status}  |  {pet.name}: {task.name} @ {task.due_time}")
print("=" * 40)
