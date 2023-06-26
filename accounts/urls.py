from django.urls import path
from .views import RegistrationView,LoginView,ProfileView,EmployeeProfileView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<user_id>/', ProfileView.as_view(), name='employer-profile'),
    path('employee_profile/<user_id>/', EmployeeProfileView.as_view(), name='employee-profile'),
]
