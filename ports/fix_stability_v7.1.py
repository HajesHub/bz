import re
import os
import shutil

# Files to sync
html_files = [
    r'E:\msharea\b7oth\ports\index.html',
    r'E:\msharea\b7oth\mah\mahmoudiah.html',
    r'E:\msharea\b7oth\mah\mahber.html'
]

css_files = [
    r'E:\msharea\b7oth\ports\universal.css',
    r'E:\msharea\b7oth\mah\style.css'
]

def apply_stability_fix(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Viewport: Standardize for Zoom Freedom
    new_vp = '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.1, user-scalable=yes">'
    content = re.sub(r'<meta name="viewport"[^>]*>', new_vp, content)

    # 2. Add Stability Override Block (in case CSS fails or loads late)
    # This specifically targets the body to stop wobble
    stability_style = """
    <style>
        /* STABILITY OVERRIDE v7.1 */
        html, body { overflow-x: hidden !important; width: 100% !important; max-width: 100% !important; }
        .table-container, .table-responsive, .nav-tabs { overflow-x: auto !important; }
        table { min-width: 800px !important; }
    </style>
    """
    
    # Clean previous overrides first
    content = re.sub(r'<style>\s*/\* FINAL FREEDOM OVERRIDE.*?/style>', '', content, flags=re.S)
    content = re.sub(r'<style>\s*/\* STABILITY OVERRIDE.*?/style>', '', content, flags=re.S)

    if '</body>' in content:
        content = content.replace('</body>', f'{stability_style}\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Applied Stability v7.1 to {file_path}")

def update_legacy_css(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ensure legacy CSS doesn't fight the new stable rules
    content = re.sub(r'overflow:\s*visible\s*!important', 'overflow-x: hidden !important', content)
    content = re.sub(r'overflow-x:\s*visible\s*!important', 'overflow-x: hidden !important', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated Legacy CSS in {file_path}")

# Run
for hf in html_files:
    apply_stability_fix(hf)

update_legacy_css(css_files[1])

# Sync Universal CSS
shutil.copy2(css_files[0], r'E:\msharea\b7oth\mah\universal.css')
print("Synced Universal CSS v7.1 to mah folder")
