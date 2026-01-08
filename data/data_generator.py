import random
from faker import Faker

class TestDataGenerator:
    """Класс для генерации тестовых данных"""

    def __init__(self, locale='ru_RU'):
        self.fake = Faker(locale)
        self.generated_emails = set()  # Для отслеживания уже использованных email

    def get_unique_email(self, domain=None):
        """Генерация уникального email"""
        if domain is None:
            domain = self.fake.free_email_domain()

        while True:
            username = self.fake.user_name()
            email = f"{username}@{domain}"

            # Проверяем уникальность в рамках текущей сессии
            if email not in self.generated_emails:
                self.generated_emails.add(email)
                return email

    def get_full_name(self):
        """Генерация полного имени"""
        # Можно выбрать разные форматы
        formats = [
            lambda: f"{self.fake.first_name_male()} {self.fake.last_name_male()}",
            lambda: f"{self.fake.first_name_female()} {self.fake.last_name_female()}",
            lambda: f"{self.fake.first_name()} {self.fake.middle_name()} {self.fake.last_name()}",
        ]
        return random.choice(formats)()

    def get_strong_password(self, length=12):
        """Генерация надежного пароля"""
        # Минимальные требования: буквы, цифры, спецсимволы
        lower = self.fake.password(length=4, special_chars=False, digits=False, upper_case=False)
        upper = self.fake.password(length=3, special_chars=False, digits=False, upper_case=True)
        digits = ''.join(str(self.fake.random_digit()) for _ in range(3))
        special = ''.join(random.choice('!@#$%^&*') for _ in range(2))

        # Собираем и перемешиваем
        password = list(lower + upper + digits + special)
        random.shuffle(password)
        return ''.join(password)

    def get_registration_data(self):
        """Полный набор данных для регистрации"""
        return {
            'full_name': self.get_full_name(),
            'email': self.get_unique_email(),
            'password': self.get_strong_password(),
        }

# Экземпляр для использования в тестах
generator = TestDataGenerator()