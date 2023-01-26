from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet, ProductViewSet

router = DefaultRouter()
router.register('companies', CompanyViewSet, basename='companies')
router.register('products', ProductViewSet, basename='products')


urlpatterns = [
    path('v1/', include(router.urls)),
]
