import logging
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Базовый класс страницы."""

    def __init__(self, driver):
        """Инициализация."""
        self.driver = driver

    def find_element(self, locator: tuple, time: int = 10):
        """Метод поиска элемента."""
        try:
            element = WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                             message=f'Can not find element by locator {locator}')
        except:
            logging.exception('Find element exception')
            element = None
        return element

    def get_element_property(self, locator: tuple, property: str) -> str | None:
        """Метод получения свойств элемента."""
        element = self.find_element(locator)
        if element:
            return element.value_of_css_property(property)
        else:
            logging.error(f'Property {property} not found i element with locator {locator}')
            return None

    def go_to_site(self, url='https://test-stand.gb.ru') -> str | None:
        """Метод открытия страницы."""
        try:
            start_browsing = self.driver.get(url)
        except:
            logging.exception('Exception while open site')
            start_browsing = None
        return start_browsing

    def get_alert_text(self):
        try:
            time.sleep(1)
            alert = self.driver.switch_to.alert
            return alert.text
        except:
            logging.exception('Exception with alert')
            return None
