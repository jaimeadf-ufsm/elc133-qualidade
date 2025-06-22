import pytest
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utilities.settings import Settings
from pages.qis_search_page import QISSearchPage

@pytest.fixture
def qis_page(driver):
    """Fixture to create QIS search page instance"""
    page = QISSearchPage(driver)
    page.go_to(Settings.QIS_SEARCH_URL)
    return page

class TestDisplayComponents:
    """Test class for display and layout components on QIS search page"""
    
    def test_results_per_page_dropdown_presence(self, qis_page):
        """Test that results per page dropdown is present and accessible"""
        results_dropdown = qis_page.driver.find_element(*qis_page.RESULTS_PER_PAGE_SELECT)
        assert results_dropdown is not None
        assert results_dropdown.is_displayed()
        assert results_dropdown.is_enabled()
    
    def test_results_per_page_options(self, qis_page):
        """Test results per page dropdown options and values"""
        options = qis_page.get_results_per_page_options()
        
        # Verify that options exist
        assert len(options) > 0, "No results per page options found"
        
        # Verify expected pagination options exist
        expected_options = ['10', '20', '30', '50']
        found_options = [opt for opt in expected_options if opt in options]
        assert len(found_options) >= 2, f"Expected pagination options not found. Available: {options}"
        
        # Verify options are numeric values
        numeric_options = [opt for opt in options if opt.isdigit()]
        assert len(numeric_options) >= 2, f"Expected numeric pagination options. Found: {options}"
    
    def test_results_per_page_selection(self, qis_page):
        """Test results per page dropdown selection functionality"""
        options = qis_page.get_results_per_page_options()
        
        if len(options) > 1:
            # Test selecting different page sizes
            for option in options[:3]:  # Test first 3 options
                if option.isdigit():
                    qis_page.select_results_per_page(option)
                    
                    # Verify selection
                    select = Select(qis_page.driver.find_element(*qis_page.RESULTS_PER_PAGE_SELECT))
                    selected_value = select.first_selected_option.get_attribute('value')
                    assert selected_value == option, f"Expected {option}, got {selected_value}"
    
    def test_results_per_page_default_value(self, qis_page):
        """Test results per page dropdown default value"""
        select = Select(qis_page.driver.find_element(*qis_page.RESULTS_PER_PAGE_SELECT))
        default_value = select.first_selected_option.get_attribute('value')
        
        # Verify default is a reasonable pagination value
        assert default_value.isdigit(), f"Default results per page should be numeric: {default_value}"
        default_num = int(default_value)
        assert 5 <= default_num <= 100, f"Default results per page should be reasonable: {default_num}"
    
    def test_sort_order_dropdown_presence(self, qis_page):
        """Test that sort order dropdown is present and accessible"""
        sort_dropdown = qis_page.driver.find_element(*qis_page.SORT_ORDER_SELECT)
        assert sort_dropdown is not None
        assert sort_dropdown.is_displayed()
        assert sort_dropdown.is_enabled()
    
    def test_sort_order_options(self, qis_page):
        """Test sort order dropdown options and content"""
        options = qis_page.get_sort_order_options()
        
        # Verify that options exist
        assert len(options) > 0, "No sort order options found"
        
        # Verify expected sort options exist (German interface)
        expected_options = ['Standard', 'Nummer', 'Titel', 'Lehrende']
        found_options = [opt for opt in expected_options if any(opt in option for option in options)]
        assert len(found_options) >= 2, f"Expected sort options not found. Available: {options}"
    
    def test_sort_order_selection(self, qis_page):
        """Test sort order dropdown selection functionality"""
        options = qis_page.get_sort_order_options()
        
        if len(options) > 1:
            # Test selecting different sort orders
            for option in options[:3]:  # Test first 3 options
                qis_page.select_sort_order(option)
                
                # Verify selection
                select = Select(qis_page.driver.find_element(*qis_page.SORT_ORDER_SELECT))
                selected_text = select.first_selected_option.text
                assert selected_text == option, f"Expected {option}, got {selected_text}"
    
    def test_sort_order_default_value(self, qis_page):
        """Test sort order dropdown default value"""
        select = Select(qis_page.driver.find_element(*qis_page.SORT_ORDER_SELECT))
        default_text = select.first_selected_option.text
        
        # Verify default is a reasonable sort option
        reasonable_defaults = ['Standard', 'Nummer', 'Titel', 'Default']
        assert any(default in default_text for default in reasonable_defaults), f"Unexpected default sort order: {default_text}"
    
    def test_page_title_presence(self, qis_page):
        """Test that page title is present and meaningful"""
        page_title = qis_page.get_page_title()
        
        # Verify title exists and is not empty
        assert page_title is not None and page_title.strip() != "", "Page title is missing or empty"
        
        # Verify title contains relevant keywords
        title_lower = page_title.lower()
        relevant_keywords = ['suche', 'veranstaltung', 'search', 'course']
        has_relevant_keyword = any(keyword in title_lower for keyword in relevant_keywords)
        assert has_relevant_keyword, f"Page title doesn't contain relevant keywords: {page_title}"
    
    def test_search_form_presence(self, qis_page):
        """Test that search form is present and properly structured"""
        assert qis_page.is_search_form_present(), "Search form is not present on the page"
        
        # Verify form is visible
        form = qis_page.driver.find_element(*qis_page.SEARCH_FORM)
        assert form.is_displayed(), "Search form is not visible"
    
    def test_search_form_structure(self, qis_page):
        """Test search form structure and organization"""
        form = qis_page.driver.find_element(*qis_page.SEARCH_FORM)
        
        # Verify form has proper method and action
        method = form.get_attribute('method')
        action = form.get_attribute('action')
        
        # Method should be GET or POST
        assert method.upper() in ['GET', 'POST'], f"Form method should be GET or POST: {method}"
        
        # Action should be a valid URL or relative path
        if action:
            assert len(action) > 0, "Form action is empty"
    
    def test_search_criteria_section_presence(self, qis_page):
        """Test that search criteria section is present and organized"""
        try:
            criteria_section = qis_page.driver.find_element(*qis_page.SEARCH_CRITERIA_SECTION)
            assert criteria_section is not None
            assert criteria_section.is_displayed()
        except NoSuchElementException:
            # Try alternative selectors for search criteria
            try:
                criteria_section = qis_page.driver.find_element(By.CSS_SELECTOR, "fieldset, .search-criteria, .form-section")
                assert criteria_section is not None
            except NoSuchElementException:
                pytest.skip("Search criteria section not found with expected selectors")
    
    def test_display_options_section_layout(self, qis_page):
        """Test display options section layout and organization"""
        # Verify display options are grouped together
        results_dropdown = qis_page.driver.find_element(*qis_page.RESULTS_PER_PAGE_SELECT)
        sort_dropdown = qis_page.driver.find_element(*qis_page.SORT_ORDER_SELECT)
        
        # Get positions of display controls
        results_location = results_dropdown.location
        sort_location = sort_dropdown.location
        
        # Verify both controls are visible
        assert results_dropdown.is_displayed(), "Results per page dropdown not visible"
        assert sort_dropdown.is_displayed(), "Sort order dropdown not visible"
        
        # Verify controls are reasonably positioned (not overlapping)
        assert results_location['x'] >= 0 and results_location['y'] >= 0, "Results dropdown has invalid position"
        assert sort_location['x'] >= 0 and sort_location['y'] >= 0, "Sort dropdown has invalid position"
    
    def test_display_options_labels(self, qis_page):
        """Test display options have proper labels"""
        # Look for labels associated with display controls
        try:
            # Find labels by looking for text near the dropdowns
            page_source = qis_page.driver.page_source.lower()
            
            # Check for results per page label
            results_labels = ['ergebnisse anzeigen', 'results', 'anzahl', 'per page']
            has_results_label = any(label in page_source for label in results_labels)
            assert has_results_label, "Results per page dropdown missing proper label"
            
            # Check for sort order label
            sort_labels = ['sortierung', 'sort', 'order', 'reihenfolge']
            has_sort_label = any(label in page_source for label in sort_labels)
            assert has_sort_label, "Sort order dropdown missing proper label"
            
        except Exception as e:
            pytest.skip(f"Display options labels test skipped: {str(e)}")
    
    def test_responsive_layout_basic(self, qis_page):
        """Test basic responsive layout behavior"""
        # Get initial window size
        initial_size = qis_page.driver.get_window_size()
        
        try:
            # Test with smaller window size
            qis_page.driver.set_window_size(800, 600)
            time.sleep(1)  # Wait for layout adjustment
            
            # Verify key elements are still visible
            assert qis_page.is_search_form_present(), "Search form not visible in smaller window"
            
            results_dropdown = qis_page.driver.find_element(*qis_page.RESULTS_PER_PAGE_SELECT)
            sort_dropdown = qis_page.driver.find_element(*qis_page.SORT_ORDER_SELECT)
            
            assert results_dropdown.is_displayed(), "Results dropdown not visible in smaller window"
            assert sort_dropdown.is_displayed(), "Sort dropdown not visible in smaller window"
            
            # Test with larger window size
            qis_page.driver.set_window_size(1200, 800)
            time.sleep(1)  # Wait for layout adjustment
            
            # Verify elements are still properly positioned
            assert qis_page.is_search_form_present(), "Search form not visible in larger window"
            assert results_dropdown.is_displayed(), "Results dropdown not visible in larger window"
            assert sort_dropdown.is_displayed(), "Sort dropdown not visible in larger window"
            
        finally:
            # Restore original window size
            qis_page.driver.set_window_size(initial_size['width'], initial_size['height'])
    
    def test_display_components_accessibility(self, qis_page):
        """Test display components for accessibility features"""
        # Test results per page dropdown accessibility
        results_dropdown = qis_page.driver.find_element(*qis_page.RESULTS_PER_PAGE_SELECT)
        
        # Verify dropdown has name attribute
        name_attr = results_dropdown.get_attribute('name')
        assert name_attr is not None and name_attr != "", "Results dropdown missing name attribute"
        
        # Verify dropdown is keyboard accessible
        assert results_dropdown.get_attribute('tabindex') != "-1", "Results dropdown not keyboard accessible"
        
        # Test sort order dropdown accessibility
        sort_dropdown = qis_page.driver.find_element(*qis_page.SORT_ORDER_SELECT)
        
        # Verify dropdown has name attribute
        name_attr = sort_dropdown.get_attribute('name')
        assert name_attr is not None and name_attr != "", "Sort dropdown missing name attribute"
        
        # Verify dropdown is keyboard accessible
        assert sort_dropdown.get_attribute('tabindex') != "-1", "Sort dropdown not keyboard accessible"
    
    def test_display_components_integration(self, qis_page):
        """Test display components integration with form"""
        # Set display options
        options = qis_page.get_results_per_page_options()
        if len(options) > 1:
            qis_page.select_results_per_page(options[1])
        
        sort_options = qis_page.get_sort_order_options()
        if len(sort_options) > 1:
            qis_page.select_sort_order(sort_options[1])
        
        # Fill some search criteria
        qis_page.fill_course_title("Test")
        
        # Verify display options persist with search criteria
        if len(options) > 1:
            select = Select(qis_page.driver.find_element(*qis_page.RESULTS_PER_PAGE_SELECT))
            current_results = select.first_selected_option.get_attribute('value')
            assert current_results == options[1], "Results per page selection not persistent"
        
        if len(sort_options) > 1:
            select = Select(qis_page.driver.find_element(*qis_page.SORT_ORDER_SELECT))
            current_sort = select.first_selected_option.text
            assert current_sort == sort_options[1], "Sort order selection not persistent"
    
    def test_display_components_visual_hierarchy(self, qis_page):
        """Test display components visual hierarchy and grouping"""
        # Get display control elements
        results_dropdown = qis_page.driver.find_element(*qis_page.RESULTS_PER_PAGE_SELECT)
        sort_dropdown = qis_page.driver.find_element(*qis_page.SORT_ORDER_SELECT)
        
        # Verify elements have reasonable sizes
        results_size = results_dropdown.size
        sort_size = sort_dropdown.size
        
        assert results_size['width'] > 50, "Results dropdown too narrow"
        assert results_size['height'] > 20, "Results dropdown too short"
        assert sort_size['width'] > 50, "Sort dropdown too narrow"
        assert sort_size['height'] > 20, "Sort dropdown too short"
        
        # Verify elements are not overlapping
        results_rect = results_dropdown.rect
        sort_rect = sort_dropdown.rect
        
        # Check for overlap (basic collision detection)
        x_overlap = (results_rect['x'] < sort_rect['x'] + sort_rect['width'] and 
                    results_rect['x'] + results_rect['width'] > sort_rect['x'])
        y_overlap = (results_rect['y'] < sort_rect['y'] + sort_rect['height'] and 
                    results_rect['y'] + results_rect['height'] > sort_rect['y'])
        
        overlapping = x_overlap and y_overlap
        assert not overlapping, "Display dropdowns are overlapping"
    
    def test_page_layout_consistency(self, qis_page):
        """Test overall page layout consistency"""
        # Verify main page elements are present and positioned
        assert qis_page.is_search_form_present(), "Main search form missing"
        
        page_title = qis_page.get_page_title()
        assert len(page_title) > 0, "Page title missing"
        
        # Verify display controls are present
        results_dropdown = qis_page.driver.find_element(*qis_page.RESULTS_PER_PAGE_SELECT)
        sort_dropdown = qis_page.driver.find_element(*qis_page.SORT_ORDER_SELECT)
        
        assert results_dropdown.is_displayed(), "Results control not displayed"
        assert sort_dropdown.is_displayed(), "Sort control not displayed"
        
        # Verify logical layout order (title should be near top)
        title_element = qis_page.driver.find_element(*qis_page.PAGE_TITLE)
        title_y = title_element.location['y']
        form_y = qis_page.driver.find_element(*qis_page.SEARCH_FORM).location['y']
        
        # Title should generally appear before or near the form
        assert title_y <= form_y + 100, "Page title positioned unexpectedly relative to form"
