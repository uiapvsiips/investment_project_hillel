from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.user_info),
    path('short_info/', api_views.user_short_info),
    path('contracts/', api_views.get_user_contracts),
    path('contracts/new/', api_views.user_new_contract),
    path('add_wallet/', api_views.user_add_wallet),
]
