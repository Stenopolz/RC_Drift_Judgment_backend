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
    """
    """

    def pilotCompare(first,second):
        def getBestRace(pilot,exceptRaceNum=None):

            racesResults = pilot.marks.values('raceNumber').annotate(best_score=models.Min('mark'),avg_score=models.Avg('mark'))

            if exceptRaceNum:
                print "excepting %s" % exceptRaceNum
                for i in range(0,len(racesResults)):
                    if racesResults[i]['raceNumber'] == exceptRaceNum:
                        del racesResults[i]
                        break

            return sorted(racesResults,key=lambda race: race['avg_score'])

        firstRace = getBestRace(first)
        secondRace = getBestRace(second)

        def compareBestMarks(firstBm,secondBm):
            if firstRace[0]['avg_score'] < secondRace[0]['avg_score']:
                return -1
            elif firstRace[0]['avg_score'] > secondRace[0]['avg_score']:
                return 1
            else:
                return 0

        # 3
        res1 = compareBestMarks(firstRace,secondRace)
        if res1 != 0:
            return res1

        # 4
        del firstRace[0]
        del secondRace[0]
        res2 = compareBestMarks(firstRace,secondRace)
        if res2 != 0:
            return res2

        # 5
        del firstRace[0]
        del secondRace[0]
        res3 = compareBestMarks(firstRace,secondRace)
        if res3 != 0:
            return res3

        # 6 compare best marks from judges
        firstMarks = first.marks.all()["-mark"]
        secondMarks = second.marks.all()["-mark"]
        if firstMarks[0].mark < secondMarks[0].mark:
            return -1
        elif  firstMarks[0].mark < secondMarks[0].mark:
            return 1

        # 7 compare by numbers
        if first.pilotNumber < second.pilotNumber:
            return -1
        elif  first.pilotNumber > second.pilotNumber:
            return 1

        return 0

    pilots = list(Pilot.objects.all())
    sortedPilots = sorted(pilots,cmp=pilotCompare)

    serializer =  PilotResultSerializer(pilots, many=True)
    return Response(serializer.data)

