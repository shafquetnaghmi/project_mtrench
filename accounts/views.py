from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404,redirect
from .models import EmployeeProfile,EmployerProfile
from django.urls import reverse

from .models import CustomUser
from .serializers import RegistrationSerializer,LoginSerializer,EmployerProfileSerializer,EmployeeProfileSerializer
from .utils import generate_access_token

class RegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_type = serializer.validated_data.get('user_type')
            if user_type=='employer':
                serializer.save()
                return Response(serializer.data)
            elif user_type == 'employee':
                print(request.user.id)
                employer = request.user.id
                employee = serializer.save()
                EmployeeProfile.objects.create(user=employee, employer=employer)
                return Response(serializer.data)
            else:
                return Response({'message': 'Only authenticated employers can register employees.'}, status=403)
            
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        access_token = generate_access_token(user)
        if user.user_type=='employer': 
            employer_profile_url = reverse('employer-profile', kwargs={'user_id': user.id})
            return redirect(employer_profile_url)
        else:
            employee_profile_url = reverse('employee-profile', kwargs={'user_id': user.id})
            return redirect(employee_profile_url)

        #return Response({'access_token': access_token})
    





class ProfileView(APIView):
    def get(self, request, *args, **kwargs):
        employer = get_object_or_404(EmployerProfile, pk=kwargs['user_id'])
        employer_serializer = EmployerProfileSerializer(employer)
        employees = EmployeeProfile.objects.filter(employer=employer)
        employee_serializer = EmployeeProfileSerializer(employees, many=True)
        
        data = {
            'employer': employer_serializer.data,
            'employees': employee_serializer.data
        }
        
        registration_url = reverse('register') 
        data['registration_url'] = request.build_absolute_uri(registration_url)
        return Response(data)

class EmployeeProfileView(APIView):
    def get(self, request, *args, **kwargs):
        employee = get_object_or_404(EmployeeProfile, pk=kwargs['user_id'])
        employee_serializer = EmployeeProfileSerializer(employee)
        data = {
            'employees': employee_serializer.data
        }
        
        return Response(data)
