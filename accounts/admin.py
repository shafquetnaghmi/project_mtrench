from django.contrib import admin
from .models import CustomUser,EmployerProfile,EmployeeProfile

#admin.site.register(CustomUser)
admin.site.register(EmployerProfile)
admin.site.register(EmployeeProfile)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display=['email','user_type']



