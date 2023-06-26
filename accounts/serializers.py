from rest_framework import serializers
from .models import CustomUser,EmployeeProfile,EmployerProfile
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model=CustomUser
        fields=['email', 'password', 'user_type']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Invalid email or password.')
        else:
            raise serializers.ValidationError('Email and password are required.')

class EmployerProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmployerProfile
		fields ='__all__'

class EmployeeProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmployeeProfile
		fields ='__all__'


