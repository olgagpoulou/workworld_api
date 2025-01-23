from rest_framework import serializers
from users.models import User
from .models import ProfessionalProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','name','email','password']
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

class ProfessionalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalProfile
        fields = ['job_type', 'ministry', 'company_type', 'specialization', 'job_name','experience', 'job_address', 'job_phone' , 'profile_picture']

        def validate(self, data):
            # Παράδειγμα: Έλεγχος αν λείπει το job_type
            if not data.get('job_type'):
                raise serializers.ValidationError({'job_type': 'Το πεδίο job_type είναι υποχρεωτικό.'})
            return data