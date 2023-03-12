from django.urls import path
from rest_framework import routers
from .api import AccountViewSet, TransactionViewSet

router = routers.DefaultRouter()

router.register('accounts', AccountViewSet, 'accounts'),
router.register('transactions', TransactionViewSet, 'transactions'),


urlpatterns = router.urls