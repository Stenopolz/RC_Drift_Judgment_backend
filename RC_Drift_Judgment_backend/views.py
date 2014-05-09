from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,Http404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.template import RequestContext
from django.shortcuts import render_to_response

from .models import *
from .views_api import getQualifyResults

def home(request):
    raise Http404()


def results(request):

    return render_to_response(
        "results.html",
        {},
        RequestContext(request, {}),
    )


def topResults(request,topNum):

    drivers = getQualifyResults()
    topNum = int(topNum)

    pairs = []
    if topNum <= len(drivers):
        N = topNum
        top = {}

        pilotsCounter = 0
        shift = -2

        for i in xrange(0, N / 8):
            position = i * 2

            top[position] = drivers[pilotsCounter]
            pilotsCounter += 1
            position += N / 2

            top[position] = drivers[pilotsCounter]
            pilotsCounter += 1
            position += shift

            top[position] = drivers[pilotsCounter]
            pilotsCounter += 1
            position += N / 2

            top[position] = drivers[pilotsCounter]
            pilotsCounter += 1

            shift -= 4

        for i in xrange(0, N, 2):
            pilotPosition = drivers.index(top[i]) + 1
            pairPosition = N - pilotPosition

            top[i + 1] = drivers[pairPosition]

        for i in xrange(0,len(top.keys()),2):
            pairs.append( (top[i],top[i+1] ))

    return render_to_response(
        "top.html",
        {'top': topNum,
         'pairs': pairs},
        RequestContext(request, {}),
    )
