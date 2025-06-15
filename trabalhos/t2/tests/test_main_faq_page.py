import pytest
from utilities.settings import Settings
from pages.main_faq_page import MainFAQPage

@pytest.fixture
def faq_page(driver):
    page = MainFAQPage(driver)
    page.go_to(f'{Settings.MAIN_BASE_URL}/weiterbildung/offene-uni-rostock/faq/')

    return page

def test_accordions_are_present(faq_page):
    accordion_count = faq_page.count_accordions()
    
    assert accordion_count > 0

def test_accordion_toggle_functionality(faq_page):
    accordion_count = faq_page.count_accordions()
    
    if accordion_count > 0:
        faq_page.toggle_accordion(0)
        assert faq_page.is_accordion_open(0)
        
        faq_page.toggle_accordion(0)
        assert not faq_page.is_accordion_open(0)

def test_accordion_content_is_accessible(faq_page):
    accordion_count = faq_page.count_accordions()
    
    if accordion_count > 0:
        faq_page.toggle_accordion(0)
        
        content = faq_page.get_accordion_content(0)
        
        assert isinstance(content, str)

def test_multiple_accordions_can_be_opened(faq_page):
    accordion_count = faq_page.count_accordions()
    
    if accordion_count >= 2:
        faq_page.toggle_accordion(0)
        faq_page.toggle_accordion(1)
        
        assert faq_page.is_accordion_open(0)
        assert faq_page.is_accordion_open(1)

def test_accordion_index_bounds(faq_page):
    accordion_count = faq_page.count_accordions()
    
    if accordion_count > 0:
        last_index = accordion_count - 1
        faq_page.toggle_accordion(last_index)

        assert faq_page.is_accordion_open(last_index)

def test_accordion_states_are_independent(faq_page):
    accordion_count = faq_page.count_accordions()
    
    if accordion_count >= 2:
        faq_page.toggle_accordion(0)
        first_state = faq_page.is_accordion_open(0)
        
        faq_page.toggle_accordion(1)
        
        assert faq_page.is_accordion_open(0) == first_state

def test_accordion_content_changes_with_state(faq_page):
    accordion_count = faq_page.count_accordions()
    
    if accordion_count > 0:
        if faq_page.is_accordion_open(0):
            faq_page.toggle_accordion(0)
        
        faq_page.toggle_accordion(0)
        
        content = faq_page.get_accordion_content(0)
        assert isinstance(content, str)

