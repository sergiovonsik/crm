from django.contrib import admin
from django.urls import path, include
from api.views import (
    ClientsViewList,
    ClientsViewDetail,
    PaymentTicketList,
    PaymentTicketDetail,
    Logout,
    GoogleAuthView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/logout/", Logout.as_view(), name="logout"),
    path("api/user/register/", ClientsViewList.as_view(), name="register"),
    path("api/user/auth/google/", GoogleAuthView.as_view(), name="login-register-google"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
]
