from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

Forms = "https://docs.google.com/forms/d/e/1FAIpQLScqsQGtInt6BdPDZ4sHve3uTF7IpD-4kHNsTO2YZE5D2NbTgg/viewform?usp=dialog"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=header)

home_renting_web_page = response.text
soup = BeautifulSoup(home_renting_web_page, 'html.parser')
#making a list of all links of the houses
all_link_elements = soup.select(".StyledPropertyCardPhotoBody a")
all_links = [link["href"] for link in all_link_elements]
print(f"There are {len(all_links)} links to individual listings in total: \n")
print(all_links)
#making a list of all house prices
all_price_elements = soup.select(".PropertyCardWrapper span")
all_price = [price.get_text().replace("/mo", "").split("+")[0] for price in all_price_elements]
print(all_price)
#making a list of the house address
all_house_address = soup.select(".StyledPropertyCardDataWrapper address")
all_address = [address.get_text().replace(" | ", " ").strip() for address in all_house_address]
print(all_address)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(all_links)):
    driver.get(Forms)
    time.sleep(2)
    # Use the xpath to select the "short answer" fields in your Google Form.
    # Note, your xpath might be different if you created a different form.
    address = driver.find_element(by=By.XPATH,
                                  value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH,
                                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH,
                               value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(by=By.XPATH,
                                        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address.send_keys(all_address[n])
    price.send_keys(all_price[n])
    link.send_keys(all_links[n])
    submit_button.click()