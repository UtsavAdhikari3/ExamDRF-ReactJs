from django.urls import path
from .views import RegisterUserView, MeView,LoginView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='user-register'),
    path('me/', MeView.as_view(), name='user-me'),
    path('login/',LoginView.as_view(), name='login')
]
