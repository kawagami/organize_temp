
# python main.py

import json
import os
import shutil

# ==========================================
# 1. 配置與路徑設定
# ==========================================
from_path = r'D:\temp'
base_path = r'C:\comic'

# 確保輸出路徑存在
if not os.path.exists(base_path):
    os.makedirs(base_path)

# 讀取分析結果
try:
    with open('get_authors_name.json', 'r', encoding='utf-8') as f:
        get_authors_name = json.load(f)

    with open('show_data.json', 'r', encoding='utf-8') as f:
        show_data = json.load(f)
except FileNotFoundError as e:
    print(f"[錯誤] 找不到必要的 JSON 檔案: {e}")
    exit()

# ==========================================
# 2. 執行「嚴格權重」搬移邏輯
# ==========================================
print(f"🚀 開始執行檔案分類 (僅處理有權重的標籤)...\n")

move_count = 0
skip_count = 0

for filename, tags in get_authors_name.items():
    source_file = os.path.join(from_path, filename)

    # A. 檢查來源檔案是否存在
    if not os.path.exists(source_file):
        continue

    # B. 權重比較：初始值設為 0
    best_tag = None
    max_weight = 0  # <--- 修正重點：至少要大於 0 才會被選中

    for tag in tags:
        weight = show_data.get(tag, 0)
        
        # 只有當權重超過目前最大值，且大於 0 時才更新
        if weight > max_weight:
            max_weight = weight
            best_tag = tag

    # C. 根據權重判斷是否執行搬移
    if best_tag:
        target_dir = os.path.join(base_path, best_tag)
        target_file = os.path.join(target_dir, filename)

        # 建立目標資料夾
        # if not os.path.exists(target_dir):
        #     # os.makedirs(target_dir)
        #     print(f"【建立資料夾】{target_dir}")

        try:
            # shutil.move(source_file, target_file)
            print(f"【搬移】({max_weight:2d}次) {filename} -> /{best_tag}/")
            move_count += 1
        except Exception as e:
            print(f"【錯誤】無法搬移 {filename}: {e}")
    else:
        # 權重為 0 的檔案會留在原地，不建立資料夾
        # print(f"【跳過】(無權重) {filename}")
        skip_count += 1

# ==========================================
# 3. 執行結果彙整
# ==========================================
print(f"\n" + "="*40)
print(f"✅ 處理完成！")
print(f"📦 成功移動檔案：{move_count} 筆")
print(f"⚠️ 權重不足留原地：{skip_count} 筆")
print(f"📂 目標根目錄：{base_path}")
print("="*40)
