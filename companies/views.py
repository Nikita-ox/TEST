from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Company, Product
from .serializers import (CompanyQRSerializer, CompanySerializer,
                          ProductSerializer)
from .tasks import send_qr_to_email


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country', 'products']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Company.objects.all()
        else:
            return Company.objects.filter(id=self.request.user.company.id)

    @action(detail=False, url_path='big_debt')
    def get_big_debt_creditors(self, request):
        '''Returns list companies whose debt bigger then average'''
        avg = Company.objects.aggregate(Avg('debt'))['debt__avg']
        queryset = Company.objects.filter(debt__gt=avg)
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, url_path='get_qr')
    def get_contact_in_qr(self, request, pk=None):
        '''Returns company contacts in QR'''
        obj = Company.objects.get(id=pk)
        serializer = CompanyQRSerializer(obj)
        email = request.user.email
        send_qr_to_email.delay(serializer.data, email)
        return Response(f'message sended to {email}')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
