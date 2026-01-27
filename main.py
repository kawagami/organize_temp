
# python main.py

import json
import os
import re

# from path
from_path = r'D:\temp'

# 設定目標根目錄
base_path = r'C:\comic'

def sanitize_filename(filename):
    """
    移除或替換 Windows 中不合法的路徑字元
    """
    # Windows 非法字元: \ / : * ? " < > |
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

# 1. 讀取 JSON 檔案
with open('extraction_results.json', 'r', encoding='utf-8') as f:
    extraction_results = json.load(f)

with open('value_counts_sorted.json', 'r', encoding='utf-8') as f:
    value_counts_sorted = json.load(f)

for filename, tags in extraction_results.items():
    # 預設沒對應的資料
    matched_authors = {}

    # 1. 拿 tags 中的每一個 string 出來
    for tag in tags:
        # 2. 檢查這個 tag 是否存在於 value_counts_sorted 的 key 中
        if tag in value_counts_sorted:
            # 3. 存在的話，取得該作者的權重
            weight = value_counts_sorted[tag]
            matched_authors[tag] = weight
            # print(f"檔案: {filename}")
            # print(f"匹配到作者: {tag}")
            # print(f"權重: {weight}")
            # print(f"")

    # 檢查是否有匹配到任何作者
    if matched_authors:
        # 使用 max 函數，依據字典的 Value (權重) 找出 Key (作者名)
        best_author = max(matched_authors, key=matched_authors.get)
        highest_weight = matched_authors[best_author]

        print(f"🏆 最終決定：")
        print(f"選擇權重最高的作者: {best_author} (權重: {highest_weight})")
        
        # 接下來就可以執行你的路徑組合與建立資料夾邏輯
        target_dir = os.path.join(base_path, sanitize_filename(best_author))
        # os.makedirs(target_dir, exist_ok=True)
    else:
        print(f"❌ 檔案 {filename} 沒有匹配到任何已知權重資料。")

    print("-" * 20)


# 該 key 的 values 就是整理出來的作者對應名稱
# 接著去 value_counts_sorted.json 取名稱權重
# 取高的建立資料夾
# 找不到的話就跳過
