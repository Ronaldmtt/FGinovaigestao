from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        # Check if columns exist
        with db.engine.connect() as conn:
            try:
                conn.execute(text("SELECT has_github FROM project LIMIT 1"))
                print("Columns 'has_github' already exists.")
            except:
                print("Adding 'has_github' column...")
                conn.execute(text("ALTER TABLE project ADD COLUMN has_github BOOLEAN DEFAULT 0 NOT NULL"))
                print("Column 'has_github' added.")
            
            try:
                conn.execute(text("SELECT has_drive FROM project LIMIT 1"))
                print("Column 'has_drive' already exists.")
            except:
                print("Adding 'has_drive' column...")
                conn.execute(text("ALTER TABLE project ADD COLUMN has_drive BOOLEAN DEFAULT 0 NOT NULL"))
                print("Column 'has_drive' added.")
            
            conn.commit()

if __name__ == "__main__":
    migrate()
