from django.contrib import admin
from .models import AppointmentDetail, Appointmentlist, Patient


# Custom admin class for AppointmentDetail
class AppointmentDetailAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'date', 'start_time', 'end_time')
    search_fields = ('doctor_id__username',)
    list_filter = ('date',)

# Custom admin class for Appointmentlist


class AppointmentlistAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'appointment_id', 'time', 'problem_description')
    search_fields = ('user_id__username',
                     'appointment_id__doctor_id__username')
    list_filter = ('time',)

# Custom admin class for Patient


class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'doctor_id', 'problem')
    search_fields = ('name', 'doctor_id__username')
    list_filter = ('doctor_id',)


# Register models and their corresponding admin classes
admin.site.register(AppointmentDetail, AppointmentDetailAdmin)
admin.site.register(Appointmentlist, AppointmentlistAdmin)
admin.site.register(Patient, PatientAdmin)
