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
  - Task, needs a name, duration, priority, category (walk, feed, give medication, wash, etc).
    - Pet ◆——— Task (tasks belong to a pet)
      - ** Methods: **
        - **Init**: Initializes the name, duration, priority and category.
  - Scheduler, given the owner, a list of pet tasks, applies constraints (based on preferences and condition), then produces a plan output in **Init**.
    - Scheduler - - -> Owner
    - Scheduler - - -> Pet
      - ** Methods: **
        - generate_daily_plan(self, owner: Owner, pet: Pet) -> list:
        - \_is_feasible(self, task: Task, pet: Pet) -> bool: Helper function
        - \_fit_to_time(self, tasks: list, time_available: int) -> list: Helper function
- The core actions (at least three) I came up with initially are:
  - Register a pet. This should be a function under owner where they append a pet object to a list.
  - Adding a task. This function will belong on the "Pet" class. The caller creates the task first, then passes in its name, duration, priority, category to the pets' personal list. Potential edge case I can think of is: What if the duration is 0, also how does it handle redundant tasks?
  - Editing a task. Pass in the task you want to modify as well as their duration, priority. Will search through pet's task list and modify any that match. So there's also an edge case here, what if it can't find a corresponding entered task.
  - Generating a daily plan: Look at the owner's preferences/constraints, the pet's condition, priority to come up with a finalized schedule. Possible edge case would be what if multiple tasks have the same priority?

b.

- My design originally had 5 classes, with an additional daily plan. However, I decided against creating a whole other class when my Scheduler class could just as easily have a method to return the daily plan list.
- I made a trade-off:
  - The Generate_daily_plan() method originally only took in the owner according to Claude's suggestions, but I proposed to take in both owner and pet because it would give more context for what tasks to do and in what order for a pet.

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

- I had a previous draft where the scheduler would cover all pets (again, refer to the part generate_daily_plan() only took in an owner parameter), but by adding in pet as a parameter, it means that the daily_plan is only generated for an individual pet.
- A potential issue could be having to be mindful and differentiate which plan generated for a pet is most up to date. In addition, time budgeting will need to be per-pet instead of global. If the owner has 60 minutes across 3 pets, then he'll need to split it up. This isn't necessarily a problem, but it also brings to mind a potential edge case of what if the owner used up all their time for 2 pets, need to account for when no time left for last pet.
- A) Not every pet has the same daily schedule, for example the owner might have a dog, cat, parakeet, all of which have different tasks to look after. B) It's more flexible even for individual pets. What if the dog gets sick and is in recovery? A plan that involves walking is not applicable then. ALSO, while the time available will now need to be split up across how many pets the owner has, it has another benefit of flexibility since maybe one day a pet will need more time than typical for tasks. Like again, being sick.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

---

- I used AI tools for design brainstorming (helping determine what classes I would need and what their attributes/methods are).

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

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
