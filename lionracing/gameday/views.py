from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import datetime

from .models import *

#####################################################################################
# Key Application Code ##############################################################
#####################################################################################

def index(request):
    if request.method == "POST":
        country = request.POST["country"]
        startdate = request.POST["startdate"]
        enddate = request.POST["enddate"]
    else:
        # Return defaults
        country = "singapore"
        now = datetime.datetime.now()
        timedelta = datetime.timedelta(weeks=4)
        startdate_object = now - timedelta
        startdate = startdate_object.strftime("%d/%m/%Y")
        enddate = now.strftime("%d/%m/%Y")

    # Get Races
    startdate_int = int(dateTimeStrToInt(startdate))
    enddate_int = int(dateTimeStrToInt(enddate)) + 2359
    raceResultsQuerySet = RaceResult.objects.filter(race_datetime__gte=startdate_int, race_datetime__lte=enddate_int).filter(country=country)
    racelist = []
    for raceResultsObject in raceResultsQuerySet:
        race_datetime = int(raceResultsObject.race_datetime)
        race_datetime_str = dateTimeIntToStr(race_datetime)
        racelist.append(race_datetime_str)
    return render(request, "gameday/index.html", {
        "country": country,
        "racelist": racelist
    })

#####################################################################################
# User Management ###################################################################
#####################################################################################

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("store"))
        else:
            return render(request, "gameday/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "gameday/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "gameday/registeremployee.html", {
                "message": "Passwords must match."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password,\
                first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "gameday/registeremployee.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "gameday/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#####################################################################################
# Supporting Functions ##############################################################
#####################################################################################

def dateTimeStrToInt(datetime_str):
    datetime_str_modified = datetime_str[6:10] + datetime_str[3:5] + datetime_str[0:2] + "0000"
    return int(datetime_str_modified)

def dateTimeIntToStr(datetime_int):
    datetime_str = str(datetime_int)
    datetime_str_modified = datetime_str[6:8] + "/" + datetime_str[4:6] + "/" + datetime_str[0:4]
    return datetime_str_modified