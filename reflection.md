# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

a.

- The 4 classes that I included were:
  - Pet, needs a name, species, age, owner_name, condition, list of tasks in **Init**.
    - **Methods: **
      - add_task(task): Add a task to this pet
      - remove_task (task): Remove a task
      - edit_task (task, duration, priority): Looking through current list of tasks, if there is a match, can modify how long the task takes or its priority
      - (idea is that if the pet gets older or has a change in health condition, some tasks may be modified or removed) .
  - Owner, needs a name, time available (total amount of time owner would have to dedicate to pet care), preferences/constraints in **Init**.
    - Owner ◆——— Pet (the idea is one owner could potentially own multiple pets).
      - **Methods: **
        - Register_pet(pet): Add pet to owner's list.
        - Remove_pet(pet): Removes pet from list. Maybe deceased, or using different services.
  - Task, needs a name, duration, priority, category (walk, feed, give medication, wash, etc), frequency, completion status.
    - Pet ◆——— Task (tasks belong to a pet)
      - ** Methods: **
        - **Init**: Initializes the name, duration, priority and category.
        - Mark_complete(): Indicates the task is done.
  - Scheduler, given the owner, a list of pet tasks, applies constraints (based on preferences and condition), then produces a plan output in **Init**.
    - Scheduler - - -> Owner
    - Scheduler - - -> Pet
      - ** Methods: **
        - generate_daily_plan(self, owner: Owner) -> list:
        - \_is_feasible(self, task: Task, pet: Pet) -> bool: Helper function
        - \_fit_to_time(self, tasks: list, time_available: int) -> list: Helper function
- The core actions (at least three) I came up with initially are:
  - Register a pet. This should be a function under owner where they append a pet object to a list.
  - Adding a task. This function will belong on the "Pet" class. The caller creates the task first, then passes in its name, duration, priority, category to the pets' personal list. Potential edge case I can think of is: What if the duration is 0, also how does it handle redundant tasks?
  - Editing a task. Pass in the task you want to modify as well as their duration, priority. Will search through pet's task list and modify any that match. So there's also an edge case here, what if it can't find a corresponding entered task.
  - Generating a daily plan: Look at the owner's preferences/constraints, the pet's condition, priority to come up with a finalized schedule. Possible edge case would be what if multiple tasks have the same priority?

b.

- My design originally had 5 classes, with an additional daily plan. However, I decided against creating a whole other class when my Scheduler class could just as easily have a method to return the daily plan list.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  - Time available: The owner's total time budget for the day. If a task cannot fit within the given time, drop it.
  - Pet condition: A pet may be sick, so skip the task for that day.
  - Task priority: Goes along with time availability, is the tie-breaker which tasks will survive the cut. Walking (pet stays in healthy shape) is typically higher priority than grooming (can wait another day).
- How did you decide which constraints mattered most?
  - I decided based on which constraints interacted with each other the best.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

- The scheduler is sorted based on priority and greedily picks tasks until the time runs out. It doesn't try EVERY OTHER combination to maximize how many tasks fit.
- The trade-off is reasonable because a pet care app should respect the owner's stated priorities above all else. If they marked something as priority 1, it should happen even if it takes longer than lower-priority tasks. The alternative would have been a knapsack style optimizier which would have skipped high-priority tasks which would be problematic in situations like what if a pet requires a medication.
- A (design) trade off is tasks are specific to pets rather than existing in a shared pool.
- Reasonable because pet care tasks are inherently pet-specific. You can't give dog medication to a cat, or walk a parakeet in place of a dog. Each pet is different and has their own needs.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

---

- I used AI tools for design brainstorming (helping determine what classes I would need and what their attributes/methods are).
- Prompts/questions I felt were most helpful were when I had the AI refer to my reflection responses, that way it would have the context what should be implemented.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

- When I visited Phase 2 of the project requirements, I noticed that there should be a way for the owner to view all the tasks for pets. I revisited my earlier project designs and created a get_all_tasks() method which would take in a pet name, and then it would check the owner's own pet list and see if the name exists, and if so, fetch the tasks.
- I noticed that the class function didn't seem to account for pet's condition. I changed pet's condition variable to be a list of strings.
- Added in scheduler to skip tasks given a certain condition, but if there is a task like say "sick" then medication should absolutely be done.

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
