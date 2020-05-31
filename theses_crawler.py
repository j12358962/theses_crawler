# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re
import logging
import pymysql
import time

# 引入 logging 配置
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 計算當前學年度
year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())

if (month < 7):
    academicYear = year - 1912
else:
    academicYear = year - 1911

driver = webdriver.Firefox()

# Database connection information
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "db": "theses-content",
    "charset": "utf8"
}

# Connect to database
try:
    conn = pymysql.connect(**db_settings)
    cur = conn.cursor()
except Exception as e:
    print(e)

# Create a table if not exists
with conn.cursor() as cursor:
    createTable = "CREATE TABLE IF NOT EXISTS `theses-information` (\
      `studentName_ch` varchar(45) NOT NULL,\
      `studentName_en` varchar(45) DEFAULT NULL,\
      `thesesName_ch` varchar(255) NOT NULL,\
      `thesesName_en` varchar(255) DEFAULT NULL,\
      `professorName_ch` varchar(45) NOT NULL,\
      `professorName_en` varchar(45) DEFAULT NULL,\
      `oralTestCommitteeName_ch` longtext,\
      `oralTestCommitteeName_en` longtext,\
      `oralTestDate` varchar(45) DEFAULT NULL,\
      `degreeType` varchar(45) DEFAULT NULL,\
      `schoolName` varchar(45) DEFAULT NULL,\
      `departmentName` varchar(45) DEFAULT NULL,\
      `discipline` varchar(45) DEFAULT NULL,\
      `educationType` varchar(45) DEFAULT NULL,\
      `publishYear` varchar(45) DEFAULT NULL,\
      `graduationYear` varchar(45) DEFAULT NULL,\
      `languageType` varchar(45) DEFAULT NULL,\
      `pageCount` varchar(45) DEFAULT NULL,\
      `keywords_ch` mediumtext,\
      `keywords_en` mediumtext,\
      `abstract_ch` longtext,\
      `abstract_en` longtext,\
      `tableOfContents` longtext,\
      `refs` longtext,\
      PRIMARY KEY (`studentName_ch`,`professorName_ch`,`thesesName_ch`)\
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
    cursor.execute(createTable)


def crawlContent(professorName, yearCrawled):
    driver.get("https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge")
    driver.find_element_by_link_text(u"指令查詢").click()
    driver.find_element_by_id("ysearchinput0").click()
    driver.find_element_by_id("ysearchinput0").clear()

    # 以教授名稱和年份執行指令查詢
    if (yearCrawled != None):
        driver.find_element_by_id("ysearchinput0").send_keys(
            u"\"" + professorName + "\".ad and \"" + str(yearCrawled) + "\".yr")
    # 只以教授名稱查詢
    else:
        driver.find_element_by_id("ysearchinput0").send_keys(u"\"" + professorName + "\".ad")

    driver.find_element_by_id("gs32search").click()
    paperAmount = driver.find_element_by_xpath(
        "//*[@id='bodyid']/form/div/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/div[1]/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/span[2]").text
    paperAmount = paperAmount.lstrip().rstrip()

    if (paperAmount == '0'):
        return

    driver.find_element_by_name("sortby").click()
    Select(driver.find_element_by_name("sortby")).select_by_visible_text(u"畢業學年度(遞增)")
    driver.find_element_by_name("sortby").click()
    xpath = "//table[@id='tablefmt1']/tbody/tr[2]/td[3]/div/div/table/tbody/tr/td/a/span"
    driver.find_element_by_xpath(xpath).click()

    for j in range(2, int(paperAmount) + 2):
        try:
            li = driver.find_elements_by_xpath('//*[@id="gs32_levelrecord"]/ul/li')
            studentName_ch = 'null'
            studentName_en = 'null'
            thesesName_ch = 'null'
            thesesName_en = 'null'
            professorName_ch = 'null'
            professorName_en = 'null'
            oralTestCommitteeName_ch = 'null'
            oralTestCommitteeName_en = 'null'
            oralTestDate = 'null'
            degreeType = 'null'
            schoolName = 'null'
            departmentName = 'null'
            discipline = 'null'
            educationType = 'null'
            publishYear = 'null'
            graduationYear = 'null'
            languageType = 'null'
            pageCount = 'null'
            keywords_ch = 'null'
            keywords_en = 'null'
            abstract_ch = 'null'
            abstract_en = 'null'
            tableOfContents = 'null'
            refs = 'null'

            for i in range(0, len(li) - 1):
                if (li[i].text == "論文基本資料"):
                    li[i].click()
                    tableList = driver.find_element_by_xpath('//*[@id="gs32_levelrecord"]/div').text.splitlines()
                    # 做字串處理
                    for data in tableList:
                        if ('研究生:' in data):
                            studentName_ch = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('研究生(外文):' in data):
                            studentName_en = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('論文名稱:' in data):
                            thesesName_ch = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('論文名稱(外文):' in data):
                            thesesName_en = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('指導教授:' in data):
                            professorName_ch = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('指導教授(外文):' in data):
                            professorName_en = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('口試委員:' in data):
                            oralTestCommitteeName_ch = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('口試委員(外文):' in data):
                            oralTestCommitteeName_en = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('口試日期:' in data):
                            oralTestDate = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('學位類別:' in data):
                            degreeType = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('校院名稱:' in data):
                            schoolName = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('系所名稱:' in data):
                            departmentName = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('學門:' in data):
                            discipline = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('學類:' in data):
                            educationType = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('論文出版年:' in data):
                            publishYear = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('畢業學年度:' in data):
                            graduationYear = re.sub("\"", "`", re.split('[: ]', data, maxsplit=1)[1]).lstrip()
                        if ('語文別:' in data):
                            languageType = re.sub("\"", "`", re.split('[:  ]', data, maxsplit=1)[1]).lstrip()
                        if ('論文頁數:' in data):
                            pageCount = re.sub("\"", "`", re.split('[:  ]', data, maxsplit=1)[1]).lstrip()
                        if ('中文關鍵詞:' in data):
                            keywords_ch = re.sub("\"", "`", re.split('[:  ]', data, maxsplit=1)[1]).lstrip()
                        if ('外文關鍵詞:' in data):
                            keywords_en = re.sub("\"", "`", re.split('[:  ]', data, maxsplit=1)[1]).lstrip()
                elif (li[i].text == "摘要"):
                    li[i].click()
                    abstract_ch = re.sub("\"", "`",
                                         driver.find_element_by_xpath('//*[@id="gs32_levelrecord"]/div').text).lstrip()
                elif (li[i].text == "外文摘要"):
                    li[i].click()
                    abstract_en = re.sub("\"", "`",
                                         driver.find_element_by_xpath('//*[@id="gs32_levelrecord"]/div').text).lstrip()
                elif (li[i].text == "目次"):
                    li[i].click()
                    tableOfContents = re.sub("\"", "`", driver.find_element_by_xpath(
                        '//*[@id="gs32_levelrecord"]/div').text).lstrip()
                elif (li[i].text == "參考文獻"):
                    li[i].click()
                    refs = re.sub("\"", "`",
                                  driver.find_element_by_xpath('//*[@id="gs32_levelrecord"]/div').text).lstrip()
                else:
                    pass

            insertThesesInfo = '''insert into `theses-information` (studentName_ch, studentName_en, thesesName_ch, thesesName_en,\
                    professorName_ch, professorName_en, oralTestCommitteeName_ch,\
                    oralTestCommitteeName_en, oralTestDate, degreeType, schoolName,\
                    departmentName, discipline, educationType, publishYear,\
                    graduationYear, languageType, pageCount, keywords_ch, keywords_en, abstract_ch, abstract_en, tableOfContents, refs)\
                    VALUES \
                    ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' % \
                               (studentName_ch, studentName_en, thesesName_ch, thesesName_en, professorName_ch,
                                professorName_en, oralTestCommitteeName_ch,
                                oralTestCommitteeName_en, oralTestDate, degreeType, schoolName, departmentName,
                                discipline, educationType, publishYear,
                                graduationYear, languageType, pageCount, keywords_ch, keywords_en, abstract_ch,
                                abstract_en, tableOfContents, refs)
            updateCrawl_log = '''UPDATE `crawler-log` set yearCrawled=%s where professorName="%s"''' % (
            graduationYear, professorName)

            try:
                cur.execute(updateCrawl_log)
                conn.commit()
            except Exception as e:
                print(e)
                pass
            logging.info('正在取得標題為{}的資料'.format(thesesName_ch))
            try:
                cur.execute(insertThesesInfo)
                conn.commit()
            except Exception as e:
                print(e)
                pass

            driver.find_element_by_name("jmpage").click()
            driver.find_element_by_name("jmpage").clear()
            driver.find_element_by_name("jmpage").send_keys(j)
            driver.find_element_by_name("jumpfmt0page").click()

        except Exception as e:
            print(e)
            pass


with conn.cursor() as cursor:
    selectCommand = "SELECT professorName, isCrawledAll, yearCrawled from `crawler-log`"
    cursor.execute(selectCommand)
    results = cursor.fetchall()
    for row in results:
        professorName = row[0]
        # Crawl all data
        if row[1] == 0:
            # None 代表未爬過這個教授的論文
            crawlContent(professorName, None)
            # 爬完這個教授的所有論文資料後設為已爬過
            cur.execute("UPDATE `crawler-log` set isCrawledAll=true where professorName=%s", (professorName))
            conn.commit()
        # 一年一年爬
        else:
            crawledYear = row[2]
            # 以教授名稱、年份為搜尋資料去爬蟲
            for i in range(crawledYear, academicYear + 1):
                crawlContent(professorName, i)
