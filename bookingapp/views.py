from time import timezone
from urllib import request
from django.shortcuts import render, redirect
from user.models import UserModel
from .models import Appointmentlist, AppointmentDetail, Patient, Patientform
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.utils import timezone


def home(request):
    return render(request, 'bookingapp/home.html')
# Create your views here.


def Doctors(request):
    doctors = UserModel.objects.filter(is_doctor=True).values()
    return render(request, 'bookingapp/doctor.html', {'doctors': doctors})


def doctordetail(request, pk):
    doctor = UserModel.objects.filter(id=pk).first()
    return render(request, 'bookingapp/doctordetail.html', {'doctor': doctor})

# Function to convert the date format


@login_required
def addappointment(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            date = request.POST['date']
            doctor = request.POST['doctorId']
            doctormodel = UserModel.objects.get(username=doctor)
            today = timezone.now().date()
            start = datetime.strptime(start_time, "%H:%M")
            end = datetime.strptime(end_time, "%H:%M")
            if start_time == '' or end_time == '' or date == '' or doctor == '':
                messages.warning(request, f'Fields cannot be empty')
            elif AppointmentDetail.objects.filter(doctor_id=doctormodel, date=date).exists():
                messages.warning(request, f'Doctor is busy for today')
            elif datetime.strptime(date, "%Y-%m-%d").date() < today:
                messages.warning(request, f'Date is not valid')
            elif start_time >= end_time:
                messages.warning(
                    request, f'Start time and End time is not matched')
            else:
                appointment = AppointmentDetail(
                    start_time=start, end_time=end, date=date, doctor_id=doctormodel)
                appointment.save()
                messages.success(request, f'Successfully added')
                return redirect('appointments')
        doctors = UserModel.objects.filter(is_doctor=True).values()
        return render(request, 'bookingapp/addappointment.html', {'doctors': doctors})
    else:
        messages.warning(request, f'Access denied!')
        return redirect('home')


def appointmentall(request):
    appointments = AppointmentDetail.objects.all()
    return render(request, 'bookingapp/appointmentall.html', {'appointments': appointments})


@login_required
def book(request, pk):
    appointment = AppointmentDetail.objects.filter(id=pk).first()
    any = True
    if request.method == 'POST':
        time = request.POST['time']
        prblm = request.POST['problem']
        if time == '' or prblm == '':
            messages.warning(request, f'Fields cannot be empty')
        elif Appointmentlist.objects.filter(time=time).exists():
            messages.warning(
                request, f'Selected time is not available. It is already booked.')
        else:
            inputtime = str(time)
            stringtime = datetime.strptime(inputtime, "%H:%M")
            for appointmentlist in Appointmentlist.objects.all():
                objtime = str(appointmentlist.time)
                stringaptime = datetime.strptime(objtime, "%H:%M:%S")
                diff = abs(stringtime-stringaptime)
                stringdiff = str(diff)
                newdiff = get_seconds(stringdiff)/60

                if abs(newdiff) <= 10:
                    messages.warning(
                        request, f'Selected time is not available. It is already booked.')
                    any = False
                    break
            stringstarttime = str(appointment.start_time)
            stringendtime = str(appointment.end_time)
            appstarttime = datetime.strptime(stringstarttime, '%H:%M:%S')
            appendtime = datetime.strptime(stringendtime, "%H:%M:%S")
            if stringtime < appstarttime or stringtime > appendtime:
                messages.warning(
                    request, f'Please select the approprite time from ' + stringstarttime+' to ' + stringendtime)
            elif any == True:
                obj = Appointmentlist(
                    user_id=request.user, appointment_id=appointment, time=time, problem_description=prblm)
                obj.save()
                messages.success(request, f'Your appointment at '+time +
                                 ' with '+appointment.doctor_id.username+' has been booked.')
                return redirect('appointed')

    return render(request, 'bookingapp/booking.html', {'appointment': appointment})


def get_seconds(time_str):
    print('Time in hh:mm:ss:', time_str)
    # split in hh, mm, ss
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)


def clients(request):
    if not request.user.is_doctor:
        messages.warning(request, f'cannot excess')
        return redirect('home')
    else:
        appoint_id = AppointmentDetail.objects.filter(
            doctor_id=request.user).first()
        peoples = Appointmentlist.objects.filter(appointment_id=appoint_id)
    return render(request, 'bookingapp/clients.html', {'peoples': peoples})


def delete_appointment(request, pk):
    obj = AppointmentDetail.objects.filter(id=pk).first()
    obj.delete()
    messages.success(request, f'Successfully deleted')
    return redirect('appointments')


def update_list(request, pk):
    if request.user.is_superuser:
        obj = AppointmentDetail.objects.filter(id=pk).first()
        if request.method == 'POST':
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            date = request.POST['date']
            doctorid = request.POST['doctorId']
            doctormodel = UserModel.objects.get(username=doctorid)
            if start_time == '' or end_time == '' or date == '' or doctorid == '':
                messages.warning(request, f'Fields cannot be empty')
            elif AppointmentDetail.objects.filter(doctor_id=doctormodel, date=date).exists():
                messages.warning(request, f'Doctor is busy for today')
            elif start_time >= end_time:
                messages.warning(
                    request, f'Start time and End time is not matched')
            else:
                obj.start_time = start_time
                obj.end_time = end_time
                obj.date = date
                obj.doctor_id = doctormodel
                appointlist = Appointmentlist.objects.filter(
                    appointment_id=obj).all()
                appointlist.delete()
                obj.save()
                messages.success(request, f'Successfully updated')
                return redirect('appointments')
    else:
        messages.warning(request, f'Access Denied')
        return redirect('home')
    return render(request, 'bookingapp/update_form.html', {'obj': obj})


def appointed(request):
    appointedlists = Appointmentlist.objects.filter(user_id=request.user)
    return render(request, 'bookingapp/appointed.html', {'appointedlists': appointedlists})


def patient_detail_view(request):
    if request.method == 'POST':
        form = Patientform(request.POST)
        if form.is_valid():
            form.save()
            # Replace 'success' with your actual success page route
            return redirect('success')
    else:
        form = Patientform()

    return render(request, 'patient_detail_form.html', {'form': form})


def patient_form(request, pk):
    appointobj = Appointmentlist.objects.filter(id=pk).first()
    if request.user.is_doctor:
        if request.method == 'POST':
            name = request.POST['name']
            contact = request.POST['contact']
            problem = request.POST['prblm']
            medicine = request.POST['medicine']
            doctorobj = UserModel.objects.filter(
                username=request.user.username).first()
            if name == '' or contact == '' or problem == '' or medicine == '':
                messages.warning(request, f'Fields cannot be empty')
            else:
                patient = Patient(
                    name=name, contact=contact, problem=problem, medicine=medicine, doctor_id=doctorobj)
                patient.save()
                messages.success(request, f'Successfully patient added')
                return redirect('clients')
    else:
        messages.warning(request, f'Access Denied')
        return redirect('home')
    return render(request, 'bookingapp/patientform.html', {'appointobj': appointobj})
