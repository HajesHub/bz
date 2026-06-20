import os

file_path = r"e:\msharea\تطبيقات الجوال\AlMahmoudia_Calc.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Target unique block
target = """                </div>
            </div>
        </div>

        <!-- Results Column -->"""

# Note: The spaces might vary, let's use a more robust search
# Looking at previous view_file:
# 472:                         </div>
# 473:                     </div>
# 474:                 </div>
# 475: 
# 476:                 <!-- Results Column -->

replacement_buttons = """                        </div>
                        
                        <!-- Control Buttons -->
                        <div class="flex gap-3 mt-4 pt-4 border-t border-gray-100">
                            <button id="restockBtn" class="flex-1 bg-amber-600 hover:bg-amber-700 text-white font-bold py-3 px-4 rounded-2xl transition shadow-lg flex items-center justify-center gap-2">
                                <span>📦 عَزِّز المخزون</span>
                            </button>
                            <button id="resetAllBtn" class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-4 rounded-2xl transition flex items-center justify-center gap-2">
                                <span>🔄 مسح الكل</span>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Results Column -->"""

# Try to find the block based on the structure
if "<!-- Results Column -->" in content:
    # Find the closing divs before Results Column
    parts = content.split("<!-- Results Column -->")
    if len(parts) > 1:
        left_part = parts[0]
        # Find the last 3 closing divs
        last_divs_idx = left_part.rfind("</div>")
        if last_divs_idx != -1:
            last_divs_idx = left_part.rfind("</div>", 0, last_divs_idx)
            if last_divs_idx != -1:
                last_divs_idx = left_part.rfind("</div>", 0, last_divs_idx)
                if last_divs_idx != -1:
                    # Found the start of the 3 divs
                    new_left = left_part[:last_divs_idx] + replacement_buttons
                    new_content = new_left + parts[1]
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print("Successfully added buttons.")
                else:
                    print("Could not find 3rd div.")
            else:
                print("Could not find 2nd div.")
        else:
            print("Could not find 1st div.")
    else:
        print("Could not split by Results Column.")
else:
    print("Could not find Results Column.")
