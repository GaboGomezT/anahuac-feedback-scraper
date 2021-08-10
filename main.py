import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options


login_url = "https://anahuac.instructure.com/login/canvas"

binary = '/usr/bin/firefox'
options = Options()
options.headless = True
options.binary = binary
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True
print("loading headless driver")
driver = webdriver.Firefox(options=options, capabilities=cap, executable_path="/home/gabo/drivers/geckodriver")

# Start the session
# session = requests.Session()

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

    for hw in assignments:
        attempts = 0
        while attempts < 3:
            try:
                print(hw.get_attribute('href'))
                break
            except Exception as e:
                print(e)
                print("trying again")
            attempts += 1

        # link = hw.get_attribute("href")
        # print(link)
    # # Post the payload to the site to log in
    # s = driver.post(login_url, data=payload)
    # print(s)
    # # Navigate to the next page and scrape the data
    # s = driver.get('https://anahuac.instructure.com/courses/1926/assignments')
    # print(s)

    # driver.quit()
    # soup = BeautifulSoup(s.text, 'html.parser')
    # print(soup)
    # for item in soup.select(".div.collectionViewItems ig-list draggable"):
    #     print(item)
except Exception as e:
    print(e)
    print(driver.page_source)
finally:
    print("exiting browser")
    driver.quit()

