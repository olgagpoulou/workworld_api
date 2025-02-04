from django.db.migrations import serializer
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .models import Conversation, Message
from .serializers import MessageSerializer
from .serializers import ConversationSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer
from rest_framework.response import Response
from django.conf import settings
from .models import User
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
import jwt, datetime
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ProfessionalProfile
from .serializers import ProfessionalProfileSerializer
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

# Δημιουργία logger
logger = logging.getLogger(__name__)

User= get_user_model()

# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Εξαίρεση από το default IsAuthenticated
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)

        # Ελέγχουμε αν τα δεδομένα είναι έγκυρα
        if serializer.is_valid():
            user = serializer.save()  # Δημιουργούμε τον χρήστη

            # Δημιουργία token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Επιστρέφουμε τα δεδομένα του χρήστη και το μήνυμα επιτυχίας
            return Response({
                'message': 'User created successfully!',
                'accessToken': access_token,
                'refreshToken': str(refresh),
                'user': serializer.data  # Επιστρέφουμε τα δεδομένα του χρήστη
            }, status=status.HTTP_201_CREATED)  # Επιτυχία με κωδικό 201 (Created)

        # Αν τα δεδομένα δεν είναι έγκυρα, επιστρέφουμε τα σφάλματα
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
class LoginView(APIView):
    permission_classes = [AllowAny]  # Εξαίρεση από το default IsAuthenticated
    def post(self, request):
        # Λήψη email και password από το αίτημα
        email=request.data['email']
        password=request.data['password']
        # Αν δεν βρεθεί χρήστης με το συγκεκριμένο email
        user=User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        # Έλεγχος κωδικού πρόσβασης
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        # Δημιουργία των JWT tokens χρησιμοποιώντας το RefreshToken
        refresh = RefreshToken.for_user(user)

        # Δημιουργία απάντησης με το Response από το Django REST Framework
        response_data = {
                'message': 'Login successful',
                'accessToken': str(refresh.access_token),  # Πρόσβαση στο access token
                'refreshToken': str(refresh)  # Πρόσβαση στο refresh token
            }

        return Response(response_data)




class UserView(APIView):
    permission_classes = [IsAuthenticated]   # Εξαίρεση από το default IsAuthenticated
    def get(self, request):
        user = request.user  # Παίρνουμε τον χρήστη από το request
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={
            'message': 'Logout successful'
        }
        return response

# Δυο Views : ένα για την δημιουργία του επαγγελματικού προφίλ του χρήστη
class ProfessionalProfileCreateView(generics.CreateAPIView):


    #authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfessionalProfileSerializer
    parser_classes = [MultiPartParser]
                      #FormParser]  # Προσθήκη του MultiPartParser για την διαχείριση των multipart δεδομένων
    def post(self, request, *args, **kwargs):
        print("Request data:", request.data)

        # Δημιουργούμε το serializer με τα δεδομένα από το request
        serializer = self.get_serializer(data=request.data)
        # Αν το serializer είναι έγκυρο, αποθηκεύουμε το αντικείμενο
        if serializer.is_valid():
            profile = serializer.save(user=self.request.user)  # Σώζουμε το profile με τον χρήστη
            print("Profile created/updated successfully")
            return Response({
                "message": "Profile created or updated successfully!",
                "profile": ProfessionalProfileSerializer(profile).data
            }, status=status.HTTP_200_OK)
        else:
            # Αν το serializer δεν είναι έγκυρο, επιστρέφουμε τα σφάλματα
            print("Serializer errors:", serializer.errors)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # Χρησιμοποιούμε τη συνάρτηση perform_create για να δημιουργήσουμε το προφίλ
        profile = serializer.save(user=self.request.user)
        # Στη συνέχεια μπορούμε να χειριστούμε άλλες ανάγκες όπως η αποθήκευση της εικόνας, αν χρειάζεται
        return profile
# ένα για την προβολή, ενημέρωση, διαγραφή του επαγγελματικού προφίλ του χρήστη
class ProfessionalProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfessionalProfile.objects.all()
    serializer_class = ProfessionalProfileSerializer
    permission_classes = [IsAuthenticated]  # Μόνο συνδεδεμένοι χρήστες μπορούν να το κάνουν

    def get_object(self):# Εξασφαλίζουμε ότι ο χρήστης θα βλέπει μόνο το δικό του επαγγελματικό προφίλ
         return self.request.user.professional_profile


# endpoint για την λίστα αυτων που εχουν δημιουργησει επαγγελματικο προφιλ
class UserProfileListView(generics.ListAPIView):
    queryset = ProfessionalProfile.objects.all()  # Λαμβάνεις όλα τα προφίλ
    serializer_class = ProfessionalProfileSerializer
    permission_classes = [IsAuthenticated]  # Προστασία της λίστας με JWT Authentication
    authentication_classes = [JWTAuthentication]  # Χρήση του JWT Authentication

class UserListView(APIView):
    permission_classes = [IsAuthenticated]  # Μόνο αυθεντικοποιημένοι χρήστες έχουν πρόσβαση

    def get(self, request):
        users = User.objects.all().exclude(email='olgi@gmail.com')  # Παίρνουμε όλους τους χρήστες
        serializer = UserSerializer(users, many=True)  # many=True επειδή είναι λίστα
        return Response(serializer.data)

#Δημιουργια των Views για Conversation και message
# Δημιουργια View για την λίστα των συνομιλιων Get-Post
class ConversationListCreateView(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Φιλτράρουμε τις συνομιλίες που ανήκουν στον χρήστη που είναι συνδεδεμένος
        return self.queryset.filter(participants=self.request.user)

#Δημιουργία View για μια συνομιλια
class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Εξασφαλίζουμε ότι ο χρήστης μπορεί να δει ή να τροποποιήσει μόνο τις συνομιλίες του
        return self.queryset.filter(participants=self.request.user)


# Viewset για τη δημιουργία μηνυμάτων και προβολη αυτων ανα χρήστη
class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation = get_object_or_404(Conversation, id=self.kwargs['conversation_id'])
        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        conversation = get_object_or_404(Conversation, id=self.kwargs['conversation_id'])
        # Ο χρήστης που στέλνει το μήνυμα είναι ο συνδεδεμένος χρήστης
        serializer.save(sender=self.request.user, conversation=conversation)