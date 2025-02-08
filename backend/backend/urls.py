from django.contrib import admin
from django.urls import path, include
from api.views import ClientsViewList, ClientsViewDetail, PaymentTicketList, PaymentTicketDetail
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import GoogleAuthView

urlpatterns = [
    path("admin/", admin.site.urls),
    #path("api/user/register/", GoogleAuthViewSet.as_view({'post':'create'}), name="register"),
    path("api/user/AuthGoogle/auth/", GoogleAuthView.as_view(), name="login-register-google"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
]
