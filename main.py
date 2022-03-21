from pyparsing import Opt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random
import json

from valid import is_valid
from jsontoexcel import to_excel
from our_airs import airport_code

# options
options_ = webdriver.FirefoxOptions()
options_.headless = True
options_.set_preference("general.useragent.override", UserAgent().random)
    
# browser
driver = webdriver.Firefox(options= options_)

coincidence = dict()
try:
    def get_html(code): 
        link = f"https://www.flightradar24.com/data/airports/{code}/departures"
        driver.get(link)
        time.sleep(random.randint(3,5))

        html = driver.find_element("css selector", "body")
        
        while True:
            xpath = "/html/body/div[7]/div[2]/section/div/section/div/div[2]/div/aside/div[1]/table/tfoot/tr[1]/td/button"
            try:
                next = driver.find_elements("xpath", xpath)
                next[0].click()
            except:
                break
            html.send_keys(Keys.END)
            time.sleep(random.randint(2,4))
        
        while True:
            colspan = "td[colspan='7']"
            prev = driver.find_elements("css selector", colspan)[0]
            try:
                prev.click()
            except:
                break
            html.send_keys(Keys.HOME)
            time.sleep(random.randint(2,4))
            

        with open(f"data/{code}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    def parse_html(fn):
        with open(fn, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "lxml")
            a_s = soup.select("tbody > tr > td:nth-child(3) > div:nth-child(1) > a:nth-child(2)")
            airs = set()
            for air in a_s:
                if is_valid(air.attrs["title"],air.text):
                    try:
                        coincidence[f'{air.attrs["title"]}{air.text}'] += 1
                    except KeyError:
                        coincidence[f'{air.attrs["title"]}{air.text}'] = 1
                    airs.add(f'{air.attrs["title"]}{air.text}')
        return list(airs)
    
    json_ = dict()
    it = 1
    size = len(airport_code)
    for code in airport_code:
        try:
            res = parse_html(f"data/{code}.html")
        except:
            get_html(code)
            res = parse_html(f"data/{code}.html")
        w = f"{airport_code[code]}({code.upper()})"
        json_[w] = res
        print(f"{it}/{size}")
        it += 1

    with open("json/result.json", "w", encoding="utf-8") as f:
        json.dump(json_,f,indent=4, ensure_ascii=False)

    with open("json/final.json", "w", encoding="utf-8") as f:
        json.dump(coincidence,f,indent=4, ensure_ascii=False)

    # to_excel("result")
    # to_excel("final")

except Exception as e:
    raise
finally:
    driver.quit()