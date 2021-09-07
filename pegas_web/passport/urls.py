  
from django.urls import path
from .views import *
from django.urls import include
from .forms import UserLoginForm
from django.contrib.auth import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('regestration/', Regestration.as_view(), name='regestration'),
    path(
        'login/',
        views.LoginView.as_view(
            template_name="passport/login.html",
            authentication_form=UserLoginForm
            ),
        name='login'
        ),
    # path('', personal_main, name='personal_main'),
    path('logout/', logout_view, name='logout_personal'),
]