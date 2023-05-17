from django.urls import path
import contracts.views

urlpatterns = [
    path('', contracts.views.get_all_contracts_handler),
]