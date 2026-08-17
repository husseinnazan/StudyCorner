from fastapi import FastAPI
from database import NoteDB , TaskDB , PomoDB
from schemas import NoteBase , NoteResponse , TaskBase , TaskResponse , SessionResponse
from fastapi import HTTPException

app = FastAPI()
ndb = NoteDB()
tdb = TaskDB()
pdb = PomoDB()

@app.post("/notes", response_model=NoteResponse)
def create_note(note: NoteBase):
    return ndb.add_note(note.title, note.content)
    
@app.get("/notes")
def read_notes():
    return ndb.get_all_notes()

@app.put("/notes/{note_id}")
def edit_note(note_id: int, note: NoteBase):
    ndb.update_note(note_id, note.title, note.content)

@app.delete("/notes/{note_id}")
def remove_note(note_id: int):
    result = ndb.delete_note(note_id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"detail": "Note deleted"}
   
@app.post("/tasks", response_model=TaskResponse)
def create(task : TaskBase):
    return tdb.add_task(task.content , task.due_at)

@app.get("/tasks")
def read_tasks():
    return tdb.get_all_tasks()

@app.patch("/tasks/{task_id}/complete")
def finish_task(task_id: int):
    result = tdb.complete_task(task_id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task completed"}

@app.delete("/tasks/{task_id}")
def remove_task(task_id : int):
    result = tdb.delete_task(task_id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}

@app.post("/pomodoro/start", response_model=SessionResponse)
def start_session():
    return pdb.start_session()

@app.patch("/pomodoro/{session_id}/end")
def end_session_route(session_id: int):
    result = pdb.end_session(session_id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"detail": "Session ended"}

@app.get("/pomodoro")
def read_sessions():
    return pdb.get_all_sessions()