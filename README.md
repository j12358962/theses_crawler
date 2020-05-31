# 碩博士論文網爬蟲程式
### 1. 建立環境
```
pip install pandas pymysql selenium #pip 版本
conda install pandas pymysql selenium #conda 版本
```
### 2. 將教授資料的 csv 檔匯入資料庫（只有得到新的教授資料時需要執行）
使用 processorName2DB.py 檔案將教授名稱存入 crawler-log資料庫，不過我暫時還沒拿到教授資料的 csv 檔案，因此 processorName2DB.py 暫時只能當參考用
### 3. 爬蟲
```
python theses_crawler.py
```
Note1: geckodriver 跟 theses_crawler.py 必須放在同一個 level 的目錄。
Note2: 程式碼的說明寫在註解裡。


