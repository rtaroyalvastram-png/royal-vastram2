
import sys
import os
import datetime

# Add backend to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.invoice_gen import create_invoice_image

class DummyItem:
    def __init__(self, name, price, qty):
        self.item_name = name
        self.price = price
        self.quantity = qty
        self.item_total = price * qty

class DummyBill:
    def __init__(self):
        self.id = 999
        self.customer_name = "Test User"
        self.customer_phone = "1234567890"
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.items = [
            DummyItem("Saree Model A", 1200.00, 2),
            DummyItem("Silk Blouse", 850.50, 1)
        ]
        self.total_amount = sum(i.item_total for i in self.items)

if __name__ == "__main__":
    bill = DummyBill()
    print(f"Generating invoice for total: {bill.total_amount}")
    image_path, pdf_path = create_invoice_image(bill)
    
    if image_path and os.path.exists(image_path):
        print(f"SUCCESS: Invoice Image generated at {image_path}")
    else:
        print("FAILURE: Invoice Image generation failed")

    if pdf_path is None:
        print("SUCCESS: PDF generation successfully skipped.")
    else:
         print(f"WARNING: PDF was generated at {pdf_path}")
