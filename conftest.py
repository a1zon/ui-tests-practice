from constants import  DEFAULT_UI_TIMEOUT
from tools import Tools
import pytest
from faker import Faker
import random


@pytest.fixture(scope="session")  # Браузер запускается один раз для всей сессии
def browser(playwright):
    """
    Создание браузера
    """
    browser = playwright.chromium.launch(headless=True,
                                         slow_mo=300)  # headless=True для CI/CD, headless=False для локальной разработки
    yield browser  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    browser.close()


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
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
def user_registration_data(fake):
    """
    Фикстура для генерации ВСЕХ данных пользователя для регистрации
    Возвращает словарь со всеми необходимыми полями
    """


    def get_unique_email():
        email = fake.email()
        return email


    def get_full_name():
        formats = [
            f"{fake.first_name_male()} {fake.last_name_male()}",
            f"{fake.first_name_female()} {fake.last_name_female()}",
            f"{fake.first_name()} {fake.last_name()}",
            f"{fake.first_name()} {fake.middle_name()} {fake.last_name()}",
        ]
        return random.choice(formats)


    def get_strong_password(min_length=8, max_length=16):
        length = random.randint(min_length, max_length)

        # Генерируем базовый пароль с помощью Faker
        password = fake.password(
            length=length,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        )
        return password

    # Формируем полный набор данных
    password = get_strong_password(12, 16)

    user_data = {
        'full_name': get_full_name(),
        'email': get_unique_email(),
        'password': password,
        'password_repeat': password,  # Для поля подтверждения пароля

    }

    return user_data

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

@pytest.fixture(scope="session")
def admin_user_data():
    """
    Фикстура для данных администратора (если нужно)
    """
    return {
        'email': 'admin@cinescope.ru',
        'password': 'AdminPassword123!',
        'role': 'admin'
    }
