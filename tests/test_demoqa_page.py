from page_objects.demoqa_page import *
import allure


@allure.epic("DemoQA")
@allure.feature("Text Box")
class TestDemoQATextBox:

    @allure.title("Заполнение Text Box формы")
    def test_demo_qa_text_box(self, page):
        """
        Тест текст бокса
        """
        text_box_page = DemoQATextBoxPage(page)

        text_box_page.open()
        text_box_page.fill_form(
            name="Andrew",
            email="ass@gmail.com",
            current_addr="burggers-street-18",
            permanent_addr="berries-street-35"
        )
        text_box_page.click_submit()
        text_box_page.check_output(
            expected_name="Andrew",
            expected_email="ass@gmail.com",
            expected_current_addr="burggers-street-18",
            expected_permanent_addr="berries-street-35"
        )


@allure.epic("DemoQA")
@allure.feature("Web Tables")
class TestDemoQAWebTables:

    @allure.title("Открытие модального окна добавления в таблицу")
    def test_demo_qa_web_tables(self, page):
        """
        Нажатие на кнопку Add в таблице
        """
        web_tables_page = DemoQAWebTablesPage(page)

        web_tables_page.open()
        web_tables_page.click_add()
        web_tables_page.check_modal_visible()


@allure.epic("DemoQA")
@allure.feature("Practice Form")
class TestDemoQAPracticeForm:

    @allure.title("Полное заполнение Practice Form")
    def test_demo_qa_practice_form(self, page):
        """
        Полное заполнение формы на регистрацию
        """
        practice_form_page = DemoQAPracticeFormPage(page)

        practice_form_page.open()
        practice_form_page.check_default_dob()

        practice_form_page.fill_first_name("Andrew")
        practice_form_page.fill_last_name("Gerger")
        practice_form_page.fill_email("ass@gmail.com")
        practice_form_page.fill_mobile("8098123123")

        practice_form_page.select_male()
        practice_form_page.select_dob()
        practice_form_page.select_maths_subject()
        practice_form_page.select_sports_hobby()

        practice_form_page.upload_file("data/test_files/cars.jpg")

        practice_form_page.fill_current_address("Burger street 23")

        practice_form_page.select_ncr_state()
        practice_form_page.select_delhi_city()

        practice_form_page.click_submit()
        practice_form_page.check_success_message()
        practice_form_page.check_footer_text()


@allure.epic("DemoQA")
@allure.feature("Radio Button")
class TestDemoQARadioButton:

    @allure.title("Проверка состояния радиокнопок")
    def test_radio_button_states(self, page):
        """
        Проверка включенности/отключенности радиокнопок
        """
        radio_page = DemoQARadioButtonPage(page)

        radio_page.open()
        radio_page.check_radio_states()

    @allure.title("Выбор радиокнопки и проверка состояния")
    def test_radio_button_selection(self, page):
        """
        Выбор радиокнопки и проверка выбранного состояния
        """
        radio_page = DemoQARadioButtonPage(page)

        radio_page.open()
        radio_page.select_yes()
        radio_page.check_selected_radio()


@allure.epic("DemoQA")
@allure.feature("Checkbox")
class TestDemoQACheckbox:

    @allure.title("Проверка видимости чекбоксов в дереве")
    def test_checkbox_visibility(self, page):
        """
        Проверка видимости чекбоксов в дереве
        """
        checkbox_page = DemoQACheckboxPage(page)

        checkbox_page.open()
        checkbox_page.check_initial_visibility()
        checkbox_page.expand_tree()
        checkbox_page.check_desktop_visible()


@allure.epic("DemoQA")
@allure.feature("Dynamic Properties")
class TestDemoQADynamicProperties:

    @allure.title("Проверка появления динамической кнопки")
    def test_dynamic_properties_wait(self, page):
        """
        Ожидание появления динамической кнопки
        """
        dynamic_page = DemoQADynamicPropertiesPage(page)

        dynamic_page.open()
        dynamic_page.check_button_hidden()
        dynamic_page.wait_for_button()

