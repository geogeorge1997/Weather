from django.shortcuts import render
from django.http import HttpResponse
from .models import CurrentAttributes,Hour24Attributes,WeeklyAttributes
import datetime

import requests

# Create your views here.

# Me : Call from appname(dataIn)/urls


def c_Name(request):

    print("c_Name")

    if("now" in request.POST):
        lists=c_Now(request)

    elif("hour" in request.POST):
        lists=c_Hour(request)

    else:
        lists=c_Day(request)

    return render(request, 'ui3.html', {'lists': lists})

def c_Now(request):

    loc_1 = request.POST['l1']
    lists = list(loc_1.split(","))
    length = len(lists)
    if (length > 5):
        length = 5

    CurrentAttributes.objects.all().delete()

    i = 0
    while (i < length):

        url_cn = 'https://api.opencagedata.com/geocode/v1/json?q=' + lists[i] + '&key=4ae3808139174985b6590ce4ff7f2cf1'
        loc_data = requests.get(url_cn).json()
        latitude = loc_data["results"][0]["geometry"]["lat"]
        longitude = loc_data["results"][0]["geometry"]["lng"]
        timezone = int(loc_data["results"][0]["annotations"]["timezone"]["offset_sec"])
        #placeinfo = loc_data["results"][0]["formatted"]
        #print(latitude,longitude,timezone,placeinfo)

        url_darksky = 'https://api.darksky.net/forecast/12660acff444d589840610d8ecc2381c/' + str(latitude) + ',' + str(longitude)

        w_data = requests.get(url_darksky).json()

        cd_obj = CurrentAttributes()
        cd_obj.temperature = str((float(w_data["currently"]["temperature"]) - 32) * 5 / 9)[0:5]
        cd_obj.appTemperature = str((float(w_data["currently"]["apparentTemperature"]) - 32) * 5 / 9)[0:5]
        cd_obj.icon = w_data["currently"]["icon"][0:14]
        cd_obj.summary = w_data["currently"]["summary"]
        cd_obj.uvindex = w_data["currently"]["uvIndex"]
        cd_obj.time = (lists[i] + " " + (str(
            datetime.datetime.fromtimestamp(int(w_data["currently"]["time"]) + timezone).strftime('%d-%m-%y %H:%M:%S')))[
                                            0:5])[0:30]
        cd_obj.rainProb = str(float(w_data["currently"]["precipProbability"]) * 100)[0:9]

        cd_obj.save()

        i = i + 1

    lists = CurrentAttributes.objects.all()
    return lists


def c_Hour(request):

    loc_1 = request.POST['l1']
    lists = list(loc_1.split(","))
    loc=lists[0]

    url_cn = 'https://api.opencagedata.com/geocode/v1/json?q=' + loc + '&key=4ae3808139174985b6590ce4ff7f2cf1'
    loc_data = requests.get(url_cn).json()
    latitude = loc_data["results"][0]["geometry"]["lat"]
    longitude = loc_data["results"][0]["geometry"]["lng"]
    timezone = int(loc_data["results"][0]["annotations"]["timezone"]["offset_sec"])
    # placeinfo = loc_data["results"][0]["formatted"]
    # print(latitude,longitude,timezone,placeinfo)

    url_darksky = 'https://api.darksky.net/forecast/12660acff444d589840610d8ecc2381c/' + str(latitude) + ',' + str(
        longitude)

    w_data = requests.get(url_darksky).json()

    Hour24Attributes.objects.all().delete()

    i = 0
    while (i < 24):
        h24_obj = Hour24Attributes()

        h24_obj.mainsummary = w_data["hourly"]["summary"]
        h24_obj.time = (str(
            datetime.datetime.fromtimestamp(int(w_data["hourly"]["data"][i]["time"]) + timezone).strftime(
                '%Y-%m-%d %H:%M:%S')))
        h24_obj.summary = w_data["hourly"]["data"][i]["summary"]
        h24_obj.icon = w_data["hourly"]["data"][i]["icon"][0:14]
        h24_obj.rainProb = str(float(w_data["hourly"]["data"][i]["precipProbability"]) * 100)[0:9]
        h24_obj.temperature = str((float(w_data["hourly"]["data"][i]["temperature"]) - 32) * 5 / 9)[0:5]
        h24_obj.appTemperature = str((float(w_data["hourly"]["data"][i]["apparentTemperature"]) - 32) * 5 / 9)[0:5]
        h24_obj.uvindex = w_data["hourly"]["data"][i]["uvIndex"]

        h24_obj.save()

        i = i + 1

    lists=Hour24Attributes.objects.all()
    return lists


def c_Day(request):

    loc_1 = request.POST['l1']
    lists = list(loc_1.split(","))
    loc = lists[0]

    url_cn = 'https://api.opencagedata.com/geocode/v1/json?q=' + loc + '&key=4ae3808139174985b6590ce4ff7f2cf1'
    loc_data = requests.get(url_cn).json()
    latitude = loc_data["results"][0]["geometry"]["lat"]
    longitude = loc_data["results"][0]["geometry"]["lng"]
    timezone = int(loc_data["results"][0]["annotations"]["timezone"]["offset_sec"])
    # placeinfo = loc_data["results"][0]["formatted"]
    # print(latitude,longitude,timezone,placeinfo)

    url_darksky = 'https://api.darksky.net/forecast/12660acff444d589840610d8ecc2381c/' + str(latitude) + ',' + str(
        longitude)

    w_data = requests.get(url_darksky).json()

    WeeklyAttributes.objects.all().delete()

    i = 0
    while (i < 7):
        wd_obj = WeeklyAttributes()

        wd_obj.mainsummary = w_data["daily"]["summary"]
        wd_obj.time = (str(datetime.datetime.fromtimestamp(int(w_data["daily"]["data"][i]["time"]) + timezone).strftime(
            '%d-%m-%y20 %H:%M:%S')))[0:10]
        wd_obj.summary = w_data["daily"]["data"][i]["summary"]
        wd_obj.icon = w_data["daily"]["data"][i]["icon"][0:14]
        wd_obj.rainProb = str(float(w_data["daily"]["data"][i]["precipProbability"]) * 100)[0:9]
        wd_obj.temperatureLow = str((float(w_data["daily"]["data"][i]["temperatureLow"]) - 32) * 5 / 9)[0:5]
        wd_obj.appTemperatureLow = str((float(w_data["daily"]["data"][i]["apparentTemperatureLow"]) - 32) * 5 / 9)[0:5]
        wd_obj.temperatureHigh = str((float(w_data["daily"]["data"][i]["temperatureHigh"]) - 32) * 5 / 9)[0:5]
        wd_obj.appTemperatureHigh = str((float(w_data["daily"]["data"][i]["apparentTemperatureHigh"]) - 32) * 5 / 9)[0:5]

        wd_obj.save()

        i = i + 1

    lists = WeeklyAttributes.objects.all()
    return lists


def ll_Name(request):
    print("ll_Name")

    if ("now" in request.POST):
        lists = ll_Now(request)

    elif ("hour" in request.POST):
        lists = ll_Hour(request)

    else:
        lists = ll_Day(request)

    return render(request, 'ui3.html', {'lists': lists})



def ll_Now(request):

    loc_2 = request.POST['l2']
    print(loc_2)
    lists = list(loc_2.split(","))

    length = len(lists)
    if (length > 9):
        length = 9

    CurrentAttributes.objects.all().delete()

    i = 0
    while (i < length):

        url_ll = 'https://api.opencagedata.com/geocode/v1/json?q=' + str(lists[i]) + '+' + str(
            lists[i + 1]) + '&key=4ae3808139174985b6590ce4ff7f2cf1'
        loc_data = requests.get(url_ll).json()
        timezone = int(loc_data["results"][0]["annotations"]["timezone"]["offset_sec"])
        place = loc_data["results"][0]["formatted"]
        placelist = list(place.split(","))
        print(placelist)

        url_darksky = 'https://api.darksky.net/forecast/12660acff444d589840610d8ecc2381c/' + str(lists[i]) + ',' + str(lists[i + 1])
        w_data = requests.get(url_darksky).json()

        cd_obj = CurrentAttributes()
        cd_obj.temperature = str((float(w_data["currently"]["temperature"]) - 32) * 5 / 9)[0:5]
        cd_obj.appTemperature = str((float(w_data["currently"]["apparentTemperature"]) - 32) * 5 / 9)[0:5]
        cd_obj.icon = w_data["currently"]["icon"][0:14]
        cd_obj.summary = w_data["currently"]["summary"]
        cd_obj.uvindex = w_data["currently"]["uvIndex"]
        cd_obj.time = (placelist[0] + " " + (str(
            datetime.datetime.fromtimestamp(int(w_data["currently"]["time"]) + timezone).strftime('%d-%m-%y %H:%M:%S')))[
                                            0:5])[0:30]
        cd_obj.rainProb = str(float(w_data["currently"]["precipProbability"]) * 100)[0:5]

        cd_obj.save()

        i = i + 2

    lists = CurrentAttributes.objects.all()

    return lists

def ll_Hour(request):

    loc_2 = request.POST['l2']
    lists = list(loc_2.split(","))

    latitude=lists[0]
    longitude=lists[1]

    Hour24Attributes.objects.all().delete()

    url_ll = 'https://api.opencagedata.com/geocode/v1/json?q=' + str(latitude) + '+' + str(
            longitude) + '&key=4ae3808139174985b6590ce4ff7f2cf1'
    loc_data = requests.get(url_ll).json()
    timezone = int(loc_data["results"][0]["annotations"]["timezone"]["offset_sec"])
    place = loc_data["results"][0]["formatted"]
    placelist = list(place.split(","))
    print(placelist)

    url_darksky = 'https://api.darksky.net/forecast/12660acff444d589840610d8ecc2381c/' + str(latitude) + ',' + str(
            longitude)
    w_data = requests.get(url_darksky).json()

    i = 0
    while (i < 24):

        h24_obj = Hour24Attributes()
        h24_obj.mainsummary = w_data["hourly"]["summary"][0:50]
        h24_obj.time = (str(
            datetime.datetime.fromtimestamp(int(w_data["hourly"]["data"][i]["time"]) + timezone).strftime(
                '%Y-%m-%d %H:%M:%S')))
        h24_obj.summary = w_data["hourly"]["data"][i]["summary"]
        h24_obj.icon = w_data["hourly"]["data"][i]["icon"][0:14]
        h24_obj.rainProb = str(float(w_data["hourly"]["data"][i]["precipProbability"]) * 100)[0:5]
        h24_obj.temperature = str((float(w_data["hourly"]["data"][i]["temperature"]) - 32) * 5 / 9)[0:5]
        h24_obj.appTemperature = str((float(w_data["hourly"]["data"][i]["apparentTemperature"]) - 32) * 5 / 9)[0:5]
        h24_obj.uvindex = w_data["hourly"]["data"][i]["uvIndex"]

        h24_obj.save()
        i = i + 1

    lists = Hour24Attributes.objects.all()

    return lists

def ll_Day(request):

    loc_2 = request.POST['l2']
    lists = list(loc_2.split(","))
    latitude = lists[0]
    longitude = lists[1]

    WeeklyAttributes.objects.all().delete()

    url_ll = 'https://api.opencagedata.com/geocode/v1/json?q=' + str(latitude) + '+' + str(
        longitude) + '&key=4ae3808139174985b6590ce4ff7f2cf1'
    loc_data = requests.get(url_ll).json()
    timezone = int(loc_data["results"][0]["annotations"]["timezone"]["offset_sec"])
    place = loc_data["results"][0]["formatted"]
    placelist = list(place.split(","))
    print(placelist)

    url_darksky = 'https://api.darksky.net/forecast/12660acff444d589840610d8ecc2381c/' + str(latitude) + ',' + str(
        longitude)
    w_data = requests.get(url_darksky).json()

    i = 0
    while (i < 7):

        wd_obj = WeeklyAttributes()
        wd_obj.mainsummary = w_data["daily"]["summary"]
        wd_obj.time = (str(datetime.datetime.fromtimestamp(int(w_data["daily"]["data"][i]["time"]) + timezone).strftime(
            '%d-%m-%y20 %H:%M:%S')))[0:10]
        wd_obj.summary = w_data["daily"]["data"][i]["summary"]
        wd_obj.icon = w_data["daily"]["data"][i]["icon"][0:14]
        wd_obj.rainProb = str(float(w_data["daily"]["data"][i]["precipProbability"]) * 100)[0:5]
        wd_obj.temperatureLow = str((float(w_data["daily"]["data"][i]["temperatureLow"]) - 32) * 5 / 9)[0:5]
        wd_obj.appTemperatureLow = str((float(w_data["daily"]["data"][i]["apparentTemperatureLow"]) - 32) * 5 / 9)[0:5]
        wd_obj.temperatureHigh = str((float(w_data["daily"]["data"][i]["temperatureHigh"]) - 32) * 5 / 9)[0:5]
        wd_obj.appTemperatureHigh = str((float(w_data["daily"]["data"][i]["apparentTemperatureHigh"]) - 32) * 5 / 9)[0:5]

        wd_obj.save()
        i = i + 1

    lists = WeeklyAttributes.objects.all()

    return lists


def home(request):

    num=[1,1,1,1,1]

    return  render(request,'ui.html',{'num':num})


