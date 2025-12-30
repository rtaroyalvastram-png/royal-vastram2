import sqlite3
import os

DB_PATH = "billing.db"

def fix_sequence():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check current max id
        cursor.execute("SELECT MAX(id) FROM bills")
        max_id = cursor.fetchone()[0]
        print(f"Current max ID: {max_id}")
        
        if max_id is None: 
            # Table empty
            new_seq = 999
        elif max_id < 1000:
            new_seq = 999
        else:
            print("Max ID is already >= 1000. No change needed unless forced.")
            new_seq = max_id # Do nothing effectively, or could set to max_id if sequence is out of sync

        if max_id is None or max_id < 1000:
            # Check if entry exists in sqlite_sequence
            cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='bills'")
            row = cursor.fetchone()
            
            if row:
                print(f"Current sequence: {row[0]}")
                if row[0] < 999:
                    print("Updating sequence to 999...")
                    cursor.execute("UPDATE sqlite_sequence SET seq = 999 WHERE name = 'bills'")
            else:
                print("Inserting sequence start at 999...")
                cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('bills', 999)")
                
            conn.commit()
            print("Sequence updated. Next bill ID should be 1000.")
        else:
            print("Skipping sequence update as IDs already high.")

        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_sequence()
