from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.views import generic

from django.forms import ModelForm

from calcs.hunter import Hunter
from calcs.huntermeta import HunterMeta
from calcs.spells import do_spells

from models import HunterModel

class CalcModelForm(ModelForm):
    class Meta:
      model = HunterModel

def CalcView(request):
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
  else:
    form = CalcModelForm()

  return render(request, 'hunter/calc.html',
                {'form': form,
                 'spelltable': spelltable})