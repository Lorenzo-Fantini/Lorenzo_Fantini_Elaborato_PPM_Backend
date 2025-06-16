from django.http import JsonResponse
from events.serializers import GetEventSerializer, DetailEventSerializer, CreateEventSerializer
from events.models import Event
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

# Create your views here.
	
class EventListAPIView(generics.ListAPIView):
	queryset= Event.objects.all()
	serializer_class= GetEventSerializer
	
class EventDetailAPIView(generics.RetrieveAPIView):
	queryset= Event.objects.all()
	serializer_class= DetailEventSerializer
	lookup_field= "title"
	
class EventCreateAPIView(generics.CreateAPIView):
	queryset= Event.objects.all()
	serializer_class= CreateEventSerializer
	authentiation_classes= [
		TokenAuthentication
	]
	permission_classes= [
		IsAdminUser,
	]
	
class EventDeleteAPIView(generics.DestroyAPIView):
	queryset= Event.objects.all()
	lookup_field= "title"
	authentiation_classes= [
		TokenAuthentication
	]
	permission_classes= [
		IsAdminUser,
	]
	
	def perform_destroy(instance):
		super.perform_destroy(instance)
