import os
import re
import json

# python get_authors_name.py

# --- 配置 ---
# 使用列表存儲多個目標路徑
target_dirs = [r"D:\temp", r"C:\comic"]
output_filename = "extraction_results.json"
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, output_filename)
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

# 儲存最終結果的字典（放在迴圈外，確保合併所有路徑的結果）
results_map = {}

# 遍歷所有的目標路徑
for target_dir in target_dirs:
    print(f"正在搜尋資料夾: {target_dir} ...")

    # 檢查資料夾是否存在
    if not os.path.isdir(target_dir):
        print(f"警告: 資料夾 {target_dir} 不存在，跳過此路徑。")
        continue

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
                    if AAA: extracted_strings.append(AAA)
                    if BBB: extracted_strings.append(BBB)
                
                # 模式二: [CCC]
                elif match.group(3) is not None:
                    CCC = match.group(3).strip()
                    if CCC: extracted_strings.append(CCC)

            # 將結果加入最終的 results_map 
            if extracted_strings:
                 results_map[filename] = extracted_strings

# --- 檔案寫入部分 (在所有資料夾掃描完後執行一次) ---
try:
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(
            results_map, 
            f, 
            indent=4, 
            ensure_ascii=False 
        )
    print(f"\n處理完成！成功將 {len(results_map)} 筆結果寫入檔案: {output_path}")
except Exception as e:
    print(f"\n寫入檔案時發生錯誤: {e}")