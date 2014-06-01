from django.db import models

from calcs.tools import RACES, SPECS, REGIONS, SERVERS

class HunterModel(models.Model):
    race = models.IntegerField(default=4, # Night Elf
                            choices=RACES,
                            max_length=20)
    spec = models.IntegerField(default=0,
                               verbose_name="Specialization",
                               choices=SPECS)
    weaponmin = models.IntegerField(default=0,
                               verbose_name="Weapon (min)",)
    weaponmax = models.IntegerField(default=0,
                               verbose_name="Weapon (max)",)
    weaponspeed = models.FloatField(default=3,
                               verbose_name="Weapon Speed",)
    #talents = models.CharField(default='0000000', max_length=7)
    agility = models.IntegerField(default=1000) #21406)
    crit = models.IntegerField(default=12765)
    haste = models.IntegerField(default=5550)
    mastery = models.IntegerField(default=4373)
    readiness = models.IntegerField(default=0)
    multistrike = models.IntegerField(default=0)
    
    #def talents(self):
    #  return ''.join([str(t) for t in (talent1,talent2,talent3,talent4,talent5,talent6,talent7,)])

class ArmoryModel(models.Model):
    region = models.CharField(choices=REGIONS,
                              default='us',
                              max_length=30)
    server = models.CharField(choices=SERVERS,
                              default='whisperwind',
                              max_length=30)
    character = models.CharField(max_length=30)