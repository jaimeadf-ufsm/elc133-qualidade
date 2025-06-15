from .base_page import *

class MainHomePage(BasePage):
    LANGUAGE_BUTTON = (By.CSS_SELECTOR, '.topbar a:first-of-type')
    
    def __init__(self, driver):
        super().__init__(driver)

    def toggle_language(self) -> None:
        self.driver.find_element(*self.LANGUAGE_BUTTON).click()
    
    def get_current_language(self) -> str:
        return self.driver.find_element(By.TAG_NAME, 'html').get_attribute('lang') or ''
