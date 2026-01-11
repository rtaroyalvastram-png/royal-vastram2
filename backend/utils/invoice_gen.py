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
        # --- 1. HEADER SECTION ---
        # Logo (if exists)
        try:
            # Locate logo relative to this file: backend/utils/invoice_gen.py -> .../frontend/public/logo.jpg
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Possible paths to check
            possible_paths = [
                os.path.join(base_dir, "frontend", "public", "logo.jpg"),
                os.path.join(base_dir, "frontend", "public", "logo.png"),
                os.path.join(base_dir, "public", "logo.jpg"), # Fallback
                "C:\\Users\\91974\\OneDrive\\Desktop\\royalvastram\\frontend\\public\\logo.jpg" # Absolute fallback
            ]
            
            logo_path = None
            for p in possible_paths:
                if os.path.exists(p):
                    logo_path = p
                    break
            
            print(f"DEBUG: Logo Path Resolution: {logo_path}")
            
            if logo_path and os.path.exists(logo_path):
                logo = Image.open(logo_path)
                # Resize to fit nicely within 180x180 but keep aspect ratio
                logo.thumbnail((180, 180), Image.Resampling.LANCZOS)
                
                # Paste
                img.paste(logo, (padding, 40))
                print("DEBUG: Logo pasted successfully.")
            else:
                print("DEBUG: Logo file not found in any expected location.")
        except Exception as e:
            print(f"DEBUG: Error loading logo: {e}")

        # Text (Centered)
        center_x = width // 2
        draw.text((center_x, 60), "ROYAL VASTRAM", font=font_serif_large, fill=color_amber_dark, anchor="ms")
        draw.text((center_x, 120), "#58 Shop no. 2, Mookambika Nilaya, 3rd Main Road, 11th Cross", font=font_sans_med, fill=color_gray_text, anchor="ms")
        draw.text((center_x, 155), "Rameshnagar, Marathahalli, Bangalore - 560037", font=font_sans_med, fill=color_gray_text, anchor="ms")
        draw.text((center_x, 190), "Ph: +91 9110611979", font=font_sans_small, fill=color_gray_light, anchor="ms")

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
        draw.text((text_x_left, info_y + 60), f"Mr/Mrs {str(bill.customer_name)}", font=font_sans_bold, fill=color_black)
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
        # Check if we need a discount column
        has_item_discount = any((getattr(i, 'discount', 0) or 0) > 0 for i in bill.items)

        # Columns Configuration
        # Default: Item (L), Price (R), Qty (R), Total (R)
        # With Disc: Item (L), Price (R), Qty (R), Disc (R), Total (R)
        
        # Columns Configuration
        # With S.No: S.No (L), Item (L), Price (R), Qty (R), Total (R)
        
        col_x_sno = padding + 10
        col_x_item = padding + 80
        
        if has_item_discount:
            col_x_price = width - padding - 500
            col_x_qty = width - padding - 350
            col_x_disc = width - padding - 200
            col_x_total = width - padding - 20
        else:
            col_x_price = width - padding - 450
            col_x_qty = width - padding - 250
            col_x_total = width - padding - 30

        y_text = table_y + (table_header_height // 2)
        draw.text((col_x_sno, y_text), "Item No.", font=font_sans_small, fill=color_white, anchor="lm")
        draw.text((col_x_item, y_text), "ITEM NAME", font=font_sans_small, fill=color_white, anchor="lm")
        draw.text((col_x_price, y_text), "PRICE", font=font_sans_small, fill=color_white, anchor="rm")
        draw.text((col_x_qty, y_text), "QTY", font=font_sans_small, fill=color_white, anchor="rm")
        
        if has_item_discount:
            draw.text((col_x_disc, y_text), "DISC", font=font_sans_small, fill=color_white, anchor="rm")
            
        draw.text((col_x_total, y_text), "TOTAL", font=font_sans_small, fill=color_white, anchor="rm")

        # Rows
        current_y = table_y + table_header_height
        
        for index, item in enumerate(bill.items):
            # Alternating Bg
            if index % 2 != 0:
                draw.rectangle((padding, current_y, width - padding, current_y + row_height), fill=color_row_alt)
            
            row_mid = current_y + (row_height // 2)
            
            # Truncate item name slightly more if we have discount col
            max_char = 38 if has_item_discount else 48
            
            draw.text((col_x_sno, row_mid), str(index + 1), font=font_sans_med, fill=color_black, anchor="lm")
            draw.text((col_x_item, row_mid), str(item.item_name)[:max_char], font=font_sans_med, fill=color_black, anchor="lm")
            draw.text((col_x_price, row_mid), f"Rs {item.price:.2f}", font=font_sans_med, fill=color_black, anchor="rm")
            draw.text((col_x_qty, row_mid), str(item.quantity), font=font_sans_med, fill=color_black, anchor="rm")
            
            if has_item_discount:
                 disc_val = getattr(item, 'discount', 0) or 0
                 draw.text((col_x_disc, row_mid), f"-{disc_val:.2f}", font=font_sans_med, fill=color_amber_dark, anchor="rm")

            draw.text((col_x_total, row_mid), f"Rs {item.item_total:.2f}", font=font_sans_bold, fill=color_black, anchor="rm")
            
            current_y += row_height

        # --- 4. TOTALS SECTION ---
        total_section_y = current_y + 30
        
        # Amount in Words (Left Side) - REMOVED, moving down

        # Total Box (Right Aligned)
        total_box_width = 500
        total_box_x = width - padding - total_box_width
        
        # Calculate Logic
        gross_subtotal = sum([i.price * i.quantity for i in bill.items])
        total_discount = gross_subtotal - bill.total_amount
        
        # Determine lines to print
        lines = []
        lines.append(("Subtotal", f"Rs {gross_subtotal:.2f}", color_gray_text, font_sans_med))
        if total_discount > 0.01:
             lines.append(("Discount", f"- Rs {total_discount:.2f}", (220, 38, 38), font_sans_med)) # Red color
        
        # Grand Total line
        lines.append(("Grand Total", f"Rs {bill.total_amount:.2f}", color_black, font_sans_bold))

        # Box Dimensions
        line_height = 40
        box_padding = 20
        box_h = (len(lines) * line_height) + (box_padding * 2)
        
        # Draw Box
        draw.rectangle((total_box_x, total_section_y, width - padding, total_section_y + box_h), fill=color_white, outline=color_black, width=2)
        
        # Draw Lines
        cursor_y = total_section_y + box_padding + 10 # slightly down for first line center
        
        for label, value, color, font in lines:
             # Draw Label
             draw.text((total_box_x + 20, cursor_y), label, font=font, fill=color, anchor="lm")
             # Draw Value
             draw.text((width - padding - 20, cursor_y), value, font=font, fill=color, anchor="rm")
             cursor_y += line_height

        # Amount in Words (Below the Total Box)
        words = num_to_indian_words(int(round(bill.total_amount)))
        words_y = total_section_y + box_h + 20
        draw.text((width - padding, words_y), "Amount in Words:", font=font_sans_small, fill=color_gray_text, anchor="ra")
        draw.text((width - padding, words_y + 30), f"{words} Only", font=font_sans_med, fill=color_black, anchor="ra")

        # --- 5. FOOTER ---
        footer_y = total_section_y + 180
        
        # Terms Header
        draw.text((padding + 30, footer_y), "Terms & Conditions", font=font_sans_bold, fill=color_black, anchor="ls")
        
        terms = [
            "1. Goods once sold will not be taken back or exchanged.",
            "2. No return/exchange on discounted items.",
            "3. Please check the saree before leaving the shop.",
            "4. Minor color or weaving variations are not defects.",
            "5. We are not responsible for damage after purchase.",
            "6. Disputes subject to Bangalore jurisdiction only"
        ]
        
        term_y_cursor = footer_y + 15
        for term in terms:
            draw.text((padding + 40, term_y_cursor), term, font=font_sans_small, fill=color_gray_text, anchor="ls")
            term_y_cursor += 30
            
        # Footer Text (Centered)
        final_msg = '"Thanks for shopping with us. We hope this saree adds beauty to your special moments"'
        draw.text((center_x, term_y_cursor + 60), final_msg, font=load_font("timesi.ttf", 26), fill=color_amber_dark, anchor="ms")
        
        # --- SAVE ---
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        invoices_dir = os.path.join(base_dir, "invoices")
        if not os.path.exists(invoices_dir):
            os.makedirs(invoices_dir)
            
        filename = f"invoice_{bill.id}.png"
        abs_path = os.path.join(invoices_dir, filename)
        img.save(abs_path, quality=100)
        
        return abs_path, None

    except Exception as e:
        print(f"Error generating invoice image: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def num_to_indian_words(n):
    """
    Converts a number to Indian currency words format.
    """
    a = [
        '', 'One ', 'Two ', 'Three ', 'Four ', 'Five ', 'Six ', 'Seven ', 'Eight ', 'Nine ', 'Ten ',
        'Eleven ', 'Twelve ', 'Thirteen ', 'Fourteen ', 'Fifteen ', 'Sixteen ', 'Seventeen ', 'Eighteen ', 'Nineteen '
    ]
    b = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']

    def in_words(num):
        if num == 0: return ""
        if num > 9:
            s = str(num)
            n_array = ('000000000' + s)[-9:]
            # Splitting: Crore(2), Lakh(2), Thousand(2), Hundred(1), Ten(2)
            # RegEx style split manual
            # indices: 01 23 45 6 78
            c = int(n_array[0:2])
            l = int(n_array[2:4])
            t = int(n_array[4:6])
            h = int(n_array[6])
            te = int(n_array[7:9])
            
            str_out = ""
            if c > 0: str_out += (a[c] if c < 20 else b[c//10] + ' ' + a[c%10]) + 'Crore '
            if l > 0: str_out += (a[l] if l < 20 else b[l//10] + ' ' + a[l%10]) + 'Lakh '
            if t > 0: str_out += (a[t] if t < 20 else b[t//10] + ' ' + a[t%10]) + 'Thousand '
            if h > 0: str_out += (a[h] if h < 20 else b[h//10] + ' ' + a[h%10]) + 'Hundred '
            if te > 0:
                if str_out != "": str_out += "and "
                str_out += (a[te] if te < 20 else b[te//10] + ' ' + a[te%10])
            
            return str_out.strip()
        else:
             return a[num].strip()

    return in_words(n)
