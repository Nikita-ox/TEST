from random import randint

from django.db.models import F

from .models import Company
from .utils import send_mail
from ..backend.celery import app


@app.task
def raise_debt_random():
    raise_debt = randint(5, 500)
    queryset = Company.objects.filter(hierarchy__gt=0)
    queryset.update(debt=F('debt') + raise_debt)


@app.task
def reduce_debt_random():
    reduce_debt = randint(100, 10000)
    queryset_first = Company.objects.filter(debt__gt=reduce_debt)
    queryset_first.update(debt=F('debt') - reduce_debt)
    queryset_second = Company.objects.filter(hierarchy__gt=0,
                                             debt__lte=reduce_debt)
    queryset_second.update(debt=0)


@app.task
def async_clear_debt(list_id):
    for id in list_id:
        Company.objects.filter(id=id['id']).update(debt=0)


@app.task
def send_qr_to_email(data, to_email):
    send_mail(data, to_email)
