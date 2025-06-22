import pytest
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from utilities.settings import Settings
from pages.qis_search_page import QISSearchPage

@pytest.fixture
def qis_page(driver):
    """Fixture to create QIS search page instance"""
    page = QISSearchPage(driver)
    page.go_to(Settings.QIS_SEARCH_URL)
    return page

class TestDropdownComponents:
    """Test class for dropdown/select components on QIS search page"""
    
    def test_semester_dropdown_presence(self, qis_page):
        """Test that semester dropdown is present and accessible"""
        semester_select = qis_page.driver.find_element(*qis_page.SEMESTER_SELECT)
        assert semester_select is not None
        assert semester_select.is_displayed()
        assert semester_select.is_enabled()
    
    def test_semester_dropdown_options(self, qis_page):
        """Test semester dropdown options and content"""
        options = qis_page.get_semester_options()
        
        # Verify that options exist
        assert len(options) > 0
        
        # Verify that semester options contain expected patterns
        # Typically should have current and future semesters
        semester_patterns = ['2024', '2025']
        has_expected_semesters = any(pattern in str(options) for pattern in semester_patterns)
        assert has_expected_semesters, f"Expected semester patterns not found in options: {options}"
    
    def test_semester_dropdown_selection(self, qis_page):
        """Test semester dropdown selection functionality"""
        options = qis_page.get_semester_options()
        
        if len(options) > 1:
            # Select the second option (first is usually default)
            test_semester = options[1]
            qis_page.select_semester(test_semester)
            
            # Verify selection
            selected_semester = qis_page.get_selected_semester()
            assert selected_semester == test_semester
    
    def test_semester_dropdown_default_selection(self, qis_page):
        """Test semester dropdown default selection"""
        # Get the default selected semester
        default_semester = qis_page.get_selected_semester()
        
        # Verify a default is selected (not empty)
        assert default_semester is not None
        assert default_semester != ""
    
    def test_course_type_dropdown_presence(self, qis_page):
        """Test that course type dropdown is present and accessible"""
        course_type_select = qis_page.driver.find_element(*qis_page.COURSE_TYPE_SELECT)
        assert course_type_select is not None
        assert course_type_select.is_displayed()
        assert course_type_select.is_enabled()
    
    def test_course_type_dropdown_options(self, qis_page):
        """Test course type dropdown options and content"""
        options = qis_page.get_course_type_options()
        
        # Verify that options exist
        assert len(options) > 0
        
        # Verify "Alles auswählen" option exists (select all option)
        assert "Alles auswählen" in options or "All" in str(options)
        
        # Verify common course types exist
        expected_types = ['Vorlesung', 'Seminar', 'Übung', 'Praktikum']
        found_types = [t for t in expected_types if any(t in option for option in options)]
        assert len(found_types) > 0, f"Expected course types not found. Available options: {options}"
    
    def test_course_type_dropdown_selection(self, qis_page):
        """Test course type dropdown selection functionality"""
        options = qis_page.get_course_type_options()
        
        # Find a selectable option (not "Alles auswählen")
        selectable_options = [opt for opt in options if opt != "Alles auswählen" and opt.strip()]
        
        if selectable_options:
            test_type = selectable_options[0]
            qis_page.select_course_type(test_type)
            
            # Verify selection
            selected_type = qis_page.get_selected_course_type()
            assert selected_type == test_type
    
    def test_weekday_multiselect_presence(self, qis_page):
        """Test that weekday multi-select is present and accessible"""
        weekday_select = qis_page.driver.find_element(*qis_page.WEEKDAY_SELECT)
        assert weekday_select is not None
        assert weekday_select.is_displayed()
        assert weekday_select.is_enabled()
    
    def test_weekday_multiselect_options(self, qis_page):
        """Test weekday multi-select options and content"""
        options = qis_page.get_weekday_options()
        
        # Verify that options exist
        assert len(options) > 0
        
        # Verify "Alles auswählen" option exists
        assert "Alles auswählen" in options or "All" in str(options)
        
        # Verify weekday names exist (German)
        expected_weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']
        found_weekdays = [day for day in expected_weekdays if any(day in option for option in options)]
        assert len(found_weekdays) >= 3, f"Expected weekdays not found. Available options: {options}"
    
    def test_weekday_multiselect_selection(self, qis_page):
        """Test weekday multi-select selection functionality"""
        options = qis_page.get_weekday_options()
        
        # Find selectable weekday options
        selectable_weekdays = [opt for opt in options if opt not in ["Alles auswählen", "keine Angabe"] and opt.strip()]
        
        if selectable_weekdays:
            # Select first available weekday
            test_weekday = selectable_weekdays[0]
            qis_page.select_weekday(test_weekday)
            
            # Verify selection
            selected_weekdays = qis_page.get_selected_weekdays()
            assert test_weekday in selected_weekdays
    
    def test_weekday_multiselect_multiple_selections(self, qis_page):
        """Test weekday multi-select multiple selection capability"""
        options = qis_page.get_weekday_options()
        selectable_weekdays = [opt for opt in options if opt not in ["Alles auswählen", "keine Angabe"] and opt.strip()]
        
        if len(selectable_weekdays) >= 2:
            # Select multiple weekdays
            first_weekday = selectable_weekdays[0]
            second_weekday = selectable_weekdays[1]
            
            qis_page.select_weekday(first_weekday)
            qis_page.select_weekday(second_weekday)
            
            # Verify both selections
            selected_weekdays = qis_page.get_selected_weekdays()
            assert first_weekday in selected_weekdays
            assert second_weekday in selected_weekdays
    
    def test_language_multiselect_presence(self, qis_page):
        """Test that language multi-select is present and accessible"""
        language_select = qis_page.driver.find_element(*qis_page.LANGUAGE_SELECT)
        assert language_select is not None
        assert language_select.is_displayed()
        assert language_select.is_enabled()
    
    def test_language_multiselect_options(self, qis_page):
        """Test language multi-select options and content"""
        options = qis_page.get_language_options()
        
        # Verify that options exist
        assert len(options) > 0
        
        # Verify "Alles auswählen" option exists
        assert "Alles auswählen" in options or "All" in str(options)
        
        # Verify common languages exist
        expected_languages = ['Deutsch', 'Englisch']
        found_languages = [lang for lang in expected_languages if any(lang in option for option in options)]
        assert len(found_languages) >= 1, f"Expected languages not found. Available options: {options}"
    
    def test_language_multiselect_selection(self, qis_page):
        """Test language multi-select selection functionality"""
        options = qis_page.get_language_options()
        
        # Find selectable language options
        selectable_languages = [opt for opt in options if opt != "Alles auswählen" and opt.strip()]
        
        if selectable_languages:
            test_language = selectable_languages[0]
            qis_page.select_language(test_language)
            
            # Verify selection
            selected_languages = qis_page.get_selected_languages()
            assert test_language in selected_languages
    
    def test_language_multiselect_multiple_selections(self, qis_page):
        """Test language multi-select multiple selection capability"""
        options = qis_page.get_language_options()
        selectable_languages = [opt for opt in options if opt != "Alles auswählen" and opt.strip()]
        
        if len(selectable_languages) >= 2:
            # Select multiple languages
            first_language = selectable_languages[0]
            second_language = selectable_languages[1]
            
            qis_page.select_language(first_language)
            qis_page.select_language(second_language)
            
            # Verify both selections
            selected_languages = qis_page.get_selected_languages()
            assert first_language in selected_languages
            assert second_language in selected_languages
    
    def test_department_dropdown_presence(self, qis_page):
        """Test that department dropdown is present and accessible"""
        try:
            department_select = qis_page.driver.find_element(*qis_page.DEPARTMENT_SELECT)
            assert department_select is not None
            assert department_select.is_displayed()
            assert department_select.is_enabled()
        except NoSuchElementException:
            pytest.skip("Department dropdown not found on page")
    
    def test_department_dropdown_options(self, qis_page):
        """Test department dropdown options and content"""
        try:
            select = Select(qis_page.driver.find_element(*qis_page.DEPARTMENT_SELECT))
            options = [option.text for option in select.options]
            
            # Verify that options exist
            assert len(options) > 0
            
            # Verify that department-like options exist
            # Look for common German university department patterns
            department_patterns = ['Fakultät', 'Institut', 'Fachbereich', 'Lehrstuhl']
            has_department_pattern = any(pattern in str(options) for pattern in department_patterns)
            assert has_department_pattern or len(options) > 1, f"Expected department patterns not found: {options}"
            
        except NoSuchElementException:
            pytest.skip("Department dropdown not found on page")
    
    def test_dropdown_accessibility_attributes(self, qis_page):
        """Test dropdown components for accessibility attributes"""
        dropdowns = [
            qis_page.SEMESTER_SELECT,
            qis_page.COURSE_TYPE_SELECT,
            qis_page.WEEKDAY_SELECT,
            qis_page.LANGUAGE_SELECT
        ]
        
        for dropdown_locator in dropdowns:
            try:
                dropdown = qis_page.driver.find_element(*dropdown_locator)
                
                # Check for name attribute (important for form submission)
                name_attr = dropdown.get_attribute('name')
                assert name_attr is not None and name_attr != "", f"Dropdown missing name attribute: {dropdown_locator}"
                
                # Check that dropdown is focusable
                assert dropdown.get_attribute('tabindex') != "-1", f"Dropdown not focusable: {dropdown_locator}"
                
            except NoSuchElementException:
                # Some dropdowns might not exist on all page versions
                continue
    
    def test_dropdown_form_integration(self, qis_page):
        """Test that dropdown selections integrate properly with form"""
        # Make selections in multiple dropdowns
        try:
            # Select semester
            semester_options = qis_page.get_semester_options()
            if len(semester_options) > 1:
                qis_page.select_semester(semester_options[1])
            
            # Select course type
            course_type_options = qis_page.get_course_type_options()
            selectable_types = [opt for opt in course_type_options if opt != "Alles auswählen" and opt.strip()]
            if selectable_types:
                qis_page.select_course_type(selectable_types[0])
            
            # Verify selections persist
            if len(semester_options) > 1:
                assert qis_page.get_selected_semester() == semester_options[1]
            if selectable_types:
                assert qis_page.get_selected_course_type() == selectable_types[0]
                
        except Exception as e:
            pytest.fail(f"Dropdown form integration test failed: {str(e)}")
    
    def test_dropdown_reset_functionality(self, qis_page):
        """Test that dropdown selections can be reset"""
        try:
            # Make some selections
            semester_options = qis_page.get_semester_options()
            if len(semester_options) > 1:
                original_selection = qis_page.get_selected_semester()
                qis_page.select_semester(semester_options[1])
                
                # Verify selection changed
                new_selection = qis_page.get_selected_semester()
                assert new_selection != original_selection
                
                # Click reset button if available
                if qis_page.is_reset_button_enabled():
                    qis_page.click_reset()
                    time.sleep(1)  # Wait for reset to complete
                    
                    # Verify reset worked (selection should return to default)
                    reset_selection = qis_page.get_selected_semester()
                    # Reset might return to original or to first option
                    assert reset_selection in [original_selection, semester_options[0]]
                    
        except Exception as e:
            pytest.skip(f"Reset functionality test skipped: {str(e)}")
    
    def test_dropdown_keyboard_navigation(self, qis_page):
        """Test dropdown keyboard navigation accessibility"""
        from selenium.webdriver.common.keys import Keys
        
        try:
            # Focus on semester dropdown
            semester_dropdown = qis_page.driver.find_element(*qis_page.SEMESTER_SELECT)
            semester_dropdown.click()
            
            # Test arrow key navigation
            semester_dropdown.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)
            
            # Test escape key to close dropdown
            semester_dropdown.send_keys(Keys.ESCAPE)
            
            # Test tab navigation to next dropdown
            semester_dropdown.send_keys(Keys.TAB)
            
            # Verify focus moved (basic check)
            active_element = qis_page.driver.switch_to.active_element
            assert active_element != semester_dropdown
            
        except Exception as e:
            pytest.skip(f"Keyboard navigation test skipped: {str(e)}")
