import typing
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base_page import *

class QISSearchPage(BasePage):
    # Text Input Fields
    COURSE_NUMBER_INPUT = (By.NAME, "veranstaltung.nummer")
    COURSE_TITLE_INPUT = (By.NAME, "veranstaltung.titel")
    INSTRUCTOR_INPUT = (By.NAME, "veranstaltung.lehrende")
    ROOM_INPUT = (By.NAME, "veranstaltung.raum")
    TIME_FROM_INPUT = (By.NAME, "veranstaltung.zeitVon")
    TIME_TO_INPUT = (By.NAME, "veranstaltung.zeitBis")
    
    # Dropdown/Select Components
    SEMESTER_SELECT = (By.NAME, "semester")
    COURSE_TYPE_SELECT = (By.NAME, "veranstaltung.veranstaltungsart")
    DEPARTMENT_SELECT = (By.NAME, "veranstaltung.einrichtung")
    STUDY_PROGRAM_SELECT = (By.NAME, "veranstaltung.studiengang")
    WEEKDAY_SELECT = (By.NAME, "veranstaltung.wochentag")
    LANGUAGE_SELECT = (By.NAME, "veranstaltung.sprache")
    REQUIREMENT_TYPE_SELECT = (By.NAME, "veranstaltung.pflichtkennzeichen")
    
    # Display Control Components
    RESULTS_PER_PAGE_SELECT = (By.NAME, "anzahl")
    SORT_ORDER_SELECT = (By.NAME, "sortierung")
    
    # Button Components
    SEARCH_BUTTON = (By.CSS_SELECTOR, "input[type='submit'][value*='Suchen']")
    RESET_BUTTON = (By.CSS_SELECTOR, "input[type='reset']")
    
    # Navigation Components
    BREADCRUMB_LINKS = (By.CSS_SELECTOR, "ul li a")
    HELP_LINK = (By.CSS_SELECTOR, "a[href*='helpsearch']")
    LANGUAGE_SWITCHER = (By.CSS_SELECTOR, "a img[src*='flag_en']")
    
    # Form and Page Elements
    SEARCH_FORM = (By.CSS_SELECTOR, "form")
    PAGE_TITLE = (By.TAG_NAME, "h1")
    SEARCH_CRITERIA_SECTION = (By.CSS_SELECTOR, "table")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    # Text Input Methods
    def fill_course_number(self, course_number: str) -> None:
        """Fill the course number input field"""
        input_field = self.driver.find_element(*self.COURSE_NUMBER_INPUT)
        input_field.clear()
        input_field.send_keys(course_number)
    
    def get_course_number(self) -> str:
        """Get the current value of course number input"""
        return self.driver.find_element(*self.COURSE_NUMBER_INPUT).get_attribute('value') or ''
    
    def fill_course_title(self, title: str) -> None:
        """Fill the course title input field"""
        input_field = self.driver.find_element(*self.COURSE_TITLE_INPUT)
        input_field.clear()
        input_field.send_keys(title)
    
    def get_course_title(self) -> str:
        """Get the current value of course title input"""
        return self.driver.find_element(*self.COURSE_TITLE_INPUT).get_attribute('value') or ''
    
    def fill_instructor(self, instructor: str) -> None:
        """Fill the instructor input field"""
        input_field = self.driver.find_element(*self.INSTRUCTOR_INPUT)
        input_field.clear()
        input_field.send_keys(instructor)
    
    def get_instructor(self) -> str:
        """Get the current value of instructor input"""
        return self.driver.find_element(*self.INSTRUCTOR_INPUT).get_attribute('value') or ''
    
    def fill_room(self, room: str) -> None:
        """Fill the room input field"""
        input_field = self.driver.find_element(*self.ROOM_INPUT)
        input_field.clear()
        input_field.send_keys(room)
    
    def get_room(self) -> str:
        """Get the current value of room input"""
        return self.driver.find_element(*self.ROOM_INPUT).get_attribute('value') or ''
    
    def fill_time_from(self, time: str) -> None:
        """Fill the time from input field"""
        input_field = self.driver.find_element(*self.TIME_FROM_INPUT)
        input_field.clear()
        input_field.send_keys(time)
    
    def get_time_from(self) -> str:
        """Get the current value of time from input"""
        return self.driver.find_element(*self.TIME_FROM_INPUT).get_attribute('value') or ''
    
    # Dropdown/Select Methods
    def select_semester(self, semester_value: str) -> None:
        """Select a semester from the dropdown"""
        select = Select(self.driver.find_element(*self.SEMESTER_SELECT))
        select.select_by_value(semester_value)
    
    def get_selected_semester(self) -> str:
        """Get the currently selected semester"""
        select = Select(self.driver.find_element(*self.SEMESTER_SELECT))
        return select.first_selected_option.get_attribute('value')
    
    def get_semester_options(self) -> typing.List[str]:
        """Get all available semester options"""
        select = Select(self.driver.find_element(*self.SEMESTER_SELECT))
        return [option.get_attribute('value') for option in select.options]
    
    def select_course_type(self, course_type: str) -> None:
        """Select a course type from the dropdown"""
        select = Select(self.driver.find_element(*self.COURSE_TYPE_SELECT))
        select.select_by_visible_text(course_type)
    
    def get_selected_course_type(self) -> str:
        """Get the currently selected course type"""
        select = Select(self.driver.find_element(*self.COURSE_TYPE_SELECT))
        return select.first_selected_option.text
    
    def get_course_type_options(self) -> typing.List[str]:
        """Get all available course type options"""
        select = Select(self.driver.find_element(*self.COURSE_TYPE_SELECT))
        return [option.text for option in select.options]
    
    def select_weekday(self, weekday: str) -> None:
        """Select a weekday from the multi-select"""
        select = Select(self.driver.find_element(*self.WEEKDAY_SELECT))
        select.select_by_visible_text(weekday)
    
    def get_selected_weekdays(self) -> typing.List[str]:
        """Get all selected weekdays"""
        select = Select(self.driver.find_element(*self.WEEKDAY_SELECT))
        return [option.text for option in select.all_selected_options]
    
    def get_weekday_options(self) -> typing.List[str]:
        """Get all available weekday options"""
        select = Select(self.driver.find_element(*self.WEEKDAY_SELECT))
        return [option.text for option in select.options]
    
    def select_language(self, language: str) -> None:
        """Select a language from the multi-select"""
        select = Select(self.driver.find_element(*self.LANGUAGE_SELECT))
        select.select_by_visible_text(language)
    
    def get_selected_languages(self) -> typing.List[str]:
        """Get all selected languages"""
        select = Select(self.driver.find_element(*self.LANGUAGE_SELECT))
        return [option.text for option in select.all_selected_options]
    
    def get_language_options(self) -> typing.List[str]:
        """Get all available language options"""
        select = Select(self.driver.find_element(*self.LANGUAGE_SELECT))
        return [option.text for option in select.options]
    
    # Display Control Methods
    def select_results_per_page(self, count: str) -> None:
        """Select number of results per page"""
        select = Select(self.driver.find_element(*self.RESULTS_PER_PAGE_SELECT))
        select.select_by_value(count)
    
    def get_results_per_page_options(self) -> typing.List[str]:
        """Get all available results per page options"""
        select = Select(self.driver.find_element(*self.RESULTS_PER_PAGE_SELECT))
        return [option.get_attribute('value') for option in select.options]
    
    def select_sort_order(self, sort_order: str) -> None:
        """Select sort order"""
        select = Select(self.driver.find_element(*self.SORT_ORDER_SELECT))
        select.select_by_visible_text(sort_order)
    
    def get_sort_order_options(self) -> typing.List[str]:
        """Get all available sort order options"""
        select = Select(self.driver.find_element(*self.SORT_ORDER_SELECT))
        return [option.text for option in select.options]
    
    # Button and Action Methods
    def click_search(self) -> None:
        """Click the search button"""
        self.driver.find_element(*self.SEARCH_BUTTON).click()
    
    def click_reset(self) -> None:
        """Click the reset button"""
        self.driver.find_element(*self.RESET_BUTTON).click()
    
    def is_search_button_enabled(self) -> bool:
        """Check if search button is enabled"""
        return self.driver.find_element(*self.SEARCH_BUTTON).is_enabled()
    
    def is_reset_button_enabled(self) -> bool:
        """Check if reset button is enabled"""
        return self.driver.find_element(*self.RESET_BUTTON).is_enabled()
    
    # Navigation Methods
    def get_breadcrumb_links(self) -> typing.List[str]:
        """Get all breadcrumb link texts"""
        links = self.driver.find_elements(*self.BREADCRUMB_LINKS)
        return [link.text.strip() for link in links if link.text.strip()]
    
    def click_help_link(self) -> None:
        """Click the help link"""
        self.driver.find_element(*self.HELP_LINK).click()
    
    def is_help_link_present(self) -> bool:
        """Check if help link is present"""
        try:
            self.driver.find_element(*self.HELP_LINK)
            return True
        except NoSuchElementException:
            return False
    
    def click_language_switcher(self) -> None:
        """Click the language switcher"""
        self.driver.find_element(*self.LANGUAGE_SWITCHER).click()
    
    def is_language_switcher_present(self) -> bool:
        """Check if language switcher is present"""
        try:
            self.driver.find_element(*self.LANGUAGE_SWITCHER)
            return True
        except NoSuchElementException:
            return False
    
    # Utility Methods
    def get_page_title(self) -> str:
        """Get the page title"""
        return self.driver.find_element(*self.PAGE_TITLE).text.strip()
    
    def is_search_form_present(self) -> bool:
        """Check if search form is present"""
        try:
            self.driver.find_element(*self.SEARCH_FORM)
            return True
        except NoSuchElementException:
            return False
    
    def clear_all_inputs(self) -> None:
        """Clear all input fields"""
        inputs = [
            self.COURSE_NUMBER_INPUT,
            self.COURSE_TITLE_INPUT,
            self.INSTRUCTOR_INPUT,
            self.ROOM_INPUT,
            self.TIME_FROM_INPUT
        ]
        
        for input_locator in inputs:
            try:
                input_field = self.driver.find_element(*input_locator)
                input_field.clear()
            except NoSuchElementException:
                continue
