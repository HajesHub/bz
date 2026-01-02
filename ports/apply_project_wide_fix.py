import re
import os
import shutil

# Paths to all discovered HTML files
html_files = [
    'index.html',
    '../mah/mahmoudiah.html',
    '../mah/mahber.html'
]

def update_html_responsiveness(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update Viewport
    new_vp = '<meta name="viewport" content="width=device-width, initial-scale=1">'
    content = re.sub(r'<meta name="viewport"[^>]*>', new_vp, content)
    
    # 2. Ensure universal.css is linked (after the local stylesheet if present)
    if 'universal.css' not in content:
        # Try to find the last CSS link or head end
        if 'style.css' in content:
            content = content.replace('style.css">', 'style.css">\n    <link rel="stylesheet" href="universal.css">')
        elif '</head>' in content:
            content = content.replace('</head>', '    <link rel="stylesheet" href="universal.css">\n</head>')
    
    # 3. Ensure Table containers have the right class if they don't
    # (Optional, but helps consistency)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path}")

# Run updates
for html_file in html_files:
    update_html_responsiveness(html_file)

# Sync latest universal.css
try:
    shutil.copy2('universal.css', '../mah/universal.css')
    print("Synced universal.css to mah folder")
except Exception as e:
    print(f"Sync failed: {e}")
