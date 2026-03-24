# python get_authors_name.py

import os
import re
import json

# ==========================================
# 1. 基礎配置 (Configuration)
# ==========================================
TARGET_DIRS = [r"D:\temp", r"D:\comic"]
OUTPUT_FILENAME = "get_authors_name.json"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, OUTPUT_FILENAME)

# ==========================================
# 2. 正規表達式定義 (Regex Pattern)
# ==========================================
regex_pattern = re.compile(
    r'.*?' 
    r'(?:' 
        r'\[\s*(.*?)\s*\(\s*(.*?)\s*\)\]'  # 模式一：[作者 (社團)]
        r'|' 
        r'\[\s*(.*?)\s*\]'                # 模式二：[單一名稱]
    r')' 
    r'.*\.zip$', 
    re.IGNORECASE 
)

def main():
    results_map = {}

    # ==========================================
    # 3. 執行遞迴掃描與提取 (Recursive Scan)
    # ==========================================
    for target_dir in TARGET_DIRS:
        print(f">>> 正在深層掃描路徑: {target_dir}")

        if not os.path.isdir(target_dir):
            print(f"    [跳過] 路徑不存在: {target_dir}")
            continue

        # 使用 os.walk 進行遞迴遍歷
        # root: 當前所在的資料夾路徑
        # dirs: 該路徑下的子資料夾清單 (此處未用到)
        # files: 該路徑下的所有檔案清單
        for root, dirs, files in os.walk(target_dir):
            for filename in files:
                # 僅處理壓縮檔 (.zip)
                if filename.lower().endswith('.zip'):
                    match = regex_pattern.search(filename)
                    extracted_names = []

                    if match:
                        if match.group(1) is not None:
                            author = match.group(1).strip()
                            circle = match.group(2).strip()
                            if author: extracted_names.append(author)
                            if circle: extracted_names.append(circle)
                        elif match.group(3) is not None:
                            name = match.group(3).strip()
                            if name: extracted_names.append(name)

                    # 如果有提取到內容，將「完整路徑」作為 Key
                    if extracted_names:
                        full_path = os.path.join(root, filename)
                        results_map[full_path] = extracted_names

    # ==========================================
    # 4. 資料持久化 (Output)
    # ==========================================
    if results_map:
        try:
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(results_map, f, indent=4, ensure_ascii=False)
            print(f"\n[完成] 成功提取 {len(results_map)} 個檔案資訊。")
            print(f"[檔案] 儲存至: {OUTPUT_PATH}")
        except Exception as e:
            print(f"\n[錯誤] 寫入 JSON 時發生問題: {e}")
    else:
        print("\n[提示] 掃描結束，未發現符合 [格式] 的檔案。")

if __name__ == "__main__":
    main()
