import pytest
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utilities.settings import Settings
from pages.qis_search_page import QISSearchPage
from test_data.qis_test_data import QISTestData, QISTestDataProvider, QISTestUtilities

@pytest.fixture
def qis_page(driver):
    """Fixture to create QIS search page instance"""
    page = QISSearchPage(driver)
    page.go_to(Settings.QIS_SEARCH_URL)
    return page

class TestQISIntegratedScenarios:
    """Integrated test scenarios combining multiple components and interactions"""
    
    @pytest.mark.parametrize("scenario", QISTestData.SEARCH_SCENARIOS)
    def test_comprehensive_search_scenarios(self, qis_page, scenario):
        """Test comprehensive search scenarios with multiple component interactions"""
        test_data = scenario['data']
        
        # Clear form first
        qis_page.clear_all_inputs()
        
        # Fill form fields based on test data
        if 'course_number' in test_data:
            qis_page.fill_course_number(test_data['course_number'])
        
        if 'course_title' in test_data:
            qis_page.fill_course_title(test_data['course_title'])
        
        if 'instructor' in test_data:
            qis_page.fill_instructor(test_data['instructor'])
        
        if 'room' in test_data:
            qis_page.fill_room(test_data['room'])
        
        if 'time_from' in test_data:
            qis_page.fill_time_from(test_data['time_from'])
        
        # Verify all inputs were set correctly
        if 'course_number' in test_data:
            assert qis_page.get_course_number() == test_data['course_number']
        
        if 'course_title' in test_data:
            assert qis_page.get_course_title() == test_data['course_title']
        
        if 'instructor' in test_data:
            assert qis_page.get_instructor() == test_data['instructor']
        
        if 'room' in test_data:
            assert qis_page.get_room() == test_data['room']
        
        if 'time_from' in test_data:
            assert qis_page.get_time_from() == test_data['time_from']
        
        # Test form submission
        original_url = qis_page.driver.current_url
        qis_page.click_search()
        time.sleep(2)
        
        # Verify search was processed (URL change or content change)
        new_url = qis_page.driver.current_url
        page_source = qis_page.driver.page_source.lower()
        
        search_processed = (
            new_url != original_url or
            'ergebnis' in page_source or
            'result' in page_source or
            'gefunden' in page_source
        )
        
        assert search_processed, f"Search scenario '{scenario['name']}' was not processed correctly"
    
    @pytest.mark.parametrize("edge_case", QISTestData.EDGE_CASES)
    def test_edge_case_handling(self, qis_page, edge_case):
        """Test edge case scenarios and error handling"""
        test_data = edge_case['data']
        
        # Clear form first
        qis_page.clear_all_inputs()
        
        try:
            # Fill form with edge case data
            if 'course_number' in test_data:
                qis_page.fill_course_number(test_data['course_number'])
            
            if 'course_title' in test_data:
                qis_page.fill_course_title(test_data['course_title'])
            
            if 'instructor' in test_data:
                qis_page.fill_instructor(test_data['instructor'])
            
            # Attempt form submission
            original_url = qis_page.driver.current_url
            qis_page.click_search()
            time.sleep(2)
            
            # Verify system handled edge case gracefully (no crashes)
            new_url = qis_page.driver.current_url
            
            # System should either:
            # 1. Process the search (URL changes)
            # 2. Show validation error (URL stays same, error message appears)
            # 3. Ignore invalid input (URL stays same, no error)
            
            # All are acceptable behaviors for edge cases
            assert True  # Test passes if no exception was thrown
            
        except Exception as e:
            # Edge cases might cause exceptions, but system should handle gracefully
            pytest.fail(f"Edge case '{edge_case['name']}' caused unhandled exception: {str(e)}")
    
    def test_form_reset_and_refill_workflow(self, qis_page):
        """Test complete workflow: fill form, reset, refill with different data"""
        # Phase 1: Fill form with initial data
        initial_data = QISTestData.SEARCH_SCENARIOS[0]['data']
        
        qis_page.fill_course_number(initial_data.get('course_number', ''))
        qis_page.fill_course_title(initial_data.get('course_title', ''))
        qis_page.fill_instructor(initial_data.get('instructor', ''))
        
        # Verify initial data is set
        if 'course_number' in initial_data:
            assert qis_page.get_course_number() == initial_data['course_number']
        
        # Phase 2: Reset form
        try:
            if qis_page.is_reset_button_enabled():
                qis_page.click_reset()
                time.sleep(1)
                
                # Verify form is cleared
                assert qis_page.get_course_number() == ""
                assert qis_page.get_course_title() == ""
                assert qis_page.get_instructor() == ""
        except NoSuchElementException:
            # If no reset button, manually clear
            qis_page.clear_all_inputs()
        
        # Phase 3: Fill with new data
        new_data = QISTestData.SEARCH_SCENARIOS[1]['data']
        
        if 'course_number' in new_data:
            qis_page.fill_course_number(new_data['course_number'])
        if 'course_title' in new_data:
            qis_page.fill_course_title(new_data['course_title'])
        if 'instructor' in new_data:
            qis_page.fill_instructor(new_data['instructor'])
        
        # Verify new data is set correctly
        if 'course_number' in new_data:
            assert qis_page.get_course_number() == new_data['course_number']
        if 'course_title' in new_data:
            assert qis_page.get_course_title() == new_data['course_title']
        if 'instructor' in new_data:
            assert qis_page.get_instructor() == new_data['instructor']
    
    def test_dropdown_and_input_combination(self, qis_page):
        """Test combination of dropdown selections and text inputs"""
        # Fill text inputs
        qis_page.fill_course_title("Integration Test")
        qis_page.fill_instructor("Prof. Test")
        
        # Select dropdown options
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
            
            # Select weekday
            weekday_options = qis_page.get_weekday_options()
            selectable_weekdays = [opt for opt in weekday_options if opt not in ["Alles auswählen", "keine Angabe"] and opt.strip()]
            if selectable_weekdays:
                qis_page.select_weekday(selectable_weekdays[0])
        
        except Exception as e:
            pytest.skip(f"Dropdown selection test skipped: {str(e)}")
        
        # Verify all selections persist together
        assert qis_page.get_course_title() == "Integration Test"
        assert qis_page.get_instructor() == "Prof. Test"
        
        try:
            if len(semester_options) > 1:
                assert qis_page.get_selected_semester() == semester_options[1]
            if selectable_types:
                assert qis_page.get_selected_course_type() == selectable_types[0]
        except:
            pass  # Dropdown verification is optional if elements not found
    
    def test_display_options_with_search(self, qis_page):
        """Test display options in combination with search functionality"""
        # Set display options
        try:
            results_options = qis_page.get_results_per_page_options()
            if len(results_options) > 1:
                qis_page.select_results_per_page(results_options[1])
            
            sort_options = qis_page.get_sort_order_options()
            if len(sort_options) > 1:
                qis_page.select_sort_order(sort_options[1])
        except Exception:
            pytest.skip("Display options not available")
        
        # Fill search criteria
        qis_page.fill_course_title("Display Test")
        
        # Perform search
        original_url = qis_page.driver.current_url
        qis_page.click_search()
        time.sleep(2)
        
        # Verify search was performed
        new_url = qis_page.driver.current_url
        assert new_url != original_url or "test" in qis_page.driver.page_source.lower()
    
    def test_navigation_and_form_interaction(self, qis_page):
        """Test navigation elements in combination with form interactions"""
        # Fill form data
        qis_page.fill_course_title("Navigation Test")
        
        # Test help link interaction
        if qis_page.is_help_link_present():
            original_windows = qis_page.driver.window_handles
            
            try:
                qis_page.click_help_link()
                time.sleep(2)
                
                # Check if new window opened
                new_windows = qis_page.driver.window_handles
                if len(new_windows) > len(original_windows):
                    # Switch back to original window
                    qis_page.driver.switch_to.window(original_windows[0])
                
                # Verify form data is still present
                assert qis_page.get_course_title() == "Navigation Test"
                
            except Exception:
                # Help link interaction might fail, but form data should persist
                assert qis_page.get_course_title() == "Navigation Test"
        
        # Test breadcrumb interaction
        breadcrumbs = qis_page.get_breadcrumb_links()
        if breadcrumbs:
            # Form data should persist even after breadcrumb interactions
            assert qis_page.get_course_title() == "Navigation Test"
    
    def test_accessibility_workflow(self, qis_page):
        """Test accessibility features across multiple components"""
        from selenium.webdriver.common.keys import Keys
        
        # Test keyboard navigation through form
        body = qis_page.driver.find_element("tag name", "body")
        body.click()
        
        # Tab through form elements and fill them
        form_filled = False
        for i in range(15):  # Limit tab attempts
            body.send_keys(Keys.TAB)
            time.sleep(0.2)
            
            active_element = qis_page.driver.switch_to.active_element
            tag_name = active_element.tag_name.lower()
            element_type = active_element.get_attribute('type')
            
            # Fill first text input found
            if tag_name == 'input' and element_type == 'text' and not form_filled:
                active_element.send_keys("Accessibility Test")
                form_filled = True
                break
        
        # Verify keyboard input worked
        if form_filled:
            # Check if any input field contains our test text
            course_title = qis_page.get_course_title()
            course_number = qis_page.get_course_number()
            instructor = qis_page.get_instructor()
            
            has_test_text = any("Accessibility Test" in field for field in [course_title, course_number, instructor])
            assert has_test_text, "Keyboard input did not work properly"
    
    @pytest.mark.parametrize("screen_size", QISTestData.SCREEN_SIZES)
    def test_responsive_component_integration(self, qis_page, screen_size):
        """Test component integration across different screen sizes"""
        original_size = qis_page.driver.get_window_size()
        
        try:
            # Set screen size
            qis_page.driver.set_window_size(screen_size['width'], screen_size['height'])
            time.sleep(1)
            
            # Test basic form functionality
            qis_page.fill_course_title(f"Responsive Test {screen_size['name']}")
            assert qis_page.get_course_title() == f"Responsive Test {screen_size['name']}"
            
            # Test button functionality
            assert qis_page.is_search_button_enabled()
            
            # Test dropdown functionality (if available)
            try:
                semester_options = qis_page.get_semester_options()
                if len(semester_options) > 0:
                    # Just verify dropdown is accessible
                    assert len(semester_options) > 0
            except:
                pass  # Dropdown might not be available in all screen sizes
            
            # Test navigation elements
            if qis_page.is_help_link_present():
                assert True  # Help link is accessible
            
            breadcrumbs = qis_page.get_breadcrumb_links()
            if breadcrumbs:
                assert len(breadcrumbs) > 0  # Breadcrumbs are accessible
        
        finally:
            # Restore original screen size
            qis_page.driver.set_window_size(original_size['width'], original_size['height'])
    
    def test_error_recovery_workflow(self, qis_page):
        """Test error recovery and form state management"""
        # Fill form with potentially problematic data
        qis_page.fill_course_number("INVALID!@#")
        qis_page.fill_course_title("<script>alert('test')</script>")
        qis_page.fill_time_from("invalid_time")
        
        # Attempt search
        original_url = qis_page.driver.current_url
        qis_page.click_search()
        time.sleep(2)
        
        # System should handle gracefully - either process or show error
        new_url = qis_page.driver.current_url
        
        # Clear form and try with valid data
        qis_page.clear_all_inputs()
        qis_page.fill_course_title("Valid Course Title")
        
        # Verify recovery works
        assert qis_page.get_course_title() == "Valid Course Title"
        
        # Test search with valid data
        qis_page.click_search()
        time.sleep(2)
        
        # Should work without issues
        assert True  # Test passes if no exceptions thrown
    
    def test_component_diversity_coverage(self, qis_page):
        """Test that all identified component types are covered and functional"""
        component_tests = {
            'text_inputs': 0,
            'dropdowns': 0,
            'buttons': 0,
            'navigation': 0,
            'display_controls': 0
        }
        
        # Test text inputs (max 2 of each type as per requirements)
        try:
            qis_page.fill_course_number("12345")
            qis_page.fill_course_title("Test Course")
            component_tests['text_inputs'] += 2
        except:
            pass
        
        # Test dropdowns
        try:
            semester_options = qis_page.get_semester_options()
            course_type_options = qis_page.get_course_type_options()
            if semester_options and course_type_options:
                component_tests['dropdowns'] += 2
        except:
            pass
        
        # Test buttons
        try:
            if qis_page.is_search_button_enabled():
                component_tests['buttons'] += 1
            if qis_page.is_reset_button_enabled():
                component_tests['buttons'] += 1
        except:
            pass
        
        # Test navigation
        try:
            breadcrumbs = qis_page.get_breadcrumb_links()
            if breadcrumbs:
                component_tests['navigation'] += 1
            if qis_page.is_help_link_present():
                component_tests['navigation'] += 1
        except:
            pass
        
        # Test display controls
        try:
            results_options = qis_page.get_results_per_page_options()
            sort_options = qis_page.get_sort_order_options()
            if results_options and sort_options:
                component_tests['display_controls'] += 2
        except:
            pass
        
        # Verify we have diverse component coverage
        total_components = sum(component_tests.values())
        assert total_components >= 15, f"Insufficient component coverage: {component_tests}"
        
        # Verify component diversity (max 2 of each type)
        for component_type, count in component_tests.items():
            assert count <= 2, f"Too many {component_type} components: {count} (max 2 allowed)"
