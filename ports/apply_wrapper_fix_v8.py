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

def apply_wrapper_structure(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Standardize Viewport for Zoom Freedom
    new_vp = '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.1, user-scalable=yes">'
    content = re.sub(r'<meta name="viewport"[^>]*>', new_vp, content)

    # 2. Inject Outer Wrapper
    # Check if already wrapped
    if '<div class="outer-wrapper">' not in content:
        # We need to find the body start and end
        # Regex to match body tag, including attributes
        body_match = re.search(r'(<body[^>]*>)', content, re.I)
        if body_match:
            body_start_tag = body_match.group(1)
            # Inject opening wrapper after body start
            content = content.replace(body_start_tag, f'{body_start_tag}\n<div class="outer-wrapper">')
            
            # Inject closing wrapper before body end
            if '</body>' in content:
                content = content.replace('</body>', '</div>\n</body>')
            else:
                # Fallback if no body tag found (rare)
                content += '</div>'
            print(f"Injected .outer-wrapper into {file_path}")
        else:
             print(f"No <body> tag found in {file_path}")
    else:
        print(f"Wrapper already present in {file_path}")

    # 3. Add v8.0 Override Block directly to HTML
    # This helps even if cache holds old CSS
    wrapper_override = """
    <style>
        /* WRAPPER TECHNIQUE v8.0 */
        html, body { overflow-x: visible !important; overflow-y: visible !important; }
        .outer-wrapper { overflow-x: clip !important; width: 100% !important; max-width: 100vw !important; }
    </style>
    """
    
    # Clean old overrides
    content = re.sub(r'<style>\s*/\* STABILITY OVERRIDE.*?/style>', '', content, flags=re.S)
    
    # Inject new override before closing body
    if '</body>' in content:
        content = content.replace('</body>', f'{wrapper_override}\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def update_legacy_css(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove any locking on body
    content = re.sub(r'body\s*{[^}]*overflow-x:\s*hidden[^}]*}', 'body { overflow-x: visible !important; }', content, flags=re.I)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated Legacy CSS in {file_path}")

# Run
for hf in html_files:
    apply_wrapper_structure(hf)

update_legacy_css(css_files[1])

# Sync Universal CSS
shutil.copy2(css_files[0], r'E:\msharea\b7oth\mah\universal.css')
print("Synced Universal CSS v8.0 to mah folder")
