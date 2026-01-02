import re
import os

path = r'E:\msharea\b7oth\mah\mahmoudiah.html'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Improved tab logic that ensures visibility management
    new_block = """ // إعادة تفعيل الألسنة للمحتوى الجديد
 const newTabs = contentDiv.querySelectorAll('.tab');
 const newTabContents = contentDiv.querySelectorAll('.tab-content');
 
 newTabs.forEach(nT => {
     nT.addEventListener('click', () => {
         newTabs.forEach(t => t.classList.remove('active'));
         newTabContents.forEach(c => {
             c.classList.remove('active');
             c.style.display = 'none';
         });
         nT.classList.add('active');
         const tId = nT.getAttribute('data-tab');
         const target = contentDiv.querySelector('#' + tId);
         if (target) {
             target.classList.add('active');
             target.style.display = 'block';
         }
     });
 });"""

    # Replace the placeholder or previous implementation
    # We look for the comment line as an anchor
    if " // إعادة تفعيل الألسنة للمحتوى الجديد" in content:
        # Find the block starting with this comment and ending with revealSections call
        pattern = r"// إعادة تفعيل الألسنة للمحتوى الجديد.*?if \(typeof revealSections === 'function'\) revealSections\(\);"
        replacement = new_block + "\n if (typeof revealSections === 'function') revealSections();"
        content = re.sub(pattern, replacement, content, flags=re.S)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated tab logic successfully')
    else:
        print('Target comment not found')
else:
    print(f'File not found: {path}')
