import pytest
from utilities.settings import Settings
from pages.main_news_page import MainNewsPage

@pytest.fixture
def news_page(driver):
    page = MainNewsPage(driver)
    page.go_to(f'{Settings.MAIN_BASE_URL}/universitaet/kommunikation-und-aktuelles/medieninformationen')

    return page

def test_pagination_accuracy(news_page):
    current_page = news_page.get_current_page()

    assert current_page.isdigit()
    assert current_page == '1'

def test_next_page_navigation(news_page):
    initial_number = news_page.get_current_page()

    news_page.click_next_page()
    
    new_number = news_page.get_current_page()

    assert int(new_number) == int(initial_number) + 1

def test_previous_page_navigation(news_page):
    news_page.click_next_page()

    initial_number = news_page.get_current_page()

    news_page.click_previous_page()

    new_number = news_page.get_current_page()
    
    assert int(new_number) == int(initial_number) - 1

def test_page_number_navigation(news_page):
    target_number = '3'

    news_page.click_numbered_page(target_number)
    
    current_number = news_page.get_current_page()

    assert current_number == target_number

def test_sequential_page_navigation(news_page):
    first_number = news_page.get_current_page()
    assert first_number == '1'
    
    news_page.click_next_page()
    second_number = news_page.get_current_page()
    assert second_number == '2'
    
    news_page.click_next_page()
    third_number = news_page.get_current_page()
    assert third_number == '3'

def test_mixed_page_navigation(news_page):
    news_page.click_numbered_page('4')
    assert news_page.get_current_page() == '4'
    
    news_page.click_previous_page()
    assert news_page.get_current_page() == '3'
    
    news_page.click_next_page()
    assert news_page.get_current_page() == '4'

