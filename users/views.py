from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ProfessionalProfile
from .serializers import ProfessionalProfileSerializer

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)

        # Ελέγχουμε αν τα δεδομένα είναι έγκυρα
        if serializer.is_valid():
            user = serializer.save()  # Δημιουργούμε τον χρήστη

            # Επιστρέφουμε τα δεδομένα του χρήστη και το μήνυμα επιτυχίας
            return Response({
                'message': 'User created successfully!',
                'user': serializer.data  # Επιστρέφουμε τα δεδομένα του χρήστη
            }, status=status.HTTP_201_CREATED)  # Επιτυχία με κωδικό 201 (Created)

        # Αν τα δεδομένα δεν είναι έγκυρα, επιστρέφουμε τα σφάλματα
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
class LoginView(APIView):
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

        # Δημιουργία του JWT token
        payload={
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()

        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # Δημιουργία απάντησης με το Response από το Django REST Framework

        # Δημιουργία απάντησης
        response_data = {
            'message': 'Login successful',
            'accessToken': token  # Προσθήκη του token στο σώμα της απόκρισης
        }

        # Δημιουργία της απόκρισης
        response = Response(response_data)

        #

        return response

class UserView(APIView):
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


#API View για επεξεργασία του Επαγγελματικού Προφίλ με DRF
#Δυο Views : ένα για την δημιουργία του επαγγελματικού προφίλ του χρήστη
class ProfessionalProfileCreateView(generics.CreateAPIView):
    queryset = ProfessionalProfile.objects.all()
    serializer_class = ProfessionalProfileSerializer
    permission_classes = [IsAuthenticated]  # Μόνο συνδεδεμένοι χρήστες μπορούν να το κάνουν

    def perform_create(self, serializer):
        # Εδώ συνδέουμε το προφίλ με τον χρήστη που είναι συνδεδεμένος
        serializer.save(user=self.request.user)


# ένα για την προβολή, ενημέρωση, διαγραφή του επαγγελματικού προφίλ του χρήστη
class ProfessionalProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfessionalProfile.objects.all()
    serializer_class = ProfessionalProfileSerializer
    permission_classes = [IsAuthenticated]  # Μόνο συνδεδεμένοι χρήστες μπορούν να το κάνουν

    def get_object(self):
        # Εξασφαλίζουμε ότι ο χρήστης θα βλέπει μόνο το δικό του επαγγελματικό προφίλ
        return self.request.user.professional_profile
