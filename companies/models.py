from django.db import models


class Product(models.Model):
    name = models.CharField(
        verbose_name='Название продукта',
        max_length=25
    )
    model = models.CharField(
        verbose_name='Модель продукта',
        max_length=100
    )
    release_date = models.DateField(
        verbose_name='Дата выхода на рынок',
        auto_now=False,
        auto_now_add=False
    )

    def __str__(self):
        return self.name


class Company(models.Model):
    TYPES = (
        (0, 'Завод'),
        (1, 'Дистрибьютер'),
        (2, 'Дилерский центр'),
        (3, 'Крупная розничная сеть'),
        (4, 'Индивидуальный предприниматель')
    )
    hierarchy = models.SmallIntegerField(
            verbose_name='Тип компании',
            choices=TYPES)
    name = models.CharField(
        verbose_name='Название компании',
        max_length=50,
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    country = models.CharField(
        verbose_name='Название страны',
        max_length=100
    )
    city = models.CharField(
        verbose_name='Название города',
        max_length=100
    )
    street = models.CharField(
        verbose_name='Название улицы',
        max_length=100
    )
    house_number = models.CharField(
        verbose_name='Номер дома',
        max_length=50
    )
    products = models.ManyToManyField(
        Product,
        related_name='сompanies'
    )
    provider = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        verbose_name='Поставщик',
        related_name='traders',
        null=True,
        blank=True,
    )
    debt = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Задолженность',
        default=0
        )
    pub_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
