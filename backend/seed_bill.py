import sqlite3
import os
import datetime

DB_PATH = "billing.db"

def seed_bill():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check max ID again
        cursor.execute("SELECT MAX(id) FROM bills")
        max_id = cursor.fetchone()[0]
        
        if max_id and max_id >= 999:
            print(f"Max ID is {max_id}, no need to seed 999.")
            return

        print("Inserting seed bill with ID 999...")
        # Insert a dummy bill. Note: 'id' is explicitly set.
        # Ensure your bill table columns match schema:
        # id, customer_name, customer_phone, date, total_amount, status, payment_mode
        # items are separate but bill insertion is enough to trigger sequence update (or just occupy the ID).
        
        # We need to know current date format. Usually ISO string or datetime object logic in Python -> SQLite adapter.
        now = datetime.datetime.now()
        
        cursor.execute("""
            INSERT INTO bills (id, customer_name, customer_phone, date, total_amount, status, payment_mode)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (999, "SYSTEM_SEED", "0000000000", now, 0.0, "System", "None"))
        
        conn.commit()
        print("Seed bill 999 inserted. Next auto-increment should be 1000.")
        
    except Exception as e:
        print(f"Error seeding: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    seed_bill()
