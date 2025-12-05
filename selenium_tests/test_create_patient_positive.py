import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Replace with your Odoo server info
ODOO_URL = "http://146.190.122.200:8069/web/login?db=testdb"
PATIENT_LIST_URL = "http://146.190.122.200:8069/web#cids=1&menu_id=285&action=395&model=hospital.patient&view_type=list"
USERNAME = "user1@yahoo.com"   # <-- use User1's actual login
PASSWORD = "user1"        # <-- use User1's actual password


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
# Test: Create Patient with Age
# ----------------------------
def test_create_patient_with_age(driver):
    # Step 1: Login first
    driver.get(ODOO_URL)
    driver.find_element(By.NAME, "login").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.RETURN)
    driver.implicitly_wait(5)
    
     # Step 2. Navigate to Patients list page
    driver.get("http://146.190.122.200:8069/web#menu_id=285&action=395&model=hospital.patient&view_type=list")
    driver.implicitly_wait(5)
    
    # Step 3. Click the "Create" button
    create_btn = driver.find_element(By.XPATH, "//button[contains(@class,'o_list_button_add')]")
    create_btn.click()
    time.sleep(2)
    # driver.implicitly_wait(5)
    
    # Step 4. Fill in patient form
    name_input = driver.find_element(By.NAME, "name")
    name_input.send_keys("Selenium Test Patient")

    age_input = driver.find_element(By.NAME, "age")
    age_input.clear()
    age_input.send_keys("45")

    # Step 5. Save the record
    save_btn = driver.find_element(By.XPATH, "//button[contains(@class,'o_form_button_save')]")
    save_btn.click()
    # driver.implicitly_wait(5)
    
    # Step 6: Wait for check for a page title or breadcrumb update

    max_attempts = 20
    for attempt in range(max_attempts):
        title_text = driver.title
        breadcrumb_texts = [el.text for el in driver.find_elements(By.XPATH, "//ol[contains(@class,'breadcrumb')]//span")]
        if any("Selenium" in b for b in breadcrumb_texts) or "Selenium" in title_text:
            break  # record view has loaded after save
        time.sleep(0.5)
    else:
        raise AssertionError("Save confirmation not detected — page title or breadcrumb never updated")

    # Step 7: Go back to Patients list (same as clicking breadcrumb manually)
    driver.get(PATIENT_LIST_URL)

    # Wait until table rows load
    for attempt in range(max_attempts):
        rows = driver.find_elements(By.XPATH, "//table//tr[td]")
        if rows:
            break
        time.sleep(0.5)

    # Step 8: Locate the row containing both name and age
    rows = driver.find_elements(By.XPATH, "//table//tr[td]")
    saved_name = None
    saved_age = None

    for row in rows:
        if "Selenium" in row.text and "45" in row.text:
            saved_name = "Selenium Test Patient"
            saved_age = "45"
            break

    assert saved_name == "Selenium Test Patient", f"Expected 'Selenium Test Patient', got {saved_name}"
    assert saved_age == "45", f"Expected age '45', got {saved_age}"
