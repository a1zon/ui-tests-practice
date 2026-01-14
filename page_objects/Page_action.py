import allure
from playwright.sync_api import Page


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def enter_text_to_element(self, locator: str, text: str):
        self.page.fill(locator, text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: str):
        self.page.click(locator)

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_redirect_for_url(self, url: str):
        self.page.wait_for_url(url)
        assert self.page.url == url, f"Редирект на {url} не произошел"

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: str) -> str:
        return self.page.locator(locator).text_content()

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def wait_for_element(self, locator: str, state: str = "visible"):
        self.page.locator(locator).wait_for(state=state)

    @allure.step("Скриншот текущей страницы")
    def make_screenshot_and_attach_to_allure(self, name: str = "Screenshot"):
        screenshot_path = "screenshot.png"
        self.page.screenshot(path=screenshot_path, full_page=True)

        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name=name, attachment_type=allure.attachment_type.PNG)

    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_pop_up_element_with_text(self, text: str):
        with allure.step(f"Проверка появления алерта с текстом: '{text}'"):
            notification_locator = self.page.get_by_text(text)
            notification_locator.wait_for(state="visible")
            assert notification_locator.is_visible(), "Уведомление не появилось"

        with allure.step(f"Проверка исчезновения алерта с текстом: '{text}'"):
            notification_locator.wait_for(state="hidden")
            assert not notification_locator.is_visible(), "Уведомление не исчезло"


class BasePage(PageAction):
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = "https://dev-cinescope.coconutqa.ru/"

        self.home_button_css = "a[href='/']"

        self.home_button_xpath = "//a[@href='/' and text()='Cinescope']"

        # Для "Все фильмы"
        self.all_movies_button_css = "a[href='/movies']"
        self.all_movies_button_xpath = "//a[@href='/movies' and text()='Все фильмы']"

        # Новые локаторы с get_by_role
        self.home_button = page.get_by_role("link", name="Cinescope")
        self.all_movies_button = page.get_by_role("link", name="Все фильмы")

    @allure.step("Переход на главную страницу, из шапки сайта")
    def go_to_home_page(self):
        """Переход на главную страницу (использует новый локатор)"""
        self.home_button.click()
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы, из шапки сайта'")
    def go_to_all_movies(self):
        """Переход на страницу 'Все фильмы' (использует новый локатор)"""
        self.all_movies_button.click()
        self.wait_redirect_for_url(f"{self.home_url}movies")

    @allure.step("Переход на главную страницу (старый метод CSS)")
    def go_to_home_page_css(self):
        """Старый метод с CSS локаторами (для совместимости)"""

        self.click_element(self.home_button_css)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на главную страницу (старый метод XPath)")
    def go_to_home_page_xpath(self):
        """Метод с XPath локатором (если CSS не работает)"""
        self.page.click(self.home_button_xpath)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы (старый метод CSS)'")
    def go_to_all_movies_css(self):
        """Старый метод с CSS локаторами (для совместимости)"""
        self.click_element(self.all_movies_button_css)
        self.wait_redirect_for_url(f"{self.home_url}movies")

    @allure.step("Переход на страницу 'Все фильмы (старый метод XPath)'")
    def go_to_all_movies_xpath(self):
        """Метод с XPath локатором (если CSS не работает)"""
        self.page.click(self.all_movies_button_xpath)
        self.wait_redirect_for_url(f"{self.home_url}movies")
