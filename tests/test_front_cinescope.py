from playwright.sync_api import expect

def test_cinescope_successful_registration(page, user_registration_data):
    """
    Тест на успешную регистрацию в Cinescope с генерацией данных
    Использует фикстуры page и user_registration_data из conftest.py
    """
    user_data = user_registration_data

    page.goto("https://dev-cinescope.coconutqa.ru/register")

    page.fill("[name='fullName']", user_data['full_name'])
    page.fill("[name='email']", user_data['email'])
    page.fill("[name='password']", user_data['password'])
    page.fill("[name='passwordRepeat']", user_data['password_repeat'])

    page.click('[type="submit"]')

    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)