from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns= [
	path("register/", views.UserCreateAPIView.as_view()),
	path("delete/", views.UserDeleteAPIView.as_view()),
	path("token/", obtain_auth_token)
]
