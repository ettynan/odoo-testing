import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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


def test_login_to_odoo(driver):
    # Step 1. Open login page
    driver.get(ODOO_URL)

    # Step 2. Enter username
    login_field = driver.find_element(By.NAME, "login")
    login_field.send_keys(USERNAME)

    # Step 3. Enter password
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    # Step 4. Wait for redirect and check the landing page
    driver.implicitly_wait(5)

    # Confirm we landed inside Odoo (not back on login)
    assert "/web" in driver.current_url, f"Expected to be inside Odoo, got {driver.current_url}"

    # Confirm Discuss is accessible
    assert "Discuss" in driver.title or "Odoo" in driver.title, f"Unexpected page title: {driver.title}"

    # Extra: verify we see Discuss in the page title or URL
    print("DEBUG URL:", driver.current_url)
    print("DEBUG TITLE:", driver.title)

    assert "web" in driver.current_url, f"Expected to be inside Odoo, got {driver.current_url}"
    assert "Discuss" in driver.page_source, "Discuss not found in page source — login may have failed"

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
    driver.implicitly_wait(5)
    
    # Step 4. Fill in patient form
    name_input = driver.find_element(By.NAME, "name")
    name_input.send_keys("Selenium Test Patient")

    age_input = driver.find_element(By.NAME, "age")
    age_input.clear()
    age_input.send_keys("45")

    # Step 5. Save the record
    save_btn = driver.find_element(By.XPATH, "//button[contains(@class,'o_form_button_save')]")
    save_btn.click()
    driver.implicitly_wait(5)
    
    # Step 6. Verify patient was saved
    saved_name = driver.find_element(By.NAME, "name").get_attribute("value")
    saved_age = driver.find_element(By.NAME, "age").get_attribute("value")

    assert saved_name == "Selenium Test Patient", f"Expected 'Selenium Test Patient', got {saved_name}"
    assert saved_age == "45", f"Expected age '45', got {saved_age}"

    print("✅ test_create_patient passed")

def test_create_vehicle(driver):
    pass