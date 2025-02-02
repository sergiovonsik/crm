from django.urls import path
from api.views import *

urlpatterns = [
    path("ticket-list/", PaymentTicketList.as_view(),
         name="tickets-list-view"),
    path("ticket/<int:pk>/", PaymentTicketDetail.as_view({  'get': 'retrieve',
                                                                  'put': 'update',
                                                                  'delete': 'destroy'}),
         name="tickets-detail-view"),
    path("user/info/", ClientsViewList.as_view(),
         name="user-data"),
    path("user/<int:pk>/", ClientsViewDetail.as_view({  'get': 'retrieve',
                                                               'put': 'update',
                                                               'delete': 'destroy',
                                                               'patch': 'partial_update'}),
         name="user-data"),
    path("user/add_passes/", AdminAddPassesToClient.as_view({'post': 'create'}),
         name="user-add-passes"),
    path("user/<int:pk>/take_pass/", AdminTakeAPassForClient.as_view({'patch': 'partial_update'}),
         name="user-add-passes"),
]
