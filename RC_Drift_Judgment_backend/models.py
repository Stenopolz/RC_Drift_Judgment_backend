from django.db import models
from django.contrib.auth.models import User

class Pilot(models.Model):
    db_table = 'pilots'

    firstName = models.CharField('First Name',max_length=120)
    middleName = models.CharField('Middle Name',max_length=120,blank=True,null=True)
    lastName = models.CharField('Last Name',max_length=120)

    teamName = models.CharField('Team',max_length=200,blank=True,null=True)

    def __unicode__(self):
        return "%s %s %s" % (self.lastName, self.firstName, self.middleName)

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
class RaceMark(models.Model):
    db_table = 'race_marks'

    raceNumber = models.IntegerField('Race number',default=1)
    pilot = models.ForeignKey(Pilot,related_name='marks')
    judge = models.ForeignKey(User,related_name='+')
    mark = models.IntegerField('Mark',choices=MARK_CHOICES,default=100,blank=False)

    class Meta:
        unique_together = ['raceNumber','judge','pilot']

    def __unicode__(self):
        return ""
