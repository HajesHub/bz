import os

file_path = r"e:\msharea\تطبيقات الجوال\AlMahmoudia_Calc.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = "window.clearGlobalLedger = function () {\n            if (confirm('⚠️ هل أنت متأكد من تفريغ السجل الشامل لتبدأ دورة مراقبة جديدة؟\\\\n(لن يتم مسح الصفقات من داخل التبويبات الخاصة بكل مخزن)')) {"
replacement = """window.clearGlobalLedger = function () {
            const modal = document.getElementById('confirmClearModal');
            const msg = document.getElementById('clearModalMessage');
            const confirmBtn = document.getElementById('confirmClearBtn');
            msg.innerText = 'هل أنت متأكد من تفريغ السجل الشامل لتبدأ دورة مراقبة جديدة؟ (لن يتم مسح صفقات المخازن)';
            modal.classList.add('active');
            confirmBtn.onclick = () => {
                globalLedgerClearTimestamp = Date.now();
                localStorage.setItem('almahmoudia_globalClearTime', globalLedgerClearTimestamp);
                loadGlobalLedger();
                modal.classList.remove('active');
                showNotification('🧹 تم تفريغ السجل الشامل بنجاح', 'info');
            };
        };
        // Removed old closing brace
        var dummy = function() {"""

# If the above doesn't match, try a more flexible match
if target in content:
    new_content = content.replace(target, replacement)
    # We need to handle the closing brace of the original function too
    # But wait, my replacement is a full function. 
    # Let's just replace the whole function block.
    
    # Better approach: find start and end
    start_str = "window.clearGlobalLedger = function () {"
    end_str = "        };"
    
    idx_start = content.find(start_str)
    if idx_start != -1:
        idx_end = content.find(end_str, idx_start)
        if idx_end != -1:
            full_target = content[idx_start:idx_end + len(end_str)]
            new_content = content.replace(full_target, replacement.split("//")[0].strip())
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Successfully updated the file.")
        else:
            print("Could not find end of function.")
    else:
        print("Could not find start of function.")
else:
    print("Exact target match failed, attempting flexible match...")
    # Flexible match logic here if needed
