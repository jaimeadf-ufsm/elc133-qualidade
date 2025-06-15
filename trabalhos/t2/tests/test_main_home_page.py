import pytest
from utilities.settings import Settings
from pages.main_home_page import MainHomePage

@pytest.fixture
def home_page(driver):
    page = MainHomePage(driver)
    page.go_to(f'{Settings.MAIN_BASE_URL}')

    return page

def test_default_language(home_page):
    current_language = home_page.get_current_language()

    assert current_language == 'de'

def test_toggle_language(home_page):
    initial_language = home_page.get_current_language()

    home_page.toggle_language()
    
    new_language = home_page.get_current_language()

    assert new_language != initial_language
    assert new_language in ['de', 'en']
