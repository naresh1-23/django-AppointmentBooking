from django.contrib import admin
from .models import AppointmentDetail, Appointmentlist, Patient
admin.site.register(Appointmentlist)
admin.site.register(AppointmentDetail)
admin.site.register(Patient)
# Register your models here.
