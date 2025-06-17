from .serializers import ListReservationSerializer, CreateReservationSerializer, UpdateReservationSerializer
from django.contrib.auth.models import User
from .models import Reservation
from events.models import Event
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

# Create your views here.

class UserReservationListAPIView(generics.ListAPIView):
	queryset= Reservation.objects.all()
	serializer_class= ListReservationSerializer
	authentication_classes= [
		TokenAuthentication
	]
	permission_classes= [
		IsAuthenticated,
	]
	
	def get_queryset(self):
		qs = super().get_queryset()
		return qs.filter(user=self.request.user)

class UserReservationCreateAPIView(generics.CreateAPIView):
	queryset= Reservation.objects.all()
	serializer_class= CreateReservationSerializer
	authentication_classes= [
		TokenAuthentication
	]
	permission_classes= [
		IsAuthenticated,
	]

	def perform_create(self, serializer):
		user = self.request.user
		# Get the event and number of tickets from the data validated by the serializer
		event = serializer.validated_data['event']
		num_tickets = serializer.validated_data['num_tickets']



class UserReservationUpdateAPIView(generics.UpdateAPIView):
	queryset= Reservation.objects.all()
	serializer_classes= UpdateReservationSerializer
	authentication_classes= [
		TokenAuthentication
	]
	permission_classes= [
		IsAuthenticated,
	]
	lookup_field= "event"
	
	def get_queryset(self):
		qs= super().get_queryset()
		return qs.filter(user= self.request.user)

class UserReservationDeleteAPIView(generics.DestroyAPIView):
	queryset= Reservation.objects.all()
	lookup_field= "event"
	authentication_classes= [
		TokenAuthentication
	]
	permission_classes= [
		IsAuthenticated,
	]
	
	def perform_destroy(self, instance):
		super.perform_destroy(instance)
