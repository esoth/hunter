from django.db import models

from calcs.tools import RACES, SPECS, REGIONS, SERVERS, TIER1, TIER2, TIER3, TIER4, TIER5, TIER6, TIER7

tier1=[(TIER1.index(t),t) for t in TIER1]
tier2=[(TIER2.index(t),t) for t in TIER2]
tier3=[(TIER3.index(t),t) for t in TIER3]
tier4=[(TIER4.index(t),t) for t in TIER4]
tier5=[(TIER5.index(t),t) for t in TIER5]
tier6=[(TIER6.index(t),t) for t in TIER6]
tier7=[(TIER7.index(t),t) for t in TIER7]

class HunterModel(models.Model):
    race = models.IntegerField(default=4, # Night Elf
                            choices=RACES,
                            max_length=20)
    spec = models.IntegerField(default=0,
                               verbose_name="Specialization",
                               choices=SPECS)
    weaponmin = models.IntegerField(default=952,
                               verbose_name="Weapon (min)",)
    weaponmax = models.IntegerField(default=1430,
                               verbose_name="Weapon (max)",)
    weaponspeed = models.FloatField(default=3,
                               verbose_name="Weapon Speed",)
#    talent1 = models.IntegerField(default=tier1[0],
#                               verbose_name="Talents - level 15",
#                               choices=tier1,max_length=30)
#    talent2 = models.IntegerField(default=tier2[0],
#                               verbose_name="Talents - level 30",
#                               choices=tier2,max_length=30)
#    talent3 = models.IntegerField(default=tier3[0],
#                               verbose_name="Talents - level 45",
#                               choices=tier3,max_length=30)
    talent4 = models.IntegerField(default=tier4[0],
                               verbose_name="Talents - level 60",
                               choices=tier4,max_length=30)
    talent5 = models.IntegerField(default=tier5[0],
                               verbose_name="Talents - level 75",
                               choices=tier5,max_length=30)
    talent6 = models.IntegerField(default=tier6[0],
                               verbose_name="Talents - level 90",
                               choices=tier6,max_length=30)
    talent7 = models.IntegerField(default=tier7[0],
                               verbose_name="Talents - level 100",
                               choices=tier7,max_length=30)
    agility = models.IntegerField(default=2377) #21406)
    crit = models.IntegerField(default=1052)
    haste = models.IntegerField(default=748)
    mastery = models.IntegerField(default=737)
    multistrike = models.IntegerField(default=506)
    versatility = models.IntegerField(default=77)

class ArmoryModel(models.Model):
    region = models.CharField(choices=REGIONS,
                              default='us',
                              max_length=30)
    server = models.CharField(choices=SERVERS,
                              default='whisperwind',
                              max_length=30)
    character = models.CharField(max_length=30)
    spec = models.BooleanField(default=True,
                               verbose_name="Use first spec")