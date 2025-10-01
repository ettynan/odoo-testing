import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Replace with your Odoo server info
ODOO_URL = "http://146.190.122.200:8069/web/login?db=testdb"
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

def test_create_vehicle(driver):
    pass