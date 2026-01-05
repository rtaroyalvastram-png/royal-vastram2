import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "billing.db")

def set_id_base():
    if not os.path.exists(DB_FILE):
        print(f"DB not found at {DB_FILE}")
        return

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        print("Connected.")
        
        # Check if 999 exists
        cursor.execute("SELECT id FROM bills WHERE id = 999")
        if cursor.fetchone():
            print("ID 999 already exists. ID sequence should be fine.")
        else:
            # Insert 999 to force next to be 1000
            # We use a status 'SYSTEM_INIT' so we can potentially filter it out later if needed
            print("Inserting Dummy Bill ID 999 to force sequence...")
            cursor.execute("INSERT INTO bills (id, customer_name, date, total_amount, status) VALUES (999, 'SYSTEM_START_SEQ', '2020-01-01', 0, 'Void')")
            print("Inserted.")

        # Also double check high IDs
        cursor.execute("SELECT MAX(id) FROM bills")
        print(f"Max ID is now: {cursor.fetchone()[0]}")

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    set_id_base()
