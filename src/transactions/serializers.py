from rest_framework import serializers
from .models import Transaction

class GetTransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model= Transaction
		fields= (
			"user",
            "event",
            "num_tickets",
			"amount",
		)