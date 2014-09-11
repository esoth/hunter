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
from calcs.tools import *

from calcs.execution import dps

from models import *
from gearitem.models import GearItem, Gem

class CalcModelForm(ModelForm):
    class Meta:
      model = HunterModel

class BMOptionsForm(ModelForm):
    class Meta:
      model = BMOptionsModel

class MMOptionsForm(ModelForm):
    class Meta:
      model = MMOptionsModel

class SVOptionsForm(ModelForm):
    class Meta:
      model = SVOptionsModel

class AOEOptionsForm(ModelForm):
    class Meta:
      model = AOEOptionsModel

class ArmoryModelForm(ModelForm):
    class Meta:
      model = ArmoryModel

class GearEquipModelForm(ModelForm):
    class Meta:
      model = GearEquipModel

def ModelView(request):
  form = CalcModelForm(request.GET)
  data = form.data
  meta,hunter = processFormData(data)
  bmo = BMOptionsForm(request.GET)
  svo = SVOptionsForm(request.GET)
  mmo = MMOptionsForm(request.GET)
  aeo = AOEOptionsForm(request.GET)
  options = processOptions(request,bmo,mmo,svo,aeo)
  single,meta,totals = dps.runner(hunter,options,lastcalc=float(request.POST.get('lastcalc') or 0))
  
  return render(request, 'hunter/model.html',
                {'single': single,
                 'meta': meta,
                 'totals': totals})

def ModelDebugView(request):
  form = CalcModelForm(request.GET)
  data = form.data
  meta,hunter = processFormData(data)
  bmo = BMOptionsForm(request.GET)
  svo = SVOptionsForm(request.GET)
  mmo = MMOptionsForm(request.GET)
  aeo = AOEOptionsForm(request.GET)
  options = processOptions(request,bmo,mmo,svo,aeo)
  single,meta,totals = dps.runner(hunter,options,lastcalc=float(request.POST.get('lastcalc') or 0))
  
  return render(request, 'hunter/model.html',
                {'single': single,
                 'meta': meta,
                 'totals': totals,
                 'debug': True})

def ModelAoEView(request):
  form = CalcModelForm(request.GET)
  data = form.data
  meta,hunter = processFormData(data)
  bmo = BMOptionsForm(request.GET)
  svo = SVOptionsForm(request.GET)
  mmo = MMOptionsForm(request.GET)
  aeo = AOEOptionsForm(request.GET)
  options = processOptions(request,bmo,mmo,svo,aeo)
  single,meta,totals = dps.runner(hunter,options,aoe=True,lastcalc=float(request.POST.get('lastcalc') or 0))
  
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

def processOptions(request,bmo,mmo,svo,aeo):
  options = {}
  options['bm3'] = bmo.data.get('opt_bm3',False)
  options['bm4'] = bmo.data.get('opt_bm4',False)
  options['bm5'] = bmo.data.get('opt_bm5',False)
  options['bm6'] = bmo.data.get('opt_bm6',False)
  options['mm1'] = int(mmo.data.get('opt_mm1',0))
  options['mm2'] = int(mmo.data.get('opt_mm2',0))
  options['mm3'] = mmo.data.get('opt_mm3',False)
  options['aoe1'] = int(mmo.data.get('opt_aoe1',0))
  options['aoe2'] = mmo.data.get('opt_aoe2',False)
  options['aoe3'] = int(mmo.data.get('opt_aoe3',0))
  return options
  

def CalcView(request,from_armory=False):
  armory = ArmoryModelForm()
  stattable = []
  spelltable = []
  meta = None
  totals = None
  aoetotals = None
  single = []
  if request.method == 'POST':
    form = CalcModelForm(request.POST)
    if from_armory:
      bmo = BMOptionsForm()
      svo = SVOptionsForm()
      mmo = MMOptionsForm()
      aeo = AOEOptionsForm()
    else:
      bmo = BMOptionsForm(request.POST)
      svo = SVOptionsForm(request.POST)
      mmo = MMOptionsForm(request.POST)
      aeo = AOEOptionsForm(request.POST)
    options = processOptions(request,bmo,mmo,svo,aeo)
    if form.is_valid():
      form_data = form.cleaned_data
      meta,hunter = processFormData(form_data)
      
      spelltable = do_spells(meta,hunter)
      if meta.race != UNDEAD:
        spelltable = [spell for spell in spelltable if spell['name'] != 'Touch of the Grave']
      stattable = hunter.do_stats()
      single,meta,totals = dps.runner(hunter,options,lastcalc=float(request.POST.get('lastcalc') or 0))
      aoe,dummy,aoetotals = dps.runner(hunter,options,aoe=True)
  else:
    form = CalcModelForm()
    bmo = BMOptionsForm()
    svo = SVOptionsForm()
    mmo = MMOptionsForm()
    aeo = AOEOptionsForm()
  import itertools
  def grouper(iterable):
    args = [iter(iterable)] * 3
    return itertools.izip_longest(*args, fillvalue=None)

  return render(request, 'hunter/calc.html',
                {'form': form,
                 'bmo': bmo,
                 'mmo': mmo,
                 'svo': svo,
                 'aeo': aeo,
                 'stattable': grouper(stattable),
                 'spelltable': grouper(spelltable),
                 'spelllist': spelltable,
                 'meta':meta,
                 'totals':totals,
                 'aoetotals':aoetotals,
                 'armory': armory})

def ScaleStatView(request):
  form = CalcModelForm(request.GET)
  data = form.data
  meta,hunter = processFormData(data)
  bmo = BMOptionsForm(request.GET)
  svo = SVOptionsForm(request.GET)
  mmo = MMOptionsForm(request.GET)
  aeo = AOEOptionsForm(request.GET)
  options = processOptions(request,bmo,mmo,svo,aeo)
  d = dps.runner(hunter,options)[-1]['dps']
  scale = [d]
  
  stat = request.GET['stat']
  gearstat = getattr(hunter,stat)
  start = gearstat.gear()
  _stat = start
  for x in range(1,11):
    _stat = start + x*100
    gearstat.gear(_stat)
    scale.append(dps.runner(hunter,options)[-1]['dps'])
    
  return HttpResponse(json.dumps(scale), content_type="application/json")
  #return json.dumps(scale)

def ScalingView(request):
  form = CalcModelForm(request.GET)
  data = form.data
  meta,hunter = processFormData(data)
  bmo = BMOptionsForm(request.GET)
  svo = SVOptionsForm(request.GET)
  mmo = MMOptionsForm(request.GET)
  aeo = AOEOptionsForm(request.GET)
  options = processOptions(request,bmo,mmo,svo,aeo)
  d = dps.runner(hunter,options)[-1]['dps']
  scales = {'agility':[d],'crit':[d],'haste':[d],'mastery':[d],'multistrike':[d],'versatility':[d]}
  
  for stat in scales.keys():
    gearstat = getattr(hunter,stat)
    start = gearstat.gear()
    _stat = start
    for x in range(1,11):
      _stat = start + x*10
      gearstat.gear(_stat)
      scales[stat].append(dps.runner(hunter,options)[-1]['dps'])
    gearstat.gear(start)
  
  specs = ['Beast Mastery','Marksmanship','Survival']
  subtitle = specs[meta.spec] + ': ' + ', '.join([TIER4[meta.talent4],TIER5[meta.talent5],TIER6[meta.talent6],TIER7[meta.talent7]])
  
  return render(request, 'hunter/scale.html',
                {'scales':scales,
                 'subtitle':subtitle})

def ArmoryProcessForm(request):
  if request.method == 'POST':
    form = ArmoryModelForm(request.POST)
    if form.is_valid():
      form_data = form.cleaned_data
      return redirect('/hunter/%s/%s/%s/%s' % (form_data['region'],form_data['server'],form_data['character'],form_data['spec'] and 1 or 2))
    return redirect('/hunter/')
  else:
    return redirect('/hunter/')

def build_item(slot):
  from gearitem.tools import stats_used
  attrs = {}
  for stat in slot['stats']:
    if stat['stat'] in stats_used:
      attrs[stats_used[stat['stat']]] = stat['amount']
  if 'gem1' in slot['tooltipParams']:
    attrs['gem'] = slot['tooltipParams']['gem1']
  attrs['id'] = slot['id']
  attrs['name'] = slot['name']
  attrs['ilvl'] = slot['itemLevel']
  return attrs

def ArmoryView(request, region, server, character, spec=None):
  kwargs = {'region':region,'server':server,'character':character,'apikey':API_KEY}
  url = 'https://%(region)s.api.battle.net/wow/character/%(server)s/%(character)s?apikey=%(apikey)s&fields=stats,talents,items' % kwargs
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
  
  # items
  head = build_item(data['items']['head'])
  neck = build_item(data['items']['neck'])
  shoulders = build_item(data['items']['shoulder'])
  chest = build_item(data['items']['chest'])
  back = build_item(data['items']['back'])
  wrists = build_item(data['items']['wrist'])
  hands = build_item(data['items']['hands'])
  waist = build_item(data['items']['waist'])
  legs = build_item(data['items']['legs'])
  feet = build_item(data['items']['feet'])
  ring1 = build_item(data['items']['finger1'])
  ring2 = build_item(data['items']['finger2'])
  trinket1 = build_item(data['items']['trinket1'])
  trinket2 = build_item(data['items']['trinket2'])
  
  request.POST['race'] = data['race']
  request.POST['spec'] = data['talents'][spec]['spec']['order']
  request.POST['weaponmin'] = squish(data['items']['mainHand']['weaponInfo']['damage']['min'])/2
  request.POST['weaponmax'] = squish(data['items']['mainHand']['weaponInfo']['damage']['max'])/2
  request.POST['weaponspeed'] = data['items']['mainHand']['weaponInfo']['weaponSpeed']
  return CalcView(request,from_armory=True)
  
def GearTableView(request):
  gear_table = {'':{'source':'','agility':'','crit':'','haste':'','mastery':'','multistrike':'','versatility':'','zone':'','source':''}}
  for g in GearItem.objects.all():
    gear_table[g.name + ' (' + (g.nameDescription or 'normal') + ')'] = {'zone':g.zone,
                 'source':g.source,
                 'agility':g.agility,
                 'crit':g.crit,
                 'haste':g.haste,
                 'mastery':g.mastery,
                 'multistrike':g.multistrike,
                 'versatility':g.versatility,
                 'zone':g.zone,
                 'source':g.source,
                 'socket1':g.socket1,
                 'socket2':g.socket2,
                 'socket3':g.socket3,
                 'socket_bonus':g.socket_bonus}
  try:
    for g in Gem.objects.all():
      gear_table[g.name] = {'agility':g.agility,
           'crit':g.crit,
           'haste':g.haste,
           'mastery':g.mastery,
           'multistrike':g.multistrike,
           'versatility':g.versatility}
  except:
    pass
  return HttpResponse(json.dumps(gear_table), mimetype='application/json')


def GearEquipTestView(request):
  form = GearEquipModelForm()
  slots = []
  
  for s in ('weapon','head','neck','shoulders','back','chest','wrists','hands','waist','legs','feet','ring1','ring2','trinket1','trinket2',):
    slots.append({'id':s,'name':s[0].upper()+s[1:]+':','small':False,'form':form[s]})
    slots.append({'id':s+'_socket1','name':'Socket 1','small':True,'form':form[s+'_socket1']})
  
  return render(request, 'hunter/geartest.html',
                {'form': form,
                 'slots': slots})

def GearEquipTestView2(request):
  form = GearEquipModelForm()
  slots = []
  
  data = json.load(urlopen('https://us.api.battle.net/wow/character/whisperwind/esoth?apikey=%s&fields=stats,talents,items' % API_KEY))
  
  armory = {'head':build_item(data['items']['head']),
            'neck':build_item(data['items']['neck']),
            'shoulders':build_item(data['items']['shoulder']),
            'chest':build_item(data['items']['chest']),
            'back':build_item(data['items']['back']),
            'wrists':build_item(data['items']['wrist']),
            'hands':build_item(data['items']['hands']),
            'waist':build_item(data['items']['waist']),
            'legs':build_item(data['items']['legs']),
            'feet':build_item(data['items']['feet']),
            'ring1':build_item(data['items']['finger1']),
            'ring2':build_item(data['items']['finger2']),
            'trinket1':build_item(data['items']['trinket1']),
            'trinket2':build_item(data['items']['trinket2'])}

  for slot,attrs in armory.items():
    slots.append({'id':attrs['id'],
                  'agility':attrs.get('agility',0),
                  'crit':attrs.get('crit',0),
                  'haste':attrs.get('haste',0),
                  'mastery':attrs.get('mastery',0),
                  'multistrike':attrs.get('multistrike',0),
                  'versatility':attrs.get('versatility',0),
                  'name':attrs.get('name',0),
                  'ilvl':attrs.get('ilvl',0),
      })
  
  return render(request, 'hunter/geartest2.html',
                {'slots': slots})