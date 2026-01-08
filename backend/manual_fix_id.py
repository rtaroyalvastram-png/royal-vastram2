import sqlite3
import datetime

DB_PATH = "billing.db"

def manual_fix():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check max ID
    cursor.execute("SELECT MAX(id) FROM bills")
    max_id = cursor.fetchone()[0]
    print(f"Current Max ID: {max_id}")
    
    if max_id is None: max_id = 0
    
    if max_id < 999:
        print("Inserting dummy bill at ID 999...")
        # Insert a dummy bill with ID 999. 
        # Mark it as 'Cancelled' or similar so it doesn't mess up reports?
        # User requests start from 1000. 
        # If we have a bill 999, next is 1000.
        
        cursor.execute("""
            INSERT INTO bills (id, customer_name, customer_phone, date, total_amount, discount, status, payment_mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (999, "SYSTEM_OFFSET_DO_NOT_DELETE", "0000000000", datetime.datetime.utcnow(), 0.0, 0.0, "Cancelled", "System"))
        
        conn.commit()
        print("Inserted bill 999.")
    else:
        print("Max ID is already >= 999.")

    conn.close()

if __name__ == "__main__":
    manual_fix()
