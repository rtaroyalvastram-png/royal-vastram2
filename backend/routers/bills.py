from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from PIL import Image
from sqlalchemy import func, extract
from typing import List, Optional
import database
import models
import schemas
import datetime
import csv
import io
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/bills",
    tags=["bills"]
)

from fastapi import BackgroundTasks
import sys
import os

# Ensure we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.invoice_gen import create_invoice_image

def send_whatsapp_task(bill_id: int, phone: str, message: str, bill_obj=None):
    try:
        import time
        import webbrowser
        import pyautogui
        import win32clipboard
        from PIL import Image
        from io import BytesIO
        from io import BytesIO
        from urllib.parse import quote
        import subprocess

        def focus_whatsapp_window():
            """
            Attempts to bring the WhatsApp Web browser window to the foreground using PowerShell.
            Checks for common browser processes with 'WhatsApp' in the title.
            """
            try:
                print("Attempting to focus WhatsApp window...")
                ps_script = """
                $w = New-Object -ComObject WScript.Shell
                $proc = Get-Process | Where-Object { $_.MainWindowTitle -like '*WhatsApp*' } | Select-Object -First 1
                if ($proc) { 
                    $w.AppActivate($proc.Id) 
                    Write-Output "FOCUSED_PID:$($proc.Id)"
                } else {
                    Write-Output "WhatsApp window not found"
                }
                """
                result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
                output = result.stdout.strip()
                print(f"Focus Result: {output}")
                
                if "FOCUSED_PID" in output:
                    time.sleep(1) # Allow transition
                    return True
                return False
            except Exception as e:
                print(f"Focus Script Error: {e}")
                return False

        # Phone must have country code. Standardizing to +91 if missing
        phone = phone.strip()
        if not phone.startswith("+"):
            phone = "+91" + phone
            
        # Clean phone (remove + for whatsapp url usually expects digits, but + works too mostly. 
        # Standard: https://web.whatsapp.com/send?phone=919611...
        phone_digits = phone.replace("+", "").replace(" ", "")

        # Generate Invoice Image
        image_path = None
        if bill_obj:
            print(f"Generating invoice for bill {bill_id}...")
            image_path, _ = create_invoice_image(bill_obj)
            
        if image_path and os.path.exists(image_path):
            abs_image_path = os.path.abspath(image_path)
            
            # 1. Copy Image to Clipboard (Reliable Method)
            try:
                image = Image.open(abs_image_path)
                output = BytesIO()
                image.convert("RGB").save(output, "BMP")
                data = output.getvalue()[14:]
                output.close()
                
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()
                print("Image copied to clipboard.")
            except Exception as e:
                 print(f"Clipboard Error: {e}")
                 return # Exit if we can't copy image (user requirement)

            # 2. Open WhatsApp Web
            # Encode message
            encoded_message = quote(message)
            url = f"https://web.whatsapp.com/send?phone={phone_digits}&text={encoded_message}"
            
            print(f"Opening WhatsApp for {phone}...")
            webbrowser.open(url)
            
            # 3. Wait for Load (Critical Step)
            # 20 seconds to be safe for network
            time.sleep(20)
            
            # 4. Paste Image
            print("Pasting image...")
            
            # FORCE FOCUS BEFORE PASTING
            focus_whatsapp_window()
            
            # Click to ensure focus on the message box
            # We assume the chat box is focused by default on load, but a click helps.
            # Clicking center of screen usually hits the chat window or background (safe)
            try:
                width, height = pyautogui.size()
                pyautogui.click(width / 2, height / 2)
            except:
                pass
                
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'v')
            
            # 5. Wait for Image Preview
            time.sleep(3)
            
            # 6. Send
            print("Sending...")
            pyautogui.press('enter')
            
            # 7. Close Tab (Safely)
            time.sleep(8)
            
            print("Attempting to close WhatsApp tab...")
            # Verify focus AGAIN before closing
            is_focused = focus_whatsapp_window()
            
            if is_focused:
                print("WhatsApp verified in focus. Closing tab...")
                pyautogui.hotkey('ctrl', 'w')
            else:
                print("WARNING: Could not verify WhatsApp focus. SKIPPING CLOSE to protect other tabs.")
            
        else:
            print("No image to send.")
            
    except Exception as e:
        print(f"WhatsApp Automation Error: {e}")
        import traceback
        traceback.print_exc()

@router.post("/", response_model=schemas.Bill)
def create_bill(
    bill: schemas.BillCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db)
):
    db_bill = models.Bill(
        customer_name=bill.customer_name,
        customer_phone=bill.customer_phone,
        date=bill.date,
        total_amount=bill.total_amount,
        discount=bill.discount,
        status=bill.status,
        payment_mode=bill.payment_mode
    )
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)

    for item in bill.items:
        db_item = models.BillItem(
            bill_id=db_bill.id,
            item_name=item.item_name,
            price=item.price,
            quantity=item.quantity,
            discount=item.discount,
            item_total=item.item_total
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_bill)

    if db_bill.status == "Paid" and db_bill.customer_phone:
        message = f"Dear {db_bill.customer_name}, here is your invoice for Rs {db_bill.total_amount}. Thanks for shopping with us. We hope this saree adds beauty to your special moments (Bill ID: {db_bill.id})"
        background_tasks.add_task(send_whatsapp_task, db_bill.id, db_bill.customer_phone, message, db_bill)

    return db_bill

    return db_bill

def apply_bill_filters(
    query, 
    year: Optional[int] = None, 
    month: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    customer_name: Optional[str] = None
):
    if year:
        query = query.filter(extract('year', models.Bill.date) == year)
        
    if month:
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        month_int = month_map.get(month)
        if month_int:
            query = query.filter(extract('month', models.Bill.date) == month_int)
        else:
            try:
                m = int(month)
                query = query.filter(extract('month', models.Bill.date) == m)
            except:
                pass

    if start_date:
        # Assuming format 'YYYY-MM-DD'
        # Compare as strings is fine for ISO format, but to be safe against time components:
        # If we want exact day matching
        query = query.filter(models.Bill.date >= start_date)
        
    if end_date:
        # Append time to end of day to make it inclusive for that day
        # If input is '2025-01-01', we check <= '2025-01-01 23:59:59'
        if len(end_date) == 10: # simple check for YYYY-MM-DD
             query = query.filter(models.Bill.date <= f"{end_date} 23:59:59")
        else:
             query = query.filter(models.Bill.date <= end_date)

    if customer_name:
        query = query.filter(models.Bill.customer_name.ilike(f"%{customer_name}%"))

    return query

@router.get("/", response_model=List[schemas.Bill])
def get_bills(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    bills = db.query(models.Bill).order_by(models.Bill.date.desc()).offset(skip).limit(limit).all()
    return bills

@router.get("/export")
def export_bills(
    year: Optional[int] = Query(None),
    month: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    customer_name: Optional[str] = Query(None),
    db: Session = Depends(database.get_db)
):
    import openpyxl
    from openpyxl.styles import Font, Alignment

    query = db.query(models.Bill)
    query = apply_bill_filters(query, year, month, start_date, end_date, customer_name)
    bills = query.order_by(models.Bill.date.desc()).all()
    
    # Create Workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Bills Export"

    # Headers
    headers = ['Bill ID', 'Date', 'Customer Name', 'Phone', 'Item Name', 'Quantity', 'Price', 'Item Total', 'Bill Total', 'Status', 'Payment Mode']
    ws.append(headers)

    # Style Header
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')

    # Data
    for bill in bills:
        # Format date
        date_val = bill.date
        if isinstance(date_val, str):
            # Try parsing if it's a string, or just keep as is
            pass
        
        # Phone - ensure it's treated as string
        phone_val = str(bill.customer_phone) if bill.customer_phone else ""

        if bill.items:
            for item in bill.items:
                ws.append([
                    bill.id,
                    date_val.strftime("%Y-%m-%d") if date_val else "",
                    bill.customer_name,
                    phone_val,
                    item.item_name,
                    item.quantity,
                    item.price,
                    item.item_total,
                    bill.total_amount,
                    bill.status,
                    bill.payment_mode
                ])
        else:
             ws.append([
                bill.id,
                date_val.strftime("%Y-%m-%d") if date_val else "",
                bill.customer_name,
                phone_val,
                "",
                "",
                "",
                "",
                bill.total_amount,
                bill.status,
                bill.payment_mode
            ])

    # Adjust Column Widths
    # A=1, B=2, ...
    column_widths = {
        'A': 10, # Bill ID
        'B': 20, # Date - THIS FIXES THE ### ISSUE
        'C': 25, # Customer Name
        'D': 15, # Phone
        'E': 30, # Item Name
        'F': 10, # Qty
        'G': 10, # Price
        'H': 12, # Item Total
        'I': 12, # Bill Total
        'J': 10, # Status
        'K': 15  # Payment Mode
    }
    
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    response = StreamingResponse(
        iter([output.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response.headers["Content-Disposition"] = "attachment; filename=bills_export.xlsx"
    return response

@router.get("/filter", response_model=List[schemas.Bill])
def filter_bills(
    year: Optional[int] = Query(None),
    month: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    customer_name: Optional[str] = Query(None),
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Bill)
    query = apply_bill_filters(query, year, month, start_date, end_date, customer_name)
    return query.order_by(models.Bill.date.desc()).all()

@router.get("/{bill_id}", response_model=schemas.Bill)
def get_bill(bill_id: int, db: Session = Depends(database.get_db)):
    db_bill = db.query(models.Bill).filter(models.Bill.id == bill_id).first()
    if db_bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    return db_bill
@router.post("/{bill_id}/send-whatsapp")
def send_whatsapp_message(
    bill_id: int, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db)
):
    db_bill = db.query(models.Bill).filter(models.Bill.id == bill_id).first()
    if db_bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
        
    if not db_bill.customer_phone:
        raise HTTPException(status_code=400, detail="Customer phone number missing")
        
    message = f"Dear {db_bill.customer_name}, here is your invoice for Rs {db_bill.total_amount}. Thanks for shopping with us. We hope this saree adds beauty to your special moments (Bill ID: {db_bill.id})"
    
    background_tasks.add_task(send_whatsapp_task, db_bill.id, db_bill.customer_phone, message, db_bill)
    
    background_tasks.add_task(send_whatsapp_task, db_bill.id, db_bill.customer_phone, message, db_bill)
    
    return {"status": "success", "detail": "Message scheduled in background"}


@router.delete("/cleanup")
def cleanup_old_data(
    retention_days: int = Query(..., description="Number of days of data to keep. Older data will be deleted."),
    db: Session = Depends(database.get_db)
):
    """
    Deletes bills and associated invoice images older than the specified retention period.
    """
    try:
        # Calculate cutoff date
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=retention_days)
        print(f"Cleanup Started. Deleting data older than: {cutoff_date}")

        # Find bills to delete
        bills_to_delete = db.query(models.Bill).filter(models.Bill.date < cutoff_date).all()
        
        deleted_bills_count = 0
        deleted_images_count = 0
        
        # Base directory for images
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        invoices_dir = os.path.join(base_dir, "invoices")

        for bill in bills_to_delete:
            # 1. Delete Image File
            try:
                filename = f"invoice_{bill.id}.png"
                file_path = os.path.join(invoices_dir, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_images_count += 1
            except Exception as e:
                print(f"Error deleting image for bill {bill.id}: {e}")

            # 2. Delete Bill Record (Cascade deletes items)
            db.delete(bill)
            deleted_bills_count += 1
            
        db.commit()
        
        return {
            "status": "success", 
            "message": f"Cleanup complete. Deleted {deleted_bills_count} bills and {deleted_images_count} images.",
            "deleted_bills": deleted_bills_count,
            "deleted_images": deleted_images_count
        }

    except Exception as e:
        print(f"Cleanup Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
