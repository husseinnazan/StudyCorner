import sqlite3

class NoteDB:
    def __init__(self, db_path: str = "studycorner.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''create table if not exists notes (
            id integer primary key,
            title text not null,
            content text,
            created_at datetime default current_timestamp
        )''')
        self.conn.commit()

    def add_note(self, title, content):
        self.cursor.execute('''insert into notes (title, content) values (?, ?)''', (title, content))
        self.conn.commit()
        new_id = self.cursor.lastrowid
        self.cursor.execute('''select id, title, content, created_at from notes where id = ?''', (new_id,))
        row = self.cursor.fetchone()
        return {"id": row[0], "title": row[1], "content": row[2], "created_at": row[3]}

    def get_all_notes(self):
        self.cursor.execute('''select * from notes''')
        return self.cursor.fetchall()

    def delete_note(self, note_id):
        self.cursor.execute('''delete from notes where id = ?''', (note_id,))
        self.conn.commit()
        return self.cursor.rowcount

    def update_note(self, note_id, title, content):
        self.cursor.execute(
            '''update notes set title = ?, content = ? where id = ?''',
            (title, content, note_id)
        )
        self.conn.commit()
        return self.cursor.rowcount


class TaskDB:
    def __init__(self, db_path: str = "studycorner.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''create table if not exists tasks (
            id integer primary key,
            content text not null,
            due_at datetime not null,
            created_at datetime default current_timestamp,
            completed_at datetime
        )''')
        self.conn.commit()
        
    def add_task(self, content, due_at):
        self.cursor.execute('''insert into tasks (content, due_at) values (?, ?)''', (content, due_at))
        self.conn.commit()
        new_id = self.cursor.lastrowid
        self.cursor.execute('''select id, content, due_at, created_at from tasks where id = ?''', (new_id,))
        row = self.cursor.fetchone()
        return {"id": row[0], "content": row[1], "due_at": row[2], "created_at": row[3], "completed_at": None}
    
    def get_all_tasks(self):
        self.cursor.execute('''select * from tasks''')
        return self.cursor.fetchall()
        
    def delete_task(self,task_id) :
        self.cursor.execute('''delete from tasks where id = ?''', (task_id,))
        self.conn.commit()
        return self.cursor.rowcount
    def complete_task(self, task_id):
        self.cursor.execute('''update tasks set completed_at = CURRENT_TIMESTAMP where id = ?''', (task_id,))
        self.conn.commit()
        return self.cursor.rowcount
    
class PomoDB:
    def __init__(self, db_path: str = "studycorner.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''create table if not exists pomodoro (
            id integer primary key,
            session_type text not null,
            started_at datetime default current_timestamp,
            duration_minutes integer not null,
            ended_at  datetime
                   )''')
        self.conn.commit()
    
    def start_session(self):
        self.cursor.execute('''select session_type from pomodoro order by id desc limit 1''')
        last = self.cursor.fetchone()

        if last is None:
            session_type = "work"
        else:
            session_type = "break" if last[0] == "work" else "work"

        duration_minutes = 25 if session_type == "work" else 5

        self.cursor.execute(
            '''insert into pomodoro (session_type, duration_minutes) values (?, ?)''',
            (session_type, duration_minutes)
        )
        self.conn.commit()
        new_id = self.cursor.lastrowid

        self.cursor.execute(
            '''select id, session_type, duration_minutes, started_at, ended_at from pomodoro where id = ?''',
            (new_id,)
        )
        row = self.cursor.fetchone()
        return {"id": row[0], "session_type": row[1], "duration_minutes": row[2], "started_at": row[3], "ended_at": row[4]}
    
    def end_session(self, session_id):
        self.cursor.execute('''update pomodoro set ended_at = CURRENT_TIMESTAMP where id = ?''', (session_id,))
        self.conn.commit()
        return self.cursor.rowcount
    
    def get_all_sessions(self):
        self.cursor.execute('''select * from pomodoro''')
        return self.cursor.fetchall()