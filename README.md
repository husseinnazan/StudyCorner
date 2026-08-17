# StudyCorner

A REST API for managing notes, tasks, and focus sessions. Built with FastAPI and SQLite.

## Features

**Notes**
- Create, read, update, and delete notes
- Each note has a title, content, and an automatically recorded creation timestamp

**Tasks**
- Create, read, and delete tasks
- Each task has content, a due date, an automatically recorded creation timestamp, and a completion timestamp
- Mark a task complete through a dedicated endpoint instead of a generic update

**Pomodoro sessions**
- Start and end focus sessions
- Session type (work or break) is determined automatically, alternating with each new session
- Session duration defaults to 25 minutes for work and 5 minutes for break
- Full session history is retrievable for review

## Tech stack

- Python 3
- FastAPI
- SQLite (via the standard library `sqlite3` module)
- Pydantic for request and response validation
- Uvicorn as the ASGI server

## API reference

| Method | Path | Description |
|---|---|---|
| POST | `/notes` | Create a note |
| GET | `/notes` | List all notes |
| PUT | `/notes/{note_id}` | Update a note |
| DELETE | `/notes/{note_id}` | Delete a note |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List all tasks |
| PATCH | `/tasks/{task_id}/complete` | Mark a task complete |
| DELETE | `/tasks/{task_id}` | Delete a task |
| POST | `/pomodoro/start` | Start a new session (work or break, chosen automatically) |
| PATCH | `/pomodoro/{session_id}/end` | End a session |
| GET | `/pomodoro` | List all sessions |

Interactive documentation is available at `/docs` once the server is running.

## Database schema

```sql
create table notes (
    id integer primary key,
    title text not null,
    content text,
    created_at datetime default current_timestamp
);

create table tasks (
    id integer primary key,
    content text not null,
    due_at datetime not null,
    created_at datetime default current_timestamp,
    completed_at datetime
);

create table pomodoro (
    id integer primary key,
    session_type text not null,
    started_at datetime default current_timestamp,
    duration_minutes integer not null,
    ended_at datetime
);
```

## Design decisions

- No authentication. This is a single-user local tool; real auth was deliberately postponed until there is an actual second user or public exposure to justify it.
- SQLite connections are opened with `check_same_thread=False` because FastAPI runs request handlers in a thread pool, not the thread that created the connection. For a single-user local app this carries no real concurrency risk.
- Pomodoro session type is not sent by the client. It is computed server side by looking up the most recently created session and alternating from it, defaulting to a work session when the table is empty.
- The link between a completed task and the Pomodoro session it happened during is not stored explicitly. It is inferred by comparing a task's `completed_at` timestamp against a session's start and end times. This is a deliberate tradeoff for the current version, not an oversight.
- The Pomodoro backend does not run a countdown. It only records start and end timestamps. The live timer display is a frontend responsibility.

## Installation

```bash
git clone https://github.com/husseinnazan/studycorner.git
cd studycorner
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
uvicorn app:app --reload
```

Then open `http://127.0.0.1:8000/docs` in a browser to interact with the API directly.

## Project structure

```
studycorner/
├── app.py           # FastAPI application instance and route definitions
├── database.py      # Data layer: NoteDB, TaskDB, PomoDB
├── schemas.py       # Pydantic request and response models
├── requirements.txt
└── .gitignore
```

## Planned for v1.1

- Frontend built with React and TypeScript, including a live countdown display for Pomodoro sessions
- Configurable Pomodoro durations, replacing the current fixed 25/5 defaults
- Optional titles or labels on Pomodoro sessions
- Explicit stored link between a task and the Pomodoro session it was completed during
- PDF reader

## Planned for v2

- Containerized with Docker
- CI/CD pipeline with GitHub Actions, running tests and deploying automatically on push
- Deployed live on AWS behind a persistent URL
- SQLite replaced with PostgreSQL to support access from more than one instance

## Changelog

**2026-08-17**
- Tasks endpoints added, including due dates and a dedicated completion endpoint
- Pomodoro endpoints added, including automatic work/break alternation

**2026-08-16**
- Initial FastAPI and SQLite setup
- Notes endpoints added
- Added 404 handling on update and delete operations
- Create endpoints now return the full created object instead of an empty response