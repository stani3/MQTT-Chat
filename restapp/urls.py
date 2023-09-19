from django.urls import path
from . import views

urlpatterns = [
	path('contacts', views.get_friends, name='contacts'),
	path('contact_requests', views.get_contact_requests, name='contact_requests'),
	path('create_contact', views.contact_request, name='create_contact'),
	path('create_contact/<str:username>/', views.contact_request_by_username, name='create_contact_username'),
	path('contact_request/<int:requester_id>/', views.update_contact_request, name='update_contact_request'),
	path('messages/<int:friend_id>/', views.get_chat, name='get-chat'),
	path('messages-last/<int:friend_id>/', views.get_last_msg, name='get-last'),
	path('message', views.send_message, name='send_message'),


]

