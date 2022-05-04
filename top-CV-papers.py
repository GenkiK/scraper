from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

last_year = datetime.today().year - 1

# 検索する年数範囲の入力
from_ = int(input("from: "))
while from_ > last_year:
    print(f"Please input smaller number than '{last_year + 1}'")
    from_ = int(input("from: "))

to = int(input("to: "))
while to < from_ or to > last_year:
    print(f"Please input number between from {from_} to {last_year}")
    to = int(input("to: "))

# 検索する語の入力
# TODO: AND入力を可能にする
search_word = input("search word: ").lower()

include_ECCV = input("include ECCV? (It takes some time) / [yes]: ").lower()
if include_ECCV == "" or include_ECCV == "yes":
    include_ECCV = "yes"
else:
    include_ECCV = "no"

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

for year in range(from_, to + 1):
    for conference in ["ICCV", "CVPR"]:
        # 偶数年はICCVは開かれない
        if conference == "ICCV" and year % 2 == 0:
            continue
        print(f"\n========================== {conference} {year} ==========================")
        driver.get(f"https://openaccess.thecvf.com/{conference}{year}")
        search_box = driver.find_element(By.NAME, "query")
        search_box.send_keys(search_word)
        search_box.submit()
        paper_titles = driver.find_elements(By.CLASS_NAME, "ptitle")
        for paper_title in paper_titles:
            print(paper_title.text)
# ECCV
if include_ECCV == "yes":
    driver.get("https://www.ecva.net/papers.php")
    from_ = from_ if from_ >= 2018 else 2018
    for year in range(from_, to + 1):
        # ECCVは偶数年のみ開かれる
        if year % 2 == 0:
            print(f"\n========================== ECCV {year} ==========================")
            yearly_content = driver.find_element(
                By.XPATH,
                f"//button[contains(text(), '{year}')]/following-sibling::div[@class='accordion-content']",
            )
            paper_titles = yearly_content.find_elements(By.XPATH, "//dt[@class='ptitle']")
            for paper_title in paper_titles:
                text = paper_title.get_attribute("textContent")
                if search_word in text.lower():
                    print(text.replace("\n", ""))
driver.quit()
