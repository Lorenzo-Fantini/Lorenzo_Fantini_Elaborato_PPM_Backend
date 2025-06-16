from django.urls import path
from . import views

urlpatterns= [
	path("register/", views.UserCreateAPIView.as_view()),
	path("delete/<str:username>/", views.UserDeleteAPIView.as_view()),
]
