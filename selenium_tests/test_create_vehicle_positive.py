import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Replace with your Odoo server info
ODOO_URL = "http://146.190.122.200:8069/web/login?db=testdb"
KANBAN_URL = "http://146.190.122.200:8069/web?debug=assets#cids=1&menu_id=97&action=128&model=fleet.vehicle&view_type=kanban"
USERNAME = "user1@yahoo.com"   # <-- replace with User1's actual login
PASSWORD = "user1"        # <-- replace with User1's actual password


@pytest.fixture
def driver():
    """Setup Chrome in headless mode."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    yield driver
    driver.quit()
    
# ----------------------------
# Test: Create Vehicle with License Plate
# ----------------------------
def test_create_vehicle_positive(driver):
    # Step 1: Login
    driver.get(ODOO_URL)
    driver.find_element(By.NAME, "login").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.RETURN)
    driver.implicitly_wait(5)

    # Step 2: Navigate to Vehicles page
    driver.get(KANBAN_URL)
    driver.implicitly_wait(5)

    # Step 3: Click "Create"
    create_btn = driver.find_element(By.XPATH, "//button[contains(@class,'o-kanban-button-new')]")
    create_btn.click()
    # Give Odoo a small real pause to load the inline form
    time.sleep(2)

    # Step 4: Fill License Plate
    license_input = driver.find_element(By.NAME, "license_plate")
    license_input.clear()
    license_input.send_keys("TEST-PLATE-123")
    driver.implicitly_wait(2)

    # Step 5: Select model (second option, Audi/A1)
    model_dropdown = driver.find_element(By.NAME, "model_id")
    model_dropdown.click()
    driver.implicitly_wait(2)
    options = driver.find_elements(By.XPATH, "//li[contains(@class,'ui-menu-item')]")
    options[1].click()   # Audi/A1 in your setup
    driver.implicitly_wait(2)

    # Step 6: Save
    save_btn = driver.find_element(By.XPATH, "//button[contains(@class,'o_form_button_save')]")
    save_btn.click()
    driver.implicitly_wait(5)

    # Step 7: Return to kanban view directly
    driver.get(KANBAN_URL)
    driver.implicitly_wait(5)

    # Step 8: Verify vehicle appears in kanban
    time.sleep(5)  # give Odoo time to load the kanban cards
    kanban_cards = driver.find_elements(By.XPATH, "//div[contains(@class,'o_kanban_record')]")

    assert any("TEST-PLATE-123" in card.text for card in kanban_cards), \
        "Vehicle not found in Fleet list view after creation"