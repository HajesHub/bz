import re
import os
import shutil

# Full paths for absolute accuracy
files_to_fix = [
    r'E:\msharea\b7oth\ports\index.html',
    r'E:\msharea\b7oth\mah\mahmoudiah.html',
    r'E:\msharea\b7oth\mah\mahber.html',
    r'E:\msharea\b7oth\ports\universal.css',
    r'E:\msharea\b7oth\mah\style.css'
]

# 1. Update Universal CSS to be the ULTIMATE authority on freedom
universal_css = r'E:\msharea\b7oth\ports\universal.css'
freedom_css = """
/* 
 * Universal Freedom CSS v5.0 - THE FINAL WORD
 * Unlocks Absolute Zoom & Smooth Scroll
 */

html, body {
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important; /* The most important rule for zoom out */
    overflow-x: visible !important;
    width: auto !important;
    min-width: 100% !important;
    position: relative !important;
    -webkit-text-size-adjust: auto !important;
}

/* Ensure ALL components that need horizontal scroll get it, without locking the page */
.table-container, .table-responsive, .nav-tabs, .nav-pills, .tabs-navigation, .tab-pane {
    display: block !important;
    width: 100% !important;
    overflow-x: auto !important; /* Internal scroll only */
    overflow-y: visible !important;
    -webkit-overflow-scrolling: touch !important;
    margin-bottom: 2rem !important;
}

/* Force tables to remain unbroken grids */
table {
    display: table !important;
    width: auto !important;
    min-width: 100% !important;
    border-collapse: collapse !important;
}

th, td {
    white-space: nowrap !important;
    padding: 12px 15px !important;
    text-align: right !important;
    border: 1px solid #dee2e6 !important;
}

/* Tabs: Forced horizontal bar */
.nav-tabs, .nav-pills {
    display: flex !important;
    flex-wrap: nowrap !important;
}

.nav-link, .tab {
    flex: 0 0 auto !important;
    white-space: nowrap !important;
}
"""

def total_cleanup(file_path):
    if not os.path.exists(file_path):
        print(f"Skipping: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Viewport: Force Absolute Freedom
    new_vp = '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.1, user-scalable=yes">'
    content = re.sub(r'<meta name="viewport"[^>]*>', new_vp, content)

    # Remove the "HIDDEN" locks from everywhere
    # Except for video-container which might need it for cropping, but for now we prioritize zoom
    content = re.sub(r'overflow:\s*hidden\s*;?', 'overflow: visible !important;', content, flags=re.I)
    content = re.sub(r'overflow-x:\s*hidden\s*;?', 'overflow-x: visible !important;', content, flags=re.I)

    # Ensure universal.css is linked in all HTML files
    if file_path.endswith('.html') and 'universal.css' not in content:
        if '</head>' in content:
            content = content.replace('</head>', '<link rel="stylesheet" href="universal.css">\n</head>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned and unlocked: {file_path}")

# Run
with open(universal_css, 'w', encoding='utf-8') as f:
    f.write(freedom_css)
print(f"Updated {universal_css}")

for f in files_to_fix:
    total_cleanup(f)

# Sync
shutil.copy2(universal_css, r'E:\msharea\b7oth\mah\universal.css')
print("Synced Universal CSS to mah folder")
