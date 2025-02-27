from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register the Client model with a custom admin interface
class PaymentTicketInline(admin.TabularInline):  # or use StackedInline for a different layout
    model = PaymentTicket
    extra = 1  # Number of empty forms to display for new objects


class CustomClientAdmin(UserAdmin):
    inlines = [PaymentTicketInline]  # Attach the inline to ClientAdmin

    list_display = ('username', 'email', 'is_staff', 'is_active')  # Customize list view
    search_fields = ('username', 'email')
    ordering = ('id',)


# Register the PaymentTicket model
@admin.register(PaymentTicket)
class PaymentTicketAdmin(admin.ModelAdmin):
    list_display = ('owner', 'status', 'amount_of_uses', 'amount_of_uses_LEFT',
                    'order_id', 'type_of_service', 'payment_day',
                    'expire_time', 'is_expired', 'id', 'price', 'left_to_pay')
    list_filter = ('type_of_service', 'payment_day', 'is_expired')
    search_fields = ('owner__username', 'type_of_service')
    ordering = ('expire_time', 'amount_of_uses_LEFT')


# Register the PaymentTicket model
@admin.register(MPPassPrice)
class PaymentTicketAdmin(admin.ModelAdmin):
    list_display = ('price', 'pass_amount', 'type_of_service')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'ticket', 'date', 'type_of_service', 'hour', 'created_at')
    list_filter = ('date', 'type_of_service', 'created_at')
    search_fields = ('client__username', 'type_of_service', 'date')
    ordering = ('date', 'created_at')


admin.site.register(Client, CustomClientAdmin)
