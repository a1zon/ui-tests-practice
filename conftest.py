import pytest
from faker import Faker
from constants import DEFAULT_UI_TIMEOUT
from data.data_generator import DataGenerator
from tools import Tools


@pytest.fixture(scope="function")
def test_user():
    """
    Фикстура для создания тестового юзера
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
    }


@pytest.fixture(scope="session")  # Браузер запускается один раз для всей сессии
def browser(playwright):
    """
    Создание браузера
    """
    browser = playwright.chromium.launch(headless=False,
                                         slow_mo=300)  # headless=True для CI/CD, headless=False для локальной разработки
    yield browser  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    """
    Создание контекста
    """
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """
    Создание страницы
    """
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session")
def fake():
    """Фикстура для Faker"""
    return Faker('ru_RU')


@pytest.fixture(scope="function")
def invalid_user_data(fake):
    """
    Фикстура для генерации НЕВАЛИДНЫХ данных пользователя
    """
    return {
        'short_password': fake.password(length=5),  # Слишком короткий пароль
        'mismatch_password': {
            'password': fake.password(length=12),
            'password_repeat': fake.password(length=12)
        },
        'invalid_email': 'not-an-email',
        'empty_name': '',
        'email_without_domain': 'user@',
        'sql_injection': "'; DROP TABLE users; --",
        'xss': '<script>alert("xss")</script>',
    }
