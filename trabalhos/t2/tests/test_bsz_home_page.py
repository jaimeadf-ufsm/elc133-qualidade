import pytest
import time
from utilities.settings import Settings
from pages.bsz_home_page import BSZHomePage

@pytest.fixture
def home_page(driver):
    page = BSZHomePage(driver)
    page.go_to(f'{Settings.BSZ_BASE_URL}')

    return page

def test_current_carousel_dot_accuracy(home_page):
    current_dot = home_page.get_carousel_dot_count()
    
    assert current_dot == 5

def test_carousel_dot_navigation(home_page):
    dot_count = home_page.get_carousel_dot_count()
    
    if dot_count > 1:
        target_dot = 1
        home_page.click_carousel_dot(target_dot)
        
        current_dot = home_page.get_current_carousel_dot()
        assert current_dot == target_dot

def test_next_carousel_button_navigation(home_page):
    dot_count = home_page.get_carousel_dot_count()
    initial_dot = home_page.get_current_carousel_dot()
    
    if dot_count > 1:
        home_page.click_next_carousel_button()
        
        new_dot = home_page.get_current_carousel_dot()
        
        assert new_dot == initial_dot + 1

def test_previous_carousel_button_navigation(home_page):
    dot_count = home_page.get_carousel_dot_count()
    
    if dot_count > 1:
        initial_dot = home_page.get_current_carousel_dot()
        
        home_page.click_next_carousel_button()
        time.sleep(1)
        
        home_page.click_previous_carousel_button()
        time.sleep(1)
        
        new_dot = home_page.get_current_carousel_dot()
        
        assert new_dot == initial_dot

def test_sequential_carousel_navigation(home_page):
    dot_count = home_page.get_carousel_dot_count()
    
    if dot_count >= 3:
        first_dot = home_page.get_current_carousel_dot()
        assert first_dot == 0
        
        home_page.click_next_carousel_button()
        time.sleep(1)
        
        second_dot = home_page.get_current_carousel_dot()
        assert second_dot == 1
        
        home_page.click_next_carousel_button()
        time.sleep(1)

        third_dot = home_page.get_current_carousel_dot()

        assert third_dot == 2

def test_mixed_carousel_navigation(home_page):
    dot_count = home_page.get_carousel_dot_count()
    
    if dot_count >= 3:
        home_page.click_carousel_dot(2)
        time.sleep(1)
        
        assert home_page.get_current_carousel_dot() == 2
        
        home_page.click_previous_carousel_button()
        time.sleep(1)

        assert home_page.get_current_carousel_dot() == 1
        
        home_page.click_next_carousel_button()
        time.sleep(1)

        assert home_page.get_current_carousel_dot() == 2

def test_carousel_content_changes_on_navigation(home_page):
    dot_count = home_page.get_carousel_dot_count()
    
    if dot_count > 1:
        initial_content = home_page.get_current_carousel_content()
        
        home_page.click_next_carousel_button()
        
        new_content = home_page.get_current_carousel_content()
        
        assert initial_content != new_content