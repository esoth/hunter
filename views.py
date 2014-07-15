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

def ModelView(request):
  form = CalcModelForm(request.GET)
  data = form.data
  meta,hunter = processFormData(data)
  single,meta,totals = dps.runsingle(hunter)
  
  return render(request, 'hunter/model.html',
                {'single': single,
                 'meta': meta,
                 'totals': totals})

def processFormData(data):
  meta = HunterMeta()
  meta.race = int(data['race'] or 0)
  meta.spec = int(data['spec'] or 0)
  meta.talent4 = int(data['talent4'] or 0)
  meta.talent5 = int(data['talent5'] or 0)
  meta.talent6 = int(data['talent6'] or 0)
  meta.talent7 = int(data['talent7'] or 0)
  #meta.talentstr = data['talents']
  
  hunter = Hunter(meta)
  hunter.weaponmin = int(data['weaponmin'])
  hunter.weaponmax = int(data['weaponmax'])
  hunter.weaponspeed = float(data['weaponspeed'])
  
  hunter.setgear(agility=int(data['agility']),
                 crit=int(data['crit']),
                 haste=int(data['haste']),
                 mastery=int(data['mastery']),
                 versatility=int(data['versatility']),
                 multistrike=int(data['multistrike']))
  return meta,hunter
  

def CalcView(request):
  armory = ArmoryModelForm()
  stattable = []
  spelltable = []
  meta = None
  totals = None
  single = []
  if request.method == 'POST':
    form = CalcModelForm(request.POST)
    if form.is_valid():
      form_data = form.cleaned_data
      meta,hunter = processFormData(form_data)
      
      spelltable = do_spells(meta,hunter)
      stattable = hunter.do_stats()
      single,meta,totals = dps.runsingle(hunter)
  else:
    form = CalcModelForm()
  import itertools
  def grouper(iterable):
    args = [iter(iterable)] * 3
    return itertools.izip_longest(*args, fillvalue=None)

  return render(request, 'hunter/calc.html',
                {'form': form,
                 'stattable': grouper(stattable),
                 'spelltable': grouper(spelltable),
                 'single': single,
                 'meta':meta,
                 'totals':totals,
                 'armory': armory})

def ArmoryProcessForm(request):
  if request.method == 'POST':
    form = ArmoryModelForm(request.POST)
    if form.is_valid():
      form_data = form.cleaned_data
      return redirect('/hunter/%s/%s/%s/%s' % (form_data['region'],form_data['server'],form_data['character'],form_data['spec'] and 1 or 2))
    return redirect('/hunter/')
  else:
    return redirect('/hunter/')
  

def ArmoryView(request, region, server, character, spec=None):
  kwargs = {'region':region,'server':server,'character':character}
  url = 'http://%(region)s.battle.net/api/wow/character/%(server)s/%(character)s?fields=stats,talents,items' % kwargs
  data = json.load(urlopen(url))
  
  try:
    spec = int(spec)
  except ValueError:
    spec = 1
  except TypeError:
    spec = 1
  spec -= 1
  
  def squish(v):
    return int(v*.0390)
  
  if data['race'] in PANDARENS:
    data['race'] = PANDARENS[0]
  request.method = 'POST'
  request.POST._mutable = True
  talents = [0,0,0,0,0,0,0]
  for talent in data['talents'][spec]['talents']:
    talents[ talent['tier'] ] = int(talent['column'])
  request.POST['talent4'] = talents[3]
  request.POST['talent5'] = talents[4]
  request.POST['talent6'] = talents[5]
  request.POST['talent7'] = talents[6]
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