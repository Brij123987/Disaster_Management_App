from django.urls import path
from user_system import views
from user_system.registration import user_register

app_name = "user_system"

urlpatterns = [
    path('getUser/', views.get_user_data, name='get_user_data'),
    path('createUser/', views.create_user_data, name='create_user_data'),
    path('register/', user_register.create_user, name='register'),
    path('login/',user_register.user_login, name='user_login'),
]