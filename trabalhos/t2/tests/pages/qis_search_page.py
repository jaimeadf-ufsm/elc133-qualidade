from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class QisSearchPage(BasePage):
    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)
        
    # Navigation elements
    BREADCRUMB_LIST = (By.CSS_SELECTOR, "ul.breadcrumb")
    NAVIGATION_LINKS = (By.CSS_SELECTOR, ".divlinks a")
    SERVICE_LINKS = (By.CSS_SELECTOR, ".divloginstatus a")
    
    # Header elements
    PAGE_TITLE = (By.TAG_NAME, "h1")
    
    # Form elements
    SEARCH_FORM = (By.CSS_SELECTOR, "form[action*='qisserver/rds']")
    
    # Display options fieldset
    RESULTS_COUNT_10 = (By.ID, "anzahl1")
    RESULTS_COUNT_20 = (By.ID, "anzahl2")
    RESULTS_COUNT_30 = (By.ID, "anzahl3")
    RESULTS_COUNT_50 = (By.ID, "anzahl4")
    
    SORT_STANDARD = (By.ID, "sort1")
    SORT_NUMBER = (By.ID, "sort2")
    SORT_TITLE = (By.ID, "sort3")
    SORT_LECTURER = (By.ID, "sort4")
    
    # Search criteria elements
    SEMESTER_SELECT = (By.ID, "veranstaltung.semester")
    EVENT_NUMBER_INPUT = (By.ID, "veranstaltung.veranstnr")
    EVENT_TITLE_INPUT = (By.ID, "veranstaltung.dtxt")
    EVENT_TYPE_SELECT = (By.ID, "veranstaltung.verartid")
    INSTITUTION_INPUT = (By.ID, "einrichtung.dtxt")
    STUDY_PROGRAM_INPUT = (By.ID, "k_abstgv.dtxt")
    LECTURER_INPUT = (By.ID, "personal.nachname")
    ROOM_INPUT = (By.ID, "raum.dtxt")
    TIME_FROM_INPUT = (By.ID, "veransttermin.beginn")
    TIME_TO_INPUT = (By.ID, "veransttermin.ende")
    WEEKDAY_SELECT = (By.ID, "k_wochentag.wochentagid")
    LANGUAGE_SELECT = (By.ID, "veranstaltung.unterrsprache")
    REQUIREMENT_SELECT = (By.ID, "r_zuordabstgv.ppflichtid")
    MODULE_INPUT = (By.ID, "lsfmodule.pnr")
    
    # Buttons
    SEARCH_START_BUTTON = (By.CSS_SELECTOR, "input[name='search_start']")
    SEARCH_CLEAR_BUTTON = (By.CSS_SELECTOR, "input[name='search_clear']")
    INSTITUTION_SELECTION_BUTTON = (By.CSS_SELECTOR, "input[name='search_FB']")
    STUDY_PROGRAM_SELECTION_BUTTON = (By.CSS_SELECTOR, "input[name='search_STG']")
    LECTURER_SELECTION_BUTTON = (By.CSS_SELECTOR, "input[name='search_Dozent']")
    ROOM_SELECTION_BUTTON = (By.CSS_SELECTOR, "input[name='search_Raum']")
    MODULE_SELECTION_BUTTON = (By.CSS_SELECTOR, "input[name='search_Module-Num']")
    
    # Fieldsets
    DISPLAY_OPTIONS_FIELDSET = (By.XPATH, "//fieldset[legend[text()='Anzeigeoptionen']]")
    SEARCH_CRITERIA_FIELDSET = (By.XPATH, "//fieldset[legend[text()='Suchkriterien']]")
    
    # Scripts
    JQUERY_SCRIPT = (By.CSS_SELECTOR, "script[src*='jquery']")
    QIS_SCRIPTS = (By.CSS_SELECTOR, "script[src*='qis']")
    
    def get_breadcrumb_items(self):
        """Get all breadcrumb navigation items"""
        breadcrumb = self.driver.find_element(*self.BREADCRUMB_LIST)
        return breadcrumb.find_elements(By.TAG_NAME, "li")
    
    def get_navigation_links(self):
        """Get main navigation links"""
        return self.driver.find_elements(*self.NAVIGATION_LINKS)
    
    def get_service_links(self):
        """Get service links from header"""
        return self.driver.find_elements(*self.SERVICE_LINKS)
    
    def get_page_title_text(self):
        """Get the main page title"""
        return self.driver.find_element(*self.PAGE_TITLE).text
    
    def select_results_count(self, count):
        """Select number of results to display"""
        count_mapping = {
            10: self.RESULTS_COUNT_10,
            20: self.RESULTS_COUNT_20,
            30: self.RESULTS_COUNT_30,
            50: self.RESULTS_COUNT_50
        }
        if count in count_mapping:
            self.driver.find_element(*count_mapping[count]).click()
    
    def select_sort_option(self, option):
        """Select sorting option"""
        sort_mapping = {
            "standard": self.SORT_STANDARD,
            "number": self.SORT_NUMBER,
            "title": self.SORT_TITLE,
            "lecturer": self.SORT_LECTURER
        }
        if option in sort_mapping:
            self.driver.find_element(*sort_mapping[option]).click()
    
    def get_semester_options(self):
        """Get all semester options"""
        select_element = Select(self.driver.find_element(*self.SEMESTER_SELECT))
        return [option.text for option in select_element.options]
    
    def select_semester(self, value):
        """Select a semester by value"""
        select_element = Select(self.driver.find_element(*self.SEMESTER_SELECT))
        select_element.select_by_value(value)
    
    def fill_event_number(self, number):
        """Fill event number field"""
        element = self.driver.find_element(*self.EVENT_NUMBER_INPUT)
        element.clear()
        element.send_keys(number)
    
    def fill_event_title(self, title):
        """Fill event title field"""
        element = self.driver.find_element(*self.EVENT_TITLE_INPUT)
        element.clear()
        element.send_keys(title)
    
    def get_event_type_options(self):
        """Get all event type options"""
        select_element = Select(self.driver.find_element(*self.EVENT_TYPE_SELECT))
        return [option.text for option in select_element.options]
    
    def select_event_type(self, value):
        """Select event type by value"""
        select_element = Select(self.driver.find_element(*self.EVENT_TYPE_SELECT))
        select_element.select_by_value(value)
    
    def fill_institution(self, institution):
        """Fill institution field"""
        element = self.driver.find_element(*self.INSTITUTION_INPUT)
        element.clear()
        element.send_keys(institution)
    
    def fill_lecturer(self, lecturer):
        """Fill lecturer field"""
        element = self.driver.find_element(*self.LECTURER_INPUT)
        element.clear()
        element.send_keys(lecturer)
    
    def get_weekday_options(self):
        """Get all weekday options"""
        select_element = Select(self.driver.find_element(*self.WEEKDAY_SELECT))
        return [option.text for option in select_element.options]
    
    def get_language_options(self):
        """Get all language options"""
        select_element = Select(self.driver.find_element(*self.LANGUAGE_SELECT))
        return [option.text for option in select_element.options]
    
    def click_search_start(self):
        """Click the search start button"""
        self.driver.find_element(*self.SEARCH_START_BUTTON).click()
    
    def click_search_clear(self):
        """Click the search clear button"""
        self.driver.find_element(*self.SEARCH_CLEAR_BUTTON).click()
    
    def is_form_present(self):
        """Check if search form is present"""
        try:
            self.driver.find_element(*self.SEARCH_FORM)
            return True
        except:
            return False
    
    def is_fieldset_present(self, fieldset_type):
        """Check if specific fieldset is present"""
        fieldset_mapping = {
            "display": self.DISPLAY_OPTIONS_FIELDSET,
            "search": self.SEARCH_CRITERIA_FIELDSET
        }
        if fieldset_type in fieldset_mapping:
            try:
                self.driver.find_element(*fieldset_mapping[fieldset_type])
                return True
            except:
                return False
        return False
    
    def get_all_labels(self):
        """Get all form labels"""
        return self.driver.find_elements(By.CLASS_NAME, "inputlabel")
    
    def get_hidden_inputs(self):
        """Get all hidden input fields"""
        return self.driver.find_elements(By.CSS_SELECTOR, "input[type='hidden']")
    
    def are_scripts_loaded(self):
        """Check if required scripts are loaded"""
        jquery_scripts = self.driver.find_elements(*self.JQUERY_SCRIPT)
        qis_scripts = self.driver.find_elements(*self.QIS_SCRIPTS)
        return len(jquery_scripts) > 0 and len(qis_scripts) > 0
    
    def get_required_field_count(self):
        """Count fields marked as required"""
        return len(self.driver.find_elements(By.CSS_SELECTOR, ".redcolor"))
    
    def get_selection_buttons(self):
        """Get all selection buttons (Auswahl buttons)"""
        return self.driver.find_elements(By.CSS_SELECTOR, "input[value='Auswahl']")
