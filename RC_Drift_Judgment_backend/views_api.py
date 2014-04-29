from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,Http404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# REST API
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from django.contrib.auth.models import User
from .serializers import *
from .models import *

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'judges' : reverse('judge-list',request=request),
        'pilots': reverse('pilot-list', request=request),
        'marks': reverse('mark-list', request=request),
        'results' : reverse('results-detail', request=request),
    })

class JudgeList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of judges.
    """
    model = User
    serializer_class = UserSerializer

class JudgeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single judge.
    """
    model = User
    serializer_class = UserSerializer

class PilotList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of pilots.
    """
    model = Pilot
    serializer_class = PilotSerializer

class RaceMarkList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of race marks.
    """
    model = RaceMark
    serializer_class = RaceMarkSerializer

class RaceMarkDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single race mark.
    """
    model = RaceMark
    serializer_class = RaceMarkSerializer

@api_view(['GET'])
def PilotDetail(request, pk=None, format=None):
    """
    API endpoint that represents a single pilot.
    """
    try:
        pilot = Pilot.objects.get(pk=pk)
    except:
        raise Http404()

    # basic pilot info
    content = PilotSerializer(pilot).data
    # marks
    content['marks'] = []
    marks = pilot.marks.all()
    for mark in marks:
        content['marks'].append( RaceMarkSerializer(mark).data )

    return Response(content)

@api_view(['GET'])
def RaceResults(request):

    sortedPilots = []

    pilots = Pilot.objects.all()
    for pilot in pilots:

        racesResults = pilot.marks.values('raceNumber').annotate(best_score=models.Min('mark'),avg_score=models.Avg('mark'))

        # get best race for pilot
        bestRace = racesResults[0]
        for race in racesResults:
            if race['best_score'] < bestRace['best_score']:
                bestRace = race

        sortedPilots.append( (bestRace['avg_score'], bestRace, pilot ) )

    # Sort pilots by avg score of best race
    sortedPilots = sorted(sortedPilots, key=lambda race: race[0])

    # Group pilots by their avg score of best race
    values = sorted(set(map(lambda x:x[0], sortedPilots)))
    newlist = { x:[ (y[1],y[2]) for y in sortedPilots if y[0]==x] for x in values}
    newlist = sorted(newlist)
    # TODO: Check 4,5,6 conditions here
    print newlist

    # Test output
    # TODO : Replace with real data
    serializer =  PilotSerializer(pilots, many=True)
    return Response({ 'res' : serializer.data })
