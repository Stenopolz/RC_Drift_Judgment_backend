from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Pilot(models.Model):
    db_table = 'pilots'

    pilotNumber = models.IntegerField('Pilot Number')
    firstName = models.CharField('First Name',max_length=120)
    middleName = models.CharField('Middle Name',max_length=120,blank=True,null=True)
    lastName = models.CharField('Last Name',max_length=120)

    teamName = models.CharField('Team',max_length=200,blank=True,null=True)
    carModel = models.CharField('Car',max_length=200,blank=True,null=True)

    def getRacesResults(self):
        racesResults = self.marks.values('raceNumber').annotate(best_score=models.Min('mark'),avg_score=models.Avg('mark'))
        return sorted(racesResults,key=lambda race: race['avg_score'])

    def __unicode__(self):
        return "#%d : %s %s %s" % (self.pilotNumber,self.lastName, self.firstName, self.middleName)

    class Meta:
        ordering = ['pilotNumber']

class PilotAdmin(admin.ModelAdmin):
    list_display = ('pilotNumber','firstName','lastName','carModel','teamName',)

admin.site.register(Pilot,PilotAdmin)

MARK_CHOICES = (
    (0,'0 - GODLIKE!'),
    (1,'1 - Very Nice!'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
    (6,'6'),
    (7,'7'),
    (8,'8'),
    (9,'9'),
    (10,'10'),
    (100,'X'),
)
tmpMarks = [ (i,str(i)) for i in xrange(0,21) ]
tmpMarks.append( (100,'X') )
MARK_CHOICES = tuple(tmpMarks)

class RaceMark(models.Model):
    db_table = 'race_marks'

    raceNumber = models.IntegerField('Race number',default=1)
    pilot = models.ForeignKey(Pilot,related_name='marks')
    judge = models.ForeignKey(User,related_name='+')
    mark = models.IntegerField('Mark',choices=MARK_CHOICES,default=100,blank=False)

    class Meta:
        unique_together = ['raceNumber','judge','pilot']

    def __unicode__(self):
        return "pilot #: %d #%d : %d" % (self.pilot.pilotNumber,self.raceNumber,self.mark)

class RaceMarkAdmin(admin.ModelAdmin):
    list_display = ('raceNumber','pilot','judge','mark',)

admin.site.register(RaceMark,RaceMarkAdmin)
