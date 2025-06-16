from django.urls import path
from . import views

urlpatterns= [
	path("list/", views.EventListAPIView.as_view()),
	path("<str:title>/", views.EventDetailAPIView.as_view()),
	path("create/", views.EventCreateAPIView.as_view()),
	path("delete/<str:title>/", views.EventDeleteAPIView.as_view())
]
