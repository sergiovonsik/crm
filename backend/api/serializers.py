from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PaymentTicket, Client
from rest_framework.serializers import models


class TicketSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())

    class Meta:
        model = PaymentTicket
        fields = ['type_of_service', 'is_expired', 'amount_of_uses_LEFT', 'owner', 'expire_time']

    def create(self, data):
        print("validated_data:", data)
        ticket = PaymentTicket.objects.create(**data)  # Use Client here
        return ticket


class ClientSerializer(serializers.ModelSerializer):
    payment_ticket = TicketSerializer(many=True, read_only=True)  # Fetch related tickets

    class Meta:
        model = Client  # Use Client instead of User
        fields = ["id", "username", "password", 'payment_ticket']
        # extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Client.objects.create_user(**validated_data)  # Use Client here
        return user
