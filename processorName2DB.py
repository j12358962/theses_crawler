# -*- coding: utf-8 -*-
import pandas as pd
import pymysql

# 這個程式的功能是假設有一個教授名單的csv檔，讀取之並將其儲存至 database 中

#database connection information
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "db": "theses-content",
    "charset": "utf8"
}

#connect to database
try:
    conn = pymysql.connect(**db_settings)
except Exception as e:
    print(e)

#create a table
with conn.cursor() as cursor:
    createTable = "CREATE TABLE IF NOT EXISTS `crawler-log` (\
      `ID` INT NOT NULL AUTO_INCREMENT,\
      `professorName` VARCHAR(45) NULL DEFAULT NULL,\
      `isCrawledAll` TINYINT NULL DEFAULT 0,\
      `yearCrawled` INT NULL DEFAULT NULL,\
      `paperAmount` INT NULL DEFAULT NULL,\
      PRIMARY KEY (`ID`));"
    cursor.execute(createTable)

#read professor list
df = pd.read_csv('professor.csv', encoding='big5')

#insert professor names to database
with conn.cursor() as cursor:
    insertCommand = "Insert IGNORE Into `crawler-log` (professorName) VALUES (%s)"
    
    for name in df.professorName:
        cursor.execute(insertCommand, name)
    conn.commit()
