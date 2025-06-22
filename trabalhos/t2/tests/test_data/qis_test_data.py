"""
Test data providers and utilities for QIS portal testing
"""

import pytest
from typing import List, Dict, Any

class QISTestData:
    """Test data provider for QIS portal tests"""
    
    # Course number test data
    VALID_COURSE_NUMBERS = [
        "12345",
        "ABC123",
        "123-456",
        "ELC133",
        "MAT001"
    ]
    
    INVALID_COURSE_NUMBERS = [
        "",
        " ",
        "!@#$%",
        "A" * 100  # Very long input
    ]
    
    # Course title test data
    VALID_COURSE_TITLES = [
        "Mathematik",
        "Einführung in die Informatik",
        "Introduction to Computer Science",
        "Mathematik & Physik (Grundlagen)",
        "Qualitätssicherung in der Softwareentwicklung"
    ]
    
    MULTILINGUAL_TITLES = [
        "Einführung in die Informatik",  # German with umlauts
        "Introduction to Computer Science",  # English
        "Mathématiques Appliquées",  # French
        "Física Cuántica",  # Spanish
        "Программирование"  # Cyrillic
    ]
    
    SPECIAL_CHARACTER_TITLES = [
        "C++ Programming",
        "Web 2.0 & Social Media",
        "Data Science (R/Python)",
        "Machine Learning - Advanced Topics",
        "Software Engineering: Theory & Practice"
    ]
    
    # Instructor test data
    VALID_INSTRUCTORS = [
        "Prof. Dr. Schmidt",
        "Dr. Müller",
        "Prof. Hans-Peter Weber",
        "Anna Weber",
        "Schmidt",
        "Prof. Dr. Maria González-López"
    ]
    
    # Room test data
    VALID_ROOMS = [
        "A101",
        "Building-A-101",
        "205",
        "HS-1.234",
        "Lab-Computer-01",
        "Hörsaal 1"
    ]
    
    # Time test data
    VALID_TIMES = [
        "09:00",
        "14:30",
        "8:00",
        "23:59",
        "00:00"
    ]
    
    INVALID_TIMES = [
        "25:00",
        "12:60",
        "abc",
        "12:345",
        ""
    ]
    
    # Dropdown option test scenarios
    SEMESTER_TEST_SCENARIOS = [
        {"description": "Current semester selection", "action": "select_current"},
        {"description": "Future semester selection", "action": "select_future"},
        {"description": "Previous semester selection", "action": "select_previous"}
    ]
    
    COURSE_TYPE_TEST_SCENARIOS = [
        {"type": "Vorlesung", "description": "Lecture course type"},
        {"type": "Seminar", "description": "Seminar course type"},
        {"type": "Übung", "description": "Exercise course type"},
        {"type": "Praktikum", "description": "Practical course type"}
    ]
    
    WEEKDAY_TEST_SCENARIOS = [
        {"days": ["Montag"], "description": "Single weekday selection"},
        {"days": ["Montag", "Mittwoch"], "description": "Multiple weekday selection"},
        {"days": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"], "description": "All weekdays selection"}
    ]
    
    LANGUAGE_TEST_SCENARIOS = [
        {"languages": ["Deutsch"], "description": "German language only"},
        {"languages": ["Englisch"], "description": "English language only"},
        {"languages": ["Deutsch", "Englisch"], "description": "Multiple languages"}
    ]
    
    # Search scenario combinations
    SEARCH_SCENARIOS = [
        {
            "name": "basic_course_search",
            "description": "Basic course number and title search",
            "data": {
                "course_number": "12345",
                "course_title": "Mathematik"
            }
        },
        {
            "name": "instructor_search",
            "description": "Search by instructor name",
            "data": {
                "instructor": "Prof. Dr. Schmidt"
            }
        },
        {
            "name": "room_and_time_search",
            "description": "Search by room and time",
            "data": {
                "room": "A101",
                "time_from": "09:00"
            }
        },
        {
            "name": "comprehensive_search",
            "description": "Search with multiple criteria",
            "data": {
                "course_number": "ELC133",
                "course_title": "Qualitätssicherung",
                "instructor": "Dr. Weber",
                "room": "Lab-01",
                "time_from": "14:00"
            }
        },
        {
            "name": "multilingual_search",
            "description": "Search with multilingual content",
            "data": {
                "course_title": "Einführung in die Informatik"
            }
        }
    ]
    
    # Edge case test data
    EDGE_CASES = [
        {
            "name": "empty_search",
            "description": "Search with all empty fields",
            "data": {}
        },
        {
            "name": "whitespace_only",
            "description": "Search with whitespace-only inputs",
            "data": {
                "course_number": "   ",
                "course_title": "   ",
                "instructor": "   "
            }
        },
        {
            "name": "very_long_inputs",
            "description": "Search with very long inputs",
            "data": {
                "course_number": "A" * 50,
                "course_title": "Very Long Course Title " * 10,
                "instructor": "Professor with Very Long Name " * 5
            }
        },
        {
            "name": "special_characters",
            "description": "Search with special characters",
            "data": {
                "course_number": "!@#$%^&*()",
                "course_title": "<script>alert('test')</script>",
                "instructor": "'; DROP TABLE courses; --"
            }
        }
    ]
    
    # Display option test data
    RESULTS_PER_PAGE_OPTIONS = ["10", "20", "30", "50"]
    SORT_ORDER_OPTIONS = ["Standard", "Nummer", "Titel", "Lehrende/-r"]
    
    # Accessibility test scenarios
    ACCESSIBILITY_SCENARIOS = [
        {
            "name": "keyboard_navigation",
            "description": "Test keyboard-only navigation",
            "keys": ["TAB", "ENTER", "SPACE", "ARROW_DOWN", "ARROW_UP"]
        },
        {
            "name": "screen_reader_compatibility",
            "description": "Test screen reader compatibility",
            "attributes": ["aria-label", "title", "alt", "role"]
        }
    ]
    
    # Browser compatibility test data
    BROWSER_SCENARIOS = [
        {"name": "chrome", "description": "Google Chrome browser"},
        {"name": "firefox", "description": "Mozilla Firefox browser"},
        {"name": "edge", "description": "Microsoft Edge browser"}
    ]
    
    # Responsive design test data
    SCREEN_SIZES = [
        {"name": "mobile", "width": 375, "height": 667, "description": "Mobile phone size"},
        {"name": "tablet", "width": 768, "height": 1024, "description": "Tablet size"},
        {"name": "desktop", "width": 1920, "height": 1080, "description": "Desktop size"},
        {"name": "small_desktop", "width": 1366, "height": 768, "description": "Small desktop size"}
    ]

class QISTestDataProvider:
    """Pytest data provider for QIS tests"""
    
    @staticmethod
    @pytest.fixture(params=QISTestData.VALID_COURSE_NUMBERS)
    def valid_course_number(request):
        """Provide valid course numbers for testing"""
        return request.param
    
    @staticmethod
    @pytest.fixture(params=QISTestData.VALID_COURSE_TITLES)
    def valid_course_title(request):
        """Provide valid course titles for testing"""
        return request.param
    
    @staticmethod
    @pytest.fixture(params=QISTestData.MULTILINGUAL_TITLES)
    def multilingual_title(request):
        """Provide multilingual course titles for testing"""
        return request.param
    
    @staticmethod
    @pytest.fixture(params=QISTestData.VALID_INSTRUCTORS)
    def valid_instructor(request):
        """Provide valid instructor names for testing"""
        return request.param
    
    @staticmethod
    @pytest.fixture(params=QISTestData.VALID_ROOMS)
    def valid_room(request):
        """Provide valid room codes for testing"""
        return request.param
    
    @staticmethod
    @pytest.fixture(params=QISTestData.VALID_TIMES)
    def valid_time(request):
        """Provide valid time formats for testing"""
        return request.param
    
    @staticmethod
    @pytest.fixture(params=QISTestData.SEARCH_SCENARIOS)
    def search_scenario(request):
        """Provide search scenarios for testing"""
        return request.param
    
    @staticmethod
    @pytest.fixture(params=QISTestData.EDGE_CASES)
    def edge_case_scenario(request):
        """Provide edge case scenarios for testing"""
        return request.param
    
    @staticmethod
    @pytest.fixture(params=QISTestData.RESULTS_PER_PAGE_OPTIONS)
    def results_per_page_option(request):
        """Provide results per page options for testing"""
        return request.param
    
    @staticmethod
    @pytest.fixture(params=QISTestData.SORT_ORDER_OPTIONS)
    def sort_order_option(request):
        """Provide sort order options for testing"""
        return request.param
    
    @staticmethod
    @pytest.fixture(params=QISTestData.SCREEN_SIZES)
    def screen_size(request):
        """Provide screen sizes for responsive testing"""
        return request.param

class QISTestUtilities:
    """Utility functions for QIS testing"""
    
    @staticmethod
    def generate_test_combinations(base_data: Dict[str, Any], variations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate test data combinations"""
        combinations = []
        for variation in variations:
            combined_data = {**base_data, **variation}
            combinations.append(combined_data)
        return combinations
    
    @staticmethod
    def validate_search_data(data: Dict[str, Any]) -> bool:
        """Validate search data format"""
        valid_keys = ['course_number', 'course_title', 'instructor', 'room', 'time_from', 'time_to']
        return all(key in valid_keys for key in data.keys())
    
    @staticmethod
    def clean_test_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and normalize test data"""
        cleaned_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                cleaned_data[key] = value.strip()
            else:
                cleaned_data[key] = value
        return cleaned_data
    
    @staticmethod
    def get_random_search_scenario() -> Dict[str, Any]:
        """Get a random search scenario for testing"""
        import random
        return random.choice(QISTestData.SEARCH_SCENARIOS)
    
    @staticmethod
    def get_test_data_by_category(category: str) -> List[Any]:
        """Get test data by category"""
        category_map = {
            'course_numbers': QISTestData.VALID_COURSE_NUMBERS,
            'course_titles': QISTestData.VALID_COURSE_TITLES,
            'instructors': QISTestData.VALID_INSTRUCTORS,
            'rooms': QISTestData.VALID_ROOMS,
            'times': QISTestData.VALID_TIMES,
            'search_scenarios': QISTestData.SEARCH_SCENARIOS,
            'edge_cases': QISTestData.EDGE_CASES
        }
        return category_map.get(category, [])
    
    @staticmethod
    def create_parameterized_test_data(test_type: str) -> List[pytest.param]:
        """Create parameterized test data for pytest"""
        if test_type == 'input_validation':
            return [
                pytest.param(data, id=f"course_number_{i}")
                for i, data in enumerate(QISTestData.VALID_COURSE_NUMBERS)
            ]
        elif test_type == 'search_scenarios':
            return [
                pytest.param(scenario, id=scenario['name'])
                for scenario in QISTestData.SEARCH_SCENARIOS
            ]
        elif test_type == 'edge_cases':
            return [
                pytest.param(case, id=case['name'])
                for case in QISTestData.EDGE_CASES
            ]
        else:
            return []

# Export commonly used test data for easy import
COURSE_NUMBERS = QISTestData.VALID_COURSE_NUMBERS
COURSE_TITLES = QISTestData.VALID_COURSE_TITLES
INSTRUCTORS = QISTestData.VALID_INSTRUCTORS
ROOMS = QISTestData.VALID_ROOMS
TIMES = QISTestData.VALID_TIMES
SEARCH_SCENARIOS = QISTestData.SEARCH_SCENARIOS
EDGE_CASES = QISTestData.EDGE_CASES
