from django.urls import path, include
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('register/', views.UserRegisterPhoneView.as_view(), name='user_register_phone'),
    path('register_code/', views.UserRegisterCodeView.as_view(), name='user_register_code'),
    path('register_info/', views.UserRegisterInfoView.as_view(), name='user_register_info'),
    path('addresses_info/', views.AddressesView.as_view(), name='addresses'),
]
