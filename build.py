#!/usr/bin/env python3
"""Katz家(12/21)向け 到着日コース選択ページ。 python3 build.py -> index.html"""
import json, html

C = json.load(open('commons.json'))
def pick(k, i):
    x = C[k][i]; return x['thumb'], x['t'].replace('File:', ''), x['lic']
P = {'sensoji':pick('sensoji',0),'cruise':pick('cruise',1),'hama':pick('hamarikyu',0),
     'teamlab':pick('teamlab',0),'toyosu':pick('toyosu',0),'yokocho':pick('toyosu',3),
     'meiji':pick('meiji',1),'takeshita':pick('takeshita2',1),'shibuya':pick('shibuya',2)}
gm = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + q.replace(' ', '+')
emb = lambda q: 'https://maps.google.com/maps?q=' + q.replace(' ', '+') + '&output=embed&z=12'
def route_emb(stops):
    s = [x.replace(' ', '+') for x in stops]
    return 'https://maps.google.com/maps?saddr=' + s[0] + '&daddr=' + '+to:'.join(s[1:]) + '&output=embed'
def route_link(stops):
    s = [x.replace(' ', '+') for x in stops]
    return ('https://www.google.com/maps/dir/?api=1&origin=' + s[0] + '&destination=' + s[-1]
            + ('&waypoints=' + '%7C'.join(s[1:-1]) if len(s) > 2 else '') + '&travelmode=transit')

COURSES = [
 dict(id='A', name='Asakusa & the river', tag='Sit down and see Tokyo',
  photos=['sensoji','cruise','hama'],
  why='The lowest-walking option. Half of the tour is spent sitting on a boat, so a jet-lagged family can still enjoy it.',
  steps=[('9:00','Leave the hotel','Taxi or train to Asakusa while the streets are still quiet. About 30 minutes from central Tokyo.'),
         ('9:20','Senso-ji temple and Nakamise street','Tokyo&rsquo;s oldest temple. Photos at the big red lantern, incense smoke, first snacks of the trip. The pier is a 5-minute walk from the temple.'),
         ('10:40','Sumida river cruise, about 40 minutes','Everyone sits. Bridges, the skyline, Tokyo Skytree behind you. Kids can nap.'),
         ('11:30','Hama-rikyu gardens','A short, flat walk in a 400-year-old garden. Tea house on the pond if energy allows.'),
         ('12:30','Lunch','See the three picks below. Tsukiji is a 10-minute walk from the garden gate.'),
         ('14:00','Back at the hotel','Nap time.')],
  stops=['Asakusa Station Tokyo','Sensoji Temple','Asakusa Pier Tokyo Cruise','Hamarikyu Gardens','Tsukiji Outer Market'],
  moves='Hotel → Asakusa about 30 min by train. Temple → pier 5 min on foot. Boat 40 min. Garden → Tsukiji 10 min on foot. Tsukiji → hotel about 20 min.',
  food=[('Daikokuya Tempura','Asakusa · tendon since 1887','A bowl of tempura over rice in a wooden old-town building. Fast, filling, no menu anxiety.','Daikokuya Tempura Asakusa'),
        ('Asakusa Imahan Kokusai-dori','Asakusa · sukiyaki','Beef cooked at your table in a private tatami room. The splurge option, and a calm place for five people.','Asakusa Imahan Kokusaidori Honten'),
        ('Tsukiji Outer Market','Tsukiji · street food','Ten minutes from the garden. Grilled scallops, tamagoyaki, strawberry daifuku. Everyone picks their own.','Tsukiji Outer Market')],
  good='Little walking. Works at any energy level. Great photos.',
  mind='December river wind is cold, so bring layers. Boat times for Dec 21 to be confirmed.',
  links=[('Senso-ji (official)','https://www.senso-ji.jp/english/'),('Tokyo Cruise (official)','https://www.suijobus.co.jp/en/'),('Hama-rikyu gardens','https://www.tokyo-park.or.jp/teien/en/hama-rikyu/')]),
 dict(id='B', name='teamLab Planets & Toyosu', tag='Indoor wow, one place only',
  photos=['teamlab','toyosu','yokocho'],
  why='One venue for the whole morning, then lunch next door. Nothing depends on the weather, and the water rooms wake everyone up.',
  steps=[('9:00','Leave the hotel','Train or taxi to Toyosu. About 25 minutes from central Tokyo.'),
         ('9:30','teamLab Planets, about 2 hours','Barefoot digital art museum. You walk through water and light, and the rooms react to you.'),
         ('11:45','Toyosu Senkyaku Banrai','Edo-style food street beside the fish market. A 10-minute walk from the museum.'),
         ('13:00','Free time or an early return','There is a rooftop hot-spring footbath in the same building.'),
         ('14:00','Back at the hotel','Nap time.')],
  stops=['Toyosu Station Tokyo','teamLab Planets TOKYO','Toyosu Senkyaku Banrai'],
  moves='Hotel → Shin-Toyosu about 25 min by train. Station → museum 1 min on foot. Museum → food street 10 min on foot. Toyosu → hotel about 25 min.',
  food=[('Sushi Dai','Toyosu Market · sushi','The market&rsquo;s most famous sushi counter. Worth it, but the queue is long, so we go straight there or skip it.','Sushi Dai Toyosu Market'),
        ('Daiwa Sushi','Toyosu Market · sushi','The other market classic, usually a shorter wait than Sushi Dai. Chef-picked sets.','Daiwa Sushi Toyosu Market'),
        ('Mekiki Yokocho, Senkyaku Banrai','Toyosu · food street','Twenty small shops under one roof: rice bowls, grilled seafood, wagyu skewers, ice cream. Easiest with five people and different appetites.','Toyosu Senkyaku Banrai Mekiki Yokocho')],
  good='Weatherproof. Only two moves all morning. The single most memorable spot for kids.',
  mind='December tickets sell out, so we book early. You get wet up to the knees, and shorts are provided. Bright immersive rooms can be a lot for a very tired child.',
  links=[('teamLab Planets (official)','https://www.teamlab.art/e/planets/'),('Toyosu Senkyaku Banrai (official)','https://toyosu-senkyakubanrai.jp/')]),
 dict(id='C', name='Meiji shrine, Harajuku & Shibuya', tag='Morning light to reset jet lag',
  photos=['meiji','takeshita','shibuya'],
  why='Daylight is the fastest jet-lag fix. A quiet forest walk first, then the colourful side of Tokyo once the family is properly awake.',
  steps=[('9:00','Leave the hotel','Train or taxi to Harajuku. About 20 minutes from central Tokyo.'),
         ('9:20','Meiji Jingu shrine','A flat walk through a forest in the middle of the city, benches along the way. Sunday mornings are calm.'),
         ('10:30','Takeshita street','Harajuku&rsquo;s teen street opens up. Crepes, character shops, photo booths.'),
         ('12:00','Lunch on Omotesando','Sit-down lunch away from the crowd, 10 minutes on foot.'),
         ('13:00','Shibuya scramble crossing','Cross it once, watch it from above, then head back.'),
         ('14:00','Back at the hotel','Nap time.')],
  stops=['Harajuku Station Tokyo','Meiji Jingu Shrine','Takeshita Street Harajuku','Omotesando Tokyo','Shibuya Scramble Crossing'],
  moves='Hotel → Harajuku about 20 min by train. Shrine walk 10 min each way. Harajuku → Omotesando 10 min on foot. Omotesando → Shibuya 12 min on foot. Shibuya → hotel about 20 min.',
  food=[('Marion Crepes','Takeshita street · crepes','The stand that started the Harajuku crepe. Thirty fillings on the photo menu, eaten while walking.','Marion Crepes Takeshita Street Harajuku'),
        ('Maisen Aoyama','Omotesando · tonkatsu','Breaded pork cutlet in a converted bathhouse. Sit-down, quiet, and easy for children.','Maisen Aoyama Honten'),
        ('Uobei Shibuya Dogenzaka','Shibuya · conveyor sushi','You order on a tablet and the plates fly to your seat on a rail. Cheap, fast, and kids ask to go back.','Uobei Shibuya Dogenzaka')],
  good='No tickets needed. Easy to shorten if anyone fades. Best course for jet lag.',
  mind='Sunday Harajuku gets crowded after 11:00. A bit more walking than course A.',
  links=[('Meiji Jingu (official)','https://www.meijijingu.or.jp/en/'),('Takeshita street','https://www.google.com/maps/search/?api=1&query=Takeshita+Street+Harajuku'),('Shibuya crossing','https://www.google.com/maps/search/?api=1&query=Shibuya+Scramble+Crossing')]),
]

def card(c):
    ph = ''.join(f'<img src="{P[k][0]}" alt="{html.escape(P[k][1])}" loading="lazy">' for k in c['photos'])
    st = ''.join(f'<li><b>{t}</b><div><strong>{h}</strong><span>{d}</span></div></li>' for t, h, d in c['steps'])
    fd = ''.join(f'<a class="eat" href="{gm(q)}" target="_blank" rel="noopener"><strong>{n}</strong>'
                 f'<em>{a}</em><span>{d}</span><i>Open in Google Maps ↗</i></a>' for n, a, d, q in c['food'])
    ln = ' '.join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(t)} ↗</a>' for t, u in c['links'])
    sub = f'Dec 21 tour: we choose course {c["id"]} ({c["name"]})'
    return f'''<section class="course" id="course-{c['id']}">
<div class="photos">{ph}</div>
<div class="body">
<p class="kicker">Course {c['id']} · {html.escape(c['tag'])}</p>
<h2>{html.escape(c['name'])}</h2>
<p class="why">{html.escape(c['why'])}</p>
<ol class="steps">{st}</ol>
<h3>The route</h3>
<div class="mapbox"><iframe src="{route_emb(c['stops'])}" loading="lazy" title="Route for course {c['id']}" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<p class="moves">{c['moves']} <a href="{route_link(c['stops'])}" target="_blank" rel="noopener">Open the route in Google Maps ↗</a></p>
<h3>Where we eat</h3>
<div class="eats">{fd}</div>
<div class="notes"><p><b>Good for</b> {html.escape(c['good'])}</p><p><b>Keep in mind</b> {html.escape(c['mind'])}</p></div>
<p class="links">{ln}</p>
<a class="choose" href="mailto:icchan417@gmail.com?subject={html.escape(sub)}">Choose course {c['id']}</a>
</div></section>'''

credits = '; '.join(f'{html.escape(v[1])} ({v[2]})' for v in P.values())
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tokyo, arrival day: three courses for the Katz family</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{{--ink:#1a1a1a;--mute:#6b6b6b;--line:#e6e6e6;--acc:#d3382c;--bg:#fff}}
*{{box-sizing:border-box;min-width:0}} html,body{{overflow-x:hidden;max-width:100%}} img{{max-width:100%}}
body{{margin:0;font-family:Inter,-apple-system,"Hiragino Sans",sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 20px}}
header{{padding:56px 0 28px;border-bottom:1px solid var(--line)}}
header .kicker{{font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--acc);margin:0 0 10px}}
h1{{font-size:clamp(28px,4.5vw,44px);line-height:1.15;margin:0 0 14px;font-weight:800;letter-spacing:-.01em}}
header p{{font-size:17px;color:var(--mute);margin:0;max-width:720px}}
.facts{{display:flex;flex-wrap:wrap;gap:8px 22px;margin:20px 0 0;padding:0;list-style:none;font-size:14px;color:var(--mute)}} .facts b{{color:var(--ink);font-weight:600}}
h3{{font-size:15px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--mute);margin:28px 0 12px}}
.arrival{{padding:32px 0;border-bottom:1px solid var(--line)}}
.arrival .grid{{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}}
.arrival p{{margin:0 0 12px;font-size:16px}} .arrival .hint{{color:var(--mute);font-size:15px}}
.mapbox{{position:relative;border-radius:10px;overflow:hidden;border:1px solid var(--line);background:#f1f1f1}}
.mapbox iframe{{display:block;width:100%;height:300px;border:0}}
.course{{padding:40px 0;border-bottom:1px solid var(--line)}}
.photos{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-bottom:22px;width:100%}}
.photos img{{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:10px;background:#f1f1f1}}
.kicker{{font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--acc);margin:0 0 6px}}
h2{{font-size:28px;margin:0 0 8px;font-weight:800;letter-spacing:-.01em}}
.why{{font-size:17px;margin:0 0 20px;max-width:720px}}
.steps{{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}}
.steps li{{display:grid;grid-template-columns:64px minmax(0,1fr);gap:12px;padding:12px 0;border-bottom:1px solid var(--line)}}
.steps b{{font-variant-numeric:tabular-nums;color:var(--acc)}} .steps strong{{display:block;font-weight:600}} .steps span{{color:var(--mute);font-size:15px}}
.moves{{font-size:15px;color:var(--mute);margin:10px 0 0}} .moves a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px;white-space:nowrap}}
.eats{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}
.eat{{display:block;text-decoration:none;color:inherit;border:1px solid var(--line);border-radius:10px;padding:16px 18px;transition:border-color .15s}}
.eat:hover{{border-color:var(--ink)}} .eat strong{{display:block;font-weight:600;font-size:17px}}
.eat em{{display:block;font-style:normal;font-size:13px;color:var(--acc);font-weight:600;margin:2px 0 8px}}
.eat span{{display:block;font-size:15px;color:var(--mute)}} .eat i{{display:block;font-style:normal;font-size:13px;margin-top:10px;text-decoration:underline;text-underline-offset:3px}}
.notes{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:28px 0 18px;font-size:15px}} .notes p{{margin:0;padding:14px 16px;background:#f7f7f5;border-radius:10px}} .notes b{{display:block;font-weight:600;margin-bottom:2px}}
.links{{margin:0 0 20px;font-size:15px;display:flex;flex-wrap:wrap;gap:6px 18px}} .links a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px}}
.choose{{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;font-weight:600;padding:14px 26px;border-radius:999px;font-size:16px}} .choose:hover{{background:#b52f25}}
footer{{padding:32px 0 60px;font-size:13px;color:var(--mute)}} footer p{{margin:0 0 6px}}
@media(max-width:700px){{
 header{{padding:36px 0 22px}} .arrival .grid{{grid-template-columns:1fr}}
 .photos{{grid-template-columns:1fr 1fr}} .photos img:first-child{{grid-column:span 2;aspect-ratio:16/9}}
 .eats{{grid-template-columns:1fr}} .notes{{grid-template-columns:1fr}} .mapbox iframe{{height:240px}}
}}
</style></head><body>
<header><div class="wrap">
<p class="kicker">Tokyo · Sunday, December 21</p>
<h1>Arrival day, done gently.<br>Three courses, pick one.</h1>
<p>You land at Haneda at 5:10 in the morning. Each course starts at your hotel at 9:00 and has you back by 14:00 for a nap. Little walking, plenty of sitting, good food, and one thing worth remembering.</p>
<ul class="facts"><li><b>Guide</b> Yuuki</li><li><b>Time</b> 9:00–14:00</li><li><b>Group</b> family of five</li><li><b>Start and end</b> your hotel</li></ul>
</div></header>
<section class="arrival"><div class="wrap">
<h3 style="margin-top:0">From the airport</h3>
<div class="grid">
<div>
<p>Haneda sits south of the city, about 30 to 45 minutes from central Tokyo by train or taxi. All three courses stay inside the ring shown on the map, so nothing is far from your hotel.</p>
<p class="hint">Tell me the hotel name and I will pin it here, with the exact door-to-door times for the course you choose. If one room is ready early, you can drop the bags and start light.</p>
</div>
<div class="mapbox"><iframe src="{emb('Haneda Airport Tokyo')}" loading="lazy" title="Haneda airport and central Tokyo" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></div></section>
<main class="wrap">{''.join(card(c) for c in COURSES)}</main>
<footer class="wrap"><p>Reply to Tree or Yuuki with A, B or C. Times are approximate and can move earlier or later on the day.</p><p>Photos: {credits}, via Wikimedia Commons.</p></footer>
<script src="devbar.js"></script></body></html>'''
open('index.html', 'w').write(page)
print('written', len(page))
