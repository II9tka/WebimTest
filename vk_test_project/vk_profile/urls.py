from django.urls import path
from django.urls import include
from .views import MainPageView

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', MainPageView.as_view(), name='main_page')
]
