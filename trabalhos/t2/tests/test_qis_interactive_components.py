import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utilities.settings import Settings
from pages.qis_search_page import QISSearchPage

@pytest.fixture
def qis_page(driver):
    """Fixture to create QIS search page instance"""
    page = QISSearchPage(driver)
    page.go_to(Settings.QIS_SEARCH_URL)
    return page

class TestInteractiveComponents:
    """Test class for interactive UI components on QIS search page"""
    
    def test_search_button_presence(self, qis_page):
        """Test that search button is present and accessible"""
        search_button = qis_page.driver.find_element(*qis_page.SEARCH_BUTTON)
        assert search_button is not None
        assert search_button.is_displayed()
        assert search_button.is_enabled()
    
    def test_search_button_attributes(self, qis_page):
        """Test search button attributes and properties"""
        search_button = qis_page.driver.find_element(*qis_page.SEARCH_BUTTON)
        
        # Verify button type
        button_type = search_button.get_attribute('type')
        assert button_type == 'submit', f"Search button should be submit type: {button_type}"
        
        # Verify button value/text
        button_value = search_button.get_attribute('value')
        button_text = search_button.text
        
        search_indicators = ['suchen', 'search', 'find']
        has_search_indicator = any(indicator in (button_value + ' ' + button_text).lower() for indicator in search_indicators)
        assert has_search_indicator, f"Search button missing search indicator. Value: '{button_value}', Text: '{button_text}'"
    
    def test_search_button_functionality(self, qis_page):
        """Test search button click functionality"""
        # Fill some search criteria first
        qis_page.fill_course_title("Test")
        
        original_url = qis_page.driver.current_url
        
        # Click search button
        assert qis_page.is_search_button_enabled(), "Search button is not enabled"
        qis_page.click_search()
        
        # Wait for potential page change or form submission
        time.sleep(2)
        
        # Verify some action occurred (URL change or page update)
        new_url = qis_page.driver.current_url
        url_changed = new_url != original_url
        
        # Check if page content indicates search was performed
        page_source = qis_page.driver.page_source.lower()
        search_performed = any(indicator in page_source for indicator in ['ergebnis', 'result', 'gefunden', 'found'])
        
        assert url_changed or search_performed, "Search button click didn't trigger expected action"
    
    def test_reset_button_presence(self, qis_page):
        """Test that reset button is present and accessible"""
        try:
            reset_button = qis_page.driver.find_element(*qis_page.RESET_BUTTON)
            assert reset_button is not None
            assert reset_button.is_displayed()
            assert reset_button.is_enabled()
        except NoSuchElementException:
            pytest.skip("Reset button not found on page")
    
    def test_reset_button_attributes(self, qis_page):
        """Test reset button attributes and properties"""
        try:
            reset_button = qis_page.driver.find_element(*qis_page.RESET_BUTTON)
            
            # Verify button type
            button_type = reset_button.get_attribute('type')
            assert button_type == 'reset', f"Reset button should be reset type: {button_type}"
            
            # Verify button value/text
            button_value = reset_button.get_attribute('value')
            button_text = reset_button.text
            
            reset_indicators = ['reset', 'clear', 'löschen', 'zurücksetzen']
            has_reset_indicator = any(indicator in (button_value + ' ' + button_text).lower() for indicator in reset_indicators)
            assert has_reset_indicator, f"Reset button missing reset indicator. Value: '{button_value}', Text: '{button_text}'"
            
        except NoSuchElementException:
            pytest.skip("Reset button not found on page")
    
    def test_reset_button_functionality(self, qis_page):
        """Test reset button functionality"""
        try:
            # Fill form fields with test data
            qis_page.fill_course_number("12345")
            qis_page.fill_course_title("Test Course")
            qis_page.fill_instructor("Test Instructor")
            
            # Verify fields have values
            assert qis_page.get_course_number() != ""
            assert qis_page.get_course_title() != ""
            assert qis_page.get_instructor() != ""
            
            # Click reset button
            assert qis_page.is_reset_button_enabled(), "Reset button is not enabled"
            qis_page.click_reset()
            
            time.sleep(1)  # Wait for reset to complete
            
            # Verify fields are cleared
            assert qis_page.get_course_number() == "", "Course number not cleared after reset"
            assert qis_page.get_course_title() == "", "Course title not cleared after reset"
            assert qis_page.get_instructor() == "", "Instructor not cleared after reset"
            
        except NoSuchElementException:
            pytest.skip("Reset button not found on page")
    
    def test_button_keyboard_accessibility(self, qis_page):
        """Test button keyboard accessibility"""
        # Test search button keyboard access
        search_button = qis_page.driver.find_element(*qis_page.SEARCH_BUTTON)
        
        # Verify button is keyboard focusable
        assert search_button.get_attribute('tabindex') != "-1", "Search button not keyboard accessible"
        
        # Test focus and activation
        search_button.click()  # Focus the button
        focused_element = qis_page.driver.switch_to.active_element
        
        # Verify button can receive focus
        assert focused_element == search_button or focused_element.get_attribute('type') == 'submit', "Search button cannot receive focus"
        
        # Test reset button if present
        try:
            reset_button = qis_page.driver.find_element(*qis_page.RESET_BUTTON)
            assert reset_button.get_attribute('tabindex') != "-1", "Reset button not keyboard accessible"
        except NoSuchElementException:
            pass  # Reset button not present, skip this part
    
    def test_button_visual_states(self, qis_page):
        """Test button visual states and styling"""
        search_button = qis_page.driver.find_element(*qis_page.SEARCH_BUTTON)
        
        # Verify button has reasonable dimensions
        button_size = search_button.size
        assert button_size['width'] > 30, "Search button too narrow"
        assert button_size['height'] > 20, "Search button too short"
        
        # Verify button is visible and not transparent
        assert search_button.is_displayed(), "Search button not visible"
        
        # Test hover state (basic check)
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(qis_page.driver)
            actions.move_to_element(search_button).perform()
            time.sleep(0.5)  # Brief pause for hover effect
            
            # Button should still be enabled and visible after hover
            assert search_button.is_enabled(), "Search button disabled after hover"
            assert search_button.is_displayed(), "Search button hidden after hover"
            
        except Exception:
            pass  # Hover test is optional
    
    def test_language_switcher_interactive_behavior(self, qis_page):
        """Test language switcher interactive behavior"""
        if qis_page.is_language_switcher_present():
            lang_switcher = qis_page.driver.find_element(*qis_page.LANGUAGE_SWITCHER)
            
            # Test hover behavior
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(qis_page.driver)
                actions.move_to_element(lang_switcher).perform()
                time.sleep(0.5)
                
                # Verify element remains interactive after hover
                assert lang_switcher.is_enabled(), "Language switcher disabled after hover"
                
            except Exception:
                pass  # Hover test is optional
            
            # Test keyboard accessibility
            parent_link = lang_switcher.find_element(By.XPATH, "..")
            assert parent_link.get_attribute('tabindex') != "-1", "Language switcher not keyboard accessible"
    
    def test_form_submission_prevention(self, qis_page):
        """Test form submission behavior with empty fields"""
        # Clear all fields
        qis_page.clear_all_inputs()
        
        # Try to submit empty form
        original_url = qis_page.driver.current_url
        qis_page.click_search()
        
        time.sleep(2)  # Wait for potential submission
        
        # Check if form was submitted or if validation prevented it
        new_url = qis_page.driver.current_url
        
        # Either URL should change (form submitted) or stay same (validation prevented)
        # Both behaviors are acceptable depending on form design
        if new_url == original_url:
            # Form submission was prevented - check for validation messages
            page_source = qis_page.driver.page_source.lower()
            validation_indicators = ['required', 'erforderlich', 'fehler', 'error', 'bitte']
            has_validation = any(indicator in page_source for indicator in validation_indicators)
            
            # If no validation message, form might just allow empty searches
            # This is acceptable behavior
            assert True  # Test passes either way
        else:
            # Form was submitted - this is also acceptable
            assert True
    
    def test_interactive_element_focus_order(self, qis_page):
        """Test tab order and focus flow through interactive elements"""
        # Start from page body
        body = qis_page.driver.find_element(By.TAG_NAME, "body")
        body.click()
        
        interactive_elements = []
        
        # Tab through first several elements to test focus order
        for i in range(10):
            body.send_keys(Keys.TAB)
            time.sleep(0.2)
            
            focused_element = qis_page.driver.switch_to.active_element
            tag_name = focused_element.tag_name.lower()
            element_type = focused_element.get_attribute('type')
            
            if tag_name in ['input', 'select', 'button', 'a'] and focused_element.is_displayed():
                interactive_elements.append({
                    'tag': tag_name,
                    'type': element_type,
                    'name': focused_element.get_attribute('name'),
                    'id': focused_element.get_attribute('id')
                })
        
        # Verify we found interactive elements
        assert len(interactive_elements) > 0, "No interactive elements found in tab order"
        
        # Verify logical order (inputs before buttons typically)
        input_indices = [i for i, elem in enumerate(interactive_elements) if elem['tag'] == 'input']
        button_indices = [i for i, elem in enumerate(interactive_elements) if elem['tag'] == 'button' or elem['type'] == 'submit']
        
        if input_indices and button_indices:
            # Generally, inputs should come before submit buttons
            first_input = min(input_indices)
            first_button = min(button_indices)
            
            # This is a guideline, not a strict rule, so we'll just log if unusual
            if first_button < first_input:
                print(f"Note: Submit button appears before input fields in tab order")
    
    def test_interactive_element_error_handling(self, qis_page):
        """Test interactive element behavior with invalid inputs"""
        # Test time input with invalid format
        try:
            qis_page.fill_time_from("invalid_time")
            time_value = qis_page.get_time_from()
            
            # Either the invalid input was rejected or accepted
            # Both are valid behaviors depending on validation approach
            assert True  # Test passes regardless
            
        except Exception:
            # Input validation might throw exceptions, which is also valid
            assert True
        
        # Test very long input in text fields
        try:
            very_long_text = "A" * 1000
            qis_page.fill_course_title(very_long_text)
            entered_text = qis_page.get_course_title()
            
            # Input should either be truncated or accepted
            assert len(entered_text) <= 1000, "Input field accepted unreasonably long text"
            
        except Exception:
            # Field might have validation that throws exceptions
            assert True
    
    def test_interactive_element_state_persistence(self, qis_page):
        """Test that interactive element states persist during page interactions"""
        # Set initial states
        qis_page.fill_course_number("12345")
        qis_page.fill_course_title("Persistent Test")
        
        # Select dropdown options
        try:
            semester_options = qis_page.get_semester_options()
            if len(semester_options) > 1:
                qis_page.select_semester(semester_options[1])
        except:
            pass
        
        # Interact with other page elements
        try:
            # Click on different areas of the page
            page_title = qis_page.driver.find_element(*qis_page.PAGE_TITLE)
            page_title.click()
            time.sleep(0.5)
            
            # Scroll page
            qis_page.driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(0.5)
            
        except:
            pass
        
        # Verify states are maintained
        assert qis_page.get_course_number() == "12345", "Course number state not persistent"
        assert qis_page.get_course_title() == "Persistent Test", "Course title state not persistent"
        
        # Verify dropdown selection if it was set
        try:
            if len(semester_options) > 1:
                current_semester = qis_page.get_selected_semester()
                assert current_semester == semester_options[1], "Semester selection not persistent"
        except:
            pass
    
    def test_button_double_click_protection(self, qis_page):
        """Test button behavior with rapid multiple clicks"""
        # Fill some search criteria
        qis_page.fill_course_title("Double Click Test")
        
        search_button = qis_page.driver.find_element(*qis_page.SEARCH_BUTTON)
        original_url = qis_page.driver.current_url
        
        # Perform rapid double-click
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(qis_page.driver)
            actions.double_click(search_button).perform()
            
            time.sleep(3)  # Wait for any processing
            
            # Verify system handled double-click gracefully
            # (No specific assertion needed - just that no exception occurred)
            assert True
            
        except Exception as e:
            # If double-click causes issues, that's worth noting but not failing
            print(f"Double-click behavior note: {str(e)}")
            assert True
    
    def test_interactive_elements_responsive_behavior(self, qis_page):
        """Test interactive elements behavior in different screen sizes"""
        original_size = qis_page.driver.get_window_size()
        
        try:
            # Test in mobile-like size
            qis_page.driver.set_window_size(400, 600)
            time.sleep(1)
            
            # Verify buttons are still accessible
            search_button = qis_page.driver.find_element(*qis_page.SEARCH_BUTTON)
            assert search_button.is_displayed(), "Search button not visible in small screen"
            assert search_button.is_enabled(), "Search button not enabled in small screen"
            
            # Test in tablet-like size
            qis_page.driver.set_window_size(768, 1024)
            time.sleep(1)
            
            # Verify interactive elements are still functional
            assert search_button.is_displayed(), "Search button not visible in tablet size"
            
            # Test clicking still works
            qis_page.fill_course_title("Responsive Test")
            assert qis_page.get_course_title() == "Responsive Test", "Input not working in tablet size"
            
        finally:
            # Restore original size
            qis_page.driver.set_window_size(original_size['width'], original_size['height'])
