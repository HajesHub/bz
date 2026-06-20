import os

file_path = r"e:\msharea\تطبيقات الجوال\AlMahmoudia_Calc.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_start = "<!-- Control Buttons -->"
# Find the div that contains this comment and remove the whole div block
idx = content.find(target_start)
if idx != -1:
    # Find the start of the div (usually a few characters before)
    # Actually, the user showed me the block. Let's find the closing tag.
    # The block ends before "</div>\n                </div>\n            </div>"
    
    # Let's use a simpler way: find the start comment and the next "<!-- Results Column -->"
    results_idx = content.find("<!-- Results Column -->")
    if results_idx != -1:
        # We want to keep the closing divs of the previous section
        # The structure is:
        # [Buttons]
        #     </div>
        # </div>
        # <!-- Results Column -->
        
        # Let's find the 3 closing divs before Results Column
        # and we want to remove everything between the comment and those 3 divs
        
        # Actually, let's just match the EXACT block provided by the user in the prompt
        user_block = """                        <!-- Control Buttons -->
                        <div class="flex gap-3 mt-4 pt-4 border-t border-gray-100">
                            <button id="restockBtn" class="flex-1 bg-amber-600 hover:bg-amber-700 text-white font-bold py-3 px-4 rounded-2xl transition shadow-lg flex items-center justify-center gap-2">
                                <span>📦 عَزِّز المخزون</span>
                            </button>
                            <button id="resetAllBtn" class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-2xl transition flex items-center justify-center gap-2">
                                <span>🔄 مسح الكل</span>
                            </button>
                        </div>"""
        
        # Try exact match first
        if user_block in content:
            new_content = content.replace(user_block, "")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Successfully removed redundant buttons.")
        else:
            print("Exact match failed, trying flexible match...")
            # Use split and join if needed
            import re
            # Remove the block using regex to ignore slight whitespace differences
            pattern = re.escape(target_start) + r".*?<\/div>\s+<\/div>\s+<\/div>"
            # Wait, that's too much.
            
            # Let's just look for the comment and remove until the next </div>
            start_idx = content.find(target_start)
            if start_idx != -1:
                # Find the closing </div> of the "flex gap-3" div
                end_div = content.find("</div>", start_idx + len(target_start))
                if end_div != -1:
                    # Found it. Let's remove from start_idx to end_div + 6
                    new_content = content[:start_idx] + content[end_div + 6:]
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print("Successfully removed redundant buttons (flexible).")
else:
    print("Could not find Control Buttons section.")
