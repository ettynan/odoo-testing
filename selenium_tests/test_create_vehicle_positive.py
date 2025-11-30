import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Replace with your Odoo server info
ODOO_URL = "http://146.190.122.200:8069/web/login?db=testdb"
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
    driver.get("http://146.190.122.200:8069/web#cids=1&menu_id=285&action=128&model=fleet.vehicle&view_type=kanban")
    driver.implicitly_wait(5)

    # Step 3: Click "Create"
    create_btn = driver.find_element(By.XPATH, "//button[contains(@class,'o-kanban-button-new')]")
    create_btn.click()
    # Give Odoo a small real pause to load the inline form
    time.sleep(2)
    driver.implicitly_wait(5)

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

    # Step 7: Verify saved License Plate
    saved_plate = driver.find_element(By.NAME, "license_plate").get_attribute("value")
    assert saved_plate == "TEST-PLATE-123", f"Expected 'TEST-PLATE-123', got {saved_plate}"