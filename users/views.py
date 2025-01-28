from django.db.migrations import serializer
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer
from rest_framework.response import Response
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
    permission_classes = [AllowAny]  # Εξαίρεση από το default IsAuthenticated
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Token not found')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token')


        user=User.objects.filter(id=payload['id']).first()

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


