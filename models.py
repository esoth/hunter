from django.db import models

from calcs.tools import RACES, SPECS

class HunterModel(models.Model):
    race = models.IntegerField(default=4, # Night Elf
                            choices=RACES,
                            max_length=20)
    spec = models.IntegerField(default=0,
                               choices=SPECS)
    weaponmin = models.IntegerField(default=0)
    weaponmax = models.IntegerField(default=0)
    weaponspeed = models.FloatField(default=3)
    talents = models.CharField(default='0000000', max_length=7)
    agility = models.IntegerField(default=0)
    crit = models.IntegerField(default=0)
    haste = models.IntegerField(default=0)
    mastery = models.IntegerField(default=0)
    readiness = models.IntegerField(default=0)
    multistrike = models.IntegerField(default=0)
    
    #def talents(self):
    #  return ''.join([str(t) for t in (talent1,talent2,talent3,talent4,talent5,talent6,talent7,)])