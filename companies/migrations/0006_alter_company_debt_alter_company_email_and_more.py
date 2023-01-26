# Generated by Django 4.1.3 on 2022-11-27 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_company_hierarchy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='debt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Задолженность'),
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='hierarchy',
            field=models.SmallIntegerField(choices=[(0, 'Завод'), (1, 'Дистрибьютер'), (2, 'Дилерский центр'), (3, 'Крупная розничная сеть'), (4, 'Индивидуальный предприниматель')], verbose_name='Тип компании'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название компании'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=25, unique=True, verbose_name='Название продукта'),
        ),
    ]
