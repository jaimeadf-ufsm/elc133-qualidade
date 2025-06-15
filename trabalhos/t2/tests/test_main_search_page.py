import pytest
import time
from utilities.settings import Settings
from pages.main_search_page import MainSearchPage

@pytest.fixture
def search_page(driver):
    page = MainSearchPage(driver)
    page.go_to(f'{Settings.MAIN_BASE_URL}/suche')
    return page

def test_search_submission_with_results(search_page):
    search_page.fill_term('k')
    search_page.submit()
    
    pagination_result = search_page.get_result_summary()

    assert pagination_result.total > 0
    assert pagination_result.page_start >= 1
    assert pagination_result.page_end >= pagination_result.page_start

def test_search_submission_with_no_results(search_page):
    search_page.fill_term('extremely_unlikely_term_that_should_yield_no_results')
    search_page.submit()
    
    pagination_result = search_page.get_result_summary()

    assert pagination_result.total == 0
    assert pagination_result.page_start == 0
    assert pagination_result.page_end == 0

def test_search_reset_functionality(search_page):
    search_page.fill_term('test query')
    search_page.submit()

    search_page.reset()

    result = search_page.get_result_summary()
    
    assert result.total == 0

def test_filter_accordion_toggle_functionality(search_page):
    search_page.fill_term('k')
    search_page.submit()
    
    search_page.toggle_filter_accordion()
    assert search_page.is_filter_accordion_open()
    
    search_page.toggle_filter_accordion()
    assert not search_page.is_filter_accordion_open()

def test_search_submission_with_filters(search_page):
    search_page.fill_term('k')
    search_page.submit()

    time.sleep(1) 
    
    if not search_page.is_filter_accordion_open():
        search_page.toggle_filter_accordion()

    available_filters = search_page.get_available_filter_names()
    initial_result = search_page.get_result_summary()

    disabled_filters = map(lambda x: not search_page.is_filter_enabled(x), available_filters)

    if len(available_filters) >= 2 and any(disabled_filters):
        search_page.toggle_filter(available_filters[0])
        time.sleep(5) 
        
        current_result = search_page.get_result_summary()

        assert current_result.total < initial_result.total

def test_pagination_accuracy(search_page):
    search_page.fill_term('k')
    search_page.submit()
    
    current_page = search_page.get_current_page_number()

    assert current_page == 1

def test_next_page_navigation(search_page):
    search_page.fill_term('k')
    search_page.submit()

    result = search_page.get_result_summary()
    
    if result.page_end > result.total:
        initial_page_number = search_page.get_current_page_number()
        
        search_page.click_next_page()
        
        current_page_number = search_page.get_current_page_number()

        assert current_page_number == initial_page_number + 1

def test_previous_page_navigation(search_page):
    search_page.fill_term('k')
    search_page.submit()

    result = search_page.get_result_summary()
    
    if result.page_end > result.total:
        initial_page_number = search_page.get_current_page_number()
    
        search_page.click_next_page()
        search_page.click_previous_page()
        
        current_page_number = search_page.get_current_page_number()

        assert current_page_number == initial_page_number

def test_page_number_navigation(search_page):
    search_page.fill_term('k')
    search_page.submit()
    
    available_pages_numbers = search_page.get_available_page_numbers()
    
    if len(available_pages_numbers) > 1:
        target_page_number = available_pages_numbers[-1]
        
        search_page.click_page_number(target_page_number)
        
        current_page_number = search_page.get_current_page_number()

        assert current_page_number == target_page_number

def test_search_result_consistency_across_pages(search_page):
    search_page.fill_term('k')
    search_page.submit()
    
    initial_pagination = search_page.get_result_summary()
    initial_total = initial_pagination.total
    
    if initial_pagination.page_end > 1:
        search_page.click_next_page()
        
        second_page_pagination = search_page.get_result_summary()
        
        assert second_page_pagination.total == initial_total
