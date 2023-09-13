# Обязательное задание (обязательно к выполнению):
# С использованием Selenium Webdriver, применяя паттерн проектирования Page Object
# и сохраняя веб-локаторы в отдельном yaml-файле выполнить следующие тесты в браузере Google Chrome для линукс:
# - логин на сайт https://test-stand.gb.ru
# - клик по ссылке About
# - проверка, что шрифт в заголовке открывшегося окна имеет размер 32 px.
import logging
import requests
from checkout import checkout
import yaml
from pages import OperationsHelper

with open('./testdata.yaml', encoding='utf-8') as f:
    testdata = yaml.safe_load(f)


def test_step_1(browser):
    """Тест на вход с неверными кредами."""
    logging.info('Test 1 starting')
    test_page = OperationsHelper(browser)
    test_page.go_to_site()
    test_page.enter_login(testdata['login'])
    test_page.enter_pass(testdata['incorrect_password'])
    test_page.click_login_button()
    assert test_page.get_error_text() == '401', 'test_step_1 FAILED'


def test_step_2(browser):
    """Тест на вход с валидными кредами."""
    logging.info('Test 2 starting')
    test_page = OperationsHelper(browser)
    test_page.enter_login(testdata['login'])
    test_page.enter_pass(testdata['password'])
    test_page.click_login_button()
    assert test_page.get_success_login_text() == f'Hello, {testdata["login"]}', 'test_step_2 FAILED'


def test_step_3(browser):
    """Тест перехода на страницу About."""
    logging.info('Test 3 staring')
    test_page = OperationsHelper(browser)
    test_page.click_about_botton()
    assert test_page.get_title_about_text() == 'About Page', 'test_step_3 FAILED'


def test_step_4(browser):
    """Тест проверки размера шрифта в заголовке страницы About."""
    logging.info('Test 4 staring')
    test_page = OperationsHelper(browser)
    assert test_page.get_title_about_font_size() == '32px', 'test_step43 FAILED'


# Дополнительное задание 1:
# Выполнить быструю проверку сайта на уязвимости при помощи утилиты командной строки nikto;
def test_step_5():
    """Проверка на уязвимости с помощью nikto."""
    logging.info('Test 5 staring')
    assert checkout(f'nikto -h {testdata["address"]} -ssl -Tuning 4', '0 error(s)'), 'test_step_5 FAILED'


# Дополнительное задание 2:
# С использованием библиотеки requests выполнить авторизацию на сайте с
# использованием токена авторизации в headers, получить данные о текущем
# пользователе и проверить, что они соответствуют данным, возвращенным в ответе на запрос авторизации.
# Нужно проверить, что запрос к https://test-stand.gb.ru/api/users/profile/{id} возвращает json с правильным username
def test_step_6(get_token, get_id):  #
    """Проверка соотвествия данных через API."""
    logging.info('Test 6 staring')
    result = requests.get(url=f'{testdata["api_address_test"]}{get_id}', headers={'X-Auth-Token': get_token}).json()
    assert result['username'] == testdata['login'], 'test_step_6 FAILED'
