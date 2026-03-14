# python get_authors_name.py

import os
import re
import json

# ==========================================
# 1. 基礎配置 (Configuration)
# ==========================================
# 指定要掃描的目標資料夾（支援多個路徑）
TARGET_DIRS = [r"D:\temp", r"C:\comic"]
# OUTPUT_FILENAME = "get_authors_name.json"
OUTPUT_FILENAME = "get_authors_name.json"

# 自動獲取腳本所在目錄，確保輸出路徑正確
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, OUTPUT_FILENAME)

# ==========================================
# 2. 正規表達式定義 (Regex Pattern)
# ==========================================
# 目標：匹配檔名開頭或中間的中括號內容，且檔案必須為 .zip
# 模式解析：
# Group 1 & 2: [作者 (社團)] -> 範例: [Artist (Circle)] title.zip
# Group 3   : [單一名稱]     -> 範例: [Artist] title.zip
regex_pattern = re.compile(
    r'.*?' 
    r'(?:' 
        r'\[\s*(.*?)\s*\(\s*(.*?)\s*\)\]'  # 模式一：處理帶括號的複合名稱
        r'|' 
        r'\[\s*(.*?)\s*\]'                # 模式二：處理單一中括號名稱
    r')' 
    r'.*\.zip$', 
    re.IGNORECASE 
)

def main():
    # 用於儲存「檔名: [提取結果]」的映射表
    results_map = {}

    # ==========================================
    # 3. 執行掃描與提取 (Execution)
    # ==========================================
    for target_dir in TARGET_DIRS:
        print(f">>> 正在掃描路徑: {target_dir}")

        # 防錯處理：檢查路徑有效性
        if not os.path.isdir(target_dir):
            print(f"    [跳過] 路徑不存在: {target_dir}")
            continue

        # 遍歷資料夾內的所有檔案
        for filename in os.listdir(target_dir):
            # 僅處理壓縮檔 (.zip)
            if filename.lower().endswith('.zip'):
                match = regex_pattern.search(filename)
                extracted_names = []

                if match:
                    # 邏輯 A：優先提取 [作者 (社團)] 格式
                    if match.group(1) is not None:
                        author = match.group(1).strip()
                        circle = match.group(2).strip()
                        if author: extracted_names.append(author)
                        if circle: extracted_names.append(circle)
                    
                    # 邏輯 B：若 A 不成立，提取 [單一名稱] 格式
                    elif match.group(3) is not None:
                        name = match.group(3).strip()
                        if name: extracted_names.append(name)

                # 如果有提取到任何內容，存入結果清單
                if extracted_names:
                    results_map[filename] = extracted_names

    # ==========================================
    # 4. 資料持久化 (Output)
    # ==========================================
    if results_map:
        try:
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(
                    results_map, 
                    f, 
                    indent=4, 
                    ensure_ascii=False 
                )
            print(f"\n[完成] 成功提取 {len(results_map)} 個檔案資訊。")
            print(f"[檔案] 儲存至: {OUTPUT_PATH}")
        except Exception as e:
            print(f"\n[錯誤] 寫入 JSON 時發生問題: {e}")
    else:
        print("\n[提示] 掃描結束，未發現符合格式的檔案。")

if __name__ == "__main__":
    main()
