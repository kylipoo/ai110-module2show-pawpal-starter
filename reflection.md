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
- Added a detect_conflicts class to the scheduler class. For every task added for the pet, it will scan through the rest of their own task list and see if there's any overlapping due time.
- Added a CONDITION_BLOCKS attribute to the scheduler class. It takes into account the pet's condition through the following: If they are sick, injured or elderly, then walking and playing should not be options (in no condition). If the pet is clean, do not have the option to groom (is redundant).
- Here is my finalized class diagram: ![alt text](<Screenshot 2026-03-24 at 4.19.29 PM.jpg>)

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
- A drawback is when I run the sort by time algorithm is that the generate daily plan method is slower due to having to compare the times to each of the other pets' individual tasks to ensure correct order.
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
- When I was implementing the pairwise detection algorithm that checked conflicting schedules, I noticed that the AI's suggestion only worked in the context there was one conflict at a time. So when I tested adding multiple conflicting tasks throughout each pet, if I resolved one conflict, it would automatcially assume the rest were resolved, so I changed the detection algorithm to resolve conflicts based on indices.

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

- I tested the following:
  - Adding tasks with due times out of order.
    - Is important because the point of pawpal is that it can create an accurate daily planner for the owner who has passed in the tasks they want done and when to do it.
  - Conflicting due times.
    - Is important because it helps the owner with double checking if they've already reserved some time for another pet.
  - Checking if the owner's time budget has been exhausted.
    - My interpretation of the project had it the owner would keep track of how much time they had for the day, and that the daily plan function should budget within that amount.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

- I am very confident that my scheduler works correctly. From my tests, it is able to fit in tasks based on what the owner's provided time budget, sort based on the due time and account for when due time overlaps for tasks (an edge case).
- I would test what would happen if the owner's time budget was small and every single one of the tasks exceeds that budget. Does it return an empty schedule?
- This also goes into things to improve, but I'd like to address situations if multiple pets can have their tasks being done at the same time, like say I have 3 dogs? I can walk all three of them together. For now I just gave the task to one pet and made the description say "Is jointly walking with other pets".

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
- The UML diagram design. While it is true that I made a couple of revisions to class methods, I felt that having a basic framework of the relations between each class significantly helped me with drafting a functional application.
  - I felt I used codepath resources very well, attending study hall sessions.
- I am also satisfied with implementing the "greedy" part of Pawpal's scheduler. Upon doing some tests, it was able to simultaneously retrieve and organize a list of tasks based on priority while using the time budget to its fullest as best possible.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
- I would add a more robust long-term planning system where the owner can set up multiple schedules for future dates, all also with the same edit tasks options in case any sudden changes happen in their routines.
- Also I briefly touched upon it with the condition object, but I would love to look for a more dynamic option when it comes to filtering available tasks based on pet's condition.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
- I shouldn't immediately start into coding, I should approach projects with a plan. I should apply this approach of drawing a UML diagram or any other workflow before moving forward on any work assignment in the future.
