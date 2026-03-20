import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

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
            if st.button(label, key=f"owner_btn_{i}"):
                st.session_state.selected_owner_index = i
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

        submitted = st.form_submit_button("Add Pet")
        if submitted:
            if pet_name.strip():
                new_pet = Pet(name=pet_name.strip(), species=pet_species, age=int(pet_age), owner_name=owner.name)
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

st.markdown(f"**{pet.name}** — {pet.species}, age {pet.age}  |  Conditions: {', '.join(pet.condition)}")

st.divider()

# ── Tasks for selected pet ────────────────────────────────────────────────────
st.subheader(f"Tasks for {pet.name}")

with st.expander("Add a Task"):
    with st.form("add_task_form", clear_on_submit=True):
        t_col1, t_col2, t_col3 = st.columns(3)
        with t_col1:
            task_name = st.text_input("Task name", value="Morning walk")
        with t_col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with t_col3:
            priority = st.selectbox("Priority (1=high)", [1, 2, 3, 4, 5], index=1)

        t_col4, t_col5 = st.columns(2)
        with t_col4:
            due_time = st.text_input("Due time", value="8:00 AM")
        with t_col5:
            category = st.selectbox("Category", ["walk", "feed", "medication", "grooming", "play", "other"])

        description = st.text_input("Description", value="")

        submitted = st.form_submit_button("Add Task")
        if submitted:
            new_task = Task(
                name=task_name,
                description=description,
                due_time=due_time,
                duration=int(duration),
                priority=priority,
                category=category,
            )
            pet.add_task(new_task)
            st.success(f"Added: {new_task}")
            st.rerun()

all_tasks = pet.get_all_tasks()
if all_tasks:
    for i, t in enumerate(all_tasks):
        col_info, col_btn = st.columns([5, 1])
        with col_info:
            st.markdown(
                f"**{t.name}** — {t.category} | Due: {t.due_time} | "
                f"{t.duration} min | Priority: {t.priority} | "
                f"{'~~Done~~' if t.completed else 'Pending'}"
            )
        with col_btn:
            if st.button("Remove", key=f"remove_task_{idx}_{pet.name}_{i}"):
                pet.remove_task(t)
                st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate Schedule ─────────────────────────────────────────────────────────
st.subheader("Build Schedule")
st.caption(f"Fits tasks for all of {owner.name}'s pets within {owner.time_available} min.")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    plan = scheduler.generate_daily_plan(owner)
    if plan:
        st.success(f"Scheduled {len(plan)} task(s) — {scheduler.remaining_time} min remaining.")
        st.table(plan)
    else:
        st.warning("No tasks could be scheduled. Add tasks to a pet first.")
