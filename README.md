
# 相關討論串
* https://chatgpt.com/c/68fd6332-04dc-8324-b583-8d2eb499ee4c

# 邏輯整理

## get_authors_name.py
* 過濾出 D:\temp & C:\comic 資料夾中的作者 or 團體名稱後寫進 get_authors_name.json

## show_data.py
* 依照 get_authors_name.json 中的資料整理出名稱權重後寫進 show_data.json
* 有另外依照 skip_keywords.txt 清單過濾非法字串

## main.py
* 根據 get_authors_name.json & show_data.json 的過濾後資料來處理要放去那個資料夾
