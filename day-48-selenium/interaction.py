from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://en.wikipedia.org/wiki/Main_Page")

article_count = driver.find_elements(By.CSS_SELECTOR, value="#articlecount ul li a")
print(article_count[1].text)
# article_count[1].click()

all_portals = driver.find_element(By.LINK_TEXT, value="Content portals")
# all_portals.click()

search = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, "search"))
)
search.send_keys("Python", Keys.ENTER)

# driver.close()