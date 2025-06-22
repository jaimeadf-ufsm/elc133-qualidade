import pytest
import time
from utilities.settings import Settings
from pages.qis_search_page import QISSearchPage

@pytest.fixture
def qis_page(driver):
    """Fixture to create QIS search page instance"""
    page = QISSearchPage(driver)
    page.go_to(Settings.QIS_SEARCH_URL)
    return page

class TestFormInputComponents:
    """Test class for form input components on QIS search page"""
    
    def test_course_number_input_presence(self, qis_page):
        """Test that course number input field is present and visible"""
        # Verify the input field exists
        course_number_input = qis_page.driver.find_element(*qis_page.COURSE_NUMBER_INPUT)
        assert course_number_input is not None
        
        # Verify the input field is displayed
        assert course_number_input.is_displayed()
        
        # Verify the input field is enabled
        assert course_number_input.is_enabled()
    
    def test_course_number_input_functionality(self, qis_page):
        """Test course number input field functionality"""
        test_course_number = "12345"
        
        # Fill the course number
        qis_page.fill_course_number(test_course_number)
        
        # Verify the value was set correctly
        assert qis_page.get_course_number() == test_course_number
        
        # Test clearing the field
        qis_page.fill_course_number("")
        assert qis_page.get_course_number() == ""
    
    def test_course_number_input_validation(self, qis_page):
        """Test course number input field validation and edge cases"""
        # Test with numeric input
        qis_page.fill_course_number("123456")
        assert qis_page.get_course_number() == "123456"
        
        # Test with alphanumeric input
        qis_page.fill_course_number("ABC123")
        assert qis_page.get_course_number() == "ABC123"
        
        # Test with special characters
        qis_page.fill_course_number("123-456")
        assert qis_page.get_course_number() == "123-456"
        
        # Test with long input
        long_input = "A" * 50
        qis_page.fill_course_number(long_input)
        entered_value = qis_page.get_course_number()
        assert len(entered_value) <= 50  # Assuming there might be a length limit
    
    def test_course_title_input_presence(self, qis_page):
        """Test that course title input field is present and visible"""
        course_title_input = qis_page.driver.find_element(*qis_page.COURSE_TITLE_INPUT)
        assert course_title_input is not None
        assert course_title_input.is_displayed()
        assert course_title_input.is_enabled()
    
    def test_course_title_input_functionality(self, qis_page):
        """Test course title input field functionality"""
        test_title = "Mathematik"
        
        # Fill the course title
        qis_page.fill_course_title(test_title)
        
        # Verify the value was set correctly
        assert qis_page.get_course_title() == test_title
        
        # Test clearing the field
        qis_page.fill_course_title("")
        assert qis_page.get_course_title() == ""
    
    def test_course_title_multilingual_support(self, qis_page):
        """Test course title input field with multilingual content"""
        # Test with German umlauts
        german_title = "Einführung in die Informatik"
        qis_page.fill_course_title(german_title)
        assert qis_page.get_course_title() == german_title
        
        # Test with English title
        english_title = "Introduction to Computer Science"
        qis_page.fill_course_title(english_title)
        assert qis_page.get_course_title() == english_title
        
        # Test with special characters
        special_title = "Mathematik & Physik (Grundlagen)"
        qis_page.fill_course_title(special_title)
        assert qis_page.get_course_title() == special_title
    
    def test_instructor_input_presence(self, qis_page):
        """Test that instructor input field is present and visible"""
        instructor_input = qis_page.driver.find_element(*qis_page.INSTRUCTOR_INPUT)
        assert instructor_input is not None
        assert instructor_input.is_displayed()
        assert instructor_input.is_enabled()
    
    def test_instructor_input_functionality(self, qis_page):
        """Test instructor input field functionality"""
        test_instructor = "Prof. Dr. Schmidt"
        
        # Fill the instructor field
        qis_page.fill_instructor(test_instructor)
        
        # Verify the value was set correctly
        assert qis_page.get_instructor() == test_instructor
        
        # Test clearing the field
        qis_page.fill_instructor("")
        assert qis_page.get_instructor() == ""
    
    def test_instructor_input_name_formats(self, qis_page):
        """Test instructor input with different name formats"""
        # Test with title and full name
        full_name = "Prof. Dr. Hans-Peter Müller"
        qis_page.fill_instructor(full_name)
        assert qis_page.get_instructor() == full_name
        
        # Test with simple name
        simple_name = "Schmidt"
        qis_page.fill_instructor(simple_name)
        assert qis_page.get_instructor() == simple_name
        
        # Test with first and last name
        first_last = "Anna Weber"
        qis_page.fill_instructor(first_last)
        assert qis_page.get_instructor() == first_last
    
    def test_room_input_presence(self, qis_page):
        """Test that room input field is present and visible"""
        room_input = qis_page.driver.find_element(*qis_page.ROOM_INPUT)
        assert room_input is not None
        assert room_input.is_displayed()
        assert room_input.is_enabled()
    
    def test_room_input_functionality(self, qis_page):
        """Test room input field functionality"""
        test_room = "A101"
        
        # Fill the room field
        qis_page.fill_room(test_room)
        
        # Verify the value was set correctly
        assert qis_page.get_room() == test_room
        
        # Test clearing the field
        qis_page.fill_room("")
        assert qis_page.get_room() == ""
    
    def test_room_input_formats(self, qis_page):
        """Test room input with different room code formats"""
        # Test with building and room number
        room_code1 = "Building-A-101"
        qis_page.fill_room(room_code1)
        assert qis_page.get_room() == room_code1
        
        # Test with simple room number
        room_code2 = "205"
        qis_page.fill_room(room_code2)
        assert qis_page.get_room() == room_code2
        
        # Test with complex room code
        room_code3 = "HS-1.234"
        qis_page.fill_room(room_code3)
        assert qis_page.get_room() == room_code3
    
    def test_time_from_input_presence(self, qis_page):
        """Test that time from input field is present and visible"""
        time_input = qis_page.driver.find_element(*qis_page.TIME_FROM_INPUT)
        assert time_input is not None
        assert time_input.is_displayed()
        assert time_input.is_enabled()
    
    def test_time_from_input_functionality(self, qis_page):
        """Test time from input field functionality"""
        test_time = "09:00"
        
        # Fill the time field
        qis_page.fill_time_from(test_time)
        
        # Verify the value was set correctly
        assert qis_page.get_time_from() == test_time
        
        # Test clearing the field
        qis_page.fill_time_from("")
        assert qis_page.get_time_from() == ""
    
    def test_time_from_input_formats(self, qis_page):
        """Test time from input with different time formats"""
        # Test with HH:MM format
        time1 = "14:30"
        qis_page.fill_time_from(time1)
        assert qis_page.get_time_from() == time1
        
        # Test with single digit hour
        time2 = "8:00"
        qis_page.fill_time_from(time2)
        entered_time = qis_page.get_time_from()
        # Accept both "8:00" and "08:00" as valid
        assert entered_time in ["8:00", "08:00"]
        
        # Test with edge case times
        time3 = "23:59"
        qis_page.fill_time_from(time3)
        assert qis_page.get_time_from() == time3
    
    def test_all_inputs_clear_functionality(self, qis_page):
        """Test clearing all input fields at once"""
        # Fill all input fields
        qis_page.fill_course_number("12345")
        qis_page.fill_course_title("Test Course")
        qis_page.fill_instructor("Test Instructor")
        qis_page.fill_room("A101")
        qis_page.fill_time_from("10:00")
        
        # Verify all fields have values
        assert qis_page.get_course_number() != ""
        assert qis_page.get_course_title() != ""
        assert qis_page.get_instructor() != ""
        assert qis_page.get_room() != ""
        assert qis_page.get_time_from() != ""
        
        # Clear all inputs
        qis_page.clear_all_inputs()
        
        # Verify all fields are cleared
        assert qis_page.get_course_number() == ""
        assert qis_page.get_course_title() == ""
        assert qis_page.get_instructor() == ""
        assert qis_page.get_room() == ""
        assert qis_page.get_time_from() == ""
    
    def test_input_fields_persistence_after_page_interaction(self, qis_page):
        """Test that input values persist during page interactions"""
        # Fill some input fields
        test_values = {
            'course_number': '54321',
            'course_title': 'Persistent Test',
            'instructor': 'Dr. Test'
        }
        
        qis_page.fill_course_number(test_values['course_number'])
        qis_page.fill_course_title(test_values['course_title'])
        qis_page.fill_instructor(test_values['instructor'])
        
        # Interact with other page elements (e.g., click on a dropdown)
        try:
            semester_select = qis_page.driver.find_element(*qis_page.SEMESTER_SELECT)
            semester_select.click()
            time.sleep(0.5)  # Brief pause for any dynamic behavior
        except:
            pass  # Continue test even if dropdown interaction fails
        
        # Verify input values are still present
        assert qis_page.get_course_number() == test_values['course_number']
        assert qis_page.get_course_title() == test_values['course_title']
        assert qis_page.get_instructor() == test_values['instructor']
