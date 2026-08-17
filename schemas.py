from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NoteBase(BaseModel) :
    title : str
    content : str
    
class NoteResponse(NoteBase) :
    id : int
    created_at : datetime
    
class TaskBase(BaseModel) :
    content : str
    due_at : datetime
    
class TaskResponse(TaskBase) :
    id : int
    created_at : datetime
    completed_at: Optional[datetime]
    

class SessionResponse(BaseModel):
    id: int
    session_type: str
    duration_minutes: int
    started_at: datetime
    ended_at: Optional[datetime]
