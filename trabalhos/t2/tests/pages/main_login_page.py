from .base_page import *

class MainLoginPage(BasePage):
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input[name="user"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[name="pass"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'input[type="submit"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, 'p:has(+ form)')
    
    def __init__(self, driver):
        super().__init__(driver)

    def fill_username(self, username: str) -> None:
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
    
    def fill_password(self, password: str) -> None:
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
    
    def submit(self) -> None:
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def is_displaying_error_message(self) -> bool:
        return len(self.driver.find_elements(*self.ERROR_MESSAGE)) > 0