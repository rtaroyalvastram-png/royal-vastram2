import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "billing.db")

def add_discount_column():
    if not os.path.exists(DB_FILE):
        print(f"DB not found at {DB_FILE}")
        return

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        print("Connected to DB.")
        
        # Check if column exists in bill_items
        cursor.execute("PRAGMA table_info(bill_items)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'discount' not in columns:
            print("Adding 'discount' column to bill_items...")
            cursor.execute("ALTER TABLE bill_items ADD COLUMN discount FLOAT DEFAULT 0.0")
            print("Column added.")
        else:
            print("'discount' column already exists in bill_items.")

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_discount_column()
