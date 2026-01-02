import re
import os

def update_viewport(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Absolute freedom viewport
    new_vp = '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.1, maximum-scale=10.0, user-scalable=yes, shrink-to-fit=no">'
    updated_content = re.sub(r'<meta name="viewport"[^>]*>', new_vp, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"Updated viewport in {file_path}")

def update_mah_style(style_path):
    if not os.path.exists(style_path):
        print(f"File not found: {style_path}")
        return
        
    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove previous fragmentation attempts AND overflow restrictions
    content = re.sub(r'/\* ===== MOBILE TABLE SCROLL.*$', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* ===== CLEAN TABLE SCROLL.*$', '', content, flags=re.DOTALL)
    content = content.replace('overflow-x: hidden;', '')
    
    table_override = '''
/* ===== ULTIMATE TABLE SCROLL & FREEDOM ===== */
@media (max-width: 768px) {
    html, body {
        overflow-x: visible !important; /* Allow zooming out beyond boundaries */
    }
    table {
        display: table !important;
        width: auto !important;
        min-width: 100% !important;
    }
    /* Wrap tab content in scrollable container */
    .tab-pane, .table-container, .table-responsive {
        display: block !important;
        width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        margin: 20px 0;
    }
    th, td {
        white-space: nowrap !important;
        min-width: 140px !important;
        display: table-cell !important;
        padding: 12px 15px !important;
    }
    tr {
        display: table-row !important;
    }
}
'''
    if 'ULTIMATE TABLE SCROLL' not in content:
        content += table_override
        
    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Refined table styles and removed overflow in {style_path}")

# Run updates
update_viewport('index.html')
update_viewport('../mah/mahmoudiah.html')
update_mah_style('../mah/style.css')
