import requests

def test_payment_update():
    # First, get all bills to find a valid ID
    print("Fetching bills...")
    try:
        response = requests.get("http://localhost:8000/bills/")
        bills = response.json()
        
        if not bills:
            print("No bills found to test.")
            return

        bill_id = bills[0]['id']
        print(f"Testing with Bill ID: {bill_id}")
        print(f"Initial Status: {bills[0].get('status', 'Unpaid')}")

        # Test Mark as Paid
        print(f"Marking bill {bill_id} as Paid (Cash)...")
        payload = {"status": "Paid", "payment_mode": "Cash"}
        patch_response = requests.patch(f"http://localhost:8000/bills/{bill_id}/status", json=payload)
        
        if patch_response.status_code == 200:
            updated_bill = patch_response.json()
            print("Success!")
            print(f"New Status: {updated_bill['status']}")
            print(f"Payment Mode: {updated_bill['payment_mode']}")
            
            # Verify phone logic (simulation)
            if updated_bill.get('customer_phone'):
                print(f"Frontend would redirect to WhatsApp for phone: {updated_bill['customer_phone']}")
            else:
                print("No phone number, frontend would not redirect.")
        else:
            print(f"Failed: {patch_response.text}")

    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    test_payment_update()
