from django.urls import path
from .views import PriceHistory

urlpatterns = [
    path('', PriceHistory.as_view(), name='price_history'),
]