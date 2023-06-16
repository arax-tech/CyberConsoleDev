from django.urls import path
from .views import ClientDomainView


urlpatterns = [
    path("domains/", ClientDomainView.as_view(), name="domains"),
]
