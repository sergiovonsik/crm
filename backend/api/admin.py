from django.contrib import admin
from .models import Client, PaymentTicket

# Register the Client model with a custom admin interface
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'classes_left', 'free_climbing_left')
    search_fields = ('username', 'email', 'id')
    ordering = ('id',)

# Register the PaymentTicket model
@admin.register(PaymentTicket)
class PaymentTicketAdmin(admin.ModelAdmin):
    list_display = ('owner', 'type_of_service', 'payment_day', 'expire_time')
    list_filter = ('type_of_service',)
    search_fields = ('owner__username', 'type_of_service')
    ordering = ('payment_day',)
