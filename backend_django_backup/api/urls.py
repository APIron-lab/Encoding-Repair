from django.urls import path
from .views import TokenCountView

urlpatterns = [
    path("token/count/", TokenCountView.as_view(), name="token-count"),
]

