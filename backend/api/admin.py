from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client, PaymentTicket


# Register the Client model with a custom admin interface
class PaymentTicketInline(admin.TabularInline):  # or use StackedInline for a different layout
    model = PaymentTicket
    extra = 1  # Number of empty forms to display for new objects
    readonly_fields = ('payment_day', 'expire_time', 'status', 'amount_of_uses_LEFT')  # Make some fields read-only


class CustomClientAdmin(UserAdmin):
    inlines = [PaymentTicketInline]  # Attach the inline to ClientAdmin

    list_display = ('username', 'email', 'is_staff', 'is_active')  # Customize list view
    search_fields = ('username', 'email')
    ordering = ('id',)


# Register the PaymentTicket model
@admin.register(PaymentTicket)
class PaymentTicketAdmin(admin.ModelAdmin):
    list_display = ('owner', 'order_id', 'type_of_service', 'payment_day',
                    'expire_time', 'id', 'price', 'left_to_pay')
    list_filter = ('type_of_service', 'payment_day')
    search_fields = ('owner__username', 'type_of_service')
    ordering = ('payment_day',)


admin.site.register(Client, CustomClientAdmin)
