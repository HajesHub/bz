import re
import os

def emergency_fix(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Use the most standard, zoom-friendly viewport
    new_vp = '<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">'
    content = re.sub(r'<meta name="viewport"[^>]*>', new_vp, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed viewport in {file_path}")

def clean_mah_style(style_path):
    if not os.path.exists(style_path):
        return
    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove all previous failed attempts
    content = re.sub(r'/\* ===== MOBILE TABLE SCROLL.*$', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* ===== CLEAN TABLE SCROLL.*$', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* ===== ULTIMATE TABLE SCROLL.*$', '', content, flags=re.DOTALL)
    
    # Ensure no global overflow is hidden
    content = content.replace('overflow-x: hidden;', '')
    
    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned {style_path}")

emergency_fix('index.html')
emergency_fix('../mah/mahmoudiah.html')
clean_mah_style('../mah/style.css')
