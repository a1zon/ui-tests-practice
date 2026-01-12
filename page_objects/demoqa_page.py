from page_objects.Page_action import BasePage
import allure
import os
from datetime import datetime
from playwright.sync_api import  expect

class DemoQAWebTablesPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://demoqa.com/webtables"

        # Локаторы
        self.add_button = page.get_by_role("button", name="Add")
        self.modal = page.locator("div.modal:has(:text('Registration Form'))")

    @allure.step("Открыть страницу Web Tables")
    def open(self):
        self.page.goto(self.url)

    @allure.step("Нажать кнопку Add")
    def click_add(self):
        self.add_button.click()

    @allure.step("Проверить видимость модального окна")
    def check_modal_visible(self):
        expect(self.modal).to_be_visible()




class DemoQAPracticeFormPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://demoqa.com/automation-practice-form"

        # Основные поля
        self.first_name_input = page.locator("#firstName")
        self.last_name_input = page.locator("#lastName")
        self.email_input = page.locator("#userEmail")
        self.mobile_input = page.locator("#userNumber")

        # Radio buttons
        self.male_radio_label = page.locator("label[for='gender-radio-1']")

        # Date of Birth
        self.dob_input = page.locator("#dateOfBirthInput")
        self.year_select = page.locator(".react-datepicker__year-select")
        self.month_select = page.locator(".react-datepicker__month-select")
        self.day_15 = page.locator(".react-datepicker__day--015")

        # Subjects
        self.subjects_container = page.locator(".subjects-auto-complete__value-container")
        self.maths_option = page.get_by_text("Maths", exact=True)

        # Hobbies
        self.sports_checkbox_label = page.locator("label[for='hobbies-checkbox-1']")

        # File upload
        self.upload_input = page.locator("#uploadPicture")

        # Address
        self.current_address_input = page.locator("#currentAddress")

        # State and City
        self.state_dropdown = page.get_by_text("Select State")
        self.ncr_option = page.get_by_text("NCR", exact=True)
        self.city_dropdown = page.get_by_text("Select City")
        self.delhi_option = page.get_by_text("Delhi", exact=True)

        # Submit
        self.submit_button = page.locator("#submit")

        # Confirmation
        self.success_message = page.get_by_text("Thanks for submitting the form")
        self.footer = page.locator("footer")

    @allure.step("Открыть страницу Practice Form")
    def open(self):
        self.page.goto(self.url)

    @allure.step("Проверить дату рождения по умолчанию")
    def check_default_dob(self):
        today = datetime.now().strftime("%d %b %Y")
        date_value = self.dob_input.get_attribute("value")
        assert date_value == today, f"Expected DOB {today}, but got {date_value}"

    @allure.step("Заполнить имя: {first_name}")
    def fill_first_name(self, first_name: str):
        self.first_name_input.fill(first_name)

    @allure.step("Заполнить фамилию: {last_name}")
    def fill_last_name(self, last_name: str):
        self.last_name_input.type(last_name)

    @allure.step("Заполнить email: {email}")
    def fill_email(self, email: str):
        self.email_input.fill(email)

    @allure.step("Заполнить номер телефона: {mobile}")
    def fill_mobile(self, mobile: str):
        self.mobile_input.type(mobile)

    @allure.step("Выбрать пол: Male")
    def select_male(self):
        self.male_radio_label.click()

    @allure.step("Выбрать дату рождения: 15 января 1995")
    def select_dob(self):
        self.dob_input.click()
        self.year_select.select_option("1995")
        self.month_select.select_option("0")  # January
        self.day_15.click()

    @allure.step("Выбрать предмет: Maths")
    def select_maths_subject(self):
        self.subjects_container.click()
        self.subjects_container.type("Ma")
        self.maths_option.click()

    @allure.step("Выбрать хобби: Sports")
    def select_sports_hobby(self):
        self.sports_checkbox_label.click()

    @allure.step("Загрузить файл: {file_path}")
    def upload_file(self, file_path: str):
        self.upload_input.set_input_files(os.path.abspath(file_path))

    @allure.step("Заполнить текущий адрес: {address}")
    def fill_current_address(self, address: str):
        self.current_address_input.fill(address)

    @allure.step("Выбрать штат: NCR")
    def select_ncr_state(self):
        self.state_dropdown.click()
        self.ncr_option.click()

    @allure.step("Выбрать город: Delhi")
    def select_delhi_city(self):
        self.city_dropdown.click()
        self.delhi_option.click()

    @allure.step("Нажать кнопку Submit")
    def click_submit(self):
        self.submit_button.click()

    @allure.step("Проверить успешное сообщение")
    def check_success_message(self):
        expect(self.success_message).to_be_visible()

    @allure.step("Проверить текст футера")
    def check_footer_text(self):
        footer_text = self.footer.inner_text()
        expected_text = "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED."
        assert footer_text == expected_text, f"Footer text does not match expected. Got: {footer_text}"

class DemoQARadioButtonPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://demoqa.com/radio-button"

        # Локаторы
        self.yes_radio = page.get_by_role("radio", name="Yes")
        self.impressive_radio = page.get_by_role("radio", name="Impressive")
        self.no_radio = page.get_by_role("radio", name="No")
        self.yes_label = page.locator('[for="yesRadio"]')

    @allure.step("Открыть страницу Radio Button")
    def open(self):
        self.page.goto(self.url)

    @allure.step("Проверить состояние радиокнопок")
    def check_radio_states(self):
        expect(self.no_radio).to_be_disabled()
        expect(self.yes_radio).to_be_enabled()
        expect(self.impressive_radio).to_be_enabled()

    @allure.step("Выбрать Yes")
    def select_yes(self):
        self.yes_label.click()

    @allure.step("Проверить выбранную радиокнопку")
    def check_selected_radio(self):
        expect(self.yes_radio).to_be_checked()
        expect(self.impressive_radio).not_to_be_checked()


class DemoQACheckboxPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://demoqa.com/checkbox"

        # Локаторы
        self.home_checkbox_text = page.get_by_text("Home", exact=True)
        self.desktop_checkbox_text = page.get_by_text("Desktop", exact=True)
        self.toggle_button = page.locator("button[title='Toggle']")

    @allure.step("Открыть страницу Checkbox")
    def open(self):
        self.page.goto(self.url)

    @allure.step("Проверить видимость элементов")
    def check_initial_visibility(self):
        expect(self.home_checkbox_text).to_be_visible()
        expect(self.desktop_checkbox_text).to_be_hidden()

    @allure.step("Раскрыть дерево")
    def expand_tree(self):
        self.toggle_button.click()

    @allure.step("Проверить видимость Desktop после раскрытия")
    def check_desktop_visible(self):
        expect(self.desktop_checkbox_text).to_be_visible()


class DemoQADynamicPropertiesPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://demoqa.com/dynamic-properties"

        # Локаторы
        self.visible_after_button = page.locator("#visibleAfter")

    @allure.step("Открыть страницу Dynamic Properties")
    def open(self):
        self.page.goto(self.url)

    @allure.step("Проверить что кнопка скрыта")
    def check_button_hidden(self):
        expect(self.visible_after_button).to_be_hidden()

    @allure.step("Дождаться появления кнопки")
    def wait_for_button(self, timeout: int = 10000):
        expect(self.visible_after_button).to_be_visible(timeout=timeout)

    @allure.step("Проверить что кнопка не прикреплена")
    def check_button_not_attached(self):
        expect(self.visible_after_button).not_to_be_attached()

    @allure.step("Дождаться селектора кнопки")
    def wait_for_button_selector(self):
        self.page.wait_for_selector("#visibleAfter")


class DemoQATextBoxPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://demoqa.com/text-box"

        # Локаторы
        self.user_name_input = page.locator("#userName")
        self.user_email_input = page.locator("#userEmail")
        self.current_address_input = page.locator("#currentAddress")
        self.permanent_address_input = page.locator("#permanentAddress")
        self.submit_button = page.locator("#submit")

        # Output локаторы
        self.output_name = page.locator("#output #name")
        self.output_email = page.locator("#output #email")
        self.output_current_address = page.locator("#output #currentAddress")
        self.output_permanent_address = page.locator("#output #permanentAddress")

    @allure.step("Открыть страницу Text Box")
    def open(self):
        self.page.goto(self.url)

    @allure.step("Заполнить поле имени: {name}")
    def fill_user_name(self, name: str):
        self.user_name_input.fill(name)

    @allure.step("Заполнить поле email: {email}")
    def fill_user_email(self, email: str):
        self.user_email_input.fill(email)

    @allure.step("Заполнить текущий адрес: {address}")
    def fill_current_address(self, address: str):
        self.current_address_input.fill(address)

    @allure.step("Заполнить постоянный адрес: {address}")
    def fill_permanent_address(self, address: str):
        self.permanent_address_input.fill(address)

    @allure.step("Заполнить всю форму")
    def fill_form(self, name: str, email: str, current_addr: str, permanent_addr: str):
        self.fill_user_name(name)
        self.fill_user_email(email)
        self.fill_current_address(current_addr)
        self.fill_permanent_address(permanent_addr)

    @allure.step("Нажать кнопку Submit")
    def click_submit(self):
        self.submit_button.click()

    @allure.step("Проверить вывод данных")
    def check_output(self, expected_name: str, expected_email: str,
                    expected_current_addr: str, expected_permanent_addr: str):
        expect(self.output_name).to_have_text(f'Name:{expected_name}')
        expect(self.output_email).to_have_text(f'Email:{expected_email}')
        expect(self.output_current_address).to_have_text(f'Current Address :{expected_current_addr}')
        expect(self.output_permanent_address).to_have_text(f'Permananet Address :{expected_permanent_addr}')
