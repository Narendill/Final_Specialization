from BaseApp import BasePage
from selenium.webdriver.common.by import By
import logging
import time
import yaml


class TestSearchLocators:
    """Класс поиска локаторов."""
    ids = dict()
    with open('./locators.yaml', encoding='utf-8') as f:
        locators = yaml.safe_load(f)
    for locator in locators['xpath'].keys():
        ids[locator] = (By.XPATH, locators['xpath'][locator])
    for locator in locators['css'].keys():
        ids[locator] = (By.CSS_SELECTOR, locators['css'][locator])


class OperationsHelper(BasePage):
    # МЕТОДЫ ВВОДА ТЕКСТА
    def enter_text_into_field(self, locator, word, description=None):
        """Вспомогательный метод для ввода текста."""
        if description:
            element_name = description
        else:
            element_name = locator
        logging.debug(f'Send {word} to element {element_name}')
        field = self.find_element(locator)
        if not field:
            logging.error(f'Element {locator} not found')
            return False
        try:
            field.clear()
            field.send_keys(word)
        except:
            logging.exception(f'Exception while operation with {locator}')
            return False
        return True

    def enter_login(self, word):
        """Ввод логина."""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_LOGIN_FIELD'], word, description='login form')

    def enter_pass(self, word):
        """Ввод пароля."""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_PASS_FIELD'], word, description='password form')

    # МЕТОДЫ НАЖАТИЯ НА КНОПКИ
    def click_button(self, locator, description=None):
        """Вспомогательный метод для клика."""
        if description:
            element_name = description
        else:
            element_name = locator
        button = self.find_element(locator)
        if not button:
            return False
        try:
            button.click()
        except:
            logging.exception('Exception with click')
            return False
        logging.debug(f'Clicked {element_name} button')
        return True

    def click_about_botton(self):
        """Клик по кнопке About."""
        self.click_button(TestSearchLocators.ids['LOCATOR_ABOUT_BTN'], description='about')

    def click_login_button(self):
        """Клик по кнопке входа."""
        self.click_button(TestSearchLocators.ids['LOCATOR_LOGIN_BTN'], description='login')

    # МЕТОДЫ ПОЛУЧЕНИЯ ТЕКСТА
    def get_text_from_element(self, locator, description=None):
        """Вспомогательный метод для получения текста."""
        if description:
            element_name = description
        else:
            element_name = locator
        field = self.find_element(locator, time=3)
        if not field:
            return None
        try:
            text = field.text
        except:
            logging.exception(f'Exception while get text from {element_name}')
            return None
        logging.debug(f'We find text {text} in field {element_name}')
        return text

    def get_title_about_text(self):
        """Получение текста заголовка страницы About."""
        time.sleep(1)
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_ABOUT_PAGE'], description='about title text')

    def get_title_about_font_size(self):
        """Получение размера текста заголовка страницы About."""
        return self.get_element_property(TestSearchLocators.ids['LOCATOR_ABOUT_PAGE'], 'font-size')

    def get_error_text(self):
        """Получение текста об ошибке."""
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_ERROR_FIELD'], description='error text')

    def get_success_login_text(self):
        """Получение текста об успешном входе."""
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_GREETINGS'], description='greetings')
