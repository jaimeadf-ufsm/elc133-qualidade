import pytest
from utilities.settings import Settings
from pages.main_login_page import MainLoginPage

@pytest.fixture
def login_page(driver):
    page = MainLoginPage(driver)
    page.go_to(f'{Settings.MAIN_BASE_URL}/login')

    return page

def test_invalid_login(login_page):
    login_page.fill_username('invalid_user')
    login_page.fill_password('invalid_pass')
    login_page.submit()

    assert login_page.is_displaying_error_message()
