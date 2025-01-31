from django.db import models
from user.models import UserModel
from user.validations import validate_length
from django.core.exceptions import ValidationError

class AppointmentDetail(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    doctor_id = models.ForeignKey(UserModel, on_delete = models.CASCADE)




class Appointmentlist(models.Model):
    user_id = models.ForeignKey(UserModel, on_delete = models.CASCADE)
    appointment_id = models.ForeignKey(AppointmentDetail, on_delete= models.CASCADE)
    time = models.TimeField()
    problem_description = models.TextField()




class Patient(models.Model):
    name = models.CharField(max_length = 150)
    contact = models.PositiveIntegerField(validators = [validate_length])
    doctor_id = models.ForeignKey(UserModel, on_delete = models.CASCADE)
    problem = models.TextField()
    medicine = models.TextField()

    def __str__(self):
        return self.name

class Patientform(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name