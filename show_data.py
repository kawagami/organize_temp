import os
import json

# 取得此 py 檔案所在資料夾
script_dir = os.path.dirname(os.path.abspath(__file__))

# JSON 來源檔案
json_path = os.path.join(script_dir, "extraction_results.json")

def load_skip_keywords(file_path="skip_keywords.txt"):
    skip_set = set()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            keyword = line.strip()
            if keyword:
                skip_set.add(keyword)
    return skip_set

# 讀取 JSON
with open(json_path, "r", encoding="utf-8") as f:
    results_map = json.load(f)

# 統計 value 內字串出現的次數
value_counts = {}

skip_keywords = load_skip_keywords("skip_keywords.txt")

for filename, values in results_map.items():
    for v in values:

        # 如果 v 內含任一 skip keyword → 跳過
        if any(kw in v for kw in skip_keywords):
            continue

        value_counts[v] = value_counts.get(v, 0) + 1

# ---- 排序（由多到少）----
sorted_counts = dict(
    sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
)

# ---- 輸出排序後的 JSON ----
json_output_path = os.path.join(script_dir, "value_counts_sorted.json")

with open(json_output_path, "w", encoding="utf-8") as f:
    json.dump(sorted_counts, f, ensure_ascii=False, indent=4)

print(f"已輸出排序後的 JSON：{json_output_path}")

# # ---- 輸出排序後的 TXT ----
# txt_output_path = os.path.join(script_dir, "value_counts_sorted.txt")

# with open(txt_output_path, "w", encoding="utf-8") as f:
#     for key, count in sorted_counts.items():
#         f.write(f"{key}: {count}\n")

# print(f"已輸出排序後的 TXT：{txt_output_path}")
