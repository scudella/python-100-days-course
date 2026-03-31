from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

zillow_clone_url = "https://appbrewery.github.io/Zillow-Clone/"
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe-wzRCJAawdKH2zJox4KEyDnRI3oR5IZfHW7RIGAoGlb3veg/viewform"

response = requests.get(zillow_clone_url)
zillow_webpage = response.text

soup = BeautifulSoup(zillow_webpage, "html.parser")

cards = soup.find_all(name="div", class_="StyledCard-c11n-8-84")

links = []
prices = []
addresses = []
for card in cards:
    link = card.find(name="a", class_="StyledPropertyCardDataArea-anchor")
    links.append(link["href"])
    price = card.find(name="span", class_="PropertyCardWrapper__StyledPriceLine")
    price_value = price.get_text().split('/', 1)[0].split('+', 1)[0]
    prices.append(price_value)
    address = card.find(name="address").get_text().strip()
    if "|" in address:
        address = address.split("|", 1)[1]
    addresses.append(address)

# print(cards[0])
print(links)
print(prices)
print(addresses)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

for listing in range(len(links)):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(form_url)

    time.sleep(random.uniform(2, 5))

    inputs = driver.find_elements(By.CSS_SELECTOR, value="input")

    text_input = []
    for input in inputs:
        if input.get_attribute("type") == "text":
            text_input.append(input)

    text_input[0].send_keys(addresses[listing].strip())
    text_input[1].send_keys(prices[listing])
    text_input[2].send_keys(links[listing])

    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    time.sleep(random.uniform(2, 5))
    driver.close()



