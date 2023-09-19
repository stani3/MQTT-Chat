from django.urls import path
from . import views

urlpatterns = [
	path('register', views.create_user, name='register'),
	path('login', views.user_login, name='login'),
	path('logout', views.logout_view, name='logout'),
	path('auth', views.verify_auth_token, name='auth'),
	path('getuser', views.get_user_by_token, name='getusr'),
	path('User/<int:user_id>/', views.get_user_by_id, name='get-user-by-id'),
]

