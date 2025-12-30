import requests
import datetime
import time

BASE_URL = "http://127.0.0.1:8000"

def verify_refactor():
    print("Verifying Refactored Bill Creation...")
    
    # 1. Create a "Paid" bill
    payload = {
        "customer_name": "Refactor Test User",
        "customer_phone": "9999999999", # Dummy, but backend will try to send
        "date": datetime.datetime.now().isoformat(),
        "total_amount": 500.0,
        "items": [
            {"item_name": "Test Saree", "price": 500.0, "quantity": 1, "item_total": 500.0}
        ],
        "status": "Paid",
        "payment_mode": "UPI"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/bills/", json=payload)
        response.raise_for_status()
        bill = response.json()
        print(f"[SUCCESS] Bill Created: ID={bill['id']}, Status={bill['status']}, Mode={bill['payment_mode']}")
        
        if bill['status'] == 'Paid' and bill['payment_mode'] == 'UPI':
            print("[PASS] Payment Status and Mode saved correctly.")
        else:
            print("[FAIL] Payment Status/Mode mismatch.")
            
        print("Note: Check server logs. You should see 'WhatsApp sent to ...' (or error) in the backend terminal shortly.")
        
    except Exception as e:
        print(f"[FAIL] Error creating bill: {e}")

if __name__ == "__main__":
    verify_refactor()
