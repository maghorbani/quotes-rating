from django.urls import path, include
from .views import QuoteView

urlpatterns = [
    path('', QuoteView.as_view({'get': 'list'}), name="quote"),
]
