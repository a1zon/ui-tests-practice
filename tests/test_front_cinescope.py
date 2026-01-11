from playwright.sync_api import expect


def test_cinescope_successful_registration(page, test_user):
    """
    Тест на успешную регистрацию в Cinescope с генерацией данных
    Использует фикстуры page и user_registration_data из conftest.py
    """

    page.goto("https://dev-cinescope.coconutqa.ru/register")
    page.wait_for_selector("[name='fullName']", state="visible", timeout=60000)
    page.wait_for_selector("[type='submit']", state="visible", timeout=30000)
    page.fill("[name='fullName']", test_user['fullName'])
    page.fill("[name='email']", test_user['email'])
    page.fill("[name='password']", test_user['password'])
    page.fill("[name='passwordRepeat']", test_user['passwordRepeat'])

    submit_button = page.locator("[type='submit']")
    expect(submit_button).to_be_enabled()
    submit_button.click()

    confirmation_text = page.get_by_text("Подтвердите свою почту", exact=True)
    expect(confirmation_text).to_be_visible(timeout=40000)

    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)
