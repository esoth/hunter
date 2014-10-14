from django.db import models
from django.db.utils import OperationalError
from gearitem.models import GearItem, Gem

from calcs.tools import RACES, SPECS, REGIONS, SERVERS, TIER1, TIER2, TIER3, TIER4, TIER5, TIER6, TIER7

tier1=[(TIER1.index(t),t) for t in TIER1]
tier2=[(TIER2.index(t),t) for t in TIER2]
tier3=[(TIER3.index(t),t) for t in TIER3]
tier4=[(TIER4.index(t),t) for t in TIER4]
tier5=[(TIER5.index(t),t) for t in TIER5]
tier6=[(TIER6.index(t),t) for t in TIER6]
tier7=[(TIER7.index(t),t) for t in TIER7]

enchants = (('','(none)'),
            ('crit','Critical Strike'),
            ('haste','Haste'),
            ('mastery','Mastery'),
            ('multistrike','Multistrike'),
            ('versatility','Versatility'),
            ('spec','Use spec attunement'),)

class HunterModel(models.Model):
    race = models.IntegerField(default=4, # Night Elf
                            choices=RACES,
                            max_length=20)
    spec = models.IntegerField(default=0,
                               verbose_name="Specialization",
                               choices=SPECS)
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
    enchants = models.CharField(choices=enchants,
                               verbose_name="Enchant/Food stat",
                            default='spec',blank=True,
                            max_length=30)

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

class BMOptionsModel(models.Model):
    opt_bm3 = models.BooleanField(default=True,
                         verbose_name="Hold Bestial Wrath until KC is ready",)
    opt_bm4 = models.BooleanField(default=False,
                         verbose_name="Do not cast Dire Beast during Bestial Wrath",)
    opt_bm5 = models.BooleanField(default=True,
                         verbose_name="Do not cast Focus Fire during Bestial Wrath",)
    opt_bm6 = models.BooleanField(default=True,
                         verbose_name="Cast Focus Fire just before Bestial Wrath",)
                        
  

carefulaim_choices=[(0,'Aimed Shot only'),
                    (1,'Aimed Shot and talents (no Chimaera)'),
                    (2,'No restrictions'),
                   ]
class MMOptionsModel(models.Model):
    opt_mm1 = models.IntegerField(default=2,
                               verbose_name="Careful Aim behavior",
                               choices=carefulaim_choices,max_length=30)
    opt_mm2 = models.IntegerField(default=0,
                         verbose_name="Aimed Shot - min focus (plus cost) to use",
                         max_length=3)
    opt_mm3 = models.BooleanField(default=True,
                         verbose_name="Only cast instant shots after Focusing Shot")

class SVOptionsModel(models.Model):
    opt_sv2 = models.BooleanField(default=True,
                         verbose_name="Null action - place holder")

class AOEOptionsModel(models.Model):
    opt_aoe1 = models.IntegerField(default=8,
                         verbose_name="Targets",
                         max_length=2)
    opt_aoe2 = models.BooleanField(default=True,
                         verbose_name="Cast main nukes")
    opt_aoe3 = models.IntegerField(default=0,
                         verbose_name="Min focus to cast main nukes",
                         max_length=3)

difficulty_options = (('normal','Normal/None'),
                      ('heroic','Heroic'),
                      ('mythic','Mythic'),)


DEFAULT_WEAPON = 113652 # Crystalline Branch of the Brackenspore
DEFAULT_HEAD = 113863 # Gronn-Skin Crown
DEFAULT_NECK = 113851 # Reaver's Nose Ring
DEFAULT_SHOULDERS = 113641 # Living Mountain Shoulderguards
DEFAULT_BACK = 113657 # Cloak of Creeping Necrosis
DEFAULT_CHEST = 113654 # Moss-Woven Mail Shirt
DEFAULT_WRISTS = 113826 # Bracers of the Crying Chorus
DEFAULT_HANDS = 113593 # Grips of Vicious Mauling
DEFAULT_WAIST = 113827 # Belt of Imminent Lies
DEFAULT_LEGS = 113839 # Leggings of Broken Magic
DEFAULT_FEET = 113849 # Face Kickers
DEFAULT_RING1 = 113611 # Flenser's Hookring
DEFAULT_RING2 = 113843 # Spell-Sink Signet
DEFAULT_TRINKET1 = 113853 # Captive Micro-Aberration
DEFAULT_TRINKET2 = 113612 # Scales of Doom

class GearEquipModel(models.Model):
    weapon = models.ForeignKey(GearItem,
                               related_name='gearequip_weapon',
                               default=DEFAULT_WEAPON,
                               limit_choices_to={'slot__in':(15,25)})
    weapon_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    weapon_socket = models.ForeignKey(Gem,related_name='gearequip_weapon_gem')
    weapon_warforged = models.BooleanField(default=False,)

    head = models.ForeignKey(GearItem,
                               related_name='gearequip_head',
                             default=DEFAULT_HEAD,
                             limit_choices_to={'slot':1})
    head_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    head_socket = models.ForeignKey(Gem,related_name='gearequip_head_gem')
    head_warforged = models.BooleanField(default=False,)

    neck = models.ForeignKey(GearItem,
                               related_name='gearequip_neck',
                             default=DEFAULT_NECK,
                             limit_choices_to={'slot':2})
    neck_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    neck_socket = models.ForeignKey(Gem,related_name='gearequip_neck_gem')
    neck_warforged = models.BooleanField(default=False,)

    shoulders = models.ForeignKey(GearItem,
                               related_name='gearequip_shoulders',
                             default=DEFAULT_SHOULDERS,
                             limit_choices_to={'slot':3})
    shoulders_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    shoulders_socket = models.ForeignKey(Gem,related_name='gearequip_shoulders_gem')
    shoulders_warforged = models.BooleanField(default=False,)

    back = models.ForeignKey(GearItem,
                               related_name='gearequip_back',
                             default=DEFAULT_BACK,
                             limit_choices_to={'slot':16})
    back_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    back_socket = models.ForeignKey(Gem,related_name='gearequip_back_gem')
    back_warforged = models.BooleanField(default=False,)

    chest = models.ForeignKey(GearItem,
                               related_name='gearequip_chest',
                             default=DEFAULT_CHEST,
                             limit_choices_to={'slot':5})
    chest_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    chest_socket = models.ForeignKey(Gem,related_name='gearequip_chest_gem')
    chest_warforged = models.BooleanField(default=False,)

    wrists = models.ForeignKey(GearItem,
                               related_name='gearequip_wrists',
                             default=DEFAULT_WRISTS,
                             limit_choices_to={'slot':9})
    wrists_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    wrists_socket = models.ForeignKey(Gem,related_name='gearequip_wrists_gem')
    wrists_warforged = models.BooleanField(default=False,)

    hands = models.ForeignKey(GearItem,
                               related_name='gearequip_hands',
                             default=DEFAULT_HANDS,
                             limit_choices_to={'slot':10})
    hands_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    hands_socket = models.ForeignKey(Gem,related_name='gearequip_hands_gem')
    hands_warforged = models.BooleanField(default=False,)

    waist = models.ForeignKey(GearItem,
                               related_name='gearequip_waist',
                             default=DEFAULT_WAIST,
                             limit_choices_to={'slot':6})
    waist_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    waist_socket = models.ForeignKey(Gem,related_name='gearequip_waist_gem')
    waist_warforged = models.BooleanField(default=False,)

    legs = models.ForeignKey(GearItem,
                               related_name='gearequip_legs',
                             default=DEFAULT_LEGS,
                             limit_choices_to={'slot':7})
    legs_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    legs_socket = models.ForeignKey(Gem,related_name='gearequip_legs_gem')
    legs_warforged = models.BooleanField(default=False,)

    feet = models.ForeignKey(GearItem,
                               related_name='gearequip_feet',
                             default=DEFAULT_FEET,
                             limit_choices_to={'slot':8})
    feet_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    feet_socket = models.ForeignKey(Gem,related_name='gearequip_feet_gem')
    feet_warforged = models.BooleanField(default=False,)

    ring1 = models.ForeignKey(GearItem,
                               related_name='gearequip_ring1',
                             default=DEFAULT_RING1,
                             limit_choices_to={'slot':11})
    ring1_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    ring1_socket = models.ForeignKey(Gem,related_name='gearequip_ring1_gem')
    ring1_warforged = models.BooleanField(default=False,)

    ring2 = models.ForeignKey(GearItem,
                               related_name='gearequip_ring2',
                             default=DEFAULT_RING2,
                             limit_choices_to={'slot':11})
    ring2_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    ring2_socket = models.ForeignKey(Gem,related_name='gearequip_ring2_gem')
    ring2_warforged = models.BooleanField(default=False,)

    trinket1 = models.ForeignKey(GearItem,
                               related_name='gearequip_trinket1',
                             default=DEFAULT_TRINKET1,
                             limit_choices_to={'slot':12})
    trinket1_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    trinket1_socket = models.ForeignKey(Gem,related_name='gearequip_trinket1_gem')
    trinket1_warforged = models.BooleanField(default=False,)

    trinket2 = models.ForeignKey(GearItem,
                               related_name='gearequip_trinket2',
                             default=DEFAULT_TRINKET2,
                             limit_choices_to={'slot':12})
    trinket2_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    trinket2_socket = models.ForeignKey(Gem,related_name='gearequip_trinket2_gem')
    trinket2_warforged = models.BooleanField(default=False,)