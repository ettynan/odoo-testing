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
    
def test_create_patient_without_age(driver):
    pass

def test_create_vehicle_without_license(driver):
    pass