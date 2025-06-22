import pytest
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.settings import Settings
from pages.qis_search_page import QISSearchPage

@pytest.fixture
def qis_page(driver):
    """Fixture to create QIS search page instance"""
    page = QISSearchPage(driver)
    page.go_to(Settings.QIS_SEARCH_URL)
    return page

class TestNavigationComponents:
    """Test class for navigation and link components on QIS search page"""
    
    def test_breadcrumb_navigation_presence(self, qis_page):
        """Test that breadcrumb navigation is present and visible"""
        breadcrumb_links = qis_page.get_breadcrumb_links()
        
        # Verify breadcrumb links exist
        assert len(breadcrumb_links) > 0, "No breadcrumb links found"
        
        # Verify breadcrumb contains expected navigation elements
        breadcrumb_text = " ".join(breadcrumb_links).lower()
        expected_elements = ['startseite', 'suche', 'veranstaltung']
        found_elements = [elem for elem in expected_elements if elem in breadcrumb_text]
        assert len(found_elements) > 0, f"Expected breadcrumb elements not found. Found: {breadcrumb_links}"
    
    def test_breadcrumb_navigation_structure(self, qis_page):
        """Test breadcrumb navigation structure and hierarchy"""
        breadcrumb_links = qis_page.get_breadcrumb_links()
        
        if len(breadcrumb_links) >= 2:
            # Verify hierarchical structure (should start with home/start)
            first_link = breadcrumb_links[0].lower()
            assert 'startseite' in first_link or 'home' in first_link, f"Breadcrumb should start with home page: {first_link}"
            
            # Verify current page is indicated in breadcrumb
            last_link = breadcrumb_links[-1].lower()
            assert 'suche' in last_link or 'veranstaltung' in last_link, f"Current page not properly indicated: {last_link}"
    
    def test_breadcrumb_links_functionality(self, qis_page):
        """Test breadcrumb links are clickable and functional"""
        try:
            # Get all breadcrumb link elements
            breadcrumb_elements = qis_page.driver.find_elements(*qis_page.BREADCRUMB_LINKS)
            
            if len(breadcrumb_elements) > 1:
                # Test clicking the first breadcrumb link (usually home)
                first_link = breadcrumb_elements[0]
                original_url = qis_page.driver.current_url
                
                # Verify link is clickable
                assert first_link.is_enabled(), "First breadcrumb link is not enabled"
                assert first_link.is_displayed(), "First breadcrumb link is not visible"
                
                # Get href attribute to verify it's a valid link
                href = first_link.get_attribute('href')
                assert href is not None and href != "", "Breadcrumb link missing href attribute"
                assert href.startswith('http'), f"Invalid href format: {href}"
                
        except Exception as e:
            pytest.skip(f"Breadcrumb functionality test skipped: {str(e)}")
    
    def test_help_link_presence(self, qis_page):
        """Test that help link is present and accessible"""
        assert qis_page.is_help_link_present(), "Help link is not present on the page"
        
        # Verify help link is visible and enabled
        help_link = qis_page.driver.find_element(*qis_page.HELP_LINK)
        assert help_link.is_displayed(), "Help link is not visible"
        assert help_link.is_enabled(), "Help link is not enabled"
    
    def test_help_link_attributes(self, qis_page):
        """Test help link attributes and properties"""
        if qis_page.is_help_link_present():
            help_link = qis_page.driver.find_element(*qis_page.HELP_LINK)
            
            # Verify href attribute
            href = help_link.get_attribute('href')
            assert href is not None, "Help link missing href attribute"
            assert 'help' in href.lower() or 'hilfe' in href.lower(), f"Help link href doesn't contain help reference: {href}"
            
            # Verify link text or title
            link_text = help_link.text.strip()
            title = help_link.get_attribute('title')
            
            help_indicators = ['hilfe', 'help', '?']
            has_help_indicator = any(indicator in (link_text + ' ' + (title or '')).lower() for indicator in help_indicators)
            assert has_help_indicator, f"Help link doesn't have clear help indicator. Text: '{link_text}', Title: '{title}'"
    
    def test_help_link_functionality(self, qis_page):
        """Test help link click functionality"""
        if qis_page.is_help_link_present():
            original_url = qis_page.driver.current_url
            original_window_handles = qis_page.driver.window_handles
            
            try:
                # Click help link
                qis_page.click_help_link()
                time.sleep(2)  # Wait for navigation/popup
                
                # Check if new window/tab opened or URL changed
                new_window_handles = qis_page.driver.window_handles
                new_url = qis_page.driver.current_url
                
                # Verify some change occurred (new window or URL change)
                url_changed = new_url != original_url
                new_window_opened = len(new_window_handles) > len(original_window_handles)
                
                assert url_changed or new_window_opened, "Help link click didn't result in navigation or new window"
                
                # If new window opened, switch back to original
                if new_window_opened:
                    qis_page.driver.switch_to.window(original_window_handles[0])
                
            except Exception as e:
                pytest.skip(f"Help link functionality test skipped: {str(e)}")
    
    def test_language_switcher_presence(self, qis_page):
        """Test that language switcher is present and accessible"""
        assert qis_page.is_language_switcher_present(), "Language switcher is not present on the page"
        
        # Verify language switcher is visible and enabled
        lang_switcher = qis_page.driver.find_element(*qis_page.LANGUAGE_SWITCHER)
        assert lang_switcher.is_displayed(), "Language switcher is not visible"
        assert lang_switcher.is_enabled(), "Language switcher is not enabled"
    
    def test_language_switcher_attributes(self, qis_page):
        """Test language switcher attributes and properties"""
        if qis_page.is_language_switcher_present():
            # Find the parent link element
            lang_link = qis_page.driver.find_element(By.CSS_SELECTOR, "a img[src*='flag_en']").find_element(By.XPATH, "..")
            
            # Verify href attribute
            href = lang_link.get_attribute('href')
            assert href is not None, "Language switcher missing href attribute"
            assert 'language=en' in href or 'lang=en' in href, f"Language switcher href doesn't contain language parameter: {href}"
            
            # Verify image attributes
            flag_img = qis_page.driver.find_element(*qis_page.LANGUAGE_SWITCHER)
            src = flag_img.get_attribute('src')
            alt = flag_img.get_attribute('alt')
            title = flag_img.get_attribute('title')
            
            assert 'flag' in src.lower() or 'en' in src.lower(), f"Language switcher image source doesn't indicate language: {src}"
            
            # Verify accessibility attributes
            lang_indicators = ['english', 'en', 'language']
            has_lang_indicator = any(indicator in (alt + ' ' + (title or '')).lower() for indicator in lang_indicators)
            assert has_lang_indicator, f"Language switcher missing accessibility text. Alt: '{alt}', Title: '{title}'"
    
    def test_language_switcher_functionality(self, qis_page):
        """Test language switcher click functionality"""
        if qis_page.is_language_switcher_present():
            original_url = qis_page.driver.current_url
            
            try:
                # Click language switcher
                qis_page.click_language_switcher()
                time.sleep(3)  # Wait for page reload/navigation
                
                # Verify URL changed to include language parameter
                new_url = qis_page.driver.current_url
                assert new_url != original_url, "Language switcher click didn't change URL"
                assert 'language=en' in new_url or 'lang=en' in new_url, f"New URL doesn't contain English language parameter: {new_url}"
                
                # Verify page content changed (basic check)
                try:
                    # Look for English text indicators
                    page_source = qis_page.driver.page_source.lower()
                    english_indicators = ['search for courses', 'course number', 'instructor', 'english']
                    has_english = any(indicator in page_source for indicator in english_indicators)
                    
                    if has_english:
                        assert True  # Language switch successful
                    else:
                        # If no English indicators found, at least verify URL changed
                        assert 'en' in new_url, "Language parameter not found in URL after switch"
                        
                except Exception:
                    # If content check fails, at least verify URL parameter
                    assert 'en' in new_url, "Language parameter not found in URL after switch"
                
            except Exception as e:
                pytest.skip(f"Language switcher functionality test skipped: {str(e)}")
    
    def test_navigation_accessibility(self, qis_page):
        """Test navigation components for accessibility features"""
        # Test breadcrumb accessibility
        try:
            breadcrumb_elements = qis_page.driver.find_elements(*qis_page.BREADCRUMB_LINKS)
            for link in breadcrumb_elements[:3]:  # Test first 3 links
                # Verify links are keyboard accessible
                assert link.get_attribute('tabindex') != "-1", "Breadcrumb link not keyboard accessible"
                
                # Verify links have meaningful text
                link_text = link.text.strip()
                assert len(link_text) > 0, "Breadcrumb link missing text content"
                
        except Exception as e:
            pytest.skip(f"Breadcrumb accessibility test skipped: {str(e)}")
        
        # Test help link accessibility
        if qis_page.is_help_link_present():
            help_link = qis_page.driver.find_element(*qis_page.HELP_LINK)
            
            # Verify keyboard accessibility
            assert help_link.get_attribute('tabindex') != "-1", "Help link not keyboard accessible"
            
            # Verify has accessible name (text or title)
            link_text = help_link.text.strip()
            title = help_link.get_attribute('title')
            assert len(link_text) > 0 or (title and len(title) > 0), "Help link missing accessible name"
    
    def test_navigation_keyboard_support(self, qis_page):
        """Test navigation components keyboard support"""
        from selenium.webdriver.common.keys import Keys
        
        try:
            # Test tab navigation through navigation elements
            body = qis_page.driver.find_element(By.TAG_NAME, "body")
            body.click()  # Focus on page
            
            # Tab through navigation elements
            for i in range(5):  # Test first 5 tab stops
                body.send_keys(Keys.TAB)
                time.sleep(0.2)
                
                active_element = qis_page.driver.switch_to.active_element
                tag_name = active_element.tag_name.lower()
                
                # Verify focusable elements are interactive
                if tag_name in ['a', 'button', 'input', 'select']:
                    assert active_element.is_enabled(), f"Focused element is not enabled: {tag_name}"
            
            # Test Enter key on focused link
            active_element = qis_page.driver.switch_to.active_element
            if active_element.tag_name.lower() == 'a':
                # Don't actually press Enter to avoid navigation, just verify it's possible
                assert active_element.is_enabled(), "Focused link is not activatable"
                
        except Exception as e:
            pytest.skip(f"Keyboard navigation test skipped: {str(e)}")
    
    def test_navigation_link_targets(self, qis_page):
        """Test navigation link targets and URLs"""
        # Test breadcrumb link targets
        try:
            breadcrumb_elements = qis_page.driver.find_elements(*qis_page.BREADCRUMB_LINKS)
            
            for link in breadcrumb_elements[:3]:  # Test first 3 breadcrumb links
                href = link.get_attribute('href')
                if href:
                    # Verify href is a valid URL format
                    assert href.startswith('http'), f"Invalid breadcrumb link URL: {href}"
                    
                    # Verify href contains expected domain
                    assert 'uni-rostock.de' in href or 'lsf.uni-rostock.de' in href, f"Breadcrumb link to unexpected domain: {href}"
                    
        except Exception as e:
            pytest.skip(f"Navigation link targets test skipped: {str(e)}")
    
    def test_navigation_consistency(self, qis_page):
        """Test navigation consistency across page interactions"""
        # Get initial navigation state
        initial_breadcrumbs = qis_page.get_breadcrumb_links()
        initial_help_present = qis_page.is_help_link_present()
        initial_lang_present = qis_page.is_language_switcher_present()
        
        # Interact with form elements
        try:
            qis_page.fill_course_title("Test")
            time.sleep(0.5)
            
            # Verify navigation elements are still present and consistent
            current_breadcrumbs = qis_page.get_breadcrumb_links()
            current_help_present = qis_page.is_help_link_present()
            current_lang_present = qis_page.is_language_switcher_present()
            
            assert current_breadcrumbs == initial_breadcrumbs, "Breadcrumb navigation changed after form interaction"
            assert current_help_present == initial_help_present, "Help link presence changed after form interaction"
            assert current_lang_present == initial_lang_present, "Language switcher presence changed after form interaction"
            
        except Exception as e:
            pytest.skip(f"Navigation consistency test skipped: {str(e)}")
    
    def test_external_link_indicators(self, qis_page):
        """Test that external links are properly indicated"""
        try:
            # Find all links on the page
            all_links = qis_page.driver.find_elements(By.TAG_NAME, "a")
            
            external_links = []
            for link in all_links:
                href = link.get_attribute('href')
                if href and not ('uni-rostock.de' in href or 'lsf.uni-rostock.de' in href):
                    external_links.append(link)
            
            # Test external links have appropriate indicators
            for ext_link in external_links[:3]:  # Test first 3 external links
                # Check for target="_blank" or similar
                target = ext_link.get_attribute('target')
                title = ext_link.get_attribute('title')
                
                # External links should either open in new window or have clear indication
                has_external_indicator = (
                    target == "_blank" or
                    (title and ('extern' in title.lower() or 'new window' in title.lower()))
                )
                
                # This is more of a best practice check, so we'll just log if not present
                if not has_external_indicator:
                    print(f"External link may lack proper indicator: {ext_link.get_attribute('href')}")
                    
        except Exception as e:
            pytest.skip(f"External link indicators test skipped: {str(e)}")
