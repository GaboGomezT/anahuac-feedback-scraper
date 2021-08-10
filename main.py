import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

login_url = "https://anahuac.instructure.com/login/canvas"

binary = '/usr/bin/firefox'
options = Options()
options.headless = True
options.binary = binary
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True
print("loading headless driver")
driver = webdriver.Firefox(options=options, capabilities=cap, executable_path="/home/gabo/drivers/geckodriver")

# Getting the token
result = driver.get(login_url)
authenticity_token = driver.find_element_by_name("authenticity_token").get_attribute("value")
print("got auth token")
# Create the payload
payload = {'pseudonym_session[unique_id]':'', 
          'pseudonym_session[password]':'',
          "authenticity_token": authenticity_token
          }
print("sending id")
driver.find_element_by_name("pseudonym_session[unique_id]").send_keys(payload["pseudonym_session[unique_id]"])
print("sending password")
driver.find_element_by_name("pseudonym_session[password]").send_keys(payload["pseudonym_session[password]"])
print("clicking login button")
driver.find_element_by_class_name("Button--login").click()
try:
    # print("waiting for page load")
    WebDriverWait(driver, 10).until(EC.title_contains("Tablero"))
    print("Going to assignments page")
    driver.get("https://anahuac.instructure.com/courses/1926/assignments")
    print("waiting for page to load")
    time.sleep(10)
    assignments = driver.find_elements_by_class_name("ig-title")
    links = dict()
    for hw in assignments:
        attempts = 0
        while attempts < 3:
            try:
                link = hw.get_attribute("href")
                name = hw.text
                links[name] = link
                break
            except Exception as e:
                print(e)
                print("trying again")
            attempts += 1
    src_links = dict()
    for name, link in links.items():
        try:
            print(name, link)
            driver.get(link)
            turn_in_link = driver.find_element_by_css_selector("div.content > div > a").get_attribute("href")
            print("going to submission page")
            driver.get(turn_in_link)
            time.sleep(5)
            print("clicking video button")
            driver.find_element_by_class_name("play_comment_link").click()
            time.sleep(5)
            print("getting video source")
            # print(driver.page_source)
            source_link = driver.find_elements_by_css_selector("div.me-cannotplay > a")[0].get_attribute("href")
            src_links[name] = source_link
        except NoSuchElementException:
            print("this assignment has no feedback, continuing")
        except ElementNotInteractableException:
            print("this assignment has no feedback, continuing")
except Exception as e:
    print(e)
    # print(driver.page_source)
finally:
    print("exiting browser")
    driver.quit()

print("*"*100)
print(src_links)
for name,url in src_links.items():
    r = requests.get(url, allow_redirects=True)

    open(f"retro/{name}.mp4", 'wb').write(r.content)