import re
import os
import shutil

# List of all project HTML files
html_files = [
    'index.html',
    '../mah/mahmoudiah.html',
    '../mah/mahber.html'
]

# List of all project CSS files to clean
css_files = [
    'universal.css',
    '../mah/style.css'
]

def apply_freedom_fix(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Viewport: Explicit range for Zoom-out (Pinch to shrink)
    # We set initial-scale=1.0 but minimum-scale=0.1 to allow shrinking immediately.
    new_vp = '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.1, maximum-scale=10.0, user-scalable=yes">'
    content = re.sub(r'<meta name="viewport"[^>]*>', new_vp, content)
    
    # 2. Cleanup internal styles that might hide overflow
    # Use re.IGNORECASE for robustness
    content = re.sub(r'overflow-x:\s*hidden\s*;?', '', content, flags=re.I)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Applied Freedom Fix to {file_path}")

def clean_css_files(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove all overflow-x hidden project-wide
    content = re.sub(r'overflow-x:\s*hidden\s*;?', '', content, flags=re.I)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned CSS restrictions in {file_path}")

# Run updates
for html_file in html_files:
    apply_freedom_fix(html_file)

for css_file in css_files:
    clean_css_files(css_file)

# Sync latest universal.css
try:
    shutil.copy2('universal.css', '../mah/universal.css')
    print("Synced latest universal.css to mah folder")
except Exception as e:
    print(f"Sync failed: {e}")
