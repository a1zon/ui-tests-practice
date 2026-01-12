from playwright.sync_api import Page
from page_objects.Page_action import BasePage
import allure

class CinescopeRegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://dev-cinescope.coconutqa.ru/register"

        # Локаторы
        self.full_name_input = page.get_by_role("textbox", name="Имя Фамилия Отчество")
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Пароль", exact=True)
        self.repeat_password_input = page.get_by_role("textbox", name="Повторите пароль")
        self.register_button = page.get_by_role("button", name="Зарегистрироваться")
        self.sign_button = page.get_by_role("link", name="Войти")

    @allure.step("Открытие страницы регистрации")
    def open(self):
        self.page.goto(self.url)

    # Базовые методы действий
    @allure.step("Ввод полного имени: {full_name}")
    def enter_full_name(self, full_name: str):
        self.full_name_input.fill(full_name)

    @allure.step("Ввод email: {email}")
    def enter_email(self, email: str):
        self.email_input.fill(email)

    @allure.step("Ввод пароля")
    def enter_password(self, password: str):
        self.password_input.fill(password)

    @allure.step("Ввод подтверждения пароля")
    def enter_repeat_password(self, password: str):
        self.repeat_password_input.fill(password)

    @allure.step("Нажатие кнопки регистрации")
    def click_register_button(self):
        self.register_button.click()

    # Основные методы для тестов (сохраняем старые имена)
    @allure.step("Выполнение регистрации")
    def register(self, full_name: str, email: str, password: str, confirm_password: str):
        """Полный процесс регистрации (сохранен для совместимости)"""
        self.enter_full_name(full_name)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_repeat_password(confirm_password)
        self.click_register_button()

    @allure.step("Ожидание редиректа на страницу логина")
    def wait_redirect_to_login_page(self):
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/login")
        assert self.page.url == "https://dev-cinescope.coconutqa.ru/login", "Редирект на страницу входа не произошел"

    @allure.step("Проверка всплывающего сообщения")
    def check_allert(self):
        """Старое название метода (сохранено для совместимости)"""
        self.check_pop_up_element_with_text("Подтвердите свою почту")

    @allure.step("Проверка редиректа на страницу входа")
    def assert_was_redirect_to_login_page(self):
        """Алиас для wait_redirect_to_login_page"""
        self.wait_redirect_to_login_page()

    @allure.step("Проверка всплывающего сообщения")
    def assert_allert_was_pop_up(self):
        """Алиас для check_allert"""
        self.check_allert()
