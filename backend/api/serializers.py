from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PaymentTicket, Client, Booking, MPPassPrice
from rest_framework.serializers import models


class MPSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPPassPrice
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())

    class Meta:
        model = PaymentTicket
        fields = '__all__'

    def create(self, data):
        print("validated_data:", data)
        amount_of_uses_LEFT = data.get('amount_of_uses')
        data['amount_of_uses_LEFT'] = amount_of_uses_LEFT
        data['order_id'] = "Manually Assigned"
        ticket = PaymentTicket.objects.create(**data)  # Use Client here
        return ticket


class BookingSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    client_username = serializers.CharField(source='client.username', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'client_username', 'client', 'date', 'created_at', 'type_of_service', 'hour', 'ticket']


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
