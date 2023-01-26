""" для генерации рандомных данных использую библиотеку mimesis
Cайт: https://mimesis.name/en/master/index.html """
from random import choice, randint

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from mimesis import Address, Datetime, Finance, Person, Transport
from mimesis.enums import Gender
from mimesis.locales import Locale

from companies.models import Company, Product
from users.models import User

# Настройки mimesis для локализации данных и гендера
LOCALES = [Locale.RU, Locale.DE, Locale.PL, Locale.EN_GB]
GENDERS = [Gender.FEMALE, Gender.MALE]
# Количество данных
COMPANY_COUNT = 15
EMPLOYEES_COUNT = 50
PRODUCT_COUNT = 2
# Пароль для сотрудников будет одинаковым для удобства тестирования
PASSWORD = make_password('1')


def get_product(iter):
    '''Returns Product instance'''
    transport = Transport()
    date = Datetime()
    return Product(
            name=transport.manufacturer(),
            model=transport.car(),
            release_date=date.date()
        )


class Command(BaseCommand):
    help = "Loads test data"

    def handle(self, *args, **options):
        print('Загрузка тестовых данных в БД')

        users = []

        # создаем продукцию. Не нашел в либе ничего более внятного, чем авто
        # поэтому не удивляйтесь если завод Макдональдс
        # выпускает Maybach.
        Product.objects.bulk_create(map(get_product, range(PRODUCT_COUNT)))
        for _ in range(COMPANY_COUNT):
            # выбираем случайную страну и создаем объекты mimesis
            locale = choice(LOCALES)
            person = Person(locale)
            finance = Finance(locale)
            address = Address(locale)
            # первый объект обязательно завод
            hierarchy = randint(0, 4) if Company.objects.exists() else 0
            company = Company(
                hierarchy=hierarchy,
                name=finance.company(),
                email=person.email(),
                country=address.country(),
                city=address.city(),
                street=address.street_name(),
                house_number=randint(1, 200)
            )
            company.save()

            # Если не завод связываем компанию со случайным поставщиком
            # стоящим выше по иерархии, добавляем продукцию и долг
            if company.hierarchy:
                company.provider = Company.objects.filter(
                    hierarchy__lt=company.hierarchy
                ).order_by("?").first()
                company.debt = randint(0, 5000)
                company.save()
                # выберем все продукты поставщика
                provider_products = company.provider.products.all()
                # немного срежем количество продуктов у дистрибьютеров
                provider_products = provider_products[
                    :randint(len(provider_products)//2, len(provider_products))
                ]
                map(company.products.add, provider_products)
            # если завод связываем со случайным количеством продукции
            else:
                for _ in range(randint(PRODUCT_COUNT/2, PRODUCT_COUNT)):
                    company.products.add(Product.objects.order_by("?").first())

            # количество работников зависит от размера компании
            employees = (EMPLOYEES_COUNT//(company.hierarchy+1))
            for _ in range(employees):
                gender = choice(GENDERS)
                users.append(User(
                    username=person.username(),
                    password=PASSWORD,
                    first_name=person.first_name(gender=gender),
                    last_name=person.last_name(gender=gender),
                    email=person.email(),
                    company=company
                ))
        User.objects.bulk_create(users)
