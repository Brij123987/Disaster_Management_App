from django.urls import path
from user_system import views

app_name = "user_system"

urlpatterns = [
    path('getUser/', views.get_user_data, name='get_user_data'),
    path('createUser/', views.create_user_data, name='create_user_data'),
]