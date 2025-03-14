from rest_framework import serializers
#from users.models import User
from .models import ProfessionalProfile
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.conf import settings
from .models import Conversation
from django.apps import apps
from .models import Message

# Λάβε το μοντέλο χρήστη μέσω της ρύθμισης AUTH_USER_MODEL
User = apps.get_model(settings.AUTH_USER_MODEL)

class UserSerializer(serializers.ModelSerializer):
    accessToken = serializers.SerializerMethodField()
    refreshToken = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields =['id','name','email','password', 'accessToken', 'refreshToken',]
        extra_kwargs={
            'password': {'write_only':True}
        }



    def create(self, validated_data):
        password=validated_data.pop('password', None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def get_accessToken(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def get_refreshToken(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh)

class ProfessionalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalProfile
        fields = ['job_type', 'ministry', 'company_type', 'specialization', 'job_name','experience', 'job_address', 'job_phone' , 'profile_picture']

#serializers για τα μοντελα convarsation και message
class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    unread_messages = serializers.SerializerMethodField()

    def get_unread_messages(self, obj):
        user = self.context['request'].user
        return obj.messages.filter(is_read=False).exclude(sender=user).count()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'unread_messages']

class MessageSerializer(serializers.ModelSerializer):
    # Ο sender είναι χρήστης, οπότε το σχετικό πεδίο θα είναι το PrimaryKeyRelatedField
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'sender', 'conversation', 'content', 'timestamp']

#δευτερος για μηνυματα
class MessageSerializersend(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content']  # Μόνο το περιεχόμενο του μηνύματος

#serializer για δημιουργια συνομιλίας
class CreateConversationSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField()

    def validate_receiver_id(self, value):
        """Ελέγχει αν ο receiver υπάρχει"""
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User not found")
        return value
