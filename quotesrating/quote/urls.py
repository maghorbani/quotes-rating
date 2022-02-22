from django.urls import path, include
from .views import QuoteView, RateView

urlpatterns = [
    path('', QuoteView.as_view({'get': 'list', 'post': 'create'}), name="quote"),
    path('<int:pk>/', QuoteView.as_view({'get': 'retrieve'}), name="get_quote"),
    path('<int:pk>/rate', RateView.as_view({'post': 'create'}), name="rate_a_quote"),
]
