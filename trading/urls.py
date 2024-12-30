from django.urls import path
from .views import SaveQuotes

urlpatterns = [
    path("save_quotes/", SaveQuotes.as_view(), name="save_quotes"),
]
