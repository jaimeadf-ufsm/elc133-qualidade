from .base_page import *

class BSZHomePage(BasePage):
    CURRENT_CAROUSEL_CONTENT = (By.CSS_SELECTOR, '.slick-slide.slick-current.slick-active')

    CAROUSEL_DOTS = (By.CSS_SELECTOR, '.slick-dots > li')

    CAROUSEL_NEXT_BUTTON = (By.CSS_SELECTOR, '.slick-next')
    CAROUSEL_PREVIOUS_BUTTON = (By.CSS_SELECTOR, '.slick-prev')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_current_carousel_content(self) -> str:
        return self.driver.find_element(*self.CURRENT_CAROUSEL_CONTENT).text.strip()

    def get_current_carousel_dot(self) -> int:
        dots = self.driver.find_elements(*self.CAROUSEL_DOTS)

        for index, dot in enumerate(dots):
            if 'slick-active' in (dot.get_attribute('class') or '').split():
                return index

        return -1

    def get_carousel_dot_count(self) -> int:
        return len(self.driver.find_elements(*self.CAROUSEL_DOTS))
    
    def click_carousel_dot(self, index: int) -> None:
        dots = self.driver.find_elements(*self.CAROUSEL_DOTS)
        dots[index].click()
    
    def click_next_carousel_button(self) -> None:
        self.driver.find_element(*self.CAROUSEL_NEXT_BUTTON).click()
    
    def click_previous_carousel_button(self) -> None:
        self.driver.find_element(*self.CAROUSEL_PREVIOUS_BUTTON).click()
    