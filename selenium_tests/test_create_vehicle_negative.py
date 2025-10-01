# test_create_vehicle_negative.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ----------------------------
# Config
# ----------------------------
ODOO_URL = "http://146.190.122.200:8069/web/login?db=testdb"
USERNAME = "user1@yahoo.com"
PASSWORD = "user1"

# ----------------------------
# Fixture
# ----------------------------
@pytest.fixture
def driver():
    """Setup Chrome in headless mode and close afterwards."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

# ----------------------------
# Test: Negative Vehicle Creation (missing license plate)
# ----------------------------
def test_create_vehicle_negative(driver):
    # Step 1. Login
    driver.get(ODOO_URL)
    driver.find_element(By.NAME, "login").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.RETURN)
    driver.implicitly_wait(5)

    # Step 2. Navigate to Vehicles page (kanban)
    driver.get("http://146.190.122.200:8069/web#cids=1&menu_id=285&action=128&model=fleet.vehicle&view_type=kanban")
    driver.implicitly_wait(5)

    # Step 3. Click Create
    create_btn = driver.find_element(By.XPATH, "//button[contains(@class,'o-kanban-button-new')]")
    create_btn.click()
    driver.implicitly_wait(5)

    # Step 4. Select a model (choose the 2nd option, e.g., Audi/A1)
    model_dropdown = driver.find_element(By.NAME, "model_id")
    model_dropdown.click()
    driver.implicitly_wait(2)

    options = driver.find_elements(By.XPATH, "//ul[contains(@class,'ui-autocomplete')]/li")
    assert len(options) > 1, "No model options available"
    options[1].click()  # safely click 2nd option

    # Step 5. Leave license plate empty and save
    save_btn = driver.find_element(By.XPATH, "//button[contains(@class,'o_form_button_save')]")
    save_btn.click()
    driver.implicitly_wait(5)

    # Step 6. Capture error notification
    error_box = driver.find_element(By.CLASS_NAME, "o_notification_manager")
    error_text = error_box.text

    assert "License Plate" in error_text or "Invalid fields" in error_text, f"Unexpected error: {error_text}"
