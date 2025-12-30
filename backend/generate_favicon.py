from PIL import Image, ImageDraw

def make_circle(image_path, output_path):
    try:
        img = Image.open(image_path).convert("RGBA")
        
        # Create a circular mask
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + img.size, fill=255)
        
        # Apply mask
        output = Image.new('RGBA', img.size, (0, 0, 0, 0))
        output.paste(img, (0, 0), mask)
        
        # Resize to favicon size (e.g. 192x192)
        output = output.resize((192, 192), Image.LANCZOS)
        
        output.save(output_path)
        print(f"Favicon saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    make_circle(
        r"c:\Users\91974\OneDrive\Desktop\royalvastram\frontend\src\assets\logo.jpg",
        r"c:\Users\91974\OneDrive\Desktop\royalvastram\frontend\public\favicon.png"
    )
