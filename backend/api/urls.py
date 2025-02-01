from django.urls import path
from api.views import ClientsViewList, ClientsViewDetail, PaymentTicketList, PaymentTicketDetail

urlpatterns = [
    path("ticket-list/", PaymentTicketList.as_view(), name="tickets-list-view"),
    path("ticket/<int:pk>/", PaymentTicketDetail.as_view({'get': 'retrieve',
                                                                'put': 'update',
                                                                'delete': 'destroy'}), name="tickets-detail-view"),
    path("user/info/", ClientsViewList.as_view(), name="user-data"),
    path("user/<int:pk>/info/", ClientsViewDetail.as_view({'get': 'retrieve',
                                                                'put': 'update',
                                                                'delete': 'destroy'}), name="user-data"),
]
