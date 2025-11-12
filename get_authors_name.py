import os
import re
import json

# --- 配置 ---
target_dir = r"D:\temp"
output_filename = "extraction_results.json"
output_path = os.path.join(target_dir, output_filename)
# --- 配置 ---

# 定義正規表達式模式
# 模式一: [AAA (BBB)] - AAA 是組1，BBB 是組2
# 模式二: [CCC]       - CCC 是組3
regex_pattern = re.compile(
    r'.*?'                            
    r'(?:'                            
        r'\[\s*(.*?)\s*\(\s*(.*?)\s*\)\]'  # 模式一: [AAA (BBB)]
        r'|'                          
        r'\[\s*(.*?)\s*\]'            # 模式二: [CCC]
    r')'                              
    r'.*\.zip$',                      
    re.IGNORECASE                     
)

# 儲存最終結果的字典
results_map = {}

print(f"開始搜尋資料夾: {target_dir} 中的 .zip 檔案...")

# 檢查資料夾是否存在
if not os.path.isdir(target_dir):
    print(f"錯誤: 資料夾 {target_dir} 不存在或不是一個目錄。")
else:
    # 遍歷資料夾中的所有項目
    for filename in os.listdir(target_dir):
        # 僅處理以 .zip 結尾的檔案
        if filename.lower().endswith('.zip'):
            match = regex_pattern.search(filename)
            extracted_strings = []

            if match:
                # 模式一: [AAA (BBB)] 優先
                if match.group(1) is not None:
                    AAA = match.group(1).strip()
                    BBB = match.group(2).strip()
                    
                    if AAA:
                        extracted_strings.append(AAA)
                    if BBB:
                        extracted_strings.append(BBB)
                
                # 模式二: [CCC]
                elif match.group(3) is not None:
                    CCC = match.group(3).strip()
                    
                    if CCC:
                        extracted_strings.append(CCC)

            # 將結果加入最終的 results_map 
            if extracted_strings:
                 results_map[filename] = extracted_strings
            
    # --- 新增的檔案寫入部分 ---
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # 使用 json.dump() 直接將 Python 字典寫入檔案
            json.dump(
                results_map, 
                f, 
                indent=4,              # 保持格式美觀
                ensure_ascii=False     # 確保中文字元正常寫入
            )
        print(f"\n成功將結果寫入檔案: {output_path}")
    except Exception as e:
        print(f"\n寫入檔案時發生錯誤: {e}")
    # --- 檔案寫入結束 ---

print("\n處理完成。")