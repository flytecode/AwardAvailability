import calendar
import datetime
import requests
import html
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, UnexpectedAlertPresentException, \
    NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc


global driver
driver = uc.Chrome()
my_cal = calendar.Calendar()
url_1 = "https://www.hyatt.com/shop/sjcal?location=Ventana%20Big%20Sur%20an%20Alila%20Resort&checkinDate="
url_2 = "&checkoutDate="
url_3 = "&rooms=1&adults=2&kids=0&rate=Standard&rateFilter=woh"
url_redirect_1 = "https://www.hyatt.com/search/Ventana%20Big%20Sur%20an%20Alila%20Resort?rooms=1&adults=2&location=Ventana%20Big%20Sur%20an%20Alila%20Resort&checkinDate="
url_redirect_3 = "&kids=0&rate=Standard"

# search_url = url_1 + str(datetime.date(2022, 1, 18)) + url_2 + str(datetime.date(2022, 1, 18) + datetime.timedelta(days=1)) + url_3
# driver.get("https://www.google.com/search?q=hyatt&sxsrf=ALeKk03O34lXswsMn-eupsoFP3LyBPJRGw%3A1626305986570&source=hp&ei=wnXvYJP9H5PpmAW6qorABA&iflsig=AINFCbYAAAAAYO-D0ogVsJr5JBrPcPuVAVG0zVuKWeZI&oq=hyatt&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgjECcyBAgjECcyBwgAELEDEEMyBAgAEEMyCwguELEDEMcBEKMCMgcILhCxAxBDMggILhDHARCvATIICC4QxwEQrwEyCwguELEDEMcBEK8BOgUIABCRAjoICAAQsQMQgwE6CAguELEDEIMBOgUILhCxAzoFCAAQsQM6AggAOgIILlCrCliNGmD3GmgCcAB4AIABqAKIAeAJkgEDMi01mAEAoAEBqgEHZ3dzLXdpeg&sclient=gws-wiz&ved=0ahUKEwiT5v303ePxAhWTNKYKHTqVAkgQ4dUDCAk&uact=5")
# driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div/div/div/div[1]/a/h3').click()
# time.sleep(5)
# driver.save_screenshot("screen.png")
# driver.get("https://www.reddit.com")
# driver.save_screenshot("reddit.png")


def ventana_scrape():
    for x in my_cal.itermonthdates(2021, 8):
        # x = datetime.date(2022, 1, 18)
        print('*' * 30)
        search_url = url_1 + str(x) + url_2 + str(x + datetime.timedelta(days=1)) + url_3
        t0 = time.time()
        driver.get(search_url)
        time.sleep(2)
        if driver.current_url == url_redirect_1 + str(x) + url_2 + str(x + datetime.timedelta(days=1)) + url_redirect_3:  # Redirect case
            print("Booking Unavailable for " + str(x) + " to " + str(x + datetime.timedelta(days=1)))
        else:  # Not Redirected
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[8]/div/div[1]/div/div/div/div[2]/div[1]')))
            # time.sleep(1)
            try:
                driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div[2]")  # Points not available
                print("Booking Unavailable for " + str(x) + " to " + str(x + datetime.timedelta(days=1)))
            except NoSuchElementException:  # Points available
                print("Booking Available for " + str(x) + " to " + str(x + datetime.timedelta(days=1)))
                time.sleep(3)
                # ul = driver.find_element_by_tag_name("ul")
                # room_types = ul.find_elements_by_tag_name("li")
                room_types2 = driver.find_elements_by_xpath("//div[contains(@data-js, 'rate-list-container')]")
                # for room_type, room_type2 in zip(room_types, room_types2):
                for room_type2 in room_types2:
                    time.sleep(1)
                    rooms = room_type2.find_elements_by_xpath(".//div[contains(@class, 'rate-information-container')]")
                    for room in rooms:
                        # print("Room: " + room.get_attribute("innerText"))
                        print("Room Type: " + room.find_element_by_xpath(".//div[contains(@data-js, 'room-title')]").get_attribute("innerText"))
                        print("Room Rate: " + room.find_element_by_xpath(".//div[contains(@class, 'rate b-text_weight-bold b-text_display-2')]").get_attribute("innerText"))
        t1 = time.time()
        print("Time Elapsed: " + str(t1 - t0))


ventana_scrape()
