# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gearitem', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AOEOptionsModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opt_aoe1', models.IntegerField(default=8, max_length=2, verbose_name=b'Targets')),
                ('opt_aoe2', models.BooleanField(default=True, verbose_name=b'Cast main nukes')),
                ('opt_aoe3', models.IntegerField(default=0, max_length=3, verbose_name=b'Min focus to cast main nukes')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArmoryModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region', models.CharField(default=b'us', max_length=30, choices=[(b'eu', b'EU'), (b'us', b'US')])),
                ('server', models.CharField(default=b'whisperwind', max_length=30, choices=[('aegwynn', 'Aegwynn'), ('aerie-peak', 'Aerie Peak'), ('agamaggan', 'Agamaggan'), ('aggramar', 'Aggramar'), ('akama', 'Akama'), ('alexstrasza', 'Alexstrasza'), ('alleria', 'Alleria'), ('altar-of-storms', 'Altar of Storms'), ('alterac-mountains', 'Alterac Mountains'), ('amanthul', "Aman'Thul"), ('andorhal', 'Andorhal'), ('anetheron', 'Anetheron'), ('antonidas', 'Antonidas'), ('anubarak', "Anub'arak"), ('anvilmar', 'Anvilmar'), ('arathor', 'Arathor'), ('archimonde', 'Archimonde'), ('area-52', 'Area 52'), ('argent-dawn', 'Argent Dawn'), ('arthas', 'Arthas'), ('arygos', 'Arygos'), ('auchindoun', 'Auchindoun'), ('azgalor', 'Azgalor'), ('azjolnerub', 'Azjol-Nerub'), ('azralon', 'Azralon'), ('azshara', 'Azshara'), ('azuremyst', 'Azuremyst'), ('baelgun', 'Baelgun'), ('balnazzar', 'Balnazzar'), ('barthilas', 'Barthilas'), ('black-dragonflight', 'Black Dragonflight'), ('blackhand', 'Blackhand'), ('blackrock', 'Blackrock'), ('blackwater-raiders', 'Blackwater Raiders'), ('blackwing-lair', 'Blackwing Lair'), ('blades-edge', "Blade's Edge"), ('bladefist', 'Bladefist'), ('bleeding-hollow', 'Bleeding Hollow'), ('blood-furnace', 'Blood Furnace'), ('bloodhoof', 'Bloodhoof'), ('bloodscalp', 'Bloodscalp'), ('bonechewer', 'Bonechewer'), ('borean-tundra', 'Borean Tundra'), ('boulderfist', 'Boulderfist'), ('bronzebeard', 'Bronzebeard'), ('burning-blade', 'Burning Blade'), ('burning-legion', 'Burning Legion'), ('caelestrasz', 'Caelestrasz'), ('cairne', 'Cairne'), ('cenarion-circle', 'Cenarion Circle'), ('cenarius', 'Cenarius'), ('chogall', "Cho'gall"), ('chromaggus', 'Chromaggus'), ('coilfang', 'Coilfang'), ('crushridge', 'Crushridge'), ('daggerspine', 'Daggerspine'), ('dalaran', 'Dalaran'), ('dalvengyr', 'Dalvengyr'), ('dark-iron', 'Dark Iron'), ('darkspear', 'Darkspear'), ('darrowmere', 'Darrowmere'), ('dathremar', "Dath'Remar"), ('dawnbringer', 'Dawnbringer'), ('deathwing', 'Deathwing'), ('demon-soul', 'Demon Soul'), ('dentarg', 'Dentarg'), ('destromath', 'Destromath'), ('dethecus', 'Dethecus'), ('detheroc', 'Detheroc'), ('doomhammer', 'Doomhammer'), ('draenor', 'Draenor'), ('dragonblight', 'Dragonblight'), ('dragonmaw', 'Dragonmaw'), ('draktharon', "Drak'Tharon"), ('drakthul', "Drak'thul"), ('draka', 'Draka'), ('drakkari', 'Drakkari'), ('dreadmaul', 'Dreadmaul'), ('drenden', 'Drenden'), ('dunemaul', 'Dunemaul'), ('durotan', 'Durotan'), ('duskwood', 'Duskwood'), ('earthen-ring', 'Earthen Ring'), ('echo-isles', 'Echo Isles'), ('eitrigg', 'Eitrigg'), ('eldrethalas', "Eldre'Thalas"), ('elune', 'Elune'), ('emerald-dream', 'Emerald Dream'), ('eonar', 'Eonar'), ('eredar', 'Eredar'), ('executus', 'Executus'), ('exodar', 'Exodar'), ('farstriders', 'Farstriders'), ('feathermoon', 'Feathermoon'), ('fenris', 'Fenris'), ('firetree', 'Firetree'), ('fizzcrank', 'Fizzcrank'), ('frostmane', 'Frostmane'), ('frostmourne', 'Frostmourne'), ('frostwolf', 'Frostwolf'), ('galakrond', 'Galakrond'), ('gallywix', 'Gallywix'), ('garithos', 'Garithos'), ('garona', 'Garona'), ('garrosh', 'Garrosh'), ('ghostlands', 'Ghostlands'), ('gilneas', 'Gilneas'), ('gnomeregan', 'Gnomeregan'), ('goldrinn', 'Goldrinn'), ('gorefiend', 'Gorefiend'), ('gorgonnash', 'Gorgonnash'), ('greymane', 'Greymane'), ('grizzly-hills', 'Grizzly Hills'), ('guldan', "Gul'dan"), ('gundrak', 'Gundrak'), ('gurubashi', 'Gurubashi'), ('hakkar', 'Hakkar'), ('haomarush', 'Haomarush'), ('hellscream', 'Hellscream'), ('hydraxis', 'Hydraxis'), ('hyjal', 'Hyjal'), ('icecrown', 'Icecrown'), ('illidan', 'Illidan'), ('jaedenar', 'Jaedenar'), ('jubeithos', "Jubei'Thos"), ('kaelthas', "Kael'thas"), ('kalecgos', 'Kalecgos'), ('kargath', 'Kargath'), ('kelthuzad', "Kel'Thuzad"), ('khadgar', 'Khadgar'), ('khaz-modan', 'Khaz Modan'), ('khazgoroth', "Khaz'goroth"), ('kiljaeden', "Kil'jaeden"), ('kilrogg', 'Kilrogg'), ('kirin-tor', 'Kirin Tor'), ('korgath', 'Korgath'), ('korialstrasz', 'Korialstrasz'), ('kul-tiras', 'Kul Tiras'), ('laughing-skull', 'Laughing Skull'), ('lethon', 'Lethon'), ('lightbringer', 'Lightbringer'), ('lightnings-blade', "Lightning's Blade"), ('lightninghoof', 'Lightninghoof'), ('llane', 'Llane'), ('lothar', 'Lothar'), ('madoran', 'Madoran'), ('maelstrom', 'Maelstrom'), ('magtheridon', 'Magtheridon'), ('maiev', 'Maiev'), ('malganis', "Mal'Ganis"), ('malfurion', 'Malfurion'), ('malorne', 'Malorne'), ('malygos', 'Malygos'), ('mannoroth', 'Mannoroth'), ('medivh', 'Medivh'), ('misha', 'Misha'), ('moknathal', "Mok'Nathal"), ('moon-guard', 'Moon Guard'), ('moonrunner', 'Moonrunner'), ('mugthol', "Mug'thol"), ('muradin', 'Muradin'), ('nagrand', 'Nagrand'), ('nathrezim', 'Nathrezim'), ('nazgrel', 'Nazgrel'), ('nazjatar', 'Nazjatar'), ('nemesis', 'Nemesis'), ('nerzhul', "Ner'zhul"), ('nesingwary', 'Nesingwary'), ('nordrassil', 'Nordrassil'), ('norgannon', 'Norgannon'), ('onyxia', 'Onyxia'), ('perenolde', 'Perenolde'), ('proudmoore', 'Proudmoore'), ('quelthalas', "Quel'Thalas"), ('queldorei', "Quel'dorei"), ('ragnaros', 'Ragnaros'), ('ravencrest', 'Ravencrest'), ('ravenholdt', 'Ravenholdt'), ('rexxar', 'Rexxar'), ('rivendare', 'Rivendare'), ('runetotem', 'Runetotem'), ('sargeras', 'Sargeras'), ('saurfang', 'Saurfang'), ('scarlet-crusade', 'Scarlet Crusade'), ('scilla', 'Scilla'), ('senjin', "Sen'jin"), ('sentinels', 'Sentinels'), ('shadow-council', 'Shadow Council'), ('shadowmoon', 'Shadowmoon'), ('shadowsong', 'Shadowsong'), ('shandris', 'Shandris'), ('shattered-halls', 'Shattered Halls'), ('shattered-hand', 'Shattered Hand'), ('shuhalo', "Shu'halo"), ('silver-hand', 'Silver Hand'), ('silvermoon', 'Silvermoon'), ('sisters-of-elune', 'Sisters of Elune'), ('skullcrusher', 'Skullcrusher'), ('skywall', 'Skywall'), ('smolderthorn', 'Smolderthorn'), ('spinebreaker', 'Spinebreaker'), ('spirestone', 'Spirestone'), ('staghelm', 'Staghelm'), ('steamwheedle-cartel', 'Steamwheedle Cartel'), ('stonemaul', 'Stonemaul'), ('stormrage', 'Stormrage'), ('stormreaver', 'Stormreaver'), ('stormscale', 'Stormscale'), ('suramar', 'Suramar'), ('tanaris', 'Tanaris'), ('terenas', 'Terenas'), ('terokkar', 'Terokkar'), ('thaurissan', 'Thaurissan'), ('the-forgotten-coast', 'The Forgotten Coast'), ('the-scryers', 'The Scryers'), ('the-underbog', 'The Underbog'), ('the-venture-co', 'The Venture Co'), ('thorium-brotherhood', 'Thorium Brotherhood'), ('thrall', 'Thrall'), ('thunderhorn', 'Thunderhorn'), ('thunderlord', 'Thunderlord'), ('tichondrius', 'Tichondrius'), ('tol-barad', 'Tol Barad'), ('tortheldrin', 'Tortheldrin'), ('trollbane', 'Trollbane'), ('turalyon', 'Turalyon'), ('twisting-nether', 'Twisting Nether'), ('uldaman', 'Uldaman'), ('uldum', 'Uldum'), ('undermine', 'Undermine'), ('ursin', 'Ursin'), ('uther', 'Uther'), ('vashj', 'Vashj'), ('veknilash', "Vek'nilash"), ('velen', 'Velen'), ('warsong', 'Warsong'), ('whisperwind', 'Whisperwind'), ('wildhammer', 'Wildhammer'), ('windrunner', 'Windrunner'), ('winterhoof', 'Winterhoof'), ('wyrmrest-accord', 'Wyrmrest Accord'), ('ysera', 'Ysera'), ('ysondre', 'Ysondre'), ('zangarmarsh', 'Zangarmarsh'), ('zuljin', "Zul'jin"), ('zuluhed', 'Zuluhed'), ('aggra-portugues', 'Aggra (Portugu\xeas)'), ('ahnqiraj', "Ahn'Qiraj"), ('alakir', "Al'Akir"), ('alonsus', 'Alonsus'), ('ambossar', 'Ambossar'), ('anachronos', 'Anachronos'), ('arakarahm', 'Arak-arahm'), ('arathi', 'Arathi'), ('ashenvale', 'Ashenvale'), ('aszune', 'Aszune'), ('azuregos', 'Azuregos'), ('blackmoore', 'Blackmoore'), ('blackscar', 'Blackscar'), ('bloodfeather', 'Bloodfeather'), ('blutkessel', 'Blutkessel'), ('booty-bay', 'Booty Bay'), ('bronze-dragonflight', 'Bronze Dragonflight'), ('burning-steppes', 'Burning Steppes'), ('cthun', "C'Thun"), ('chamber-of-aspects', 'Chamber of Aspects'), ('chants-eternels', 'Chants \xe9ternels'), ('colinas-pardas', 'Colinas Pardas'), ('confrerie-du-thorium', 'Confr\xe9rie du Thorium'), ('conseil-des-ombres', 'Conseil des Ombres'), ('culte-de-la-rive-noire', 'Culte de la Rive noire'), ('darkmoon-faire', 'Darkmoon Faire'), ('darksorrow', 'Darksorrow'), ('das-konsortium', 'Das Konsortium'), ('das-syndikat', 'Das Syndikat'), ('deathguard', 'Deathguard'), ('deathweaver', 'Deathweaver'), ('deepholm', 'Deepholm'), ('defias-brotherhood', 'Defias Brotherhood'), ('der-mithrilorden', 'Der Mithrilorden'), ('der-rat-von-dalaran', 'Der Rat von Dalaran'), ('der-abyssische-rat', 'Der abyssische Rat'), ('die-aldor', 'Die Aldor'), ('die-arguswacht', 'Die Arguswacht'), ('die-nachtwache', 'Die Nachtwache'), ('die-silberne-hand', 'Die Silberne Hand'), ('die-todeskrallen', 'Die Todeskrallen'), ('die-ewige-wacht', 'Die ewige Wacht'), ('drekthar', "Drek'Thar"), ('dun-modr', 'Dun Modr'), ('dun-morogh', 'Dun Morogh'), ('echsenkessel', 'Echsenkessel'), ('emeriss', 'Emeriss'), ('eversong', 'Eversong'), ('festung-der-sturme', 'Festung der St\xfcrme'), ('fordragon', 'Fordragon'), ('forscherliga', 'Forscherliga'), ('frostwhisper', 'Frostwhisper'), ('genjuros', 'Genjuros'), ('gordunni', 'Gordunni'), ('grim-batol', 'Grim Batol'), ('grom', 'Grom'), ('hellfire', 'Hellfire'), ('howling-fjord', 'Howling Fjord'), ('karazhan', 'Karazhan'), ('kazzak', 'Kazzak'), ('korgall', "Kor'gall"), ('kragjin', "Krag'jin"), ('krasus', 'Krasus'), ('kult-der-verdammten', 'Kult der Verdammten'), ('la-croisade-ecarlate', 'La Croisade \xe9carlate'), ('les-clairvoyants', 'Les Clairvoyants'), ('les-sentinelles', 'Les Sentinelles'), ('lich-king', 'Lich King'), ('lordaeron', 'Lordaeron'), ('los-errantes', 'Los Errantes'), ('madmortem', 'Madmortem'), ('marecage-de-zangar', 'Mar\xe9cage de Zangar'), ('mazrigos', 'Mazrigos'), ('minahonda', 'Minahonda'), ('moonglade', 'Moonglade'), ('naxxramas', 'Naxxramas'), ('nefarian', 'Nefarian'), ('neptulon', 'Neptulon'), ('nerathor', "Nera'thor"), ('nethersturm', 'Nethersturm'), ('nozdormu', 'Nozdormu'), ('outland', 'Outland'), ('pozzo-delleternita', "Pozzo dell'Eternit\xe0"), ('rajaxx', 'Rajaxx'), ('rashgarroth', 'Rashgarroth'), ('razuvious', 'Razuvious'), ('sanguino', 'Sanguino'), ('scarshield-legion', 'Scarshield Legion'), ('shattrath', 'Shattrath'), ('shendralar', "Shen'dralar"), ('sinstralis', 'Sinstralis'), ('soulflayer', 'Soulflayer'), ('sporeggar', 'Sporeggar'), ('sunstrider', 'Sunstrider'), ('sylvanas', 'Sylvanas'), ('taerar', 'Taerar'), ('talnivarr', 'Talnivarr'), ('tarren-mill', 'Tarren Mill'), ('teldrassil', 'Teldrassil'), ('temple-noir', 'Temple noir'), ('terrordar', 'Terrordar'), ('the-maelstrom', 'The Maelstrom'), ('the-shatar', "The Sha'tar"), ('theradras', 'Theradras'), ('thermaplugg', 'Thermaplugg'), ('throkferoth', "Throk'Feroth"), ('tirion', 'Tirion'), ('todeswache', 'Todeswache'), ('twilights-hammer', "Twilight's Hammer"), ('tyrande', 'Tyrande'), ('ulduar', 'Ulduar'), ('ungoro', "Un'Goro"), ('varimathras', 'Varimathras'), ('veklor', "Vek'lor"), ('voljin', "Vol'jin"), ('wrathbringer', 'Wrathbringer'), ('xavius', 'Xavius'), ('zenedar', 'Zenedar'), ('zirkel-des-cenarius', 'Zirkel des Cenarius')])),
                ('character', models.CharField(max_length=30)),
                ('spec', models.BooleanField(default=True, verbose_name=b'Use first spec')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BMOptionsModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opt_bm3', models.BooleanField(default=True, verbose_name=b'Hold Bestial Wrath until KC is ready')),
                ('opt_bm4', models.BooleanField(default=False, verbose_name=b'Do not cast Dire Beast during Bestial Wrath')),
                ('opt_bm5', models.BooleanField(default=True, verbose_name=b'Do not cast Focus Fire during Bestial Wrath')),
                ('opt_bm6', models.BooleanField(default=True, verbose_name=b'Cast Focus Fire just before Bestial Wrath')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GearEquipModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weapon_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('weapon_warforged', models.BooleanField(default=False)),
                ('head_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('head_warforged', models.BooleanField(default=False)),
                ('neck_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('neck_warforged', models.BooleanField(default=False)),
                ('shoulders_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('shoulders_warforged', models.BooleanField(default=False)),
                ('back_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('back_warforged', models.BooleanField(default=False)),
                ('chest_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('chest_warforged', models.BooleanField(default=False)),
                ('wrists_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('wrists_warforged', models.BooleanField(default=False)),
                ('hands_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('hands_warforged', models.BooleanField(default=False)),
                ('waist_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('waist_warforged', models.BooleanField(default=False)),
                ('legs_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('legs_warforged', models.BooleanField(default=False)),
                ('feet_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('feet_warforged', models.BooleanField(default=False)),
                ('ring1_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('ring1_warforged', models.BooleanField(default=False)),
                ('ring2_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('ring2_warforged', models.BooleanField(default=False)),
                ('trinket1_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('trinket1_warforged', models.BooleanField(default=False)),
                ('trinket2_difficulty', models.CharField(default=b'', max_length=30, choices=[(b'normal', b'Normal/LFR'), (b'heroic', b'Heroic'), (b'mythic', b'Mythic')])),
                ('trinket2_warforged', models.BooleanField(default=False)),
                ('back', models.ForeignKey(related_name=b'gearequip_back', default=113657, to='gearitem.GearItem')),
                ('back_socket', models.ForeignKey(related_name=b'gearequip_back_gem', to='gearitem.Gem')),
                ('chest', models.ForeignKey(related_name=b'gearequip_chest', default=113654, to='gearitem.GearItem')),
                ('chest_socket', models.ForeignKey(related_name=b'gearequip_chest_gem', to='gearitem.Gem')),
                ('feet', models.ForeignKey(related_name=b'gearequip_feet', default=113849, to='gearitem.GearItem')),
                ('feet_socket', models.ForeignKey(related_name=b'gearequip_feet_gem', to='gearitem.Gem')),
                ('hands', models.ForeignKey(related_name=b'gearequip_hands', default=113593, to='gearitem.GearItem')),
                ('hands_socket', models.ForeignKey(related_name=b'gearequip_hands_gem', to='gearitem.Gem')),
                ('head', models.ForeignKey(related_name=b'gearequip_head', default=113863, to='gearitem.GearItem')),
                ('head_socket', models.ForeignKey(related_name=b'gearequip_head_gem', to='gearitem.Gem')),
                ('legs', models.ForeignKey(related_name=b'gearequip_legs', default=113839, to='gearitem.GearItem')),
                ('legs_socket', models.ForeignKey(related_name=b'gearequip_legs_gem', to='gearitem.Gem')),
                ('neck', models.ForeignKey(related_name=b'gearequip_neck', default=113851, to='gearitem.GearItem')),
                ('neck_socket', models.ForeignKey(related_name=b'gearequip_neck_gem', to='gearitem.Gem')),
                ('ring1', models.ForeignKey(related_name=b'gearequip_ring1', default=113611, to='gearitem.GearItem')),
                ('ring1_socket', models.ForeignKey(related_name=b'gearequip_ring1_gem', to='gearitem.Gem')),
                ('ring2', models.ForeignKey(related_name=b'gearequip_ring2', default=113843, to='gearitem.GearItem')),
                ('ring2_socket', models.ForeignKey(related_name=b'gearequip_ring2_gem', to='gearitem.Gem')),
                ('shoulders', models.ForeignKey(related_name=b'gearequip_shoulders', default=113641, to='gearitem.GearItem')),
                ('shoulders_socket', models.ForeignKey(related_name=b'gearequip_shoulders_gem', to='gearitem.Gem')),
                ('trinket1', models.ForeignKey(related_name=b'gearequip_trinket1', default=113853, to='gearitem.GearItem')),
                ('trinket1_socket', models.ForeignKey(related_name=b'gearequip_trinket1_gem', to='gearitem.Gem')),
                ('trinket2', models.ForeignKey(related_name=b'gearequip_trinket2', default=113612, to='gearitem.GearItem')),
                ('trinket2_socket', models.ForeignKey(related_name=b'gearequip_trinket2_gem', to='gearitem.Gem')),
                ('waist', models.ForeignKey(related_name=b'gearequip_waist', default=113827, to='gearitem.GearItem')),
                ('waist_socket', models.ForeignKey(related_name=b'gearequip_waist_gem', to='gearitem.Gem')),
                ('weapon', models.ForeignKey(related_name=b'gearequip_weapon', default=113652, to='gearitem.GearItem')),
                ('weapon_socket', models.ForeignKey(related_name=b'gearequip_weapon_gem', to='gearitem.Gem')),
                ('wrists', models.ForeignKey(related_name=b'gearequip_wrists', default=113826, to='gearitem.GearItem')),
                ('wrists_socket', models.ForeignKey(related_name=b'gearequip_wrists_gem', to='gearitem.Gem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HunterModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('race', models.IntegerField(default=4, max_length=20, choices=[(1, b'Human'), (3, b'Dwarf'), (4, b'Night Elf'), (7, b'Gnome'), (11, b'Draenei'), (22, b'Worgen'), (2, b'Orc'), (5, b'Undead'), (6, b'Tauren'), (8, b'Troll'), (9, b'Goblin'), (10, b'Blood Elf'), (24, b'Pandaren')])),
                ('spec', models.IntegerField(default=0, verbose_name=b'Specialization', choices=[(0, b'Beast Mastery'), (1, b'Marksmanship'), (2, b'Survival')])),
                ('talent4', models.IntegerField(default=(0, b'Steady Focus'), max_length=30, verbose_name=b'Talents - level 60', choices=[(0, b'Steady Focus'), (1, b'Dire Beast'), (2, b'Thrill of the Hunt')])),
                ('talent5', models.IntegerField(default=(0, b'A Murder of Crows'), max_length=30, verbose_name=b'Talents - level 75', choices=[(0, b'A Murder of Crows'), (1, b'Blink Strikes'), (2, b'Stampede')])),
                ('talent6', models.IntegerField(default=(0, b'Glaive Toss'), max_length=30, verbose_name=b'Talents - level 90', choices=[(0, b'Glaive Toss'), (1, b'Powershot'), (2, b'Barrage')])),
                ('talent7', models.IntegerField(default=(0, b'Exotic Munitions'), max_length=30, verbose_name=b'Talents - level 100', choices=[(0, b'Exotic Munitions'), (1, b'Focusing Shot'), (2, b'Versatility')])),
                ('enchants', models.CharField(default=b'spec', max_length=30, verbose_name=b'Enchant/Food stat', blank=True, choices=[(b'', b'(none)'), (b'crit', b'Critical Strike'), (b'haste', b'Haste'), (b'mastery', b'Mastery'), (b'multistrike', b'Multistrike'), (b'versatility', b'Versatility'), (b'spec', b'Use spec attunement')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MMOptionsModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opt_mm1', models.IntegerField(default=2, max_length=30, verbose_name=b'Careful Aim behavior', choices=[(0, b'Aimed Shot only'), (1, b'Aimed Shot and talents (no Chimaera)'), (2, b'No restrictions')])),
                ('opt_mm2', models.IntegerField(default=0, max_length=3, verbose_name=b'Aimed Shot - min focus (plus cost) to use')),
                ('opt_mm3', models.BooleanField(default=True, verbose_name=b'Only cast instant shots after Focusing Shot')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SVOptionsModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opt_sv2', models.BooleanField(default=True, verbose_name=b'Null action - place holder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
