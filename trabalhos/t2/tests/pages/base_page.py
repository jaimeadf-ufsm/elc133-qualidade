from selenium import webdriver
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def go_to(self, url: str) -> None:
        self.driver.get(url)
    
    def get_title(self) -> str:
        return self.driver.title

    def get_url(self) -> str:
        return self.driver.current_url