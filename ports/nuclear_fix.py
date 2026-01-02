import re
import os
import shutil

# Files to process
html_files = [
    r'E:\msharea\b7oth\ports\index.html',
    r'E:\msharea\b7oth\mah\mahmoudiah.html',
    r'E:\msharea\b7oth\mah\mahber.html'
]

css_files = [
    r'E:\msharea\b7oth\ports\universal.css',
    r'E:\msharea\b7oth\mah\style.css'
]

# 1. Update Universal CSS to be Brutally Permissive
universal_css_content = """
/* 
 * Universal Freedom CSS v4.0 - FINAL EMERGENCY VERSION
 * Forces Absolute Zoom Out and Table Scrolling
 */

html, body {
    overflow: visible !important;
    overflow-x: visible !important;
    width: auto !important;
    min-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    position: relative !important;
}

/* Ensure all tables and tabs are scrollable and don't fragment */
.table-container, .table-responsive, .nav-tabs, .nav-pills, .tabs-navigation, .tab-pane {
    display: block !important;
    width: 100% !important;
    overflow-x: auto !important;
    overflow-y: visible !important;
    -webkit-overflow-scrolling: touch !important;
    margin-bottom: 20px !important;
    position: relative !important;
}

table {
    display: table !important;
    width: 100% !important;
    min-width: 800px !important; /* Forces scroll incentive */
    border-collapse: collapse !important;
}

th, td {
    white-space: nowrap !important;
    padding: 12px 15px !important;
    text-align: right !important;
    border: 1px solid #dee2e6 !important;
}

/* Tab specific - Horizontal scroll */
.nav-tabs, .nav-pills {
    display: flex !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    padding: 10px 0 !important;
}

.nav-link, .tab {
    flex: 0 0 auto !important;
    white-space: nowrap !important;
}
"""

with open(css_files[0], 'w', encoding='utf-8') as f:
    f.write(universal_css_content)

def nuclear_cleanup(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # A. Viewport Reset
    new_vp = '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.1, user-scalable=yes">'
    content = re.sub(r'<meta name="viewport"[^>]*>', new_vp, content)

    # B. Strip all overflow:hidden
    content = re.sub(r'overflow:\s*hidden\s*;?', 'overflow: visible !important;', content, flags=re.I)
    content = re.sub(r'overflow-x:\s*hidden\s*;?', 'overflow-x: visible !important;', content, flags=re.I)

    # C. Inject final override before </body>
    override_style = """
    <style>
        /* FINAL FREEDOM OVERRIDE */
        html, body { overflow: visible !important; overflow-x: visible !important; width: auto !important; min-width: 100% !important; }
        .table-container, .table-responsive, .nav-tabs, .tab-pane { overflow-x: auto !important; display: block !important; width: 100% !important; }
        table { min-width: 900px !important; display: table !important; }
    </style>
    """
    if '</body>' in content:
        content = content.replace('</body>', f'{override_style}\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Nuclear cleanup applied to {file_path}")

def clean_other_css(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(r'overflow:\s*hidden\s*;?', 'overflow: visible !important;', content, flags=re.I)
    content = re.sub(r'overflow-x:\s*hidden\s*;?', 'overflow-x: visible !important;', content, flags=re.I)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"CSS Nuclear cleanup applied to {file_path}")

# Run
for hf in html_files:
    nuclear_cleanup(hf)

clean_other_css(css_files[1])

# Sync
shutil.copy2(css_files[0], r'E:\msharea\b7oth\mah\universal.css')
print("Synced Universal CSS to mah folder")
