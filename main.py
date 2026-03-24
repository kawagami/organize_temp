
# python main.py

import json
import os
import shutil

# ==========================================
# 1. 配置與路徑設定
# ==========================================
base_path = r'D:\comic' # 這是分類後的根目錄

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
print(f"🚀 開始執行檔案分類 (支援子資料夾路徑)...\n")

move_count = 0
skip_count = 0

# 這裡的 filename 其實是 JSON 裡的 Key (完整路徑)
for full_source_path, tags in get_authors_name.items():
    if move_count >= 500:
        break

    # A. 檢查來源檔案是否存在 (直接使用 Key，不需 join)
    if not os.path.exists(full_source_path):
        # print(f"【跳過】找不到檔案: {full_source_path}")
        continue

    # B. 權重比較
    best_tag = None
    max_weight = 0

    for tag in tags:
        weight = show_data.get(tag, 0)
        if weight > max_weight:
            max_weight = weight
            best_tag = tag

    # C. 根據權重判斷是否執行搬移
    if best_tag:
        # 提取純檔名，用於拼接到目標資料夾
        pure_filename = os.path.basename(full_source_path)
        target_dir = os.path.join(base_path, best_tag)
        target_file = os.path.join(target_dir, pure_filename)

        # 建立目標資料夾
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # 防止「來源」與「目標」相同時報錯 (例如檔案已經在目標分類資料夾裡了)
        if os.path.abspath(full_source_path) == os.path.abspath(target_file):
            continue

        try:
            shutil.move(full_source_path, target_file)
            print(f"【搬移】({max_weight:2d}次) {pure_filename} -> /{best_tag}/")
            move_count += 1
        except Exception as e:
            print(f"【錯誤】無法搬移 {pure_filename}: {e}")
    else:
        skip_count += 1

# ==========================================
# 3. 執行結果彙整
# ==========================================
print(f"\n" + "="*40)
print(f"✅ 處理完成！")
print(f"📦 成功移動檔案：{move_count} 筆")
print(f"⚠️ 權重不足或已在位：{skip_count} 筆")
print("="*40)
