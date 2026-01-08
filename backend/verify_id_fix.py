import sqlite3
import datetime

DB_PATH = "billing.db"

def verify():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert a dummy bill
    cursor.execute("""
        INSERT INTO bills (customer_name, customer_phone, date, total_amount, discount, status, payment_mode)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("TEST_VERIFY", "1234567890", datetime.datetime.utcnow(), 100.0, 0.0, "Unpaid", "Cash"))
    
    bill_id = cursor.lastrowid
    print(f"Inserted Bill ID: {bill_id}")
    
    if bill_id >= 1000:
        print("SUCCESS: Bill ID is >= 1000")
    else:
        print("FAILURE: Bill ID is < 1000")
        
    # Cleanup
    cursor.execute("DELETE FROM bills WHERE id = ?", (bill_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    verify()
