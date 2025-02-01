from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PaymentTicket, Client

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTicket
        fields = '__all__'  # Correct way to reference all fields
        extra_kwargs = {"owner": {"read_only": True}}  # Make 'belongs_to' read-only


class ClientSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)  # Fetch related tickets
    class Meta:
        model = Client  # Use Client instead of User
        fields = ["id", "username", "password",
                  "classes_left", "free_climbing_left", 'tickets']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        # Create a Client object (not a User object)
        user = Client.objects.create_user(**validated_data)  # Use Client here
        return user
