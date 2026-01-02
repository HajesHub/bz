import re
import os
import shutil

# Files to update
html_files = [
    r'E:\msharea\b7oth\ports\index.html',
    r'E:\msharea\b7oth\mah\mahmoudiah.html',
    r'E:\msharea\b7oth\mah\mahber.html'
]

css_files = [
    r'E:\msharea\b7oth\ports\universal.css',
    r'E:\msharea\b7oth\mah\style.css'
]

def apply_professional_sync(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Viewport: Fit to screen + preserve Zoom Freedom
    new_vp = '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.1, user-scalable=yes">'
    content = re.sub(r'<meta name="viewport"[^>]*>', new_vp, content)

    # 2. Cleanup disruptive internal styles
    # Replace overflow:hidden with something more professional (clip or visible)
    # targeting only body/html in internal styles
    content = re.sub(r'body\s*{[^}]*overflow-x:\s*hidden;?[^}]*}', lambda m: m.group(0).replace('hidden', 'clip'), content, flags=re.I)
    
    # ensure universal.css is linked
    if 'universal.css' not in content:
        if '</head>' in content:
            content = content.replace('</head>', '    <link rel="stylesheet" href="universal.css">\n</head>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Professional sync applied to {file_path}")

def cleanup_legacy_styles(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove old aggressive overrides
    content = content.replace('overflow: visible !important', '/* freedom */')
    content = content.replace('overflow-x: visible !important', '/* freedom */')
    # Change hidden to clip for stability
    content = re.sub(r'overflow-x:\s*hidden;?', 'overflow-x: clip;', content, flags=re.I)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned legacy styles in {file_path}")

# Run
for hf in html_files:
    apply_professional_sync(hf)

cleanup_legacy_styles(css_files[1])

# Sync Universal CSS
shutil.copy2(css_files[0], r'E:\msharea\b7oth\mah\universal.css')
print("Synced Universal CSS v6.0 to mah folder")
