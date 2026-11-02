"""Example lesson in the kit's format: a short compounding lesson that shows every scene pattern.

Patterns shown: title scene, definition cards, an equation that counts up, growing bars, a table that
reveals row by row, a pause-and-think question with its worked answer, a New words scene, and Practice.
Build it with:  python3 engine.py day1   (copy this file into the build folder first)
"""
from common import table, checks

DAY = 1
H1 = 'Day 1: Money, inflation and compounding'
SUB = 'Example course · why investing exists and how compounding works · about 3 minutes'

HOLD = 1.6  # extra silence after "Pause and think"; with the 1.5 s scene tail that is about 3 s

CSS = r'''
.q { font-family: var(--display); font-weight: 700; font-size: 2.8cqw; line-height: 1.22; margin: 0; }
.q b { color: var(--gold); }
.pausebox { display: flex; align-items: center; gap: 1.6cqw; font-family: var(--mono); font-weight: 700; font-size: 2.2cqw; color: var(--gold); }
.pausebox .ring { width: 6cqw; height: 6cqw; border-radius: 50%; border: .5cqw solid var(--gold); display: grid; place-items: center; font-size: 3cqw; }
.steps { display: grid; gap: .9cqw; font-family: var(--mono); font-size: max(10px, 2cqw); }
.steps > div span { color: var(--dim); font-family: var(--body); font-size: .85em; }
.words { display: grid; grid-template-columns: 1fr 1fr; gap: .8cqw 2.4cqw; margin: 0; padding: 0; list-style: none; }
.words li { font-size: max(9px, 1.7cqw); line-height: 1.3; color: var(--dim); }
.words li b { color: var(--gold); font-weight: 600; }
@media (max-width: 560px) { .words { grid-template-columns: 1fr; } }
'''


def pause(pre):
    return f'<div class="pausebox rv" id="{pre}p"><span class="ring" id="{pre}n">3</span>Pause and think</div>'


def pause_js(pre):
    # D is the spoken length of the scene, so the countdown runs in the silence that follows it
    return f"show('{pre}p',t>D-0.2); txt('{pre}n',String(Math.max(1,Math.min(3,Math.ceil(3-(t-D))))));"


WORDS = [('Inflation', 'the yearly rise in prices'), ('Real return', 'your return minus inflation'),
         ('Compounding', 'earning returns on past returns'), ('Rule of 72', '72 ÷ return % ≈ years to double')]

SCENES = [
 dict(label='Intro', cap='Day 1 · Investing exists to beat inflation; compounding is the engine that does it',
  show='Title with two cards: inflation, compounding',
  say="Welcome to Day one. Investing exists to beat inflation, and compounding is the engine that does it. Let's see what both mean for your own money.",
  html='''<div class="daytag"><b>Day 1</b> Foundations</div>
<h2 class="big">Money, inflation and <span class="gold">compounding</span></h2>
<div class="split2"><div class="card rv" id="a0"><span class="k">The problem</span><h3>Inflation</h3><p>Prices rise every year</p></div>
<div class="card rv" id="a1"><span class="k">The engine</span><h3 class="mint">Compounding</h3><p>Returns on your returns</p></div></div>''',
  js="show('a0',t>.3*D); show('a1',t>.55*D);"),

 dict(label='Real return', cap='Real return ≈ nominal return − inflation · 2.5% savings − 5% inflation ≈ −2.5%',
  show='Equation counting to −2.5%',
  say="Inflation is the yearly rise in prices. What counts is your real return: your return minus inflation. A savings account paying two point five percent, with five percent inflation, has a real return of about minus two point five percent. Your money is quietly shrinking.",
  html='''<div class="eyebrow">Real return is what counts</div>
<div class="eq"><div class="rv" id="b0"><div class="chip">2.5%</div><small>savings rate</small></div><span class="rv" id="b1">−</span>
<div class="rv" id="b2"><div class="chip">5%</div><small>inflation</small></div><span class="rv" id="b3">=</span>
<div class="rv" id="b4"><div class="chip rose" id="b5">0%</div><small>real return</small></div></div>''',
  js="seq('b',5,t,.45*D,.06*D); txt('b5',(-2.5*P(t,.75*D,.9*D)).toFixed(1)+'%');"),

 dict(label='Compounding', cap='₹1 lakh at 12% a year: ₹3.1 lakh after 10 years · ₹9.6 lakh after 20 · ₹30 lakh after 30',
  show='Table of values revealing row by row, with growing bars',
  say="Compounding means earning returns on your past returns. One lakh rupees at twelve percent a year becomes three point one lakh after ten years, nine point six lakh after twenty, and thirty lakh after thirty. The last ten years add more than the first twenty.",
  html='<div class="eyebrow">₹1 lakh at 12% a year</div>' + table('c', ['After', 'Value'], [('10 years', '₹3.1 lakh'), ('20 years', '₹9.6 lakh'), ('30 years', '₹30 lakh')]) +
       '''<div class="bars"><div class="hbar"><span>30 years</span><div class="tr"><i id="c3"></i></div><span class="v">₹30 lakh</span></div></div>''',
  js="const at=[.35,.5,.65]; for(let i=0;i<3;i++) show('c'+i,t>at[i]*D); w('c3',P(t,.65*D,.85*D)*100);"),

 dict(label='Question', cap='Question · How long does money take to double at 12% a year?',
  show='Question with a pause-and-think countdown',
  say="A quick test. Using the Rule of seventy two, how many years does money take to double at twelve percent a year? Pause and think.",
  hold=HOLD,
  html='<div class="eyebrow">Your turn</div><p class="q rv" id="dq">Rule of 72: how many years to double at <b>12%</b> a year?</p>' + pause('d'),
  js="show('dq',t>.05*D); " + pause_js('d')),

 dict(label='Answer', cap='72 ÷ 12 = 6 years · 7.1% doubles in about 10 years · 2.5% in about 29',
  show='Worked answer counting up',
  say="Seventy two divided by twelve is six. So money doubles in about six years. At seven point one percent it takes about ten years, and at two point five percent, about twenty nine.",
  html='''<div class="eyebrow">Answer</div><div class="steps">
<div class="rv" id="e0">72 ÷ 12 = <b class="gold" id="e1">0</b> years</div>
<div class="rv" id="e2">72 ÷ 7.1 ≈ 10 years <span>· 72 ÷ 2.5 ≈ 29 years</span></div></div>''',
  js="show('e0',t>.05*D); txt('e1',String(Math.round(6*P(t,.15*D,.3*D)))); show('e2',t>.5*D);"),

 dict(label='New words', cap='New words: inflation, real return, compounding, Rule of 72',
  show='Glossary of the lesson\'s new words',
  say="Today's new words: inflation, real return, compounding, and the Rule of seventy two.",
  html='<div class="eyebrow">New words in this lesson</div><ul class="words">' +
       ''.join(f'<li class="rv" id="f{i}"><b>{a}:</b> {b}</li>' for i, (a, b) in enumerate(WORDS)) + '</ul>',
  js="seq('f',4,t,.1*D,.15*D);"),

 dict(label='Practice', cap='Practice: Rule of 72 at 6%, 9% and 12%',
  show='Practice checklist; next lesson',
  say="Your practice: use the Rule of seventy two to find how long ten thousand rupees takes to double at six, nine and twelve percent. Tomorrow: building your safety net.",
  html=checks('g', ['Use the Rule of 72 to find how long ₹10,000 takes to double at 6%, 9% and 12%.'], 'Next: Day 2, your safety net.'),
  js="show('g0',t>.1*D); show('g1',t>.7*D);"),
]
