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
        racelist_object = {"datetime_str": race_datetime_str, "race_id": raceResultsObject.id}
        racelist.append(racelist_object)
    return render(request, "gameday/index.html", {
        "country": country,
        "racelist": racelist,
        "startdate": startdate,
        "enddate": enddate
    })

def viewrace(request, id):
    raceResultObject = RaceResult.objects.get(id=id)
    countryObject = raceResultObject.country
    country = countryObject.name
    race_datetime = raceResultObject.race_datetime
    race_datetime_str = dateTimeIntToStr(race_datetime)
    racers_list = []
    racers_list.append(raceResultObject.position_1)
    racers_list.append(raceResultObject.position_2)
    racers_list.append(raceResultObject.position_3)
    racers_list.append(raceResultObject.position_4)
    racers_list.append(raceResultObject.position_5)
    racers_list.append(raceResultObject.position_6)
    racers_list.append(raceResultObject.position_7)
    racers_list.append(raceResultObject.position_8)
    racers_list.append(raceResultObject.position_9)
    racers_list.append(raceResultObject.position_10)
    racers_list_out = []
    for racerStr in racers_list:
        racerStrSplit = racerStr.split(",")
        raceObject = {"position": racerStrSplit[0],
                    "driver_name": racerStrSplit[1],
                    "team": racerStrSplit[2],
                    "score": racerStrSplit[3]
                    }
        racers_list_out.append(raceObject)
    return render(request, "gameday/raceresults.html", {
        "country": countryObject.formatted_name,
        "race_datetime": race_datetime_str,
        "racers_list": racers_list_out
    })

@login_required
def viewbetslist(request):
    if request.user.is_authenticated:
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

        betResultsObjectsList = BetResult.objects.filter(user=request.user, country=country, race_datetime__gte=startdate_int, race_datetime__lte=enddate_int)
        betResultsList = []
        for betResultsObject in betResultsObjectsList:
            betResultsList.append({"race_datetime": dateTimeIntToStr(betResultsObject.betResultsObject),"id": betResultsObject.id})
        return render(request, "gameday/betslist.html", {
            "country": countryObject.formatted_name,
            "betResultsList": betResultsList,
            "startdate": startdate,
            "enddate": enddate
        })
    else:
        # Return Error: To Do
        pass


@login_required
def viewbetresults(request, id):
    if request.user.is_authenticated:
        betResultsObject = BetResult.objects.get(id=id)
        if betResultsObject.user == request.user:
            countryObject = betResultsObject.country
            country = countryObject.formatted_name
            bet_type = betResultsObject.bet_type
            race_datetime = dateTimeIntToStr(betResultsObject.race_datetime)
            bet_amount = betResultsObject.bet_amount
            winnings = betResultsObject.winnings
            bet_value = betResultsObject.bet_value
            result_value = betResultsObject.result_value
            return render(request, "gameday/betresults.html", {
                "country": country,
                "bet_type": bet_type,
                "race_datetime": race_datetime,
                "bet_amount": bet_amount,
                "winnings": winnings,
                "bet_value": bet_value,
                "result_value": result_value
            })
        else:
            # Return Error: Not authorized
            pass

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