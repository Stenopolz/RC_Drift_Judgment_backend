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
    (0,'0'),
	(1,'1'),
	(2,'2'),
	(3,'3'),
	(4,'4'),
	(5,'5'),
	(6,'6'),
	(7,'7'),
	(8,'8'),
	(9,'9'),
	(10,'10'),
	(10,'11'),
	(10,'12'),
	(10,'13'),
	(10,'14'),
	(10,'15'),
	(10,'16'),
	(10,'17'),
	(10,'18'),
	(10,'19'),
	(20,'20'),
	(20,'21'),
	(20,'22'),
	(20,'23'),
	(20,'24'),
	(20,'25'),
	(20,'26'),
	(20,'27'),
	(20,'28'),
	(20,'29'),
	(30,'30'),
	(30,'31'),
	(30,'32'),
	(30,'33'),
	(30,'34'),
	(30,'35'),
	(30,'36'),
	(30,'37'),
	(30,'38'),
	(30,'39'),
	(40,'40'),
	(40,'41'),
	(40,'42'),
	(40,'43'),
	(40,'44'),
	(40,'45'),
	(40,'46'),
	(40,'47'),
	(40,'48'),
	(40,'49'),
	(50,'50'),
	(50,'51'),
	(50,'52'),
	(50,'53'),
	(50,'54'),
	(50,'55'),
	(50,'56'),
	(50,'57'),
	(50,'58'),
	(50,'59'),
	(60,'60'),
	(60,'61'),
	(60,'62'),
	(60,'63'),
	(60,'64'),
	(60,'65'),
	(60,'66'),
	(60,'67'),
	(60,'68'),
	(60,'69'),
	(70,'70'),
	(70,'71'),
	(70,'72'),
	(70,'73'),
	(70,'74'),
	(70,'75'),
	(70,'76'),
	(70,'77'),
	(70,'78'),
	(70,'79'),
	(80,'80'),
	(80,'80'),
	(80,'81'),
	(80,'82'),
	(80,'83'),
	(80,'84'),
	(80,'85'),
	(80,'86'),
	(80,'87'),
	(80,'88'),
	(80,'89'),
	(90,'90'),
	(90,'91'),
	(90,'92'),
	(90,'93'),
	(90,'94'),
	(90,'95'),
	(90,'96'),
	(90,'97'),
	(90,'98'),
	(90,'99'),
	(100,'100'),
    (101,'X'),
)
tmpMarks = [ (i,str(i)) for i in xrange(0,101) ]
tmpMarks.append( (101,'X') )
MARK_CHOICES = tuple(tmpMarks)

class RaceMark(models.Model):
    db_table = 'race_marks'

    raceNumber = models.IntegerField('Race number',default=1)
    pilot = models.ForeignKey(Pilot,related_name='marks')
    judge = models.ForeignKey(User,related_name='+')
    mark = models.IntegerField('Mark',choices=MARK_CHOICES,default=101,blank=False)

    class Meta:
        unique_together = ['raceNumber','judge','pilot']

    def __unicode__(self):
        return "pilot #: %d #%d : %d" % (self.pilot.pilotNumber,self.raceNumber,self.mark)

class RaceMarkAdmin(admin.ModelAdmin):
    list_display = ('raceNumber','pilot','judge','mark',)

admin.site.register(RaceMark,RaceMarkAdmin)
