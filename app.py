import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

CONDITION_OPTIONS = ["healthy", "injured", "sick", "elderly", "pregnant", "clean"]

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Session state: list of Owner objects ──────────────────────────────────────
if "owners" not in st.session_state:
    st.session_state.owners = []

if "selected_owner_index" not in st.session_state:
    st.session_state.selected_owner_index = None

owners: list[Owner] = st.session_state.owners

# ── Sidebar: Owner management ─────────────────────────────────────────────────
with st.sidebar:
    st.header("Owners")

    # Add new owner form
    with st.expander("Add Owner", expanded=len(owners) == 0):
        new_owner_name = st.text_input("Name", key="new_owner_name")
        new_owner_time = st.number_input("Time available (min/day)", min_value=1, max_value=1440, value=120, key="new_owner_time")
        if st.button("Create Owner"):
            if new_owner_name.strip():
                owners.append(Owner(name=new_owner_name.strip(), time_available=int(new_owner_time)))
                st.session_state.selected_owner_index = len(owners) - 1
                st.rerun()
            else:
                st.warning("Please enter a name.")

    st.divider()

    # List existing owners as selectable buttons
    if owners:
        st.subheader("Select Owner")
        for i, o in enumerate(owners):
            label = f"{o.name} ({len(o.pets)} pet{'s' if len(o.pets) != 1 else ''})"
            col_select, col_remove = st.columns([3, 1])
            with col_select:
                if st.button(label, key=f"owner_btn_{i}"):
                    st.session_state.selected_owner_index = i
                    st.rerun()
            with col_remove:
                if st.button("✕", key=f"owner_remove_{i}", help=f"Remove {o.name}"):
                    owners.pop(i)
                    if st.session_state.selected_owner_index == i:
                        st.session_state.selected_owner_index = None
                    elif st.session_state.selected_owner_index and st.session_state.selected_owner_index > i:
                        st.session_state.selected_owner_index -= 1
                    st.rerun()
    else:
        st.info("No owners yet. Create one above.")

# ── Main panel ────────────────────────────────────────────────────────────────
idx = st.session_state.selected_owner_index

if idx is None or idx >= len(owners):
    st.info("Create an owner in the sidebar to get started.")
    st.stop()

owner: Owner = owners[idx]

# Owner header + edit
col_title, col_edit = st.columns([3, 1])
with col_title:
    st.subheader(f"Owner: {owner.name}")
    st.caption(f"Time available: {owner.time_available} min/day")

with col_edit:
    if st.button("Edit Owner"):
        st.session_state[f"editing_owner_{idx}"] = True

if st.session_state.get(f"editing_owner_{idx}"):
    with st.form(f"edit_owner_form_{idx}"):
        updated_name = st.text_input("Name", value=owner.name)
        updated_time = st.number_input("Time available (min/day)", min_value=1, max_value=1440, value=owner.time_available)
        col_save, col_cancel = st.columns(2)
        with col_save:
            save = st.form_submit_button("Save")
        with col_cancel:
            cancel = st.form_submit_button("Cancel")
    if save:
        owner.name = updated_name.strip() or owner.name
        owner.time_available = int(updated_time)
        st.session_state[f"editing_owner_{idx}"] = False
        st.rerun()
    if cancel:
        st.session_state[f"editing_owner_{idx}"] = False
        st.rerun()

st.divider()

# ── Pets section ──────────────────────────────────────────────────────────────
st.subheader("Pets")

# Add pet form
with st.expander("Add a Pet"):
    with st.form("add_pet_form", clear_on_submit=True):
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1:
            pet_name = st.text_input("Pet name")
        with p_col2:
            pet_species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "other"])
        with p_col3:
            pet_age = st.number_input("Age", min_value=0, max_value=50, value=1)

        pet_conditions = st.multiselect(
            "Conditions",
            CONDITION_OPTIONS,
            default=["healthy"],
            help="Conditions affect which tasks are scheduled and their priority.",
        )

        submitted = st.form_submit_button("Add Pet")
        if submitted:
            if pet_name.strip():
                new_pet = Pet(
                    name=pet_name.strip(),
                    species=pet_species,
                    age=int(pet_age),
                    owner_name=owner.name,
                    condition=pet_conditions or ["healthy"],
                )
                owner.register_pet(new_pet)
                st.rerun()
            else:
                st.warning("Please enter a pet name.")

if not owner.pets:
    st.info("No pets yet. Add one above.")
    st.stop()

# Pet selector tabs
pet_names = [p.name for p in owner.pets]
selected_pet_name = st.radio("Select pet", pet_names, horizontal=True, key=f"pet_radio_{idx}")
pet: Pet = next(p for p in owner.pets if p.name == selected_pet_name)

pet_key = f"editing_pet_{idx}_{pet.name}"

col_petinfo, col_petedit = st.columns([4, 1])
with col_petinfo:
    st.markdown(f"**{pet.name}** — {pet.species}, age {pet.age}  |  Conditions: {', '.join(pet.condition)}")
with col_petedit:
    if st.button("Edit Pet"):
        st.session_state[pet_key] = True

if st.session_state.get(pet_key):
    with st.form(f"edit_pet_form_{idx}_{pet.name}"):
        e_col1, e_col2, e_col3 = st.columns(3)
        with e_col1:
            updated_pet_name = st.text_input("Name", value=pet.name)
        with e_col2:
            updated_species = st.selectbox(
                "Species", ["dog", "cat", "bird", "rabbit", "other"],
                index=["dog", "cat", "bird", "rabbit", "other"].index(pet.species)
                      if pet.species in ["dog", "cat", "bird", "rabbit", "other"] else 4,
            )
        with e_col3:
            updated_age = st.number_input("Age", min_value=0, max_value=50, value=pet.age)

        updated_conditions = st.multiselect(
            "Conditions",
            CONDITION_OPTIONS,
            default=[c for c in pet.condition if c in CONDITION_OPTIONS],
            help="Conditions block certain task categories and affect scheduling priority.",
        )

        e_save, e_cancel = st.columns(2)
        with e_save:
            save_pet = st.form_submit_button("Save")
        with e_cancel:
            cancel_pet = st.form_submit_button("Cancel")

    if save_pet:
        pet.name = updated_pet_name.strip() or pet.name
        pet.species = updated_species
        pet.age = int(updated_age)
        pet.condition = updated_conditions or ["healthy"]
        st.session_state[pet_key] = False
        st.rerun()
    if cancel_pet:
        st.session_state[pet_key] = False
        st.rerun()

st.divider()

# ── Tasks for selected pet ────────────────────────────────────────────────────
st.subheader(f"Tasks for {pet.name}")

st.markdown(
    "<style>small.st-emotion-cache-ue6h4q { display: none; }</style>",
    unsafe_allow_html=True,
)

with st.expander("Add a Task"):
    # Compute which categories are blocked by this pet's current conditions
    _blocked = set()
    for _cond in pet.condition:
        _blocked.update(Scheduler.CONDITION_BLOCKS.get(_cond, []))
    _all_categories = ["walk", "feed", "medication", "grooming", "play", "other"]
    available_categories = [c for c in _all_categories if c not in _blocked]

    if _blocked:
        st.caption(f"Blocked for {pet.name}'s conditions: {', '.join(sorted(_blocked))}")

    with st.form("add_task_form", clear_on_submit=True):
        t_col1, t_col2, t_col3 = st.columns(3)
        with t_col1:
            task_name = st.text_input("Task name", placeholder="e.g. Morning walk")
        with t_col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=None, placeholder="20")
        with t_col3:
            priority = st.selectbox("Priority (1=high)", [1, 2, 3, 4, 5], index=None, placeholder="Select priority")

        t_col4, t_col5 = st.columns(2)
        with t_col4:
            due_time = st.text_input("Due time", placeholder="e.g. 8:00 AM")
        with t_col5:
            category = st.selectbox("Category", available_categories, index=None, placeholder="Select category")

        description = st.text_input("Description", placeholder="Optional")

        submitted = st.form_submit_button("Add Task")
        if submitted:
            if not task_name.strip():
                st.warning("Please enter a task name.")
            else:
                new_task = Task(
                    name=task_name.strip(),
                    description=description,
                    due_time=due_time or "",
                    duration=int(duration) if duration else 1,
                    priority=priority if priority else 2,
                    category=category if category else "other",
                )
                pet.add_task(new_task)
                conflicts = Scheduler().detect_conflicts(owner)
                if conflicts:
                    st.session_state["task_conflicts"] = [
                        {
                            "pet_a": pa.name, "task_a": ta.name, "time": ta.due_time,
                            "pet_b": pb.name, "task_b": tb.name,
                        }
                        for pa, ta, pb, tb in conflicts
                    ]
                st.rerun()

if "task_conflicts" in st.session_state:
    for i, c in enumerate(st.session_state["task_conflicts"]):
        st.warning(
            f"Time conflict at {c['time']}: **{c['task_a']}** ({c['pet_a']}) "
            f"and **{c['task_b']}** ({c['pet_b']})"
        )
        col_a, col_b, col_dismiss = st.columns(3)
        with col_a:
            if st.button(f"Drop '{c['task_a']}'", key=f"drop_a_{i}"):
                for p in owner.pets:
                    if p.name == c["pet_a"]:
                        p.tasks = [t for t in p.tasks if not (t.name == c["task_a"] and t.due_time == c["time"])]
                st.session_state["task_conflicts"].pop(i)
                if not st.session_state["task_conflicts"]:
                    st.session_state.pop("task_conflicts")
                st.rerun()
        with col_b:
            if st.button(f"Drop '{c['task_b']}'", key=f"drop_b_{i}"):
                for p in owner.pets:
                    if p.name == c["pet_b"]:
                        p.tasks = [t for t in p.tasks if not (t.name == c["task_b"] and t.due_time == c["time"])]
                st.session_state["task_conflicts"].pop(i)
                if not st.session_state["task_conflicts"]:
                    st.session_state.pop("task_conflicts")
                st.rerun()
        with col_dismiss:
            if st.button("Keep both", key=f"dismiss_{i}"):
                st.session_state["task_conflicts"].pop(i)
                if not st.session_state["task_conflicts"]:
                    st.session_state.pop("task_conflicts")
                st.rerun()

all_tasks = pet.get_all_tasks()
if all_tasks:
    for i, t in enumerate(all_tasks):
        task_edit_key = f"editing_task_{idx}_{pet.name}_{i}"
        col_info, col_edit, col_remove = st.columns([4, 1, 1])
        with col_info:
            st.markdown(
                f"**{t.name}** — {t.category} | Due: {t.due_time} | "
                f"{t.duration} min | Priority: {t.priority} | "
                f"{'~~Done~~' if t.completed else 'Pending'}"
            )
        with col_edit:
            if st.button("Edit", key=f"edit_task_btn_{idx}_{pet.name}_{i}"):
                st.session_state[task_edit_key] = True
        with col_remove:
            if st.button("Remove", key=f"remove_task_{idx}_{pet.name}_{i}"):
                pet.remove_task(t)
                st.rerun()

        if st.session_state.get(task_edit_key):
            with st.form(f"edit_task_form_{idx}_{pet.name}_{i}"):
                et_col1, et_col2, et_col3 = st.columns(3)
                with et_col1:
                    updated_task_name = st.text_input("Task name", value=t.name)
                with et_col2:
                    updated_duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=t.duration)
                with et_col3:
                    updated_priority = st.selectbox("Priority (1=high)", [1, 2, 3, 4, 5], index=t.priority - 1)

                et_col4, et_col5 = st.columns(2)
                with et_col4:
                    updated_due_time = st.text_input("Due time", value=t.due_time)
                with et_col5:
                    _all_categories = ["walk", "feed", "medication", "grooming", "play", "other"]
                    cat_index = _all_categories.index(t.category) if t.category in _all_categories else 5
                    updated_category = st.selectbox("Category", _all_categories, index=cat_index)

                updated_description = st.text_input("Description", value=t.description)

                et_save, et_cancel = st.columns(2)
                with et_save:
                    save_task = st.form_submit_button("Save")
                with et_cancel:
                    cancel_task = st.form_submit_button("Cancel")

            if save_task:
                t.name = updated_task_name.strip() or t.name
                t.duration = int(updated_duration)
                t.priority = updated_priority
                t.due_time = updated_due_time
                t.category = updated_category
                t.description = updated_description
                st.session_state[task_edit_key] = False
                st.rerun()
            if cancel_task:
                st.session_state[task_edit_key] = False
                st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate Schedule ─────────────────────────────────────────────────────────
st.subheader("Build Schedule")
st.caption(f"Fits tasks for all of {owner.name}'s pets within {owner.time_available} min.")

col_gen, col_reset = st.columns([3, 1])
with col_gen:
    if st.button("Generate schedule", use_container_width=True):
        scheduler = Scheduler()
        plan = scheduler.generate_daily_plan(owner)
        if plan:
            st.success(f"Scheduled {len(plan)} task(s) — {scheduler.remaining_time} min remaining.")
            st.table(plan)
        else:
            st.warning("No tasks could be scheduled. Add tasks to a pet first.")
with col_reset:
    if st.button("Reset all tasks", use_container_width=True, type="secondary"):
        Scheduler().reset_tasks(owner)
        st.success(f"All tasks cleared for {owner.name}'s pets.")
        st.rerun()
