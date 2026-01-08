import pytest
import re
import os
from playwright.sync_api import Playwright, sync_playwright, expect
from pathlib import Path
from datetime import datetime

class Tools:
    @staticmethod
    def project_dir():
        """
        Возвращает корневую директорию проекта.
        Предполагается, что текущий файл находится в поддиректории `common`.
        """
        return Path(__file__).parent

    @staticmethod
    def files_dir(nested_directory: str = None, filename: str = None):
        """
        Возвращает путь к директории `files` (или её поддиректории).
        Если директория не существует, она создается.
        Если указан `filename`, возвращает полный путь к файлу.
        """
        files_path = Tools.project_dir() / "files"
        if nested_directory:
            files_path = files_path / nested_directory
        files_path.mkdir(parents=True, exist_ok=True)

        if filename:
            return files_path / filename
        return files_path

    @staticmethod
    def get_timestamp():
        """
        Возвращает текущую временную метку в формате YYYY-MM-DD_HH-MM-SS.
        """
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")



DEFAULT_UI_TIMEOUT = 30000 # Пример значения таймаута


@pytest.fixture(scope="session")  # Браузер запускается один раз для всей сессии
def browser(playwright):
    """
    Создание браузера
    """
    browser = playwright.chromium.launch(headless=False,slow_mo=300)  # headless=True для CI/CD, headless=False для локальной разработки
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





def test_demo_qa(page):
    """
    Тест текст бокса
    """
    page.goto("https://demoqa.com/text-box")

    page.fill("#userName","Andrew")
    page.fill("#userEmail","ass@gmail.com")
    page.fill("#currentAddress","burggers-street-18")
    page.fill("#permanentAddress","berries-street-35")

    page.click('#submit')

    expect(page.locator('#output #name')).to_have_text('Name:Andrew')
    expect(page.locator('#output #email')).to_have_text('Email:ass@gmail.com')
    expect(page.locator('#output #currentAddress')).to_have_text('Current Address :burggers-street-18')
    expect(page.locator('#output #permanentAddress')).to_have_text('Permananet Address :berries-street-35')

@pytest.mark.xfail(reason = "Падает потому что нет генерации данных")
def test_cinescope_qa(page):
    """
    Тест на регистрацию в кино
    Падает потому что нет генерации данных

    """
    page.goto("https://dev-cinescope.coconutqa.ru/register")

    page.fill("[name='fullName']","Andrew hizenberg second")
    page.fill("[name='email']","met@drugs.com")
    page.fill("[name='password']","BigGengstaSeller123")
    page.fill("[name='passwordRepeat']","BigGengstaSeller123")

    page.click('[type="submit"]')

    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)

def test_demo_qa_obj(page):
    """
    Нажатие на кнопку
    """
    page.goto("https://demoqa.com/webtables")
    page.get_by_role("button", name = "Add").click()

    modal = page.locator("div.modal:has(:text('Registration Form'))")
    assert modal.is_visible()





def test_demo_qa_full_fill(page):
    """
    Полное заполнение формы на регистрацию
    """
    page.goto("https://demoqa.com/automation-practice-form")


    today = datetime.now().strftime("%d %b %Y")
    date_value = page.get_attribute("#dateOfBirthInput", "value")
    assert date_value == today, f"Expected DOB {today}, but got {date_value}"


    page.fill("#firstName", "Andrew")          # fill
    page.type("#lastName", "Gerger")           # type
    page.fill("#userEmail", "ass@gmail.com")
    page.type("#userNumber", "8098123123")


    page.locator("label[for='gender-radio-1']").click()  # Male


    page.click("#dateOfBirthInput")
    page.locator(".react-datepicker__year-select").select_option("1995")
    page.locator(".react-datepicker__month-select").select_option("0")  # January
    page.locator(".react-datepicker__day--015").click()


    page.locator(".subjects-auto-complete__value-container").click()
    page.type(".subjects-auto-complete__value-container", "Ma")
    page.get_by_text("Maths", exact=True).click()


    page.locator("label[for='hobbies-checkbox-1']").click()  # Sports


    page.set_input_files(
        "#uploadPicture",
        os.path.abspath("/Users/Geyger.Andrey/Desktop/cars.jpg")
    )


    page.fill("#currentAddress", "Burger street 23")


    page.get_by_text("Select State").click()
    page.get_by_text("NCR", exact=True).click()

    page.get_by_text("Select City").click()
    page.get_by_text("Delhi", exact=True).click()


    page.click("#submit")
    expect(page.get_by_text("Thanks for submitting the form")).to_be_visible()

    footer_text = page.locator("footer").inner_text()
    assert footer_text == "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED.", \
        "Footer text does not match expected"



def test_radio_button_disabled(page):
    """
    Проверка включенности/отключенности элементов - радиобаттонов
    """
    page.goto("https://demoqa.com/radio-button")

    assert page.locator("#yesRadio").is_enabled()
    assert page.locator("#impressiveRadio").is_enabled()
    assert page.locator("#noRadio").is_disabled()

def test_checkbox_visibility(page):
    """
    Проверка видимости чебоксов
    """
    page.goto("https://demoqa.com/checkbox")

    home = page.get_by_text("Home", exact=True)
    desktop = page.get_by_text("Desktop", exact=True)


    assert home.is_visible()
    assert desktop.is_hidden()


    page.locator("button[title='Toggle']").click()


    assert desktop.is_visible()


def test_dynamic_properties_wait_for_element(page):
    """
    Проверка ожиданий
    """
    page.goto("https://demoqa.com/dynamic-properties",)

    button_selector = "#visibleAfter"

    assert page.locator(button_selector).count() == 0

    page.wait_for_selector(button_selector, timeout=7000)

    assert page.locator(button_selector).is_visible()

def test_radio_buttons_expect(page):
    page.goto("https://demoqa.com/radio-button")

    yes_radio = page.get_by_role("radio", name="Yes")
    impressive_radio = page.get_by_role("radio", name="Impressive")
    no_radio = page.get_by_role("radio", name="No")


    expect(no_radio).to_be_disabled()
    expect(yes_radio).to_be_enabled()
    expect(impressive_radio).to_be_enabled()


    page.locator('[for="yesRadio"]').click()


    expect(yes_radio).to_be_checked()
    expect(impressive_radio).not_to_be_checked()



def test_checkbox_visibility_expect(page):
    page.goto("https://demoqa.com/checkbox")

    home = page.get_by_text("Home", exact=True)
    desktop = page.get_by_text("Desktop", exact=True)


    expect(home).to_be_visible()
    expect(desktop).to_be_hidden()


    page.locator("button[title='Toggle']").click()


    expect(desktop).to_be_visible()



def test_dynamic_properties_expect(page):
    page.goto("https://demoqa.com/dynamic-properties")

    button = page.locator("#visibleAfter")

    expect(button).not_to_be_attached()

    page.wait_for_selector("#visibleAfter", timeout=7000)

    expect(button).to_be_visible()







