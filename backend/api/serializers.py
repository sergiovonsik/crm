from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PaymentTicket, Client, Booking
from rest_framework.serializers import models


class TicketSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())

    class Meta:
        model = PaymentTicket
        fields = '__all__'

    def create(self, data):
        print("validated_data:", data)
        ticket = PaymentTicket.objects.create(**data)  # Use Client here
        return ticket


class BookingSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())

    class Meta:
        model = Booking
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    payment_ticket = TicketSerializer(many=True, read_only=True)  # Fetch related tickets
    bookings = BookingSerializer(many=True, read_only=True)  # Fetch related tickets

    class Meta:
        model = Client  # Use Client instead of User
        fields = ["id", "username", 'password', 'email', 'bookings',
                  'is_staff', 'date_joined', 'payment_ticket']
        extra_kwargs = {
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
            "date_joined": {"read_only": True}
        }

    def create(self, validated_data):
        user = Client.objects.create_user(**validated_data)  # Use Client here
        return user

