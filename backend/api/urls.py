from django.urls import path
from api.views import *




urlpatterns = [
    path("ticket-list/", PaymentTicketList.as_view(),
         name="tickets-list-view"),
    path("ticket/<int:pk>/", PaymentTicketDetail.as_view({'get': 'retrieve',
                                                                'put': 'update',
                                                                'delete': 'destroy'}),
         name="tickets-detail-view"),

    #userActions
    path("users/info/", ClientsViewList.as_view(),
         name="users-data"),
    path("user/<int:pk>/info/", ClientsViewDetail.as_view({'get': 'retrieve',
                                                                 'put': 'update',
                                                                 'delete': 'destroy',
                                                                 'patch': 'partial_update'}),
         name="user-data"),
    path("user/me/info/", ClientsViewDetail.as_view({'get': 'list'}),
         name="user-data"),
    path("user/add_passes/", AdminAddPassesToClient.as_view({'post': 'create'}),
         name="user-add-passes"),
    path("user/book_pass/", UserBookingViewSet.as_view({'post': 'create'}),
         name="user-book-passes"),

    #mercadoPago
    path("mercadopago/pay/", MercadoPagoTicket.as_view({'post': 'create'}),
         name="mercadopago"),
    path("mercadopago/succes-hook/", MercadoPagoSuccesHook.as_view(),
         name='webhook'),

    #adminActions
    path("userAdmin/BookingChart/", AdminPassesChartData.as_view(),
         name="booking-chart-data"),
    path("userAdmin/TicketChart/", AdminTicketsChartData.as_view(),
         name="ticket-chart-data"),
    path("userAdmin/ActiveClientsChart/", AdminActiveClientsChartData.as_view(),
         name="active-clients-chart-data"),
    path("userAdmin/TypeOfServiceChartData/", AdminTypeOfServiceChartData.as_view(),
         name="type-of-service-chart-data"),


]
