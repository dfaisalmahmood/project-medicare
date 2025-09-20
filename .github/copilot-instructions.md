---
applyTo: "**"
---

GENERAL GUIDELINES:

1. Use DRY principle. Reuse code and components where possible.
2. Before installing a package, confirm with user.
3. Always create tasks and follow TASK MANAGEMENT rules when told to do something. This is for both management and audit purpose.
4. Documentation should be clear, concise, and easy to follow. Diagrams should be made using Mermaid syntax.
5. Use comments in code to explain complex logic or important sections.
6. Always use extensive error handling and logging.
7. Always read the code carefully before making changes. Understand the existing logic and structure, and preserve existing conventions and practices.

TASK MANAGEMENT:

1. Top level tasks in `docs/tasks/00_ALL_TASKS.csv` file.
2. Subtasks in `docs/tasks/[PARENT_ID_NUMBER]_[PARENT_TASK_NAME_PASCAL_CASE]_TASKS.csv` file.

- Example: For task `T01`, subtasks should be in `docs/tasks/01_DockerComposeDB_TASKS.csv`.

3. Task format:
   - `TASK_ID`: Unique identifier for the task, formatted as `T[TASK_NUMBER]` for tasks, and `T[PARENT_ID_NUMBER]-[TASK_NUMBER]`.
     - Example: `T01`, `T02`, `T01-01`, `T01-02`.
   - `Task Name`: Short name (alias) for task. Should not exceed 3-4 words.
   - `Task Description`: Detailed description of the task, including any specific requirements or constraints.
   - `Task Status`: Current status of the task. One of [`TODO`, `IN PROGRESS`, `DONE`].
   - `Task Priority`: Priority level of the task if applicable. One of [`High`, `Medium`, `Low`].
   - `Task Dependencies`: List of task IDs that this task depends on, if any.
4. A tasks should be sub-divided into smaller subtasks if they are too large or complex only. Do NOT over-divide tasks.
5. Always update task status when starting a task, and when it is completed.

TECH STACK:

- Python 3.12+
- FastAPI (web framework)
- uv (package/project manager for Python)
- PostgreSQL (DB)
- SQLAlchemy (ORM)
- Alembic (for DB migrations)
- Pydantic (data validation)
- Docker & Docker Compose (containerization)
