from rest_framework import serializers
from users.models import User
from .models import ProfessionalProfile
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    accessToken = serializers.SerializerMethodField()
    refreshToken = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields =['id','name','email','password', 'accessToken', 'refreshToken', 'refreshToken']
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
