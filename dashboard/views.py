from django.core import serializers
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseServerError, HttpResponseRedirect
from accounts.decorators import client_required, active_user_required
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Smellsensor, Tissuesensor, Soupsensor, Company
import json
import requests
# Create your views here.

# user = get_user_model()


def calculate_percentage(level, empty, full):
    # full = 3
    x = float(level) - float(full)
    y = float(empty) - float(full)
    x_div_y = x / y
    percentage = (1 - x_div_y) * 100
    pretty_percentage = round(percentage, 2)

    return pretty_percentage


def smell_quality(level):
    if level > 1.00:
        return "Bad"
    else:
        return"Good"


@login_required(login_url='login')
@active_user_required
@client_required
def index(request):
    try:
        client_id = request.user.company
        user = request.user
        user_email = request.user.email

        obj =Tissuesensor.objects.filter(owner_id=client_id).last()
        obj_smell = Smellsensor.objects.filter(owner_id=client_id).last()
        obj_soup = Soupsensor.objects.filter(owner_id=client_id).last()

        percentage_tissue = calculate_percentage(obj.level_tissuesensor, obj.empty_reading, obj.initial_reading)
        quality_smell = smell_quality(float(obj_smell.level_smellsensor))
        percentage_soup = calculate_percentage(obj_soup.level_soupsensor, obj_soup.empty_reading, obj_soup.initial_reading)

        context = {

            "tissue_sensor": obj,
            "smell_sensor": obj_smell,
            "soup_sensor": obj_soup,
            "percentage_tissue": percentage_tissue,
            "quality_smell": quality_smell,
            "percentage_soup":percentage_soup
        }


        # try:
        #     if percentage_tissue <= 30.00:
        #         subject = 'Alert your Tissues are about to finish'
        #         message = 'Sunway Toilet 1 tissue roll is finishing. Please refill'
        #         from_email = settings.EMAIL_HOST_USER
        #         to_list = [user_email]
        #         send_mail(subject, message, from_email, to_list, fail_silently=True)
        #     else:
        #         pass
        # except:
        #     pass

        return render(request, 'index.html', context)
    except:
        return render(request, 'index.html', {})


@csrf_exempt
def read_data_tissue(request):

    response = request.body.decode("utf-8")
    json_dict = json.loads(response)
    print(type(json_dict))
    print(json_dict)

    sensor_id = json_dict['title']
    level = json_dict['level_tissuesensor']

    data = Tissuesensor(
        title= sensor_id,
        level_tissuesensor=level,
    )

    data.save()
    print("Successfully Saved TissueSensor Reading into the database")
    
    all_data = Tissuesensor.objects.all()

    return HttpResponse("Received the POST request Successfully")
    # return HttpResponse(json_dict)


@csrf_exempt
def read_data_smell(request):
    response = request.body.decode("utf-8")
    json_dict = json.loads(response)
    print(type(json_dict))
    print(json_dict)

    sensor_id = json_dict['title']
    level = json_dict['level_smellsensor']

    data = Smellsensor(
        title=sensor_id,
        level_smellsensor=level,
    )

    data.save()
    print("Successfully Saved SmellSensor Reading into the database")

    all_data = Smellsensor.objects.all()

    return HttpResponse("Received the POST request Successfully")


@csrf_exempt
def read_data_soup(request):
    response = request.body.decode("utf-8")
    json_dict = json.loads(response)
    print(type(json_dict))
    print(json_dict)

    sensor_id = json_dict['title']
    level = json_dict['level_soupsensor']

    data = Soupsensor(
        title=sensor_id,
        level_soupsensor=level,
    )

    data.save()
    print("Successfully Saved SoupSensor Reading into the database")

    all_data = Soupsensor.objects.all()

    return HttpResponse("Received the POST request Successfully")


def show_data(request):
    tissue_sensor = Tissuesensor.objects.all()

    context = {
        "tissue_sensor":tissue_sensor,

    }

    return render(request, 'data.html', context)

    
def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def error_500(request):
    data = {}
    return render(request, '500.html', data)


