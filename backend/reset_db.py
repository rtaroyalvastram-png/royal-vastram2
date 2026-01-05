from database import engine, Base
from models import Bill, BillItem
from sqlalchemy import text

def reset_database():
    print("Resetting database...")
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("Dropped all tables.")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Created all tables.")
        
        # Set autoincrement start by inserting a dummy record at 999
        with engine.connect() as conn:
            # We insert a dummy record with ID 999
            # This forces the next auto-incremented ID to be 1000
            print("Seeding ID sequence...")
            conn.execute(text("INSERT INTO bills (id, customer_name, customer_phone, total_amount, status) VALUES (999, 'SYSTEM_INIT', '0000000000', 0, 'Hidden')"))
            conn.execute(text("DELETE FROM bills WHERE id = 999"))
            conn.commit()
            print("Database reset successfully. Next Bill ID will be 1000.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    reset_database()
