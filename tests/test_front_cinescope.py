from playwright.sync_api import expect
from helpers.navigation import NavigationHelper

def test_cinescope_successful_registration(page, user_registration_data):
    """
    Тест на успешную регистрацию в Cinescope с генерацией данных
    Использует фикстуры page и user_registration_data из conftest.py
    """
    user_data = user_registration_data

    NavigationHelper.safe_goto(page,"https://dev-cinescope.coconutqa.ru/register")

    page.fill("[name='fullName']", user_data['full_name'])
    page.fill("[name='email']", user_data['email'])
    page.fill("[name='password']", user_data['password'])
    page.fill("[name='passwordRepeat']", user_data['password_repeat'])

    submit_button = page.locator("[type='submit']")
    expect(submit_button).to_be_enabled()

    # явно ждем ответа от сервра и обновление навигации ui
    with page.expect_response(lambda r: "/register" in r.url and r.status == 200):
        submit_button.click()

    # явно ждём финальный текст
    confirmation_text = page.get_by_text("Подтвердите свою почту", exact=True)
    expect(confirmation_text).to_be_visible(timeout=60000)

    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)