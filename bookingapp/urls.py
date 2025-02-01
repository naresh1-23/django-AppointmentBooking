from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('doctors/', views.Doctors, name='doctors'),
    path('doctors/<int:pk>/', views.doctordetail, name='doctordetail'),
    path('doctors/appointments/', views.appointmentall, name='appointments'),
    path('addappointment/', views.addappointment, name='add-appointment'),
    path('doctors/appointments/<int:pk>', views.book, name='booking'),
    path('appointment/list/', views.appointed, name='appointed'),
    path('appointment/clients/', views.clients, name='clients'),
    path('appointments/delete/<int:pk>',
         views.delete_appointment, name='delete'),
    path('appointments/update/<int:pk>', views.update_list, name='update_form'),
    path('appointments/patient-detail/<int:pk>',
         views.patient_form, name='patientform'),
    path('form/', views.book_appointment, name='form')
]
