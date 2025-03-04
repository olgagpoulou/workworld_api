
from django.contrib.messages import api
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import RegisterView, LoginView, UserView, LogoutView,UserProfileListView,UserListView
from .views import ProfessionalProfileCreateView, ProfessionalProfileDetailView
from .views import ConversationListCreateView, ConversationDetailView, MessageListCreateView,CreateConversationView,MarkMessagesAsRead
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
    path('user_profiles/', UserProfileListView.as_view(), name='user_profile_list'),
    path('users/', UserListView.as_view(), name='users-list'),
    #με αυτο το url μπορω να κανω Get-Post τις λιστες συνομιλιών
    path('conversations/<int:id>/', ConversationDetailView.as_view(), name='conversations-detail'),
    #με αυτο το url μπορω να κανω Get-Put/Patch-Delete μια συγκεκριμενη συνομιλία
    path('conversations/', ConversationListCreateView.as_view(), name='conversations-list-create'),
    #με αυτο το url μπορω να κανω Get-Post μνμ σε μια συγκεκριμενη συνομιλία
    path('conversations/<int:conversation_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    #με αυτο το url ελεγχω αν υπάρχει συνομιλία και αν οχι την δημιουργώ
    path('conversations/create/', CreateConversationView.as_view(), name='create-conversation'),
    #με αυτο το url ελέγχω αν υπάρχουν αδιαβαστα μηνυματα ωστε να εμφανισω ενδειξη
path('conversations/<int:conversation_id>/mark-read/', MarkMessagesAsRead.as_view(), name='mark-messages-read'),
]
# Αν είμαστε σε κατάσταση ανάπτυξης, εξυπηρετούμε τα media αρχεία
if settings.DEBUG:
    urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)