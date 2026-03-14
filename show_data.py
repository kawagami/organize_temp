import os
import json

# ==========================================
# 1. 路徑與環境配置
# ==========================================
# 取得目前腳本所在的目錄，確保後續檔案讀寫路徑正確
script_dir = os.path.dirname(os.path.abspath(__file__))

# 定義輸入與輸出的檔案路徑
INPUT_JSON_PATH = os.path.join(script_dir, "get_authors_name.json")
OUTPUT_JSON_PATH = os.path.join(script_dir, "show_data.json")
SKIP_WORDS_FILE = "skip_keywords.txt"

# ==========================================
# 2. 功能函式：讀取過濾關鍵字
# ==========================================
def load_skip_keywords(file_path):
    """
    從外部 txt 檔案讀取要排除的關鍵字，回傳一個 set 集合（查詢速度較快）。
    """
    skip_set = set()
    # 檢查檔案是否存在，避免程式崩潰
    if not os.path.exists(file_path):
        print(f"[提示] 找不到 {file_path}，將不進行過濾。")
        return skip_set

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            keyword = line.strip()
            if keyword:
                skip_set.add(keyword)
    return skip_set

# ==========================================
# 3. 核心處理邏輯
# ==========================================
def main():
    # A. 載入過濾名單
    skip_keywords = load_skip_keywords(SKIP_WORDS_FILE)

    # B. 讀取原始 JSON 資料 (格式: { "檔名": ["作者", "社團"], ... })
    try:
        with open(INPUT_JSON_PATH, "r", encoding="utf-8") as f:
            results_map = json.load(f)
    except FileNotFoundError:
        print(f"[錯誤] 找不到原始資料檔: {INPUT_JSON_PATH}")
        return

    # C. 統計各項名稱出現的次數
    value_counts = {}

    for filename, names in results_map.items():
        for name in names:
            # 檢查當前名稱是否包含任何「排除關鍵字」
            # 只要有一個關鍵字命中了 name 的一部分，就跳過不統計
            if any(kw in name for kw in skip_keywords):
                continue

            # 使用 dict.get() 進行計數：如果存在就 +1，不存在則初始化為 0
            value_counts[name] = value_counts.get(name, 0) + 1

    # D. 排序邏輯 (由多到少)
    # x[1] 代表字典中的 value（即出現次數），reverse=True 代表遞減排序
    sorted_counts = dict(
        sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
    )

    # ==========================================
    # 4. 輸出結果
    # ==========================================
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(
            sorted_counts, 
            f, 
            ensure_ascii=False, 
            indent=4
        )

    print(f"✅ 統計完成！")
    print(f"📊 總計不重複作者/社團數：{len(sorted_counts)}")
    print(f"📂 結果已儲存至：{OUTPUT_JSON_PATH}")

if __name__ == "__main__":
    main()
