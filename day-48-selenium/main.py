from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.amazon.com/Owala-FreeSip-Insulated-Stainless-BPA-Free/dp/B0BZYCJK89/?_encoding=UTF8&pd_rd_w=2aoWJ&content-id=amzn1.sym.f2128ffe-3407-4a64-95b5-696504f68ca1&pf_rd_p=f2128ffe-3407-4a64-95b5-696504f68ca1&pf_rd_r=5829RVSX58HRZJE4TV6N&pd_rd_wg=ZKt0O&pd_rd_r=88b88a70-b021-4200-9e3b-65125940f474&ref_=pd_hp_d_btf_crs_zg_bs_284507&th=1")

price_dollar = driver.find_element(By.CLASS_NAME, value="a-price-whole")
price_cents = driver.find_element(By.CLASS_NAME, value="a-price-fraction")

print(f"The price is {price_dollar.text}.{price_cents.text}")

driver.get("https://www.python.org")
search_bar = driver.find_element(By.NAME, value='q')
print(search_bar.get_attribute("placeholder"))

button = driver.find_element(By.ID, value="submit")
print(button.size)

documentation_link = driver.find_element(By.CSS_SELECTOR, value=".documentation-widget a")
print(documentation_link.text)

bug_link = driver.find_element(By.XPATH, value='//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
print(bug_link.text)

event_times = driver.find_elements(By.CSS_SELECTOR, value='.event-widget time')
event_names = driver.find_elements(By.CSS_SELECTOR, value='.event-widget li a')
events = {}

for n in range(len(event_times)):
    events[n] = {
        "time:": event_times[n].get_attribute("datetime")[:10],
        "name": event_names[n].text,
    }

print(events)

driver.close()
# driver.quit()