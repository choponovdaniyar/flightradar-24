from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random
import json
import re


airport_code = {
    'atl': "Hartsfield-Jackson International Airport",
    'dfw': "Dallas/Fort Worth International Airport",
    'den': "Denver International Airport",
    'ord': "O'Hare International Airport",
    'lax': "Los Angeles International Airport",
    'clt': "Charlotte Douglas International Airport",
    'las': "Harry Reid International Airport",
    'phx': "Phoenix Sky Harbor International Airport",
    'mco': "Orlando International Airport",
    'sea': "Seattle–Tacoma International Airport",
    'mia': "Miami International Airport",
    'iah': "George Bush Intercontinental Airport",
    'jfk': "John F. Kennedy International Airport",
    'fll': "Fort Lauderdale–Hollywood International Airport",
    'ewr': "Newark Liberty International Airport",
    'sfo': "San Francisco International Airport",
    'msp': "Minneapolis–Saint Paul International Airport",
    'dtw': "Detroit Metropolitan Airport",
    'bos': "Logan International Airport",
    'slc': "Salt Lake City International Airport",
    'phl': "Philadelphia International Airport",
    'bwi': "Baltimore/Washington International Airport",
    'tpa': "Tampa International Airport",
    'san': "San Diego International Airport",
    'mdw': "Midway International Airport",
    'lga': "LaGuardia Airport",
    'bna': "Nashville International Airport",
    'iad': "Washington Dulles International Airport"
}

# options
options_ = webdriver.FirefoxOptions()
options_.set_preference("general.useragent.override", UserAgent().random)
    
# browser
driver = webdriver.Firefox(options= options_)


password = "Qazwsx_00"
login = "choponov.099@gmail.com"


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
        print(w)
        json_[w] = res
        print(f"{it}/{size}")
        it += 1

    with open("res.json", "w", encoding="utf-8") as f:
        json.dump(json_,f,indent=4, ensure_ascii=False)

except Exception as e:
    raise
finally:
    driver.quit()