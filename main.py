
# python main.py

import json
import os  # 引入作業系統模組

# from path
from_path = r'D:\temp'

# 設定目標根目錄
base_path = r'C:\comic'

# 1. 讀取 JSON 檔案
with open('extraction_results.json', 'r', encoding='utf-8') as f:
    extraction_results = json.load(f)

with open('value_counts_sorted.json', 'r', encoding='utf-8') as f:
    value_counts_sorted = json.load(f)

for filename, tags in extraction_results.items():
    for author_name, weight in value_counts_sorted.items():
        if author_name in filename:
            # --- 核心邏輯開始 ---
            
            # 1. 組合完整路徑 (例如 C:\comic\平つくね)
            target_dir = os.path.join(base_path, author_name)
            
            # 2. 檢查資料夾是否存在，不存在則建立
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
                print(f"建立新資料夾: {author_name}")
            
            # 3. 輸出
            print(f"檔案: {filename} -> 預計移至: {target_dir}")
            
            # --- 核心邏輯結束 ---
            break

# 該 key 的 values 就是整理出來的作者對應名稱
# 接著去 value_counts_sorted.json 取名稱權重
# 取高的建立資料夾
# 找不到的話就跳過
