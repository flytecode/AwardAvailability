import calendar
import datetime
import unicodecsv as csv
import csv as csv2
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, UnexpectedAlertPresentException, \
    NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc
from datetime import date, timedelta
import urllib.parse
import numpy as np


# global driver
driver = uc.Chrome()
# my_cal = calendar.Calendar()
# url_1 = "https://www.hyatt.com/shop/sjcal?location=Ventana%20Big%20Sur%20an%20Alila%20Resort&checkinDate="
# url_2 = "&checkoutDate="
# url_3 = "&rooms=1&adults=2&kids=0&rate=Standard&rateFilter=woh"
# url_redirect_1 = "https://www.hyatt.com/search/Ventana%20Big%20Sur%20an%20Alila%20Resort?rooms=1&adults=2&location=Ventana%20Big%20Sur%20an%20Alila%20Resort&checkinDate="
# url_redirect_3 = "&kids=0&rate=Standard"

# search_url = url_1 + str(datetime.date(2022, 1, 18)) + url_2 + str(datetime.date(2022, 1, 18) + datetime.timedelta(days=1)) + url_3
# driver.get("https://www.google.com/search?q=hyatt&sxsrf=ALeKk03O34lXswsMn-eupsoFP3LyBPJRGw%3A1626305986570&source=hp&ei=wnXvYJP9H5PpmAW6qorABA&iflsig=AINFCbYAAAAAYO-D0ogVsJr5JBrPcPuVAVG0zVuKWeZI&oq=hyatt&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgjECcyBAgjECcyBwgAELEDEEMyBAgAEEMyCwguELEDEMcBEKMCMgcILhCxAxBDMggILhDHARCvATIICC4QxwEQrwEyCwguELEDEMcBEK8BOgUIABCRAjoICAAQsQMQgwE6CAguELEDEIMBOgUILhCxAzoFCAAQsQM6AggAOgIILlCrCliNGmD3GmgCcAB4AIABqAKIAeAJkgEDMi01mAEAoAEBqgEHZ3dzLXdpeg&sclient=gws-wiz&ved=0ahUKEwiT5v303ePxAhWTNKYKHTqVAkgQ4dUDCAk&uact=5")
# driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div/div/div/div[1]/a/h3').click()
# time.sleep(5)
# driver.save_screenshot("screen.png")
# driver.get("https://www.reddit.com")
# driver.save_screenshot("reddit.png")


# Does not scrape ALL, some are missing categories
def hyatt_url_scraper():
    """scrapes info from hyatt full hotel list to later generate urls"""
    with open('hyatt_hotel_data.csv', mode='wb') as hyatt_hotel_data, open('hyatt_hotel_key.csv', mode='wb') as hyatt_hotel_key:
        hyatt_writer1 = csv.writer(hyatt_hotel_data, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        hyatt_writer2 = csv.writer(hyatt_hotel_key, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        hyatt_writer1.writerow(["name", "name_enc", "region_code", "link", "category"])
        hyatt_writer2.writerow(["name", "index"])
        category = 1
        while category < 9:
            list_url = 'https://www.hyatt.com/explore-hotels?categories=' + str(category) + '&regionGroup=0-All'
            driver.get(list_url)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div[2]/div[1]/h2')))
            regions = driver.find_elements_by_css_selector(".region-group")
            index = 0
            for region in regions:
                hotels = region.find_elements_by_css_selector(".b-text_copy-3")
                for hotel in hotels:
                    link = hotel.get_attribute('href')
                    # state = link.split('/')[5]
                    name = hotel.get_attribute("innerText")
                    name_enc = urllib.parse.quote(name, safe='')
                    region_code = link.split('/')[7]
                    hyatt_writer1.writerow([name, name_enc, region_code, link, category])
                    hyatt_writer2.writerow([name, index])
                    index += 1
            category += 1


def hyatt_url_reader():
    with open('hyatt_list.csv', encoding='utf-8') as f:
        return([{k: str(v) for k, v in row.items()}
                for row in csv2.DictReader(f, skipinitialspace=True, delimiter=';')])


def date_generator(start_date, end_date):
    """Creates a generator for start and end dates"""
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def hyatt_scrape_v2(hotel_key, start_date, end_date):
    """Opens database, pulls url data from stored dictionary, runs scrape, writes to database"""
    hyatt_list = hyatt_url_reader()
    current_hotel = list(filter(lambda x: x['name'] == hotel_key, hyatt_list))
    print(current_hotel[0]['name_enc'])
    for start in date_generator(start_date, end_date):
        search_url = "https://www.hyatt.com/shop/" + current_hotel[0]['region_code'] + "?location=" + current_hotel[0]['name_enc'] + "&checkinDate=" + str(start) + "&checkoutDate=" + str(start + datetime.timedelta(days=1)) + "&rooms=1&adults=2&kids=0&rate=Standard&rateFilter=woh"
        redirect_url = "https://www.hyatt.com/search/" + current_hotel[0]['name_enc'] + "?rooms=1&adults=2&location=" + current_hotel[0]['name_enc'] + "&checkinDate=" + str(start) + "&kids=0&rate=Standard"
        print(search_url)
        t0 = time.time()
        driver.get(search_url)
        if driver.current_url == redirect_url:  # Redirect case
            print("Booking Unavailable for " + str(start) + " to " + str(start + datetime.timedelta(days=1)))
        else:  # Not Redirected
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[8]/div/div[1]/div/div/div/div[2]/div[1]')))
            try:
                driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div[2]")  # Points not available
                print("Booking Unavailable for " + str(start) + " to " + str(start + datetime.timedelta(days=1)))
            except NoSuchElementException:  # Points available
                print("Booking Available for " + str(start) + " to " + str(start + datetime.timedelta(days=1)))
                time.sleep(3)
                room_types2 = driver.find_elements_by_xpath("//div[contains(@data-js, 'rate-list-container')]")
                res = {}
                for room_type2 in room_types2:
                    time.sleep(1)
                    rooms = room_type2.find_elements_by_xpath(".//div[contains(@class, 'rate-information-container')]")
                    res[room_type2] = rooms
                    for room in rooms:
                        print("Room Type: " + room.find_element_by_xpath(".//div[contains(@data-js, 'room-title')]").get_attribute("innerText"))
                        print("Room Rate: " + room.find_element_by_xpath(".//div[contains(@class, 'rate b-text_weight-bold b-text_display-2')]").get_attribute("innerText"))
                return res
    t1 = time.time()
    print("Time Elapsed: " + str(t1 - t0))

# def hyatt_scrape_v1():
#     for x in my_cal.itermonthdates(2021, 8):
#         # x = datetime.date(2022, 1, 18)
#         print('*' * 30)
#         search_url = url_1 + str(x) + url_2 + str(x + datetime.timedelta(days=1)) + url_3
#         t0 = time.time()
#         driver.get(search_url)
#         time.sleep(2)
#         if driver.current_url == url_redirect_1 + str(x) + url_2 + str(x + datetime.timedelta(days=1)) + url_redirect_3:  # Redirect case
#             print("Booking Unavailable for " + str(x) + " to " + str(x + datetime.timedelta(days=1)))
#         else:  # Not Redirected
#             WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[8]/div/div[1]/div/div/div/div[2]/div[1]')))
#             # time.sleep(1)
#             try:
#                 driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div[2]")  # Points not available
#                 print("Booking Unavailable for " + str(x) + " to " + str(x + datetime.timedelta(days=1)))
#             except NoSuchElementException:  # Points available
#                 print("Booking Available for " + str(x) + " to " + str(x + datetime.timedelta(days=1)))
#                 time.sleep(3)
#                 # ul = driver.find_element_by_tag_name("ul")
#                 # room_types = ul.find_elements_by_tag_name("li")
#                 room_types2 = driver.find_elements_by_xpath("//div[contains(@data-js, 'rate-list-container')]")
#                 # for room_type, room_type2 in zip(room_types, room_types2):
#                 for room_type2 in room_types2:
#                     time.sleep(1)
#                     rooms = room_type2.find_elements_by_xpath(".//div[contains(@class, 'rate-information-container')]")
#                     for room in rooms:
#                         # print("Room: " + room.get_attribute("innerText"))
#                         print("Room Type: " + room.find_element_by_xpath(".//div[contains(@data-js, 'room-title')]").get_attribute("innerText"))
#                         print("Room Rate: " + room.find_element_by_xpath(".//div[contains(@class, 'rate b-text_weight-bold b-text_display-2')]").get_attribute("innerText"))
#         t1 = time.time()
#         print("Time Elapsed: " + str(t1 - t0))


# query = urllib.parse.quote('M/Y Kontiki Wayra', safe='')
# print(query)

hyatt_scrape_v2("Hyatt Place Birmingham/Hoover", datetime.date(2021, 9, 1), datetime.date(2021, 9, 5))

