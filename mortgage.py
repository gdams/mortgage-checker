import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

webhook_url = os.environ['SLACK_WEBHOOK_URL']

purchase_price = os.environ['PURCHASE_PRICE']
deposit = os.environ['DOWN_PAYMENT']

def send_to_slack(message):
    payload = {
        'text': message,
        'username': 'MortgageScraper',
        'icon_emoji': ':robot_face:'
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Request to slack returned an error {response.status_code}, the response is:\n{response.text}")

# Initialize the driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get("https://mortgages.secure.halifax-online.co.uk/homes/?action=mortgage_calculator&type=hmv")

driver.set_window_size(2048, 1024)

wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".sc-hknOHE:nth-child(1) div")))
driver.find_element(By.CSS_SELECTOR, ".sc-hknOHE:nth-child(1) div").click()
driver.find_element(By.CSS_SELECTOR, ".IntentQuestionnairestyled__StyledButton-sc-1psifir-4").click()
driver.find_element(By.CSS_SELECTOR, ".sc-hknOHE:nth-child(2) .sc-aXZVg").click()
driver.find_element(By.CSS_SELECTOR, ".IntentQuestionnairestyled__StyledButton-sc-1psifir-4 > .sc-gEvEer").click()
driver.find_element(By.CSS_SELECTOR, ".sc-hknOHE:nth-child(4) div").click()
driver.find_element(By.CSS_SELECTOR, ".IntentQuestionnairestyled__StyledButton-sc-1psifir-4 > .sc-gEvEer").click()
driver.find_element(By.CSS_SELECTOR, ".sc-hknOHE:nth-child(2) > .sc-uVWWZ").click()
driver.find_element(By.CSS_SELECTOR, ".IntentQuestionnairestyled__StyledButton-sc-1psifir-4 > .sc-gEvEer").click()
driver.find_element(By.CSS_SELECTOR, ".sc-hknOHE:nth-child(2) > .sc-uVWWZ").click()
driver.find_element(By.CSS_SELECTOR, ".IntentQuestionnairestyled__StyledButton-sc-1psifir-4 > .sc-gEvEer").click()
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, ".sc-kbousE:nth-child(4) .sc-gEvEer > .sc-gEvEer:nth-child(1)").click()
driver.find_element(By.CSS_SELECTOR, ".iXlUzX > .sc-gEvEer").click()
# wait until the element is clickable
wait.until(expected_conditions.element_to_be_clickable((By.ID, "rateCheckerPropertyPrice")))
driver.find_element(By.ID, "rateCheckerPropertyPrice").click()
driver.find_element(By.ID, "rateCheckerPropertyPrice").send_keys(purchase_price)
# wait for element to exist
driver.find_element(By.CSS_SELECTOR, ".iXlUzX").click()
wait.until(expected_conditions.element_to_be_clickable((By.ID, "rateCheckerDeposit")))
driver.find_element(By.ID, "rateCheckerDeposit").click()
driver.find_element(By.ID, "rateCheckerDeposit").send_keys(deposit)
driver.find_element(By.CSS_SELECTOR, ".iXlUzX").click()
driver.find_element(By.CSS_SELECTOR, ".iXlUzX").click()
time.sleep(3)
driver.find_element(By.CSS_SELECTOR, ".iXlUzX").click()
time.sleep(5)
# scroll to bottom of page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.find_element(By.CSS_SELECTOR, ".knbxcb > .sc-gEvEer").click()

time.sleep(5)
# Find all rate card elements on the page.
rate_cards = driver.find_elements(By.XPATH, "//div[@data-qa-id='rate-card']")

# Loop through the rate cards to find the one with "5 Year Fixed Rate" and product fee of £999.
for card in rate_cards:
    term = card.find_element(By.XPATH, ".//span[@data-qa-id='rate-card-fixed-term']").text
    product_fee_element = card.find_element(By.XPATH, ".//p[@data-qa-id='rate-card-product-fee-value']")
    
    if "5 Year Fixed Rate" in term and product_fee_element.text == "£999":
        interest_rate_element = card.find_element(By.XPATH, ".//p[@data-qa-id='rate-card-initial-rate-value']")
        interest_rate = interest_rate_element.text
        print(interest_rate)
        send_to_slack(f"The 5 Year Fixed Rate with £999 product fee is: {interest_rate}")
        break

# Close the browser window
driver.quit()
