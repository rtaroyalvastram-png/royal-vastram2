from PIL import Image, ImageDraw, ImageFont
import os
import datetime

def create_invoice_image(bill):
    """
    Generates a high-quality invoice image for the given bill object.
    Matches the "Amber/Serif" visual style of the React frontend.
    """
    try:
        # --- CONFIGURATION ---
        width = 1200
        padding = 80
        
        # Colors (RGB)
        color_white = (255, 255, 255)
        color_black = (17, 24, 39)       # gray-900
        color_amber_dark = (146, 64, 14) # text-amber-800
        color_amber_bg = (255, 251, 235) # bg-amber-50
        color_amber_border = (254, 243, 199) # border-amber-100/200
        color_gray_text = (55, 65, 81)   # gray-700
        color_gray_light = (107, 114, 128)# gray-500
        color_header_bg = (31, 41, 55)   # gray-800
        color_header_text = (255, 255, 255)
        color_row_alt = (249, 250, 251)  # gray-50
        color_highlight = (251, 191, 36) # text-amber-400

        # Layout Calculations
        header_height = 350
        table_header_height = 60
        row_height = 50
        footer_height = 400
        
        items_height = len(bill.items) * row_height
        total_height = header_height + table_header_height + items_height + 150 + footer_height
        
        # Create Canvas
        img = Image.new('RGB', (width, total_height), color=color_white)
        draw = ImageDraw.Draw(img)
        
        # --- FONTS ---
        # Helper to load fonts with fallback
        def load_font(name, size):
            try:
                return ImageFont.truetype(name, size)
            except:
                return ImageFont.load_default()

        # Try to use standard Windows fonts for that "Premium" look
        font_serif_large = load_font("timesbd.ttf", 60) # Royal Vastram Title
        font_sans_bold = load_font("arialbd.ttf", 28)
        font_sans_med = load_font("arial.ttf", 24)
        font_sans_small = load_font("arial.ttf", 20)
        font_sans_xs = load_font("arial.ttf", 18)
        
        # --- 1. HEADER SECTION ---
        # Logo (if exists)
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            logo_path = os.path.join(base_dir, "frontend", "public", "logo.jpg")
            if os.path.exists(logo_path):
                logo = Image.open(logo_path)
                logo.thumbnail((180, 180))
                # Center logo relative to text or place left? 
                # CSS says: absolute left-8. We'll place it at padding-left.
                img.paste(logo, (padding, 40))
        except:
            pass

        # Text (Centered)
        center_x = width // 2
        draw.text((center_x, 60), "ROYAL VASTRAM", font=font_serif_large, fill=color_amber_dark, anchor="ms")
        draw.text((center_x, 120), "#58 Mookambika Nilaya, 3rd Main Road, 11th Cross", font=font_sans_med, fill=color_gray_text, anchor="ms")
        draw.text((center_x, 155), "Ramesh Nagara, Marathahalli, Bangalore - 560037", font=font_sans_med, fill=color_gray_text, anchor="ms")
        draw.text((center_x, 190), "Ph: +91 96119 61979", font=font_sans_small, fill=color_gray_light, anchor="ms")

        # Divider Line
        draw.line((padding + 50, 230, width - padding - 50, 230), fill=color_amber_dark, width=3)

        # --- 2. INFO BOXES ---
        info_y = 260
        box_height = 160
        
        # Background for Info Section
        draw.rectangle((padding, info_y, width - padding, info_y + box_height), fill=color_amber_bg, outline=color_amber_border, width=2)
        
        # Left: Billed To
        text_x_left = padding + 40
        draw.text((text_x_left, info_y + 30), "BILLED TO", font=font_sans_xs, fill=color_amber_dark)
        draw.text((text_x_left, info_y + 60), str(bill.customer_name), font=font_sans_bold, fill=color_black)
        draw.text((text_x_left, info_y + 100), str(bill.customer_phone), font=font_sans_med, fill=color_gray_text)
        
        # Right: Invoice Details
        text_x_right = width - padding - 40
        draw.text((text_x_right, info_y + 30), "INVOICE DETAILS", font=font_sans_xs, fill=color_amber_dark, anchor="ra")
        draw.text((text_x_right, info_y + 60), f"#{str(bill.id).zfill(6)}", font=font_sans_bold, fill=color_black, anchor="ra")
        
        # Format date nicely
        dt = bill.date
        if isinstance(dt, str):
            try:
                # If ISO string, parse it
                dt = datetime.datetime.fromisoformat(dt)
            except:
                pass
        
        date_str = dt.strftime("%B %d, %Y") if hasattr(dt, 'strftime') else str(dt)
        draw.text((text_x_right, info_y + 100), date_str, font=font_sans_med, fill=color_gray_text, anchor="ra")

        # --- 3. TABLE ---
        table_y = info_y + box_height + 40
        
        # Header Background
        draw.rectangle((padding, table_y, width - padding, table_y + table_header_height), fill=color_header_bg)
        
        # Columns: Item (L), Price (R), Qty (R), Total (R)
        col_x_item = padding + 30
        col_x_price = width - padding - 450
        col_x_qty = width - padding - 250
        col_x_total = width - padding - 30
        
        y_text = table_y + (table_header_height // 2)
        draw.text((col_x_item, y_text), "ITEM NAME", font=font_sans_small, fill=color_white, anchor="lm")
        draw.text((col_x_price, y_text), "PRICE", font=font_sans_small, fill=color_white, anchor="rm")
        draw.text((col_x_qty, y_text), "QTY", font=font_sans_small, fill=color_white, anchor="rm")
        draw.text((col_x_total, y_text), "TOTAL", font=font_sans_small, fill=color_white, anchor="rm")

        # Rows
        current_y = table_y + table_header_height
        
        for index, item in enumerate(bill.items):
            # Alternating Bg
            if index % 2 != 0:
                draw.rectangle((padding, current_y, width - padding, current_y + row_height), fill=color_row_alt)
            
            row_mid = current_y + (row_height // 2)
            
            draw.text((col_x_item, row_mid), str(item.item_name)[:50], font=font_sans_med, fill=color_black, anchor="lm")
            draw.text((col_x_price, row_mid), f"Rs {item.price:.2f}", font=font_sans_med, fill=color_black, anchor="rm")
            draw.text((col_x_qty, row_mid), str(item.quantity), font=font_sans_med, fill=color_black, anchor="rm")
            draw.text((col_x_total, row_mid), f"Rs {item.item_total:.2f}", font=font_sans_bold, fill=color_black, anchor="rm")
            
            current_y += row_height

        # --- 4. TOTALS SECTION ---
        total_section_y = current_y + 30
        
        # Total Box (Right Aligned) - INCREASED WIDTH TO PREVENT OVERLAP
        total_box_width = 500
        total_box_x = width - padding - total_box_width
        
        # Background
        draw.rectangle((total_box_x, total_section_y, width - padding, total_section_y + 120), fill=color_header_bg, outline=color_black)
        
        # Calculate Logic
        subtotal = sum([i.item_total for i in bill.items])
        discount = getattr(bill, 'discount', 0.0) or 0.0
        # Grand Total Text
        
        # Adjusted positions for overlap safety
        draw.text((total_box_x + 30, total_section_y + 60), "GRAND TOTAL", font=font_sans_bold, fill=color_white, anchor="lm")
        draw.text((width - padding - 30, total_section_y + 60), f"Rs {bill.total_amount:.2f}", font=load_font("arialbd.ttf", 36), fill=color_highlight, anchor="rm")

        if discount > 0:
             pass

        # --- 5. FOOTER ---
        # INCREASED SPACING to prevent cutoff
        footer_y = total_section_y + 180
        
        # Terms
        draw.text((center_x, footer_y), "Terms & Conditions", font=font_sans_bold, fill=color_black, anchor="ms")
        
        terms = [
            "1. Goods once sold will not be taken back or exchanged.",
            "2. No return/exchange on discounted items.",
            "3. Please check the saree before leaving the shop.",
            "4. Minor color or weaving variations are not defects.",
            "5. We are not responsible for damage after purchase.",
            "6. Disputes subject to Bangalore jurisdiction only"
        ]
        
        term_y_cursor = footer_y + 40
        for term in terms:
            draw.text((center_x, term_y_cursor), term, font=font_sans_small, fill=color_gray_text, anchor="ms")
            term_y_cursor += 30
            
        # Extra padding at bottom
        draw.text((center_x, term_y_cursor + 40), "Thank you for shopping with Royal Vastram!", font=font_sans_med, fill=color_amber_dark, anchor="ms")
        
        # Extend image if content pushes past
        final_y = term_y_cursor + 100
        if final_y > total_height:
             # Crop/Resize is hard on existing canvas, but we allocated footer_height=400 which should be enough.
             # If cropping happens, it's likely calculate height was short.
             pass

        # --- SAVE ---
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        invoices_dir = os.path.join(base_dir, "invoices")
        if not os.path.exists(invoices_dir):
            os.makedirs(invoices_dir)
            
        filename = f"invoice_{bill.id}.png"
        abs_path = os.path.join(invoices_dir, filename)
        img.save(abs_path, quality=100)
        
        # PDF Removed as per user request
        
        return abs_path, None

    except Exception as e:
        print(f"Error generating invoice image: {e}")
        import traceback
        traceback.print_exc()
        return None, None
