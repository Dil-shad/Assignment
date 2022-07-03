from email.mime import image
import os
from django.core.files import File
from posixpath import splitext
import zipfile
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
from django.db.models import Q


def register_usr(request):
    if request.method == 'POST':
        user_name = request.POST['uname']
        email = request.POST['uemail']
        pwd = request.POST['upass']
        if not user_name == '':
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'username already exists...!!')
                return redirect('register_usr')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email already registerd..!!')
                return redirect('register_usr')
            else:
                user = User.objects.create_user(
                    username=user_name,
                    password=pwd,
                    email=email,
                )
                user.save()
                return redirect('login')
        messages.info(request, 'Not valid')

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        try:
            if request.method == 'POST':
                uname = request.POST['uname']
                pwd = request.POST['pswd']
                user = auth.authenticate(username=uname, password=pwd)

                if user is not None:
                    request.session['uid'] = user.id
                    auth.login(request, user)
                    return redirect('index')
                else:
                    messages.info(
                        request, 'Invalid Username or Password. Try Again.IN')
                    return redirect('login')

            return render(request, 'login.html')
        except:
            # messages.info(request, 'Invalid username or password')
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout(request):
    request.session['uid'] = ''
    auth.logout(request)
    return redirect('/')


def index(request):

    tm = TeacherModel.objects.all()

    context = {
        'obj': tm
    }

    return render(request, 'index.html', context)


@login_required(login_url='login')
def importer(request):
    if request.method == "POST":
        print('------------------------')
        csv_file = request.FILES.get('tname')
        img_zip_file = request.FILES.get('timg')

        teacher_details = pd.read_csv(csv_file, delimiter=',')
        n_rows = len(teacher_details)
        teacher_details = teacher_details.dropna(
            subset=['First Name', 'Email Address'], how='any')
        removed_rows = n_rows - len(teacher_details)
        img_zip = zipfile.ZipFile(img_zip_file, 'r')
        img_name_list = img_zip.namelist()

        duplicate_rows = 0
        for index, teacher in teacher_details.iterrows():
            email_id = teacher['Email Address'].strip()
            if email_id:
                if TeacherModel.objects.filter(email__iexact=email_id).exists():
                    duplicate_rows = duplicate_rows + 1
                    continue
            Tr = TeacherModel()
            Tr.first_name = teacher['First Name'].strip()
            Tr.last_name = teacher['Last Name'].strip()
            Tr.email = email_id
            Tr.phone_number = teacher['Phone Number'].strip()
            Tr.room_number = teacher['Room Number'].strip()
            Tr.save()
            subjects = teacher['Subjects taught'].strip().split(',')
            if len(subjects) > 5:
                subjects = subjects[:5]
                print(subjects)
            for subject in subjects:
                subject = subject.strip().lower()
                print(subject)
                if subjects != '':
                    subject, created = SubjectsModel.objects.get_or_create(
                        subject_name=subject)
                    Tr.subjects.add(subject)

            image_name = teacher['Profile picture'].strip()
            if image_name in img_name_list:
                image = img_zip.open(image_name, 'r')
                img = File(image)
                Tr.image.save(image_name, img, save=True)
                image.close()
        img_zip.close()
        return redirect('/')

    return render(request, 'importer.html')


@csrf_exempt
def add_teacher(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacherid')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        room_number = request.POST.get('room_number')
        subjects_taught = request.POST.get('subjects_taught')
        print('----------------'+subjects_taught)
        file = request.FILES.get("file")

        print('-------------------'+str(teacher_id))
        if (teacher_id == ''):
            tm = TeacherModel(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                room_number=room_number,
            )
            try:
                fss = FileSystemStorage()
                image = fss.save(file.name, file)
                url = fss.url(image)
                if image != '':
                    tm.image = image
                else:
                    tm.image = "/static/image/default.png"
            except:
                pass
            tm.save()

            if subjects_taught != '':
                subject, created = SubjectsModel.objects.get_or_create(
                    subject_name=subjects_taught)
            tm.subjects.add(subject)
        else:

            tm = TeacherModel(
                id=teacher_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                room_number=room_number,
            )
            try:
                fss = FileSystemStorage()
                image = fss.save(file.name, file)
                url = fss.url(image)
                if image != '':
                    tm.image = image
                else:
                    pass
            except:
                pass
            tm.save()
            if subjects_taught != '':
                subject, created = SubjectsModel.objects.get_or_create(
                    subject_name=subjects_taught)
            tm.subjects.add(subject)

        x = TeacherModel.objects.values()
        r_data = list(x)
        return JsonResponse({'status': 1, 'r_data': r_data})


@csrf_exempt
def view_teacher(request):
    if request.method == 'POST':
        pk = request.POST['pid']
        mdl = TeacherModel.objects.get(id=pk)
        n = str(mdl.image)
        fss = FileSystemStorage()
        url = fss.url(mdl.image)
        ls = [x.subject_name for x in mdl.subjects.all()]
        print(ls)

        view_teacher = {
            'first_name': mdl.first_name,
            'last_name': mdl.last_name,
            'email': mdl.email,
            'phone_number': mdl.phone_number,
            'room_number': mdl.room_number,
            'image': url,
            'subjects': ls,


        }

        return JsonResponse(view_teacher)


@csrf_exempt
def filter_teacher(request):
    if request.method == 'POST':
        q = request.POST['q']
        print(q)
        x = TeacherModel.objects.filter(last_name__istartswith=q).values()
        r_data = list(x)
        print(r_data)

    return JsonResponse({'status': 1, 'r_data': r_data})


@csrf_exempt
def edit(request):
    if request.method == 'POST':

        pk = request.POST['pid']
        mdl = TeacherModel.objects.get(id=pk)
        n = str(mdl.image)
        fss = FileSystemStorage()
        url = fss.url(mdl.image)
        ls = [x.subject_name for x in mdl.subjects.all()]
        print(ls)

        edit_teacher = {
            'teacherid': mdl.id,
            'first_name': mdl.first_name,
            'last_name': mdl.last_name,
            'email': mdl.email,
            'phone_number': mdl.phone_number,
            'room_number': mdl.room_number,
            'image': url,
            'subjects': ls,


        }
        return JsonResponse({'status': 1, 'r_data': edit_teacher})
