import pytest
from utilities.settings import Settings
from pages.main_contact_page import MainContactPage

@pytest.fixture
def contact_page(driver):
    page = MainContactPage(driver)
    page.go_to(f'{Settings.MAIN_BASE_URL}/universitaet/kommunikation-und-aktuelles/presse-und-kommunikationsstelle/')

    return page

def test_office_address_information(contact_page):
    office_address_information = contact_page.get_office_address_information()

    assert 'Universität Rostock' in office_address_information
    assert 'Universitätsplatz 1' in office_address_information
    assert '18055 Rostock' in office_address_information
    
def test_postal_address_information(contact_page):
    postal_address_information = contact_page.get_postal_address_information()

    print(postal_address_information)

    assert 'Universität Rostock' in postal_address_information
    assert 'Pressestelle' in postal_address_information
    assert '18051 Rostock' in postal_address_information

def test_phone_and_email_information(contact_page):
    phone_and_email_information = contact_page.get_phone_and_email_information()

    assert '+49 381 498-1012' in phone_and_email_information
    assert '+49 381 498-1032' in phone_and_email_information
    assert 'pressestelle@uni-rostock.de' in phone_and_email_information
