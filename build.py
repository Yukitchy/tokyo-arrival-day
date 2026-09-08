#!/usr/bin/env python3
"""Katz家(12/21)向け 到着日コース選択ページ。 python3 build.py -> index.html"""
import json, html

# 写真は「ワクワク採点」で選ぶ。建物の外観でなく、そこで人が楽しんでいる絵を最優先。
# 採点と選定理由は photos.json の score / note を見る。
PH = json.load(open('photos.json'))
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
 dict(id='A', chips=['Least walking','40 minutes on a boat','No tickets needed'], name='Asakusa & the river', tag='Sit down and see Tokyo',
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
 dict(id='B', chips=['Indoor, any weather','One place all morning','Tickets needed'], name='teamLab Planets & Toyosu', tag='Indoor wow, one place only',
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
  links=[('teamLab Planets (official)','https://www.teamlab.art/e/planets/'),('Watch the rooms in motion (teamLab official channel)','https://www.youtube.com/@teamLabART'),('Toyosu Senkyaku Banrai (official)','https://toyosu-senkyakubanrai.jp/')]),
 dict(id='C', chips=['Best for jet lag','Outdoors, no tickets','Most photogenic'], name='Meiji shrine, Harajuku & Shibuya', tag='Morning light to reset jet lag',
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

def menu(c):
    x = PH[c['id']]['card']
    ch = ''.join(f'<li>{html.escape(t)}</li>' for t in c['chips'])
    return f'''<button class="mcard" type="button" data-course="{c['id']}" aria-expanded="false" aria-controls="detail-{c['id']}">
<img src="{x["thumb"]}" alt="{html.escape(x["title"])}" loading="lazy">
<span class="mb"><span class="mk">Course {c['id']}</span><span class="mt">{html.escape(c['name'])}</span>
<span class="mtag">{html.escape(c['tag'])}</span><ul class="mch">{ch}</ul><span class="mopen">See the plan</span></span></button>'''

def detail(c):
    ph = ''.join(f'<img src="{x["thumb"]}" alt="{html.escape(x["title"])}" loading="lazy">' for x in PH[c['id']]['detail'])
    st = ''.join(f'<li><b>{t}</b><div><strong>{h}</strong><span>{d}</span></div></li>' for t, h, d in c['steps'])
    fd = ''.join(f'<a class="eat" href="{gm(q)}" target="_blank" rel="noopener">'
                 f'<img src="{im["thumb"]}" alt="{html.escape(im["title"])}" loading="lazy">'
                 f'<span class="eb"><strong>{n}</strong><em>{a}</em><span>{d}</span>'
                 f'<i>Open in Google Maps ↗</i></span></a>'
                 for (n, a, d, q), im in zip(c['food'], PH[c['id']]['food']))
    ln = ' '.join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(t)} ↗</a>' for t, u in c['links'])
    sub = f'Dec 21 tour: we choose course {c["id"]} ({c["name"]})'
    return f'''<section class="detail" id="detail-{c['id']}" hidden><div class="dwrap"><div class="dtop"></div>
<div class="dhead"><div><p class="kicker">Course {c['id']} · {html.escape(c['tag'])}</p><h2>{html.escape(c['name'])}</h2></div>
<button class="dclose" type="button" aria-label="Close">Close ✕</button></div>
<p class="why">{html.escape(c['why'])}</p>
<div class="photos">{ph}</div>
<div class="dgrid">
<div><h3>The day</h3><ol class="steps">{st}</ol></div>
<div><h3>The route</h3><div class="mapbox"><iframe src="{route_emb(c['stops'])}" loading="lazy" title="Route for course {c['id']}" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<p class="moves">{c['moves']} <a href="{route_link(c['stops'])}" target="_blank" rel="noopener">Open the route in Google Maps ↗</a></p></div>
</div>
<h3>Where we eat</h3><div class="eats">{fd}</div>
<div class="notes"><p><b>Good for</b> {html.escape(c['good'])}</p><p><b>Keep in mind</b> {html.escape(c['mind'])}</p></div>
<p class="links">{ln}</p>
<a class="choose" href="mailto:icchan417@gmail.com?subject={html.escape(sub)}">Choose course {c['id']}</a>
</div></section>'''

credits = '; '.join(html.escape(x['title'].replace('File:','')) + ' (' + x['lic'] + ')' for v in PH.values() for x in [v['card']] + v['detail'] + v['food'])
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tokyo, arrival day: three courses for the Katz family</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fffdf6;--card:#fff;--ink:#111;--mute:#767065;--line:#eae4d6;--acc:#1a5c3a;--r:10px}}
*{{box-sizing:border-box;min-width:0}} html,body{{overflow-x:hidden;max-width:100%}} img{{max-width:100%}}
body{{margin:0;font-family:Inter,-apple-system,"Hiragino Sans",sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
.kicker{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 10px}}
h1{{font-weight:800;font-size:clamp(34px,5.4vw,54px);line-height:1.06;letter-spacing:-.025em;margin:0 0 16px}}
h2{{font-weight:800;font-size:clamp(30px,4.2vw,42px);line-height:1.06;letter-spacing:-.025em;margin:0}}
h3{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 12px}}
header{{padding:56px 0 30px}} header p{{font-size:18px;color:var(--mute);margin:0;max-width:620px}}
.facts{{display:flex;flex-wrap:wrap;gap:6px 20px;margin:20px 0 0;padding:0;list-style:none;font-size:14px;color:var(--mute)}} .facts b{{color:var(--ink);font-weight:600}}
.sechead{{display:flex;align-items:baseline;gap:14px;padding:26px 0 16px;border-top:1px solid var(--line)}}
.sechead .n{{font-weight:800;font-size:26px;line-height:1;letter-spacing:-.02em;color:var(--acc)}}
.sechead b{{font-size:19px;font-weight:600}} .sechead span{{font-size:14px;color:var(--mute)}}
.menu{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
.mcard{{display:flex;flex-direction:column;text-align:left;font:inherit;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;padding:0;cursor:pointer;transition:transform .18s,box-shadow .18s,border-color .18s}}
.mcard:hover{{transform:translateY(-3px);box-shadow:0 10px 24px rgba(34,31,27,.10)}}
.menu.picked .mcard:not([aria-expanded=true]){{opacity:.42;filter:saturate(.45)}}
.menu.picked .mcard:not([aria-expanded=true]):hover{{opacity:.75;filter:none}}
.mcard[aria-expanded=true]{{border:2px solid var(--ink);box-shadow:0 12px 28px rgba(17,17,17,.16);transform:translateY(-3px)}}
.mcard[aria-expanded=true] .mopen{{color:var(--acc);border-bottom-color:var(--acc)}}
.mcard>img{{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:#f0ebe0}}
.mb{{display:flex;flex-direction:column;flex:1;padding:18px 20px 20px}}
.mk{{display:block;font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin-bottom:6px}}
.mt{{display:block;font-weight:800;font-size:26px;line-height:1.12;letter-spacing:-.025em;margin-bottom:6px}}
.mtag{{display:block;font-size:15px;color:var(--mute);margin-bottom:12px}}
.mch{{list-style:none;margin:auto 0 14px;padding:0;display:flex;flex-wrap:wrap;gap:6px}}
.mch li{{font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;border:1px solid var(--line);border-radius:4px;padding:3px 8px;color:var(--mute)}}
.mopen{{align-self:flex-start;display:inline-block;font-size:14px;font-weight:600;border-bottom:2px solid var(--acc);padding-bottom:1px}}
.mcard[aria-expanded=true] .mopen::after{{content:" ▲"}} .mcard[aria-expanded=false] .mopen::after{{content:" ▾"}}
.detail{{display:grid;grid-template-rows:0fr;transition:grid-template-rows .32s ease;margin-top:14px;position:relative}}
.detail[hidden]{{display:none}} .detail.open{{grid-template-rows:1fr}}
.dwrap{{overflow:hidden;min-height:0;background:var(--card);border:2px solid var(--ink);border-radius:var(--r);position:relative}}
.detail::before{{content:'';position:absolute;top:-11px;left:var(--arrow,50%);width:20px;height:20px;margin-left:-10px;background:var(--acc);border-left:2px solid var(--acc);border-top:2px solid var(--acc);transform:rotate(45deg);z-index:2;opacity:0;transition:opacity .2s .12s}}
.detail.open::before{{opacity:1}}
.dtop{{height:5px;background:var(--acc)}}
.detail.open .dwrap{{overflow:visible}}
.dwrap>*{{margin-left:26px;margin-right:26px}} .dwrap>.dtop{{margin:0}} .dwrap>.photos{{margin-left:26px;margin-right:26px}}
.dhead{{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;padding-top:26px}}
.dclose{{flex:none;font:inherit;font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--mute);background:none;border:1px solid var(--line);border-radius:6px;padding:8px 14px;cursor:pointer}}
.dclose:hover{{color:var(--ink);border-color:var(--ink)}}
.why{{font-size:17px;color:var(--mute);margin:10px 0 20px;max-width:640px}}
.photos{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-bottom:26px}}
.photos img{{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:8px;background:#f0ebe0}}
.dgrid{{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-bottom:28px}}
.steps{{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}}
.steps li{{display:grid;grid-template-columns:60px minmax(0,1fr);gap:12px;padding:11px 0;border-bottom:1px solid var(--line)}}
.steps b{{font-variant-numeric:tabular-nums;color:var(--acc);font-weight:600;font-size:14px}} .steps strong{{display:block;font-weight:600;font-size:16px}} .steps span{{color:var(--mute);font-size:14px}}
.mapbox{{border-radius:8px;overflow:hidden;background:#f0ebe0}} .mapbox iframe{{display:block;width:100%;height:300px;border:0}}
.moves{{font-size:14px;color:var(--mute);margin:12px 0 0}} .moves a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px;white-space:nowrap}}
.eats{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:26px}}
.eat{{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:var(--bg);border:1px solid var(--line);border-radius:8px;overflow:hidden}}
.eat>img{{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;background:#f0ebe0}}
.eb{{display:flex;flex-direction:column;flex:1;padding:14px 16px 16px}}
.eat:hover{{border-color:var(--ink)}}
.eat strong{{display:block;font-weight:700;font-size:18px;line-height:1.2;letter-spacing:-.015em}}
.eat em{{display:block;font-style:normal;font-size:11px;color:var(--acc);font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin:5px 0 9px}}
.eb>span{{display:block;font-size:14px;color:var(--mute)}} .eat i{{display:block;font-style:normal;font-size:12px;margin-top:auto;padding-top:10px;text-decoration:underline;text-underline-offset:3px}}
.notes{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px;font-size:14px}} .notes p{{margin:0;padding:16px 18px;background:var(--bg);border:1px solid var(--line);border-radius:8px}} .notes b{{display:block;font-weight:600;margin-bottom:3px}}
.links{{margin:0 0 22px;font-size:14px;display:flex;flex-wrap:wrap;gap:6px 18px}} .links a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px}}
.choose{{display:inline-block;background:var(--ink);color:#fff;text-decoration:none;font-weight:700;padding:16px 32px;border-radius:8px;font-size:16px;letter-spacing:-.01em;margin-bottom:28px}} .choose:hover{{background:#333}}
.arrival{{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start;padding-bottom:40px}}
.arrival p{{margin:0 0 10px;font-size:16px}} .arrival .hint{{color:var(--mute);font-size:15px}}
.arrival .mapbox iframe{{height:260px}}
footer{{padding:26px 0 60px;font-size:13px;color:var(--mute);border-top:1px solid var(--line)}} footer p{{margin:0 0 6px}}
@media(max-width:820px){{
 .menu{{grid-template-columns:1fr}} .mcard>img{{aspect-ratio:16/9}}
 .dgrid,.eats,.notes,.arrival,.photos{{grid-template-columns:1fr}}
 .dwrap>*{{margin-left:18px;margin-right:18px}} .mapbox iframe{{height:230px}}
}}
@media(max-width:560px){{
 .wrap{{padding:0 18px}}
 header{{padding:26px 0 18px}}
 h1{{font-size:31px;line-height:1.1;letter-spacing:-.03em;margin-bottom:12px}}
 header p{{font-size:16px;line-height:1.55;max-width:none}}
 .facts{{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;margin-top:16px;font-size:13px;line-height:1.5}}
 .facts li{{display:contents}} .facts b{{white-space:nowrap}}
 .sechead{{display:block;padding:22px 0 12px}}
 .sechead .n{{font-size:20px;margin-right:8px;display:inline}}
 .sechead b{{font-size:17px}} .sechead span{{display:block;font-size:13px;line-height:1.5;margin-top:2px}}
 .menu{{gap:12px}}
 .mb{{padding:15px 16px 16px}} .mt{{font-size:23px;line-height:1.15}} .mtag{{font-size:14px;margin-bottom:10px}}
 .mch{{gap:5px;margin-bottom:12px}} .mch li{{font-size:10.5px;padding:2px 7px}}
 .mopen{{font-size:13.5px}}
 h2{{font-size:26px;line-height:1.12}}
 .dhead{{padding-top:20px}} .why{{font-size:15.5px;line-height:1.55;margin:8px 0 16px}}
 .dwrap>*{{margin-left:16px;margin-right:16px}}
 .photos{{gap:8px;margin-bottom:20px}} .photos img{{aspect-ratio:3/2}}
 h3{{margin:22px 0 10px}} .dgrid{{gap:0;margin-bottom:0}}
 .steps li{{grid-template-columns:52px minmax(0,1fr);gap:10px;padding:10px 0}}
 .steps strong{{font-size:15.5px}} .steps span{{font-size:13.5px;line-height:1.5}}
 .eats{{gap:10px;margin-bottom:20px}} .eat>img{{aspect-ratio:16/9}} .eb{{padding:12px 14px 14px}}
 .notes{{gap:10px;margin-bottom:16px}} .notes p{{padding:14px 16px;font-size:13.5px}}
 .links{{font-size:13.5px;gap:4px 14px;margin-bottom:18px}}
 .choose{{display:block;text-align:center;padding:15px 0;margin-bottom:22px}}
 .arrival{{gap:16px;padding-bottom:32px}} .arrival p{{font-size:15.5px;line-height:1.55}} .arrival .hint{{font-size:14px}}
 .mapbox iframe{{height:210px}}
 footer{{padding:20px 0 44px;font-size:11.5px;line-height:1.55}}
}}
</style></head><body>
<header class="wrap">
<p class="kicker">Tokyo · Sunday, December 21</p>
<h1>Arrival day, done gently.</h1>
<p>You land at Haneda at 5:10 in the morning. Every course starts at your hotel at 9:00 and has you back by 14:00 for a nap. Little walking, plenty of sitting, and one thing worth remembering.</p>
<ul class="facts"><li><b>Guide</b> Yuuki</li><li><b>Time</b> 9:00–14:00</li><li><b>Group</b> family of five</li><li><b>Start and end</b> your hotel</li></ul>
</header>
<div class="wrap">
<div class="sechead"><span class="n">1</span><div><b>Pick a course</b> <span>Tap one to see the plan, the route and where we eat.</span></div></div>
<div class="menu">{''.join(menu(c) for c in COURSES)}</div>
{''.join(detail(c) for c in COURSES)}
<div class="sechead"><span class="n">2</span><div><b>From the airport</b> <span>Haneda is 30 to 45 minutes from central Tokyo.</span></div></div>
<div class="arrival">
<div><p>All three courses stay close to the middle of the city, so nothing is far from your hotel.</p>
<p class="hint">Tell me the hotel name and I will pin it here, with the exact door-to-door times for the course you choose. If one room is ready early, you can drop the bags and start light.</p></div>
<div class="mapbox"><iframe src="{emb('Haneda Airport Tokyo')}" loading="lazy" title="Haneda airport and central Tokyo" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div>
</div>
<footer class="wrap"><p>Reply to Tree or Yuuki with A, B or C. Times are approximate and can move earlier or later on the day.</p><p>Photos: {credits}, via Wikimedia Commons.</p></footer>
<script>
(function(){{
 var cards=[].slice.call(document.querySelectorAll('.mcard'));
 function close(id){{var d=document.getElementById('detail-'+id);d.classList.remove('open');document.querySelector('.menu').classList.remove('picked');setTimeout(function(){{if(!d.classList.contains('open'))d.hidden=true}},320);
   document.querySelector('.mcard[data-course="'+id+'"]').setAttribute('aria-expanded','false')}}
 var menuEl=document.querySelector('.menu');
 function point(id){{var b=document.querySelector('.mcard[data-course="'+id+'"]'),d=document.getElementById('detail-'+id);
   var r=b.getBoundingClientRect(),w=d.getBoundingClientRect();
   d.style.setProperty('--arrow',(r.left+r.width/2-w.left)+'px')}}
 function open_(id){{var d=document.getElementById('detail-'+id);d.hidden=false;menuEl.classList.add('picked');
   requestAnimationFrame(function(){{d.classList.add('open');point(id)}});
   document.querySelector('.mcard[data-course="'+id+'"]').setAttribute('aria-expanded','true')}}
 window.addEventListener('resize',function(){{var o=document.querySelector('.mcard[aria-expanded=true]');if(o)point(o.dataset.course)}});
 var want=(location.hash.match(/^#detail-([ABC])$/)||[])[1]||(location.search.match(/[?&]open=([ABC])/)||[])[1];
 if(want){{open_(want);setTimeout(function(){{document.getElementById('detail-'+want).scrollIntoView()}},80)}}
 cards.forEach(function(b){{
  b.addEventListener('click',function(){{
   var id=b.dataset.course,was=b.getAttribute('aria-expanded')==='true';
   cards.forEach(function(o){{if(o.getAttribute('aria-expanded')==='true')close(o.dataset.course)}});
   if(was)return;
   open_(id);history.replaceState(null,'','#detail-'+id);
   setTimeout(function(){{document.getElementById('detail-'+id).scrollIntoView({{behavior:'smooth',block:'start'}})}},60);
  }});
 }});
 document.querySelectorAll('.dclose').forEach(function(x){{
  x.addEventListener('click',function(){{var d=x.closest('.detail'),id=d.id.replace('detail-','');close(id);
   document.querySelector('.mcard[data-course="'+id+'"]').scrollIntoView({{behavior:'smooth',block:'center'}})}});
 }});
}})();
</script>
{{DEVBAR}}</body></html>'''
open('index.html', 'w').write(page.replace('{DEVBAR}', ''))
open('preview.html', 'w').write(page.replace(
    '{DEVBAR}',
    '<script>window.DEVBAR_FORCE=1</script><script src="devbar.js?v=3"></script>'))
print('written', len(page), '-> index.html + preview.html')
