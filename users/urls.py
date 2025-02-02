
from django.contrib.messages import api
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import RegisterView, LoginView, UserView, LogoutView
from .views import ProfessionalProfileCreateView, ProfessionalProfileDetailView
urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/create/', ProfessionalProfileCreateView.as_view(), name='create-profile'),
    path('profile/', ProfessionalProfileDetailView.as_view(), name='get-update-delete-profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
# Αν είμαστε σε κατάσταση ανάπτυξης, εξυπηρετούμε τα media αρχεία
if settings.DEBUG:
    urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)