from .base_page import *

class MainFAQPage(BasePage):
    ACCORDION_ITEM = (By.CSS_SELECTOR, '[data-accordion]')
    ACCORDION_BUTTON = (By.CSS_SELECTOR, '[data-accordion] > button')
    ACCORDION_CONTENT = (By.CSS_SELECTOR, '[data-accordion] > div')

    def __init__(self, driver):
        super().__init__(driver)
    
    def count_accordions(self) -> int:
        return len(self.driver.find_elements(*self.ACCORDION_ITEM))
    
    def toggle_accordion(self, index: int) -> None:
        self.driver.find_elements(*self.ACCORDION_BUTTON)[index].click()
    
    def get_accordion_content(self, index: int) -> str:
        return self.driver.find_elements(*self.ACCORDION_CONTENT)[index].text.strip()
    
    def is_accordion_open(self, index: int) -> bool:
        classNames = self.driver.find_elements(*self.ACCORDION_ITEM)[index].get_attribute('class') or ''

        return 'accordion--open' in classNames.split()


    
    