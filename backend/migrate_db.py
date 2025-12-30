import sqlite3
import os

# Database file path (assuming it's in the current directory or backend directory)
DB_FILE = "sql_app.db" # Default name for FastAPI SQLAlchemy tutorial, let me check the actual name from database.py or just try to find it.

# Let's double check the db file name first using a list_dir or assuming standard 'billing.db' or similar if defined. 
# Looking at previous file views, 'database.py' was imported but I haven't seen its content. 
# I'll rely on common naming or check current dir.

def migrate():
    # Try to find the database file
    db_path = os.path.join(os.getcwd(), "backend", "billing.db")
    if not os.path.exists(db_path):
        # try simple name
        db_path = os.path.join(os.getcwd(), "billing.db")
    
    # If still not found, search in backend dir
    if not os.path.exists(db_path):
        files = os.listdir(os.path.join(os.getcwd(), "backend"))
        db_files = [f for f in files if f.endswith(".db")]
        if db_files:
            db_path = os.path.join(os.getcwd(), "backend", db_files[0])
        else:
            print("Database file not found!")
            return

    print(f"Migrating database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(bills)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "discount" not in columns:
            print("Adding discount column...")
            cursor.execute("ALTER TABLE bills ADD COLUMN discount FLOAT DEFAULT 0")
            conn.commit()
            print("Migration successful.")
        else:
            print("Column 'discount' already exists.")
            
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
