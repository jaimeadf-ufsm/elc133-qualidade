import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def driver():
    service = ChromeService(ChromeDriverManager().install())

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(10)

    yield driver

    driver.quit()