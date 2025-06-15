import typing
import re
from .base_page import *

class ResultSummary:
    def __init__(self, page_start: int, page_end: int, total: int):
        self.page_start = page_start
        self.page_end = page_end
        self.total = total

class MainSearchPage(BasePage):
    TERM_INPUT = (By.CSS_SELECTOR, '#main input[name="tx_solr[q]"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '#main button[type="submit"]')
    RESET_BUTTON = (By.CSS_SELECTOR, '#main a[href="/suche/#tx-solr-search"]')

    FILTER_ACCORDION = (By.CSS_SELECTOR, '#main #kesearch_filters [data-accordion]')
    FILTER_ACCORDION_BUTTON = (By.CSS_SELECTOR, '#main #kesearch_filters [data-accordion] > button')
    FILTER_ACCORDION_CHECKBOXES = (By.CSS_SELECTOR, '#main #kesearch_filters [data-accordion] input[type="checkbox"]')

    RESULT_SUMMARY = (By.CSS_SELECTOR, '.pagination-search-result')

    PAGINATION_PREVIOUS_BUTTON = (By.CSS_SELECTOR, '.pagination-search a.prev')
    PAGINATION_NEXT_BUTTON = (By.CSS_SELECTOR, '.pagination-search a.next')
    PAGINATION_CURRENT_PAGE = (By.CSS_SELECTOR, '.pagination-search .current a')
    PAGINATION_PAGE_LINKS = (By.CSS_SELECTOR, '.pagination-search .page-link')
    PAGINATION_PAGE_ITEMS = (By.CSS_SELECTOR, '.pagination-search .page-item')
    PAGINATION_DOTS = (By.CSS_SELECTOR, '.pagination-search .pagination-dots')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def fill_term(self, query: str) -> None:
        search_input = self.driver.find_element(*self.TERM_INPUT)
        search_input.clear()
        search_input.send_keys(query)
    
    def get_term(self) -> str:
        return self.driver.find_element(*self.TERM_INPUT).get_attribute('value') or ''
    
    def reset(self) -> None:
        self.driver.find_element(*self.RESET_BUTTON).click()

    def submit(self) -> None:
        self.driver.find_element(*self.SUBMIT_BUTTON).click()
    
    def toggle_filter_accordion(self) -> None:
        self.driver.find_element(*self.FILTER_ACCORDION_BUTTON).click()
    
    def is_filter_accordion_open(self) -> bool:
        class_names = self.driver.find_element(*self.FILTER_ACCORDION).get_attribute('class') or ''

        print(class_names)

        return 'accordion--open' in class_names.split()

    def toggle_filter(self, name: str) -> None:
        filters = self.driver.find_elements(*self.FILTER_ACCORDION_CHECKBOXES)

        for filter in filters:
            if filter.get_attribute('name') == name:
                self.driver.execute_script("arguments[0].click();", filter)
                return
    
    def is_filter_enabled(self, name: str) -> bool:
        filters = self.driver.find_elements(*self.FILTER_ACCORDION_CHECKBOXES)

        for filter in filters:
            if filter.get_attribute('name') == name:
                return filter.is_selected()
        
        return False

    def get_available_filter_names(self) -> typing.List[str]:
        names = []
        filters = self.driver.find_elements(*self.FILTER_ACCORDION_CHECKBOXES)

        for filter in filters:
            name = filter.get_attribute('name') or ''

            if name:
                names.append(name)
        
        return names

    def get_result_summary(self) -> ResultSummary:
        try:
            summary_element = self.driver.find_element(*self.RESULT_SUMMARY)
            summary_text = summary_element.text

            pattern = r'Zeige Ergebnisse (\d+) bis (\d+) von (\d+)\.'
            match = re.search(pattern, summary_text)

            if match:
                page_start = int(match.group(1))
                page_end = int(match.group(2))
                total = int(match.group(3))

                return ResultSummary(page_start, page_end, total)
        except:
            pass
    
        return ResultSummary(0, 0, 0)
    
    def get_current_page_number(self) -> int:
        try:
            current_page_element = self.driver.find_element(*self.PAGINATION_CURRENT_PAGE)
            return int(current_page_element.text.strip())
        except:
            return 1
    
    def get_available_page_numbers(self) -> typing.List[int]:
        page_numbers = []
        
        page_numbers.append(self.get_current_page_number())
        
        page_links = self.driver.find_elements(*self.PAGINATION_PAGE_LINKS)

        for link in page_links:
            page_number = int(link.text.strip())

            if page_number not in page_numbers:
                page_numbers.append(page_number)
        
        return sorted(page_numbers)
    
    def click_page_number(self, page_number: int) -> None:
        page_links = self.driver.find_elements(*self.PAGINATION_PAGE_LINKS)

        for link in page_links:
            if int(link.text.strip()) == page_number:
                link.click()

    def click_next_page(self) -> None:
     self.driver.find_element(*self.PAGINATION_NEXT_BUTTON).click()
    
    def click_previous_page(self) -> None:
        self.driver.find_element(*self.PAGINATION_PREVIOUS_BUTTON).click()

