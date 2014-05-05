from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name',]

class PilotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pilot
        fields = ['id','firstName','middleName','lastName','teamName','pilotNumber',]

class PilotResultSerializer(serializers.ModelSerializer):

    racesResults = serializers.Field(source='getRacesResults')

    class Meta:
        model = Pilot
        fields = ['id','firstName','middleName','lastName','teamName','pilotNumber','racesResults',]

class RaceMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceMark
        fields = ['id','judge','pilot','mark','raceNumber',]
