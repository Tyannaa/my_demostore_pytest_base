from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.HomePage import HomePage

import os

os.environ['BASE_URL'] = 'http://dev.bootcamp.store.supersqa.com/'

driver_service = Service(executable_path="/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=driver_service)
driver.implicitly_wait(20)

homepage = HomePage(driver)
homepage.go_to_home_page()
homepage.click_first_add_to_cart_button()

cartpage = CartPage(driver)
cartpage.go_to_cart_page()
cartpage.apply_coupon("EXP20231031")

# Update the error message locator here
error_message_locator = (By.XPATH, '//ul[@class="woocommerce-error"]/li[contains(text(), "This coupon has expired.")]')

WebDriverWait(driver, 20).until(EC.visibility_of_element_located(error_message_locator))

error_message_element = driver.find_element(*error_message_locator)
displayed_message = error_message_element.text

if displayed_message == "This coupon has expired.":
    print("Successful")
else:
    print("Coupon validation failed")

driver.quit()
