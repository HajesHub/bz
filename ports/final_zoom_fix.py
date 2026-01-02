import re
import os
import shutil

def simplify_viewport(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Use the simplest viewport as requested by the user
    new_vp = '<meta name="viewport" content="width=device-width, initial-scale=1">'
    # Replace any existing viewport tag
    updated_content = re.sub(r'<meta name="viewport"[^>]*>', new_vp, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"Simplified viewport in {file_path}")

# 1. Update viewports
simplify_viewport('index.html')
simplify_viewport('../mah/mahmoudiah.html')

# 2. Sync universal.css
shutil.copy2('universal.css', '../mah/universal.css')
print("Synced universal.css to mah folder")
