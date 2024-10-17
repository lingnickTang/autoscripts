import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_browser(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (optional)
    # Initialize the WebDriver
    service = Service(executable_path=r"./chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    is_loging = wait.until(EC.url_changes(url))
    return driver
    

def request_and_click_button(url, button_selector):
    # Make the initial request
    response = requests.get(url)
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (optional)
    
    # Initialize the WebDriver
    service = Service(executable_path=r"./chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Load the page content into the driver
        driver.get("data:text/html;charset=utf-8," + response.text)
        
        print(driver.page_source)
        # Wait for the button to be clickable
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
        )
        
        # Click the button
        button.click()

        # Wait for any changes after clicking (you might need to adjust this)
        WebDriverWait(driver, 10).until(
            EC.staleness_of(button)
        )
        
        # Get the new page source
        new_page_source = driver.page_source
        
        return new_page_source
    finally:
        driver.quit()

# Example usage
url = "https://main.m.taobao.com/order/index.html?skuId=5320306445942&quantity=1&itemId=714273870642"
driver = open_browser(url)
# button_selector = "button[aria-label='提交订单']"
# new_page_content = request_and_click_button(url, button_selector)
# print(new_page_content)
