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

def apply_localized_stability(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. REMOVE v8.0 Wrapper
    # Remove opening tag
    content = re.sub(r'<div class="outer-wrapper">\s*', '', content)
    # Remove closing tag (tricky, but we look for the one before body end)
    # Standardize end first
    if '</div>\n</body>' in content:
        content = content.replace('</div>\n</body>', '</body>')
    elif '</div></body>' in content:
        content = content.replace('</div></body>', '</body>')

    # 2. Add v9.0 Localized Stability Override
    stability_style = """
    <style>
        /* LOCALIZED STABILITY v9.0 */
        html, body { overflow-x: visible !important; width: 100% !important; }
        .container, header, footer, section { overflow-x: clip !important; max-width: 100vw !important; }
        .outer-wrapper { display: contents !important; } /* Neutered if lingering */
    </style>
    """
    
    # Clean old overrides
    content = re.sub(r'<style>\s*/\* WRAPPER TECHNIQUE.*?/style>', '', content, flags=re.S)
    
    # Inject new override before closing body
    if '</body>' in content:
        content = content.replace('</body>', f'{stability_style}\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Applied Logic v9.0 to {file_path}")

def update_legacy_css(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ensure legacy CSS allows visible body
    content = re.sub(r'body\s*{[^}]*overflow-x:\s*hidden[^}]*}', 'body { overflow-x: visible !important; }', content, flags=re.I)
    content = re.sub(r'html\s*{[^}]*overflow-x:\s*hidden[^}]*}', 'html { overflow-x: visible !important; }', content, flags=re.I)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated Legacy CSS in {file_path}")

# Run
for hf in html_files:
    apply_localized_stability(hf)

update_legacy_css(css_files[1])

# Sync Universal CSS
shutil.copy2(css_files[0], r'E:\msharea\b7oth\mah\universal.css')
print("Synced Universal CSS v9.0 to mah folder")
