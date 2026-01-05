import os

# Mimic the logic in invoice_gen.py
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # This puts us in 'backend' relative to this script running in 'backend'
# invoice_gen.py is in 'backend/utils', so __file__ there is .../backend/utils/invoice_gen.py
# dirname -> utils
# dirname -> backend
# dirname -> foot (royalvastram)

# But here I am running in 'c:\Users\91974\OneDrive\Desktop\royalvastram\backend'
# so __file__ is 'backend/check_logo.py'
# dirname -> backend
# dirname -> royalvastram (root)

root_dir = os.path.dirname(os.path.abspath(__file__)) # c:\...\backend
project_root = os.path.dirname(root_dir) # c:\...\royalvastram

logo_path = os.path.join(project_root, "frontend", "public", "logo.jpg")

print(f"Project Root: {project_root}")
print(f"Checking for logo at: {logo_path}")

if os.path.exists(logo_path):
    print("FOUND: Logo exists.")
else:
    print("NOT FOUND: Logo missing.")
    # List directory
    public_dir = os.path.join(project_root, "frontend", "public")
    if os.path.exists(public_dir):
        print(f"Listing {public_dir}:")
        print(os.listdir(public_dir))
    else:
        print(f"Public dir not found at {public_dir}")
