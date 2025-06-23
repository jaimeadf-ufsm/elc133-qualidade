import pytest
import time
from selenium.webdriver.common.by import By
from pages.qis_search_page import QisSearchPage

QIS_SEARCH_URL = "https://lsf.uni-rostock.de/qisserver/rds?state=change&type=5&moduleParameter=veranstaltungSearch&nextdir=change&next=search.vm&subdir=veranstaltung&_form=display&function=search&clean=y&category=veranstaltung.search&navigationPosition=lectures%2Csearch&breadcrumb=searchLectures&topitem=lectures&subitem=search"

@pytest.fixture
def qis_search_page(driver):
    page = QisSearchPage(driver)
    page.go_to(QIS_SEARCH_URL)
    return page

# Teste 1: Verificar título da página
def test_page_title_presence_and_content(qis_search_page):
    """Testa se o título principal da página está presente e contém o texto correto"""
    title = qis_search_page.get_page_title_text()
    assert title is not None
    assert "Suche nach Veranstaltungen" in title
    assert len(title.strip()) > 0

# Teste 2: Verificar navegação breadcrumb
def test_breadcrumb_navigation_structure(qis_search_page):
    """Testa a estrutura e conteúdo da navegação breadcrumb"""
    breadcrumb_items = qis_search_page.get_breadcrumb_items()
    assert len(breadcrumb_items) >= 2
    
    # Verifica se o primeiro item é "Startseite"
    first_item = breadcrumb_items[0]
    assert "Startseite" in first_item.text
    
    # Verifica se contém link para busca de disciplinas
    breadcrumb_texts = [item.text for item in breadcrumb_items]
    assert any("Suche nach Veranstaltungen" in text for text in breadcrumb_texts)

# Teste 3: Verificar links de navegação principal
def test_main_navigation_links(qis_search_page):
    """Testa a presença e conteúdo dos links de navegação principal"""
    nav_links = qis_search_page.get_navigation_links()
    assert len(nav_links) >= 5
    
    expected_links = ["Studentisches Leben", "Veranstaltungen", "Einrichtungen", "Räume und Gebäude", "Personen", "Forschung"]
    nav_texts = [link.text for link in nav_links]
    
    for expected in expected_links:
        assert expected in nav_texts

# Teste 4: Verificar formulário de busca
def test_search_form_presence(qis_search_page):
    """Testa se o formulário de busca está presente e acessível"""
    assert qis_search_page.is_form_present()
    
    # Verifica se o formulário tem a action correta
    form = qis_search_page.driver.find_element(*qis_search_page.SEARCH_FORM)
    action = form.get_attribute("action")
    assert "qisserver/rds" in action

# Teste 5: Verificar opções de quantidade de resultados (Radio buttons - 1)
def test_results_count_radio_options(qis_search_page):
    """Testa as opções de quantidade de resultados e sua funcionalidade"""
    # Verifica se todas as opções estão presentes
    count_10 = qis_search_page.driver.find_element(*qis_search_page.RESULTS_COUNT_10)
    count_20 = qis_search_page.driver.find_element(*qis_search_page.RESULTS_COUNT_20)
    count_30 = qis_search_page.driver.find_element(*qis_search_page.RESULTS_COUNT_30)
    count_50 = qis_search_page.driver.find_element(*qis_search_page.RESULTS_COUNT_50)
    
    assert count_10.is_displayed()
    assert count_20.is_displayed()
    assert count_30.is_displayed()
    assert count_50.is_displayed()
    
    # Verifica se 10 está selecionado por padrão
    assert count_10.is_selected()
    assert not count_20.is_selected()
    
    # Testa seleção de outra opção
    qis_search_page.select_results_count(20)
    assert count_20.is_selected()
    assert not count_10.is_selected()

# Teste 6: Verificar opções de ordenação (Radio buttons - 2)
def test_sort_options_radio_buttons(qis_search_page):
    """Testa as opções de ordenação e sua funcionalidade"""
    sort_standard = qis_search_page.driver.find_element(*qis_search_page.SORT_STANDARD)
    sort_number = qis_search_page.driver.find_element(*qis_search_page.SORT_NUMBER)
    sort_title = qis_search_page.driver.find_element(*qis_search_page.SORT_TITLE)
    sort_lecturer = qis_search_page.driver.find_element(*qis_search_page.SORT_LECTURER)
    
    # Verifica presença
    assert sort_standard.is_displayed()
    assert sort_number.is_displayed()
    assert sort_title.is_displayed()
    assert sort_lecturer.is_displayed()    # Verifica ordem dos labels
    labels = qis_search_page.driver.find_elements(By.CSS_SELECTOR, "label[for^='sort']")
    label_texts = [label.text for label in labels]
    assert "Standard" in label_texts[0]
    
    # Testa funcionalidade
    qis_search_page.select_sort_option("title")
    assert sort_title.is_selected()

# Teste 7: Verificar dropdown de semestre
def test_semester_dropdown_options(qis_search_page):
    """Testa o dropdown de seleção de semestre"""
    semester_options = qis_search_page.get_semester_options()
    assert len(semester_options) >= 3
    
    # Verifica se contém semestres esperados
    option_texts = " ".join(semester_options)
    assert "SS 2025" in option_texts
    assert "WS" in option_texts
    
    # Testa seleção
    qis_search_page.select_semester("20241")
    current_semester = qis_search_page.driver.find_element(*qis_search_page.SEMESTER_SELECT)
    assert current_semester.get_attribute("value") == "20241"

# Teste 8: Verificar campo de número da disciplina (Input field - 1)
def test_event_number_input_field(qis_search_page):
    """Testa o campo de entrada do número da disciplina"""
    input_field = qis_search_page.driver.find_element(*qis_search_page.EVENT_NUMBER_INPUT)
    assert input_field.is_displayed()
    assert input_field.is_enabled()
    
    # Testa entrada de dados
    test_number = "12345"
    qis_search_page.fill_event_number(test_number)
    assert input_field.get_attribute("value") == test_number
    
    # Verifica atributos
    assert input_field.get_attribute("size") == "70"
    assert input_field.get_attribute("type") == "text"

# Teste 9: Verificar campo de título da disciplina (Input field - 2)
def test_event_title_input_field(qis_search_page):
    """Testa o campo de entrada do título da disciplina"""
    input_field = qis_search_page.driver.find_element(*qis_search_page.EVENT_TITLE_INPUT)
    assert input_field.is_displayed()
    assert input_field.is_enabled()
    
    # Testa entrada de dados
    test_title = "Mathematik"
    qis_search_page.fill_event_title(test_title)
    assert input_field.get_attribute("value") == test_title    # Verifica label associado
    label = qis_search_page.driver.find_element(By.CSS_SELECTOR, "label[for='veranstaltung.dtxt']")
    assert "Titel der Veranstaltung" in label.text

# Teste 10: Verificar dropdown de tipo de disciplina
def test_event_type_dropdown(qis_search_page):
    """Testa o dropdown de tipo de disciplina"""
    event_types = qis_search_page.get_event_type_options()
    assert len(event_types) > 10
    
    # Verifica alguns tipos específicos
    type_texts = " ".join(event_types)
    assert "Vorlesung" in type_texts
    assert "Seminar" in type_texts
    assert "Praktikum" in type_texts
    assert "Alles auswählen" in event_types[0]
    
    # Testa seleção
    qis_search_page.select_event_type("9")  # Vorlesung
    dropdown = qis_search_page.driver.find_element(*qis_search_page.EVENT_TYPE_SELECT)
    assert dropdown.get_attribute("value") == "9"

# Teste 11: Verificar campos de horário (time inputs)
def test_time_input_fields(qis_search_page):
    """Testa os campos de entrada de horário (von/bis)"""
    time_from = qis_search_page.driver.find_element(*qis_search_page.TIME_FROM_INPUT)
    time_to = qis_search_page.driver.find_element(*qis_search_page.TIME_TO_INPUT)
    
    assert time_from.is_displayed()
    assert time_to.is_displayed()
    assert time_from.is_enabled()
    assert time_to.is_enabled()
    
    # Testa entrada de horários
    time_from.clear()
    time_from.send_keys("08:00")
    time_to.clear()
    time_to.send_keys("10:00")
    
    assert time_from.get_attribute("value") == "08:00"
    assert time_to.get_attribute("value") == "10:00"

# Teste 12: Verificar links de serviços no cabeçalho
def test_service_links_in_header(qis_search_page):
    """Testa os links de serviços no cabeçalho da página"""
    service_links = qis_search_page.get_service_links()
    assert len(service_links) >= 2
    
    # Verifica links específicos
    link_texts = [link.text for link in service_links]
    assert any("Startseite" in text for text in link_texts)
    assert any("Anmelden" in text for text in link_texts)
    
    # Verifica se os links têm href
    for link in service_links:
        href = link.get_attribute("href")
        assert href is not None and len(href) > 0

# Teste 13: Verificar botão de limpar (Button - 2)
def test_search_clear_button(qis_search_page):
    """Testa o botão de limpar busca"""
    button = qis_search_page.driver.find_element(*qis_search_page.SEARCH_CLEAR_BUTTON)
    assert button.is_displayed()
    assert button.is_enabled()
    assert button.get_attribute("value") == "Einträge verwerfen"
    assert button.get_attribute("type") == "submit"
    assert button.get_attribute("name") == "search_clear"

# Teste 14: Verificar imagens e ícones da página
def test_page_images_and_icons(qis_search_page):
    """Testa a presença de imagens e ícones na página"""
    # Verifica imagens de separadores
    separator_images = qis_search_page.driver.find_elements(By.CSS_SELECTOR, "img[src*='his_strich.gif']")
    assert len(separator_images) > 0
    
    # Verifica ícone de idioma
    language_icon = qis_search_page.driver.find_elements(By.CSS_SELECTOR, "img[src*='world.svg']")
    assert len(language_icon) > 0
    
    # Verifica se as imagens têm atributos alt
    for img in separator_images[:2]:  # Testa apenas as primeiras 2
        alt_text = img.get_attribute("alt")
        assert alt_text is not None

# Teste 15: Verificar tabindex e acessibilidade
def test_tabindex_accessibility(qis_search_page):
    """Testa os atributos de tabindex para acessibilidade"""
    # Verifica elementos com tabindex
    elements_with_tabindex = qis_search_page.driver.find_elements(By.CSS_SELECTOR, "[tabindex]")
    assert len(elements_with_tabindex) >= 10
    
    # Verifica se os tabindex são sequenciais e válidos
    tabindex_values = []
    for element in elements_with_tabindex:
        tabindex = element.get_attribute("tabindex")
        if tabindex and tabindex.isdigit():
            tabindex_values.append(int(tabindex))
    
    # Verifica se há uma sequência lógica
    assert len(tabindex_values) >= 5
    assert min(tabindex_values) >= 1

# Teste 16: Verificar meta tags e estrutura do documento
def test_document_structure_and_meta_tags(qis_search_page):
    """Testa a estrutura do documento e meta tags"""
    # Verifica title tag
    page_title = qis_search_page.get_title()
    assert "Suche nach Veranstaltungen" in page_title
    assert "Universität Rostock" in page_title
    
    # Verifica meta tags
    meta_charset = qis_search_page.driver.find_elements(By.CSS_SELECTOR, "meta[http-equiv='content-type']")
    assert len(meta_charset) > 0
    
    # Verifica se há meta description
    meta_description = qis_search_page.driver.find_elements(By.CSS_SELECTOR, "meta[name='description']")
    assert len(meta_description) > 0

# Teste 17: Verificar CSS e estilos
def test_css_stylesheets_loading(qis_search_page):
    """Testa o carregamento de folhas de estilo CSS"""
    # Verifica links para CSS
    css_links = qis_search_page.driver.find_elements(By.CSS_SELECTOR, "link[rel='stylesheet']")
    assert len(css_links) >= 2
    
    # Verifica CSS específico da universidade
    qis_css = False
    print_css = False
    
    for css_link in css_links:
        href = css_link.get_attribute("href")
        if "QISDesign_UNI-ROSTOCK.css" in href:
            qis_css = True
        if "Print.css" in href:
            print_css = True
    
    assert qis_css, "CSS principal do QIS não encontrado"
    assert print_css, "CSS de impressão não encontrado"

# Teste 18: Verificar divs de layout e estrutura
def test_layout_divs_structure(qis_search_page):
    """Testa a estrutura de divs de layout da página"""
    # Verifica div wrapper principal
    wrapper_div = qis_search_page.driver.find_elements(By.ID, "wrapper")
    assert len(wrapper_div) == 1
    
    # Verifica divs de conteúdo
    content_divs = qis_search_page.driver.find_elements(By.CLASS_NAME, "divcontent")
    assert len(content_divs) >= 1
    
    # Verifica div de links
    links_divs = qis_search_page.driver.find_elements(By.CLASS_NAME, "divlinks")
    assert len(links_divs) >= 1
    
    # Verifica se os divs estão estruturados corretamente
    content_div = content_divs[0]
    assert content_div.is_displayed()

