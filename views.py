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

from calcs.execution import dps

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
  meta = None
  totals = None
  single = []
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
                     versatility=form_data['versatility'],
                     multistrike=form_data['multistrike'])
      
      spelltable = do_spells(meta,hunter)
      stattable = hunter.do_stats()
      single,meta,totals = dps.runsingle(hunter)
  else:
    form = CalcModelForm()

  return render(request, 'hunter/calc.html',
                {'form': form,
                 'stattable': stattable,
                 'spelltable': spelltable,
                 'single': single,
                 'meta':meta,
                 'totals':totals,
                 'armory': armory})

def ArmoryProcessForm(request):
  if request.method == 'POST':
    form = ArmoryModelForm(request.POST)
    if form.is_valid():
      form_data = form.cleaned_data
      return redirect('/hunter/%s/%s/%s' % (form_data['region'],form_data['server'],form_data['character']))
    return redirect('/hunter/')
  else:
    return redirect('/hunter/')
  

def ArmoryView(request, region, server, character):
  kwargs = {'region':region,'server':server,'character':character}
  url = 'http://%(region)s.battle.net/api/wow/character/%(server)s/%(character)s?fields=stats,talents,items' % kwargs
  data = json.load(urlopen(url))
  
  spec = 0 # first spec
  
  def squish(v):
    return int(v*.0390)
  
  if data['race'] in PANDARENS:
    data['race'] = PANDARENS[0]
  request.method = 'POST'
  request.POST._mutable = True
  request.POST['agility'] = squish(data['stats']['agi'])
  request.POST['crit'] = squish(data['stats']['critRating'])
  request.POST['haste'] = squish(data['stats']['hasteRating'])
  request.POST['mastery'] = squish(data['stats']['masteryRating'])
  request.POST['versatility'] = 0
  request.POST['multistrike'] = 0
  request.POST['race'] = data['race']
  request.POST['spec'] = data['talents'][spec]['spec']['order']
  request.POST['weaponmin'] = squish(data['items']['mainHand']['weaponInfo']['damage']['min'])/2
  request.POST['weaponmax'] = squish(data['items']['mainHand']['weaponInfo']['damage']['max'])/2
  request.POST['weaponspeed'] = data['items']['mainHand']['weaponInfo']['weaponSpeed']
  return CalcView(request)