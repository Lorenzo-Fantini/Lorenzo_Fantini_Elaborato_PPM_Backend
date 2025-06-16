from django.urls import path
from . import views

urlpatterns= [
	path("list/", views.UserReservationListAPIView.as_view()),
	path("create/", views.UserReservationCreateAPIView.as_view()),
	path("delete/<str:event>/", views.UserReservationDeleteAPIView.as_view()),
]
