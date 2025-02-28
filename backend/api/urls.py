from django.urls import path
from api.views import *

urlpatterns = [
    path("ticket-list/", PaymentTicketList.as_view(),
         name="tickets-list-view"),
    path("ticket/<int:pk>/", PaymentTicketDetail.as_view({'get': 'retrieve',
                                                          'put': 'update',
                                                          'delete': 'destroy'}),
         name="tickets-detail-view"),

    # userActions
    path("users/info/", ClientsViewList.as_view(),
         name="users-data"),
    path("user/me/info/", UserGetHisData.as_view({'get': 'retrieve'}),
         name="user-data"),
    path("user/book_pass/", UserBookingViewSet.as_view({'post': 'create'}),
         name="user-book-passes"),

    # MERCADO PAGO
    path("mercadopago/pay/", MercadoPagoTicket.as_view({'post': 'create'}),
         name="mercadopago"),
    path("mercadopago/succes-hook/", MercadoPagoSuccesHook.as_view(),
         name='webhook'),
    path("mercadopago/set_price/<int:priceId>/", AdminSetPrices.as_view(),
         name='delete_price'),
    path("mercadopago/set_price/", AdminSetPrices.as_view(),
         name='set_price'),

    path("mercadopago/show_all_prices/", AdminShowAllPrices.as_view({'get': 'list'}),
         name='set_price'),

    # ADMIN ACTIONS
    path("userAdmin/BookingChart/", AdminPassesChartData.as_view(),
         name="booking-chart-data"),
    path("userAdmin/TicketChart/", AdminTicketsChartData.as_view(),
         name="ticket-chart-data"),
    path("userAdmin/ActiveClientsChart/", AdminActiveClientsChartData.as_view(),
         name="active-clients-chart-data"),
    path("userAdmin/TypeOfServiceChartData/", AdminTypeOfServiceChartData.as_view(),
         name="type-of-service-chart-data"),
    path("userAdmin/SearchUsers/", AdminSearchClients.as_view(),
         name="search-clients"),
    path("userAdmin/todayPasses/", AdminGetsTodayPasses.as_view(),
         name="today-passes"),
    path("userAdmin/<int:pk>/info/", AdminGetClientData.as_view({'get': 'retrieve',
                                                                   'put': 'update',
                                                                   'delete': 'destroy',
                                                                   'patch': 'partial_update'}),
         name="user-data"),
    path("userAdmin/<int:pk>/addPasses/", AdminAddPassesToClient.as_view({'post': 'create'}),
         name="admin-add-passes"),
    path("userAdmin/<int:pk>/takeAPass/", AdminTakeAPassForClient.as_view({'post': 'create'}),
         name="admin-take-pass"),

]
