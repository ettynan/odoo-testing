import pytest
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
    
def test_create_patient_without_age(driver):
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
    
    # Step 4. Fill only the name and gender, leave age blank
    name_input = driver.find_element(By.NAME, "name")
    name_input.send_keys("Negative Test Patient")
    
    gender_select = driver.find_element(By.NAME, "gender")
    gender_select.send_keys("Female")

    # Step 5. Attempt to save without age
    save_btn = driver.find_element(By.XPATH, "//button[contains(@class,'o_form_button_save')]")
    save_btn.click()
    driver.implicitly_wait(5)
    
    # Step 6. Verify error is shown (Odoo will display a red validation error bar)
    error_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-header .modal-title"))
    ).text

    assert "validation error" in error_title.lower(), \
        f"Expected Validation Error, got {error_title}"
    
def test_create_vehicle_without_license(driver):
    pass