from django import forms
from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http.request import QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.views import generic
import json
import itertools
from urllib2 import urlopen

from django.forms import ModelForm

from calcs.hunter import Hunter
from calcs.huntermeta import HunterMeta
from calcs.spells import do_spells
from calcs.tools import *

from calcs.execution import dps
from calcs.execution import procs

from models import *
from gearitem.models import GearItem, Gem
from gearitem.tools import stats_used

def grouper(iterable):
  args = [iter(iterable)] * 3
  return itertools.izip_longest(*args, fillvalue=None)

class HunterModelForm(ModelForm):
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
    excludes = []
    class Meta:
      model = GearEquipModel

def ModelView(request):
  gearform = GearEquipModelForm(request.GET)
  gear = processEquippedGear(gearform.data)
  metadata = HunterModelForm(request.GET)
  bmo = BMOptionsForm(request.GET)
  svo = SVOptionsForm(request.GET)
  mmo = MMOptionsForm(request.GET)
  aeo = AOEOptionsForm(request.GET)
  data = process_form_data(gear,metadata,bmo,mmo,svo,aeo)
  single,meta,totals = dps.runner(data['hunter'],data['options'],lastcalc=float(request.POST.get('lastcalc') or 0))

  return render(request, 'hunter/model.html',
                {'single': single,
                 'meta': meta,
                 'totals': totals})

def ModelDebugView(request):
  gearform = GearEquipModelForm(request.GET)
  gear = processEquippedGear(gearform.data)
  metadata = HunterModelForm(request.GET)
  bmo = BMOptionsForm(request.GET)
  svo = SVOptionsForm(request.GET)
  mmo = MMOptionsForm(request.GET)
  aeo = AOEOptionsForm(request.GET)
  data = process_form_data(gear,metadata,bmo,mmo,svo,aeo)
  single,meta,totals = dps.runner(data['hunter'],data['options'],lastcalc=float(request.POST.get('lastcalc') or 0))

  return render(request, 'hunter/model.html',
                {'single': single,
                 'meta': meta,
                 'totals': totals,
                 'debug': True})

def ModelAoEView(request):
  gearform = GearEquipModelForm(request.GET)
  gear = processEquippedGear(gearform.data)
  metadata = HunterModelForm(request.GET)
  bmo = BMOptionsForm(request.GET)
  svo = SVOptionsForm(request.GET)
  mmo = MMOptionsForm(request.GET)
  aeo = AOEOptionsForm(request.GET)
  data = process_form_data(gear,metadata,bmo,mmo,svo,aeo)
  single,meta,totals = dps.runner(data['hunter'],data['options'],aoe=True,lastcalc=float(request.POST.get('lastcalc') or 0))

  return render(request, 'hunter/model.html',
                {'single': single,
                 'meta': meta,
                 'totals': totals})

def ScaleStatView(request):
  gearform = GearEquipModelForm(request.GET)
  gear = processEquippedGear(gearform.data)
  metadata = HunterModelForm(request.GET)
  bmo = BMOptionsForm(request.GET)
  svo = SVOptionsForm(request.GET)
  mmo = MMOptionsForm(request.GET)
  aeo = AOEOptionsForm(request.GET)
  data = process_form_data(gear,metadata,bmo,mmo,svo,aeo)
  d = dps.runner(data['hunter'],data['options'])[-1]['dps']
  scale = [d]

  stat = request.GET['stat']
  gearstat = getattr(data['hunter'],stat)
  start = gearstat.gear()
  _stat = start
  for x in range(1,4):
    _stat = start + x*500
    gearstat.gear(_stat)
    scale.append(dps.runner(data['hunter'],data['options'])[-1]['dps'])

  return HttpResponse(json.dumps(scale), content_type="application/json")

def ScalingView(request):
  gearform = GearEquipModelForm(request.GET)
  gear = processEquippedGear(gearform.data)
  metadata = HunterModelForm(request.GET)
  bmo = BMOptionsForm(request.GET)
  svo = SVOptionsForm(request.GET)
  mmo = MMOptionsForm(request.GET)
  aeo = AOEOptionsForm(request.GET)
  data = process_form_data(gear,metadata,bmo,mmo,svo,aeo)
  d = dps.runner(data['hunter'],data['options'])[-1]['dps']
  scales = {'agility':[d],'crit':[d],'haste':[d],'mastery':[d],'multistrike':[d],'versatility':[d]}

  meta = data['meta']
  specs = ['Beast Mastery','Marksmanship','Survival']
  subtitle = specs[meta.spec] + ': ' + ', '.join([TIER4[meta.talent4],TIER5[meta.talent5],TIER6[meta.talent6],TIER7[meta.talent7]])

  return render(request, 'hunter/scale.html',
                {'scales':scales,
                 'subtitle':subtitle})



def ArmoryView(request, region, server, character, spec=None):
  pass
  # do a redirect

def contextsort(val):
  ranks = ['raid-mythic','raid-heroic','raid-normal','dungeon-heroic']
  if val and val[0] and val[0] in ranks:
    return ranks.index(val[0])
  return len(ranks)

@cache_page(3600)
def GearTableView(request):
  gear_table = {'':{'source':'','agility':'','crit':'','haste':'','mastery':'','multistrike':'','versatility':'','zone':'','source':''}}

  for g in GearItem.objects.all():
    contexts = {}
    for context in g.gearcontext_set.all():
      contexts[context.context] = {'agility':context.agility,
                           'crit':context.crit,
                           'haste':context.haste,
                           'mastery':context.mastery,
                           'multistrike':context.multistrike,
                           'versatility':context.versatility,
                           'weapon_min':context.weapon_min,
                           'weapon_max':context.weapon_max,
                           'weapon_speed':context.weapon_speed,
                           'ilvl':context.ilvl,
                           'contextPretty':context.contextPretty()}
    if not contexts:
      contexts[g.nameDescription or 'na'] = {'agility':g.agility,
                           'crit':g.crit,
                           'haste':g.haste,
                           'mastery':g.mastery,
                           'multistrike':g.multistrike,
                           'versatility':g.versatility,
                           'weapon_min':g.weapon_min,
                           'weapon_max':g.weapon_max,
                           'weapon_speed':g.weapon_speed,
                           'ilvl':g.ilvl,
                           'contextPretty':g.nameDescription or '(N/A)'}
    contextOpts = sorted([(k,v['contextPretty']) for k,v in contexts.items()], key=contextsort, reverse=True)
    gear_table[g.id] = {'zone':g.zone,
                        'name':g.name,
                        'source':g.source,
                        'icon':g.icon,
                        'zone':g.zone,
                        'source':g.source,
                        'contexts':contexts,
                        'contextOpts':contextOpts}
  for g in Gem.objects.all():
    gear_table[g.name] = {'agility':g.agility,
         'crit':g.crit,
         'haste':g.haste,
         'mastery':g.mastery,
         'multistrike':g.multistrike,
         'versatility':g.versatility}
  return HttpResponse(json.dumps(gear_table)) #, mimetype='application/json')

def processEquippedGear(data):
  _stats = ('agility','crit','haste','mastery','multistrike','versatility')
  _data = {'agility':0,
           'crit':0,
           'haste':0,
           'mastery':0,
           'multistrike':0,
           'versatility':0,
           'weapon_min':0,
           'weapon_max':0,
           'weapon_speed':3.0,
           'icon':'',
           'equipped':[],
           'name':'',
           }
  # sockets
  sockets = []
  for s in SLOTS:
    if data[s]:
      try:
        _data['equipped'].append({'id':int(data[s]),'bonus':''})
      except ValueError: # unknown gear
        pass
    if data.get(s+'_socket'):
      gem = Gem.objects.filter(id=data[s+'_socket'])
      if gem:
        gem = gem[0]
        for stat in _stats:
          _data[stat] += getattr(gem,stat,0)

  # weapon
  try:
    _data['weapon_min'] = float(data['weapon_min'])
    _data['weapon_max'] = float(data['weapon_max'])
    _data['weapon_speed'] = float(data['weapon_speed'])
  except ValueError:
    pass # bad data - leave defaults

  _data['icon'] = data.get('icon')
  for s in _stats:
    for idx in range(1,16):
      _data[s] += int(data['%s[%d]' % (s,idx)])

  return _data


def process_form_data(gear,metadata,bmo,mmo,svo,aeo):
  ### Do this on all modeling using just form data
  meta = HunterMeta()
  meta.race = int(metadata.data['race'] or 0)
  meta.spec = int(metadata.data['spec'] or 0)
  meta.talent4 = int(metadata.data['talent4'] or 0)
  meta.talent5 = int(metadata.data['talent5'] or 0)
  meta.talent6 = int(metadata.data['talent6'] or 0)
  meta.talent7 = int(metadata.data['talent7'] or 0)
  meta.enchants = metadata.data['enchants']

  hunter = Hunter(meta,gear['equipped'])
  hunter.weaponmin = int(gear['weapon_min'])
  hunter.weaponmax = int(gear['weapon_max'])
  hunter.weaponspeed = float(gear['weapon_speed'])

  hunter.setgear(agility=int(gear['agility']),
                 crit=int(gear['crit']),
                 haste=int(gear['haste']),
                 mastery=int(gear['mastery']),
                 versatility=int(gear['versatility']),
                 multistrike=int(gear['multistrike']))

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

  spelltable = do_spells(meta,hunter)
  if meta.race != UNDEAD:
    spelltable = [spell for spell in spelltable if spell['name'] != 'Touch of the Grave']
  stattable = hunter.do_stats()
  proc_info = procs.proc_info(gear['equipped'],hunter.haste.total())
  hunter.do_procs(proc_info)
  stattable = hunter.do_stats()
  return {'meta':meta,
          'hunter':hunter,
          'spelltable':spelltable,
          'stattable':stattable,
          'proc_info':proc_info,
          'options':options,
          }

def process_armory(armory_form):
  region = armory_form['region']
  server = armory_form['server']
  character = armory_form['character']
  spec = armory_form.get('spec')
  kwargs = {'region':region,
            'server':armory_form['server'],
            'character':armory_form['character'],
            'apikey':API_KEY}
  url = 'https://%(region)s.api.battle.net/wow/character/%(server)s/%(character)s?apikey=%(apikey)s&fields=stats,talents,items' % kwargs
  title = '%s of %s (%s)' % (character, SERVER_NAMES.get(server,server), region)
  data = json.load(urlopen(url.encode('utf-8')))
  if data.get('status') == 'nok':
    return None
  spc = not spec and 1 or 0
  _spec = data['talents'][spc]['spec']['order']
  talents = {}
  for talent in data['talents'][spc]['talents']:
    talents['talent%d' % (talent['tier']+1)] = talent['column']

  talent4 = talents.get('talent4') or 0
  talent5 = talents.get('talent5') or 0
  talent6 = talents.get('talent6') or 0
  talent7 = talents.get('talent7') or 0
  race = data['race']

  def build_item(slot):
    if not slot:
      return {}
    attrs = {}
    for stat in slot['stats']:
      if stat['stat'] in stats_used:
        attrs[stats_used[stat['stat']]] = stat['amount']
    if 'gem0' in slot['tooltipParams']:
      attrs['socket'] = slot['tooltipParams']['gem0']
    attrs['id'] = slot['id']
    attrs['name'] = slot['name']
    attrs['ilvl'] = slot['itemLevel']
    attrs['icon'] = slot['icon']
    attrs['context'] = slot['context']
    attrs['bonuses'] = slot['bonusLists']

    # check our database to add heroic to ilvls below 600
    if (attrs['ilvl'] <= 600 or 'Fen-Yu' in attrs['name']) and GearItem.objects.filter(id=slot['id']):
      match = GearItem.objects.filter(id=slot['id'])[0]
      if match.nameDescription:
        attrs['name'] += ' (%s)' % match.nameDescription

    if 'weaponInfo' in slot:
      attrs['min'] = slot['weaponInfo']['damage']['exactMin']/2
      attrs['max'] = slot['weaponInfo']['damage']['exactMax']/2
      attrs['speed'] = slot['weaponInfo']['weaponSpeed']
    return attrs

  armory = {'slots':{'head':build_item(data['items'].get('head')),
            'neck':build_item(data['items'].get('neck')),
            'shoulders':build_item(data['items'].get('shoulder')),
            'chest':build_item(data['items'].get('chest')),
            'back':build_item(data['items'].get('back')),
            'wrists':build_item(data['items'].get('wrist')),
            'hands':build_item(data['items'].get('hands')),
            'waist':build_item(data['items'].get('waist')),
            'legs':build_item(data['items'].get('legs')),
            'feet':build_item(data['items'].get('feet')),
            'ring1':build_item(data['items'].get('finger1')),
            'ring2':build_item(data['items'].get('finger2')),
            'trinket1':build_item(data['items'].get('trinket1')),
            'trinket2':build_item(data['items'].get('trinket2')),
            'weapon':build_item(data['items'].get('mainHand'))},
            'spec':_spec,
            'talent4':talent4,
            'talent5':talent5,
            'talent6':talent6,
            'talent7':talent7,
            'race':race}
  return armory


def CalcView(request):
  data = {'stattable':[],
          'spelltable':[],
          'proc_info':[]}
  totals = None
  aoetotals = None
  single = []
  minw = maxw = speedw = 0

  # the basics, if no request
  meta = HunterModelForm()
  bmo = BMOptionsForm()
  svo = SVOptionsForm()
  mmo = MMOptionsForm()
  aeo = AOEOptionsForm()

  if request.method == 'POST':
    # we don't know which form was submitted
    if 'region' in request.POST:
      armory_form = ArmoryModelForm(request.POST)
      gear = GearEquipModelForm()
    else:
      armory_form = ArmoryModelForm()
      gear = GearEquipModelForm(request.POST)
  else:
    gear = GearEquipModelForm()
    armory_form = ArmoryModelForm()
  slots = []

  for s in SLOTS:
    slots.append({'id':s,
                  'name':s[0].upper()+s[1:]+':',
                  'form':gear[s],
                  'socket':gear[s+'_socket'],
                  'warforged':gear[s+'_warforged'],
                  'difficulty':gear[s+'_difficulty']})

  equipped = []
  minw = maxw = 0
  speedw = 3
  title = ''

  notfound = ''
  if armory_form.data:
    armory = process_armory(armory_form.data)
    if not armory:
      notfound = '/'.join([armory_form.data['region'],armory_form.data['server'],armory_form.data['character']])
    else:
      metastring = 'race=%d&spec=%d&talent4=%d&talent5=%d&talent6=%d&talent7=%d' % (armory['race'],
                                                                                    armory['spec'],
                                                                                    armory['talent4'],
                                                                                    armory['talent5'],
                                                                                    armory['talent6'],
                                                                                    armory['talent7'])
      meta = HunterModelForm(QueryDict(metastring))

      for slot,attrs in armory['slots'].items():
        if slot == 'weapon':
          minw = attrs.get('min',0)
          maxw = attrs.get('max',0)
          speedw = attrs.get('speed',3)
        warforged = False
        if attrs.get('bonuses') and attrs['bonuses'] and 499 in attrs['bonuses']:
          warforged = True
        equipped.append({'id':attrs.get('id') or '(Not equipped - %s)' % slot,
                      'agility':attrs.get('agility',0),
                      'crit':attrs.get('crit',0),
                      'haste':attrs.get('haste',0),
                      'mastery':attrs.get('mastery',0),
                      'minw':minw,
                      'maxw':maxw,
                      'speedw':speedw,
                      'multistrike':attrs.get('multistrike',0),
                      'versatility':attrs.get('versatility',0),
                      'icon':attrs.get('icon','inv_misc_questionmark'),
                      'name':attrs.get('name') or '(Not equipped)',
                      'socket':attrs.get('socket'),
                      'context':attrs.get('context'),
                      'warforged':warforged,
                      'slot':slot,
                      'ilvl':attrs.get('ilvl',0),
          })
  elif request.method == 'POST':
    #gear_table_ids = [str(i) for i in GearItem.objects.all().values_list('id',flat=True)]
    for slot in SLOTS: # if custom gear was imported, we need to handle it
      #if gear.data[slot] not in gear_table_ids:
        equipped.append({'id':gear.data[slot],
                    'agility':gear.data['agility[%d]' % (SLOTS.index(slot)+1)],
                    'crit':gear.data['crit[%d]' % (SLOTS.index(slot)+1)],
                    'haste':gear.data['haste[%d]' % (SLOTS.index(slot)+1)],
                    'mastery':gear.data['mastery[%d]' % (SLOTS.index(slot)+1)],
                    'minw':gear.data['weapon_min'],
                    'maxw':gear.data['weapon_max'],
                    'speedw':gear.data['weapon_speed'],
                    'multistrike':gear.data['multistrike[%d]' % (SLOTS.index(slot)+1)],
                    'versatility':gear.data['versatility[%d]' % (SLOTS.index(slot)+1)],
                    'context':gear.data[slot+'_difficulty'],
                    'icon':'inv_misc_questionmark',
                    'name':'(armory import - %s)' % slot,
                    'slot':slot,
                    'ilvl':0,
        })
    gear = processEquippedGear(gear.data)
    meta = HunterModelForm(request.POST)
    bmo = BMOptionsForm(request.POST)
    svo = SVOptionsForm(request.POST)
    mmo = MMOptionsForm(request.POST)
    aeo = AOEOptionsForm(request.POST)

    #meta,hunter,spelltable,stattable,proc_info,options =
    data = process_form_data(gear,meta,bmo,svo,mmo,aeo)
    single,dummy,totals = dps.runner(data['hunter'],data['options'],lastcalc=float(request.POST.get('lastcalc') or 0))
    aoe,dummy,aoetotals = dps.runner(data['hunter'],data['options'],aoe=True)

  return render(request, 'hunter/calc.html',
                {'slots': slots,
                 'notfound':notfound,
                 'armory_form': armory_form,
                 'bmo': bmo,
                 'mmo': mmo,
                 'svo': svo,
                 'aeo': aeo,
                 'gear':gear,
                 'stattable': grouper(data['stattable']),
                 'spelltable': grouper(data['spelltable']),
                 'proc_info': data['proc_info'],
                 'meta':meta,
                 'totals':totals,
                 'aoetotals':aoetotals,
                 'minw': minw,
                 'maxw': maxw,
                 'speedw': speedw,
                 'title': title,
                 'equipped': json.dumps(equipped)})