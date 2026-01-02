import re
import os

mahmoudiah_path = r'E:\msharea\b7oth\mah\mahmoudiah.html'

def fix_fetch_logic(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Stop removing nav-tabs from component
    content = content.replace("const navToRemove = tempDiv.querySelector('.nav-tabs');", "// nav preserved")
    content = content.replace("if (navToRemove) navToRemove.remove();", "// nav preserved")

    # 2. Stop forcing all sections to be visible at once
    # We want to keep them hidden so tabs work
    content = re.sub(r"tempDiv\.querySelectorAll\('\.tab-content'\)\.forEach\(c => {[^}]*}\);", "// contents hidden for tab logic", content, flags=re.S)

    # 3. Add Re-initialization Logic for Injected Tabs
    reinit_script = """
 // إعادة تفعيل الألسنة للمحتوى الجديد
 const newTabs = contentDiv.querySelectorAll('.tab');
 const newTabContents = contentDiv.querySelectorAll('.tab-content');
 
 newTabs.forEach(nT => {
     nT.addEventListener('click', () => {
         newTabs.forEach(t => t.classList.remove('active'));
         newTabContents.forEach(c => c.classList.remove('active'));
         nT.classList.add('active');
         const tId = nT.getAttribute('data-tab');
         contentDiv.querySelector(`#${tId}`).classList.add('active');
     });
 });
"""
    # Insert before the end of the fetch callback
    content = content.replace("if (typeof revealSections === 'function') revealSections();", 
                              f"{reinit_script}\n if (typeof revealSections === 'function') revealSections();")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed Fetch/Injection logic in {file_path}")

# Execute
fix_fetch_logic(mahmoudiah_path)
