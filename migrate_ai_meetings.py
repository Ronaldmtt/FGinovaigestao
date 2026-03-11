import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

def migrate():
    load_dotenv()
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not found!")
        return

    # Use raw engine to bypass models.py and any pgvector dependencies mapped in there
    engine = create_engine(db_url)
    
    with engine.begin() as conn:
        print("Creating table meetings...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS meetings (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                date_time TIMESTAMP NOT NULL,
                project_id INTEGER REFERENCES project(id),
                transcription_id VARCHAR(100),
                transcription_content TEXT,
                analysis_summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by_id INTEGER NOT NULL REFERENCES "user"(id),
                status VARCHAR(20) DEFAULT 'agendada'
            );
        """))
        
        print("Creating table meeting_participants...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS meeting_participants (
                meeting_id INTEGER REFERENCES meetings(id),
                user_id INTEGER REFERENCES "user"(id),
                PRIMARY KEY (meeting_id, user_id)
            );
        """))
        
        print("Creating table ai_chat_history...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ai_chat_history (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES "user"(id),
                role VARCHAR(20) NOT NULL,
                content TEXT,
                tool_calls TEXT,
                tool_call_id VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        print("Schema updated successfully via Raw Engine SQL!")

if __name__ == '__main__':
    migrate()
