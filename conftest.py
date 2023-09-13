import logging
import pytest
import yaml
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

with open('./testdata.yaml', encoding='utf-8') as f:
    testdata = yaml.safe_load(f)
    current_browser = testdata['browser']


@pytest.fixture(scope='session')
def browser():
    """Фикстура инициализации браузера."""
    if current_browser == 'firefox':
        service = Service(executable_path=GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=service, options=options)
    else:
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()


@pytest.fixture()
def get_token() -> str | None:
    """Возвращает токен с сайта, полученный по логину и паролю."""
    try:
        result = requests.post(url=testdata['api_auth'],
                               data={'username': testdata['login'], 'password': testdata['password']}).json()['token']
    except:
        logging.exception('Exception while getting token')
        return None
    return result


@pytest.fixture()
def get_id() -> str | None:
    """Возвращает id с сайта, полученный по логину и паролю."""
    try:
        result = requests.post(url=testdata['api_auth'],
                               data={'username': testdata['login'], 'password': testdata['password']}).json()['id']
    except:
        logging.exception('Exception while getting id')
        return None
    return result
