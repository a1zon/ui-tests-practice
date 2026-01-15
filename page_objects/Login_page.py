import allure
from playwright.sync_api import Page

from page_objects.Page_action import BasePage
from constants import REGISTER_PAGE, LOGIN_PAGE


class CinescopeLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = LOGIN_PAGE

        # Локаторы
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Пароль")
        self.login_button = page.locator("button[type='submit']", has_text="Войти")
        self.register_button = page.get_by_role("link", name="Зарегистрироваться")

    @allure.step("Открытие страницы входа")
    def open(self):
        self.page.goto(self.url)

    # Базовые методы действий
    @allure.step("Ввод email: {email}")
    def enter_email(self, email: str):
        self.email_input.fill(email)

    @allure.step("Ввод пароля")
    def enter_password(self, password: str):
        self.password_input.fill(password)

    @allure.step("Нажатие кнопки входа")
    def click_login_button(self):
        self.login_button.click()

    # Основные методы для тестов
    @allure.step("Выполнение входа")
    def login(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    @allure.step("Ожидание редиректа на домашнюю страницу")
    def wait_redirect_to_home_page(self):
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")
        assert self.page.url == "https://dev-cinescope.coconutqa.ru/", "Редирект на домашнюю страницу не произошел"

    @allure.step("Проверка всплывающего сообщения")
    def check_allert(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")

    # ДОБАВЛЕННЫЕ МЕТОДЫ (которых не хватало)
    @allure.step("Проверка редиректа на домашнюю страницу")
    def assert_was_redirect_to_home_page(self):
        """Алиас для wait_redirect_to_home_page"""
        self.wait_redirect_to_home_page()

    @allure.step("Проверка всплывающего сообщения")
    def assert_allert_was_pop_up(self):
        """Алиас для check_allert"""
        self.check_allert()
