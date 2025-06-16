from django.http import JsonResponse
from .serializers import ListReservationSerializer, CreateReservationSerializer
from django.contrib.auth.models import User
from .models import Reservation
from events.models import Event
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# Create your views here.

class UserReservationListAPIView(generics.ListAPIView):
	queryset= Reservation.objects.all()
	serializer_class= ListReservationSerializer
	permission_classes= [
		IsAuthenticated,
	]
	
	def get_queryset(self):
		qs= super().get_queryset()
		return qs.filter(user= self.request.user)

class UserReservationCreateAPIView(generics.CreateAPIView):
	queryset= Reservation.objects.all()
	serializer_class= CreateReservationSerializer
	permission_classes= [
		IsAuthenticated,
	]

class UserReservationDeleteAPIView(generics.DestroyAPIView):
	queryset= Reservation.objects.all()
	lookup_field= "event"
	permission_classes= [
		IsAuthenticated,
	]
	
	def perform_destroy(instance):
		super.perform_destroy(instance)
