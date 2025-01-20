
from django.contrib.messages import api
from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView
from .views import ProfessionalProfileCreateView, ProfessionalProfileDetailView
urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/create/', ProfessionalProfileCreateView.as_view(), name='create-profile'),
    path('profile/', ProfessionalProfileDetailView.as_view(), name='get-update-delete-profile'),
]