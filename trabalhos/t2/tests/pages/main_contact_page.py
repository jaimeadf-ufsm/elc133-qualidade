from .base_page import *

class MainContactPage(BasePage):
    OFFICE_ADDRESS_CONTENT = (By.CSS_SELECTOR, 'main > div:nth-of-type(1) p:nth-of-type(1)')
    POSTAL_ADDRESS_CONTENT = (By.CSS_SELECTOR, 'main > div:nth-of-type(1) p:nth-of-type(2)')
    PHONE_AND_EMAIL_CONTENT = (By.CSS_SELECTOR, 'main > div:nth-of-type(2)')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_office_address_information(self) -> str:
        return self.driver.find_element(*self.OFFICE_ADDRESS_CONTENT).text.strip()
    
    def get_postal_address_information(self) -> str:
        return self.driver.find_element(*self.POSTAL_ADDRESS_CONTENT).text.strip()
    
    def get_phone_and_email_information(self) -> str:
        return self.driver.find_element(*self.PHONE_AND_EMAIL_CONTENT).text.strip()