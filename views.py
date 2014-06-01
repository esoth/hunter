from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.views import generic
import json
from urllib import urlopen

from django.forms import ModelForm

from calcs.hunter import Hunter
from calcs.huntermeta import HunterMeta
from calcs.spells import do_spells
from calcs.tools import PANDARENS

from models import HunterModel, ArmoryModel

class CalcModelForm(ModelForm):
    class Meta:
      model = HunterModel

class ArmoryModelForm(ModelForm):
    class Meta:
      model = ArmoryModel

def CalcView(request):
  armory = ArmoryModelForm()
  stattable = None
  spelltable = None
  if request.method == 'POST':
    form = CalcModelForm(request.POST)
    if form.is_valid():
      form_data = form.cleaned_data
      meta = HunterMeta()
      meta.race = form_data['race']
      meta.spec = form_data['spec']
      #meta.talentstr = form_data['talents']
      
      hunter = Hunter()
      hunter.meta = meta
      hunter.weaponmin = form_data['weaponmin'] #19049
      hunter.weaponmax = form_data['weaponmax'] # 35379
      hunter.weaponspeed = form_data['weaponspeed']
      
      hunter.setgear(agility=form_data['agility'],
                     crit=form_data['crit'],
                     haste=form_data['haste'],
                     mastery=form_data['mastery'],
                     readiness=form_data['readiness'],
                     multistrike=form_data['multistrike'])
      
      spelltable = do_spells(meta,hunter)
      stattable = hunter.do_stats()
  else:
    form = CalcModelForm()

  return render(request, 'hunter/calc.html',
                {'form': form,
                 'stattable': stattable,
                 'spelltable': spelltable,
                 'armory': armory})

def ArmoryProcessForm(request):
  if request.method == 'POST':
    form = ArmoryModelForm(request.POST)
    if form.is_valid():
      form_data = form.cleaned_data
    
    return redirect('/hunter/%s/%s/%s' % (form_data['region'],form_data['server'],form_data['character']))
  else:
    return redirect('/hunter/')
  

def ArmoryView(request, region, server, character):
  kwargs = {'region':region,'server':server,'character':character}
  url = 'http://%(region)s.battle.net/api/wow/character/%(server)s/%(character)s?fields=stats,talents,items' % kwargs
  data = json.load(urlopen(url))
  
  spec = 0 # first spec
  
  if data['race'] in PANDARENS:
    data['race'] = PANDARENS[0]
  request.method = 'POST'
  request.POST._mutable = True
  request.POST['agility'] = data['stats']['agi']
  request.POST['crit'] = data['stats']['critRating']
  request.POST['haste'] = data['stats']['hasteRating']
  request.POST['mastery'] = data['stats']['masteryRating']
  request.POST['readiness'] = 0
  request.POST['multistrike'] = 0
  request.POST['race'] = data['race']
  request.POST['spec'] = data['talents'][spec]['spec']['order']
  request.POST['weaponmin'] = data['items']['mainHand']['weaponInfo']['damage']['min']
  request.POST['weaponmax'] = data['items']['mainHand']['weaponInfo']['damage']['max']
  request.POST['weaponspeed'] = data['items']['mainHand']['weaponInfo']['weaponSpeed']
  return CalcView(request)