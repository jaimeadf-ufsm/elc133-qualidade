from .base_page import *

class MainNewsPage(BasePage):
    PAGE_ITEM = (By .CSS_SELECTOR, '.pagination__item')
    CURRENT_PAGE_ITEM = (By.CSS_SELECTOR, '.pagination__item--current')
    PREVIOUS_PAGE_BUTTON = (By.CSS_SELECTOR, '.pagination a[aria-label="vorherige"]')
    NEXT_PAGE_BUTTON = (By.CSS_SELECTOR, '.pagination a[aria-label="nächste"]')
    
    def __init__(self, driver):
        super().__init__(driver)

    def get_current_page(self) -> str:
        return self.driver.find_element(*self.CURRENT_PAGE_ITEM).text.strip()
    
    def click_previous_page(self) -> None:
        self.driver.find_element(*self.PREVIOUS_PAGE_BUTTON).click()
    
    def click_next_page(self) -> None:
        self.driver.find_element(*self.NEXT_PAGE_BUTTON).click()
    
    def click_numbered_page(self, page: str) -> None:
        page_items = self.driver.find_elements(*self.PAGE_ITEM)

        for item in page_items:

            if item.text.strip() == page:
                item.click()
                return
