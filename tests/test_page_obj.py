import allure
import pytest

from data.data_generator import DataGenerator
from page_objects.Login_page import CinescopeLoginPage
from page_objects.Register_page import CinescopeRegisterPage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestLoginPage:
    @allure.title("Проведение успешного входа в систему")
    @pytest.mark.xfail(reason="авторизация не работает корректно - регает только после перезагрузки")
    def test_login_by_ui_allure(self, page, registered_user):
        """Тест с использованием существующей фикстуры page"""

        page.set_default_timeout(5000)
        login_page = CinescopeLoginPage(page)

        with allure.step("Открытие страницы входа"):
            login_page.open()

        with allure.step(f"Ввод данных пользователя: {registered_user['email']}"):
            login_page.login(registered_user["email"], registered_user["password"])

        with allure.step("Проверка редиректа на домашнюю страницу"):
            login_page.assert_was_redirect_to_home_page()

        with allure.step("Создание скриншота"):
            login_page.make_screenshot_and_attach_to_allure("После успешного входа")

        with allure.step("Проверка всплывающего сообщения"):
            login_page.assert_allert_was_pop_up()

    #
    @allure.title("Проверка элементов страницы входа")
    def test_login_page_elements(self, page):
        """Тест проверки видимости элементов на странице входа"""
        login_page = CinescopeLoginPage(page)
        login_page.open()

        with allure.step("Проверка видимости полей ввода"):
            assert login_page.email_input.is_visible(), "Поле email не отображается"
            assert login_page.password_input.is_visible(), "Поле пароля не отображается"
            assert login_page.login_button.is_visible(), "Кнопка входа не отображается"
            assert login_page.register_button.is_visible(), "Ссылка регистрации не отображается"


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui_allure(self, page):
        """Тест с использованием существующей фикстуры page"""
        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()

        register_page = CinescopeRegisterPage(page)

        with allure.step("Открытие страницы регистрации"):
            register_page.open()

        with allure.step(f"Заполнение формы регистрации: {random_email}"):
            register_page.register(f"PlaywrightTest {random_name}", random_email, random_password, random_password)

        with allure.step("Проверка редиректа на страницу входа"):
            register_page.assert_was_redirect_to_login_page()

        with allure.step("Создание скриншота"):
            register_page.make_screenshot_and_attach_to_allure("После успешной регистрации")

        with allure.step("Проверка всплывающего сообщения"):
            register_page.assert_allert_was_pop_up()

    @allure.title("Проверка элементов страницы регистрации")
    def test_register_page_elements(self, page):
        """Тест проверки видимости элементов на странице регистрации"""
        register_page = CinescopeRegisterPage(page)
        register_page.open()

        with allure.step("Проверка видимости полей ввода"):
            assert register_page.full_name_input.is_visible(), "Поле имени не отображается"
            assert register_page.email_input.is_visible(), "Поле email не отображается"
            assert register_page.password_input.is_visible(), "Поле пароля не отображается"
            assert register_page.repeat_password_input.is_visible(), "Поле подтверждения пароля не отображается"
            assert register_page.register_button.is_visible(), "Кнопка регистрации не отображается"

#
