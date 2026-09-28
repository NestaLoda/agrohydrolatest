# FINAL PRODUCT + RESEARCH CONTRACT
# 2204-D KONYA → TÜRKİYE → FUTURE NORTH → TASE-VII
# THIS IS NOW THE AUTHORITATIVE PRODUCT AND RESEARCH SPECIFICATION

Read this completely before changing more code.

Do NOT restart the repository.

Do NOT discard:
- official Türkiye agricultural datasets,
- current crop database,
- FAO-56 water calculations,
- provenance architecture,
- NASA / future-climate data,
- existing multi-crop optimizer,
- PWN importer,
- PRE/POST run infrastructure,
- tests.

However, previous implementation prompts have gradually overcomplicated
the product and narrowed the Arctic research connection too much.

This document defines the FINAL intended product and research logic.

If an older UI/product instruction conflicts with this document,
THIS DOCUMENT WINS.

Create:

docs/FINAL_PRODUCT_CONTRACT.md

with this specification and treat it as the highest-level
implementation contract beneath the scientific source-of-truth documents.

Then IMPLEMENT it.

Do not answer with another large design proposal before starting.

======================================================================
1. WHAT ARE WE ACTUALLY BUILDING?
======================================================================

The product can be explained in one sentence:

“A decision-support simulator that automatically analyzes the best
available climate, water and agricultural data for a region and calculates
what should be produced, how much should be produced, by which production
method and using which water resources under selected conditions.”

The central question is:

“DEĞİŞEN İKLİM VE SU KOŞULLARI ALTINDA,
NERede HANGİ ÜRÜNLERDEN NE KADAR
VE HANGİ YÖNTEMLE ÜRETMELİYİZ?”

This is NOT primarily:

- a website,
- a climate viewer,
- a map product,
- a PWN dashboard,
- a desalination calculator,
- a hydroponic lettuce calculator,
- a collection of data cards.

It is a scientific planning simulator.

======================================================================
2. THE SCIENTIFIC CONTINUITY
======================================================================

The complete evolution is:

KONYA
Existing Crop Pattern
→ water/climate pressure
→ optimized Crop Pattern

↓

TÜRKİYE
Regional baseline agriculture
→ regional climate/water conditions
→ optimized Regional Crop Pattern

↓

FUTURE NORTH
Future climate suitability
+ terrestrial water security
+ soil/permafrost
+ production infrastructure
+ energy
+ water sources

→ Future Production System Pattern

↓

TASE-VII
Actual Arctic observations
+ physical water samples

→ update scientifically relevant uncertain inputs

↓

SAME DECISION ENGINE

→ Post-observation Production System Pattern

↓

CONTROLLED VALIDATION
Hydroponic / greenhouse pilot
+ real water / energy / yield data

→ improve the model.

This scientific continuity must be visible in:
- code,
- UI,
- documentation,
- interview story,
- research plan.

======================================================================
3. THREE STATES — NOT MANY PRODUCTS
======================================================================

The entire application has THREE scientific states.

STATE A — BUGÜN / TÜRKİYE

Question:

“Mevcut tarımsal üretim desenini
bugünkü veya seçilen su/iklim koşullarında
nasıl değiştirmeliyiz?”

STATE B — GELECEK / KUZEY

Question:

“Gelecekte bu bölgede
hangi üretim sistemi kurulmalı?”

STATE C — SAHA GÜNCELLEMESİ / TASE

Question:

“Gerçek Arktik saha bilgisi,
sefer öncesinde verdiğimiz kararı değiştiriyor mu?”

Do NOT turn these into disconnected websites.

They use the SAME conceptual decision engine.

======================================================================
4. THE INTERACTION MODEL
======================================================================

The main application should feel like scientific desktop software.

Mental model:

LEFT = EXPERIMENT / SCENARIO CONTROLS

RIGHT = MODEL RESULT

Use a compact top bar and one primary workspace.

Desktop layout:

┌────────────────────────────────────────────────────────────┐
│ MODE · REGION · PERIOD · SCENARIO · SAVE · EVIDENCE      │
├───────────────────┬────────────────────────────────────────┤
│                   │                                        │
│   SCENARIO LAB    │       DECISION / PATTERN CANVAS       │
│                   │                                        │
│   parameters      │       baseline                         │
│   sliders         │          ↓                             │
│   toggles         │       optimized pattern                │
│   crop controls   │                                        │
│   water           │       resources / constraints          │
│   priorities      │       explanations                     │
│                   │                                        │
│ [ CALCULATE ]     │                                        │
└───────────────────┴────────────────────────────────────────┘

Do NOT return to:
large page sections,
giant cards,
hero sections,
map-first composition,
large narrative paragraphs.

======================================================================
5. DATA SHOULD COME TO THE USER
======================================================================

A core principle:

THE USER SHOULD NOT NEED TO ENTER SCIENTIFIC DATA
THAT THE SYSTEM CAN ALREADY OBTAIN.

The platform should automatically load available:

- agricultural baseline,
- climate,
- future climate,
- crop parameters,
- water calculations,
- soil/permafrost,
- hydrological context,
- evidence and provenance.

The user mainly controls:

- planning scenario,
- resource restrictions,
- planning objective,
- manual what-if overrides.

Source data is always the baseline.

There should NOT be two confusing worlds called
“source data” and “manual system”.

Instead:

BASELINE VALUE

and, if edited:

MANUAL OVERRIDE.

Every override is visible.

======================================================================
6. BUGÜN / TÜRKİYE — SIMPLE SIMULATOR
======================================================================

When the user selects:

BUGÜN / TÜRKİYE

and:

KONYA

the system automatically loads:

- official current crop pattern,
- crop areas,
- derived production/yield context,
- relevant climate/reanalysis,
- crop-water calculations,
- known model assumptions.

The user immediately sees the crop pattern.

Example interaction structure:

HIZLI SENARYO

[ Referans ]
[ Su -10% ]
[ Su -20% ]
[ Kuraklık ]
[ Özel ]

IKLIM

Sıcaklık senaryo değişimi
[ slider ]

Yağış
[ slider ]

ET0
[ slider / multiplier ]

SU

Kullanılabilir / scenario water
[ input / slider ]

Sulama verimi
[ slider ]

ÜRÜN DESENİ

Buğday
[ slider ] 46.6%

Arpa
[ slider ] 30.1%

Dane mısır
[ slider ] 14.5%

Şeker pancarı
[ slider ] ...

Patates
[ slider ] ...

Display:

[ % PAY ] [ HEKTAR ]

Advanced crop constraints should be hidden under:

GELİŞMİŞ KISITLAR

Do NOT require “edit” mode for every normal slider.

If the user moves a baseline value,
mark only that value as:

MANUEL SENARYO.

Sticky bottom button:

[ ÜRÜN DESENİNİ HESAPLA ]

======================================================================
7. TÜRKİYE — WHAT THE SYSTEM OUTPUTS
======================================================================

Before optimization:

show:

MEVCUT ÜRÜN DESENİ.

After optimization:

MEVCUT ÜRÜN DESENİ
→
ÖNERİLEN ÜRÜN DESENİ.

This is the HERO output.

For each crop:

current ha / %
recommended ha / %
difference
water requirement
production change.

Also show:

current total modeled water requirement
scenario water budget
recommended water use
assigned area
unassigned area
production impact
binding constraints.

Then:

NEDEN BU DESEN?

These explanations MUST be derived from solver state.

No generic LLM explanations.

Example:

“Buğday minimum üretim sınırına kadar azaltıldı.”

“Su bütçesi bağlayıcı olduğu için bütün arazi kullanılamadı.”

etc.

======================================================================
8. TÜRKİYE REGIONAL GENERALIZATION
======================================================================

The existing regions remain valuable:

Konya
Adana
Manisa
Şanlıurfa
Edirne.

But regional comparison is SECONDARY.

Primary workflow:

select region
→ baseline loads
→ modify scenario
→ optimize that region.

The same decision philosophy is applied to different regions.

This is how we demonstrate:

the Konya idea is not only a Konya-specific interface.

======================================================================
9. FUTURE NORTH — THE REAL RESEARCH QUESTION
======================================================================

When the mode changes to:

GELECEK / KUZEY

the SAME simulator evolves.

The question becomes:

“Gelecekte seçilen kuzey bölgesinde
hangi ürünlerden ne kadar üretmeliyiz,
hangilerini açık tarla / sera / hidroponik sistemde üretmeliyiz
ve hangi su kaynaklarını kullanmalıyız?”

This is the second-generation meaning of:

CROP PATTERN
→
PRODUCTION SYSTEM PATTERN.

The North result cannot remain:

“1000 kg lettuce.”

It cannot remain:

“hydroponics is conditional.”

It must calculate an actual production-system pattern.

======================================================================
10. FUTURE NORTH — AUTOMATIC INPUT LAYERS
======================================================================

The system should automatically assemble the strongest available evidence.

A — FUTURE CLIMATE

- scenario/model
- temperature
- precipitation
- GDD
- frost-free period
- relevant seasonal indicators.

B — LAND / GROUND

- soil
- drainage
- permafrost
- active layer where relevant
- usable land.

C — TERRESTRIAL WATER SECURITY

This is CRITICAL.

Separate:

PHYSICAL WATER PRESENCE

from:

SEASONALLY RELIABLE USABLE PRODUCTION WATER.

Possible inputs:

- precipitation
- snowmelt
- runoff
- freshwater bodies
- seasonal flow
- storage
- access
- competing uses
- environmental requirements.

PWN DOES NOT calculate this annual quantity.

D — PRODUCTION INFRASTRUCTURE

- open-field capacity
- greenhouse capacity
- hydroponic / CEA capacity
- energy availability.

E — WATER-SOURCE PORTFOLIO

- local freshwater
- stored precipitation / meltwater
- reuse
- desalinated seawater where appropriate.

F — CANDIDATE CROPS

Automatically filter a researched crop database.

Do NOT ask the user to invent the candidate crop list from zero.

======================================================================
11. THE ARCTIC WATER QUESTION
======================================================================

The simple scientific concept should become visible in the product:

1. SU FİZİKSEL OLARAK VAR MI?

2. İHTİYAÇ DUYULAN YERDE VE ZAMANDA
   KULLANILABİLİR Mİ?

3. ÜRETİM İÇİN YETERLİ VE UYGUN MU?

Snow, ice, rainfall, lakes or seawater existing
does not automatically mean
reliable agricultural production water exists.

Therefore the model evaluates:

timing
storage
access
quality
treatment
energy
reliability.

This is a core scientific connection between
climate change and water management.

======================================================================
12. FUTURE NORTH — DO NOT MAKE THE USER SPECIFY THE ANSWER
======================================================================

The current simulator asks the user to provide arbitrary targets such as:

3000 kg barley
10000 kg potato
1000 kg lettuce.

Do NOT make this the primary planning interaction.

That makes the user provide much of the answer before optimization.

Instead create a higher-level:

PLANLAMA AMACI

control.

Support modes such as:

A. KAYNAK KAPASİTESİNİ KEŞFET

“Bu kaynaklarla hangi üretim portföyü mümkün?”

B. TALEBİ KARŞILA

“Bu tanımlı üretim / demand basket için hangi pattern gerekir?”

C. DENGELİ PLAN

transparent multi-objective / lexicographic planning.

D. SU ÖNCELİKLİ

E. ENERJİ ÖNCELİKLİ.

Do not create arbitrary hidden weights.

Every planning objective and assumption must be explicit.

Türkiye can continue to use current production
as its natural baseline / target context.

Future North does not have an existing agricultural baseline,
so the planning objective must be explicitly defined.

======================================================================
13. FUTURE NORTH — OUTPUT
======================================================================

The HERO result:

GELECEĞİN ÜRETİM DESENİ.

Display in FOUR connected layers.

LAYER 1 — CROP PATTERN

Which crops?
How much?

LAYER 2 — METHOD PATTERN

For each crop:

open field
greenhouse
hydroponic / CEA.

LAYER 3 — WATER-SOURCE PATTERN

For each relevant option:

local freshwater
stored water
reuse
desalination.

LAYER 4 — SEASON / RESOURCE PLAN

when?
water?
energy?
area/capacity?
binding constraints?

Example STRUCTURE only:

ARPA
X ha
Y kg
Açık tarla
Yerel/depolanmış freshwater

PATATES
X ha
Y kg
Açık tarla
...

YAPRAKLI ÜRÜN
X m²
Y kg
Hidroponik
Reuse / conditioned source

Numbers MUST come from the model.

Do not invent them.

======================================================================
14. NOT ONE UNIVERSAL “BEST PATTERN”
======================================================================

For Future North,
there may not be one universal best agricultural future.

Show transparent alternatives where useful:

DENGELİ DESEN

SU ÖNCELİKLİ DESEN

ENERJİ ÖNCELİKLİ DESEN.

This is more scientifically honest than a magic score.

The recommendation is always:

“best under THESE stated planning priorities and constraints.”

======================================================================
15. CROP PORTFOLIO RESEARCH
======================================================================

The current barley + potato + lettuce portfolio
is only an assumption-based engine demonstration.

Strengthen it.

Research a small, defensible northern crop portfolio.

Possible categories to evaluate:

OPEN FIELD:
barley
potato
other evidence-supported high-latitude crops.

CONTROLLED ENVIRONMENT:
lettuce
leafy greens
herbs
microgreens
other justified crops.

For each retained candidate record:

- climate evidence,
- growing period,
- GDD if valid,
- frost sensitivity,
- soil constraint,
- water requirement,
- yield basis,
- production method compatibility,
- high-latitude precedent,
- uncertainty.

Do not force every candidate into the optimizer.

======================================================================
16. PRE-TASE MODEL
======================================================================

Before going to the Arctic,
we should already produce:

PRE-TASE FUTURE PRODUCTION SYSTEM PATTERN.

Inputs may include:

future climate
terrestrial water estimates
soil/permafrost
energy
production infrastructure
historical/model ocean conditions
existing literature.

Every uncertain input must be classified.

For example:

HIGH EVIDENCE

MODELED

ASSUMPTION

DATA MISSING

FIELD OBSERVATION POSSIBLE.

======================================================================
17. A NEW CORE FEATURE: DECISION UNCERTAINTY / VALUE OF INFORMATION
======================================================================

This is important.

After the Future North pattern is calculated,
the system should ask:

“WHICH UNCERTAINTY COULD ACTUALLY CHANGE THIS DECISION?”

Perform transparent sensitivity / value-of-information style analysis.

For each uncertain parameter:

- plausible range,
- source,
- effect on resulting production pattern,
- whether the decision changes,
- whether TASE can actually measure it.

Output something like:

KARAR İÇİN KRİTİK BELİRSİZLİKLER

Seasonal terrestrial freshwater
Decision impact: HIGH
TASE PWN can measure directly: NO
Needed source: hydrology / infrastructure

Marine source-water temperature
Decision impact: MEDIUM
TASE measurable: YES

Marine salinity
Decision impact: MEDIUM / UNKNOWN
TASE measurable: YES

Treatment-relevant chemistry
Decision impact: POTENTIALLY HIGH
TASE physical sample: POSSIBLE, protocol required.

This is not a fake probability model.

It is transparent sensitivity analysis.

======================================================================
18. THIS IS ONE OF THE STRONGEST REASONS FOR TASE
======================================================================

The application should not merely state:

“We need Arctic data.”

It should calculate:

which uncertain variables influence the decision

and then identify:

which of those variables can be physically measured during TASE.

This creates:

MODEL
→ DECISION
→ UNCERTAINTY
→ FIELD RESEARCH NEED.

The expedition becomes a scientific experiment,
not a travel destination.

======================================================================
19. TASE-VII FIELD RESEARCH PROGRAM
======================================================================

The TASE field work should be defined as THREE connected research packages.

--------------------------------------------------
FIELD PACKAGE A — WATER COLUMN GROUND TRUTH
--------------------------------------------------

Before each permitted cast:

freeze and store the relevant model snapshot.

Then collect with Arctic PWN:

- conductivity / salinity
- temperature
- pressure / depth
- UTC
- ship/deck position
- quality / calibration metadata.

Where available:
compare to reference CTD.

Scientific question:

“How accurately does the existing model represent
the real water-column structure
at this time and location?”

Do not assume the model must be wrong.

Agreement is also a result.

--------------------------------------------------
FIELD PACKAGE B — PHYSICAL WATER SAMPLES
--------------------------------------------------

At scientifically meaningful / operationally permitted depths,
collect physical samples.

Exact depths are NOT fixed now.

Potential logic:

standard depth(s)
+
important gradient / transition
+
background.

The PWN profile may help identify
an information-rich sampling depth.

Possible analyses, only after expert/lab confirmation:

SOURCE CHARACTERIZATION:
δ18O
δ2H
and appropriate supporting variables.

TREATMENT / PRODUCTION RELEVANCE:
salinity/EC
Na
Cl
Ca
Mg
boron
alkalinity
and only other justified parameters.

Do not create a giant chemistry panel.

Every analysis must answer a decision question.

--------------------------------------------------
FIELD PACKAGE C — DECISION INFORMATION VALUE
--------------------------------------------------

After observations:

compare:

MODEL EXPECTATION

vs

FIELD OBSERVATION.

Update ONLY variables that the field data
scientifically support.

Then rerun:

THE SAME production-system optimizer.

Measure:

- crop-pattern difference,
- production-method difference,
- water-source allocation difference,
- energy difference,
- feasibility difference,
- binding-constraint difference.

Possible answer:

NO DECISION CHANGE.

That is valid.

======================================================================
20. OPTIONAL SECONDARY FIELD RESEARCH — ADAPTIVE SAMPLING
======================================================================

If expedition logistics and expert feedback support it:

test whether PWN-guided gradient/anomaly information
can improve physical sampling depth selection.

Compare, with the same small sample budget:

fixed-depth sampling

vs

gradient-informed sampling.

Do not claim AI superiority unless real data support it.

A classical gradient method is a valid baseline.

This is SECONDARY.

Do not let it overtake the main project.

======================================================================
21. IMPORTANT: WHAT TASE DOES NOT PROVE
======================================================================

TASE does NOT directly:

- measure 2050 climate,
- measure all future agricultural water,
- validate all terrestrial hydrology,
- prove that a crop will grow in the future,
- validate the entire Sustainable Production Frontier.

TASE provides real physical Arctic evidence
for specific model / source-water questions.

Terrestrial future agriculture still uses:
climate,
hydrology,
soil,
permafrost,
infrastructure
and other external data.

======================================================================
22. AGRICULTURAL / HYDROPONIC VALIDATION AFTER FIELD SAMPLING
======================================================================

We also want the agricultural side to become experimentally testable.

Do NOT claim we will validate the entire crop pattern
by growing crops on the expedition ship.

That would be scientifically weak and operationally risky.

Instead create a POST-EXPEDITION controlled validation path.

If physical samples can legally/logistically be returned
and the laboratory protocol allows:

ARCTIC SOURCE WATER SAMPLE

→ characterization

→ scientifically appropriate treatment / conditioning

→ standardized hydroponic nutrient preparation

→ small controlled growth experiment.

If transporting/using the sample is not possible:

reconstruct a SYNTHETIC SOURCE WATER
based on measured chemistry
and clearly label it as reconstructed.

======================================================================
23. SOURCE-WATER → HYDROPONIC VALIDATION
======================================================================

Design a future controlled experiment such as:

CONTROL:
standard suitable source water.

TEST:
appropriately treated/conditioned
Arctic source-water condition
or measurement-derived synthetic equivalent.

The crop should be selected for:
- short cycle,
- controlled-environment relevance,
- measurable response.

Possible endpoints:

water input
EC / relevant solution properties
energy/treatment requirement
germination if appropriate
fresh/dry biomass
growth rate
yield proxy
water-use efficiency.

Exact protocol will be chosen with
plant-production / laboratory expertise.

This experiment tests:

SOURCE WATER / TREATMENT / PRODUCTION COMPATIBILITY.

It does NOT prove the entire future Arctic crop pattern.

======================================================================
24. HYDROPONIC / GREENHOUSE PILOT — PROJECT CONTINUITY
======================================================================

If the decision system recommends controlled production,
the next research/product phase becomes:

MODEL RECOMMENDATION

→ pilot controlled-production system

→ REAL operating data:

water
energy
temperature
humidity
EC / nutrient solution
yield
failures

→ model-vs-reality comparison

→ parameter improvement.

This is how the project continues after the expedition.

The greenhouse is not the project itself.

It is a validation environment for
one production method recommended by the project.

======================================================================
25. WHY WE NEED TO GO TO THE ARCTIC — THE COMPLETE ANSWER
======================================================================

The project should make these reasons visible naturally.

We go because the expedition allows us to:

1. obtain new same-time / same-location
   physical Arctic water-column observations;

2. collect physical water samples
   that cannot be created from a remote dataset;

3. test how well existing ocean/model information
   represents actual field conditions;

4. characterize field-dependent source-water variables
   relevant to treatment/usability;

5. measure whether replacing modeled assumptions
   with real observations changes our production decision;

6. evaluate which observations actually have
   high decision information value;

7. improve and validate the PWN field workflow;

8. generate the physical evidence needed
   for later source-water / controlled-production validation.

Do not turn this into a marketing list in the UI.

The application and research design should make it obvious.

======================================================================
26. PWN'S EXACT ROLE
======================================================================

The conceptual relationship:

FUTURE PRODUCTION MODEL
        ↓
UNCERTAIN WATER-SYSTEM INPUT
        ↓
TASE
        ↓
PWN + PHYSICAL SAMPLE
        ↓
QUALITY CONTROL / MODEL COMPARISON
        ↓
UPDATED VALID INPUT
        ↓
SAME OPTIMIZATION ENGINE
        ↓
UPDATED PRODUCTION PATTERN.

PWN is the measurement tool.

The project is the decision-support research system.

======================================================================
27. PWN UI
======================================================================

Do not make PWN a dominant separate product.

From Future North results:

[ SAHA ARAŞTIRMASI ]

opens a compact research drawer.

Show:

CURRENT VARIABLE

Current source
Model value/range
Decision sensitivity

FIELD STATUS

Can TASE measure it?
Instrument / sample method
Observation status

If real compatible observation exists:

[ GİRDİYİ GÜNCELLE VE YENİDEN HESAPLA ]

Then display:

PRE-TASE

vs

POST-OBSERVATION.

A separate technical PWN view may exist for:
raw profile,
quality,
calibration,
gradient,
engineering.

But the main user journey remains decision-first.

======================================================================
28. DESIGN DIRECTION — CURRENT UI STILL LOOKS GENERATED
======================================================================

The software must become visually intentional.

Do not make it decorative,
but stop making it look like a generic AI-generated admin panel.

Design concept:

RESEARCH FIELD CONSOLE.

Use a restrained domain visual system.

Core shell:
deep forest / petrol green.

Canvas:
warm off-white.

Domain accents:

CROPS / PRODUCTION:
green.

WATER:
cool blue.

CLIMATE:
muted warm / rust accent.

ENERGY:
amber.

FIELD OBSERVATION:
icy cyan.

UNCERTAINTY / UNKNOWN:
neutral gray.

Use restrained accents.
Do NOT make a rainbow dashboard.

======================================================================
29. VISUAL LANGUAGE
======================================================================

Use meaningful minimal icons:

crop / leaf
water droplet
snow / melt
soil
greenhouse
energy
wave / water column
sample bottle
sensor
evidence.

Use consistent iconography.

Add subtle scientific visual texture where appropriate:

contour lines
water-column lines
small map context
future-period timeline.

No stock photography.

No giant illustrations.

======================================================================
30. MICROINTERACTIONS
======================================================================

Use subtle effects that communicate state.

Examples:

When a baseline slider changes:

SOURCE
→
MANUAL OVERRIDE.

When optimization completes:

existing pattern bars smoothly transition
to recommended bars.

When field data replaces a model value:

MODELLED
→
OBSERVED

state visibly changes.

When a constraint becomes binding:
highlight the relevant resource subtly.

When data are missing:
show clear UNKNOWN / DATA NEEDED state.

Effects must explain state,
not exist for decoration.

======================================================================
31. INFORMATION DENSITY
======================================================================

Desktop is primary.

Use compact controls.

Important variables should be visible
without opening multiple forms.

Advanced scientific settings:
collapsed.

Evidence:
drawer / tooltip.

Raw tables:
secondary analysis tab/drawer.

The user should feel relaxed,
not surrounded by equal-priority text.

Strong hierarchy:

1. scenario
2. pattern
3. decision
4. reason
5. evidence.

======================================================================
32. USER SHOULD NOT NEED TO UNDERSTAND OUR BACKEND
======================================================================

Do not expose raw technical complexity by default.

User should not need to understand:

HiGHS
LP variables
NetCDF
manifest hashes
FAO tables
CMIP6 file versions

to use the simulator.

Those remain available through:

KANIT / YÖNTEM.

The main interface speaks the language of:

region
crop
water
climate
energy
production
decision.

======================================================================
33. AI ROLE
======================================================================

Do NOT call mathematical optimization AI.

Core engine:

MATHEMATICAL OPTIMIZATION / DECISION SUPPORT.

Actual future AI/ML candidates:

- PWN anomaly detection,
- adaptive sampling,
- model residual correction,
- uncertainty calibration,
- learned crop-suitability model
  only if appropriate training data exist.

AI is a method when justified,
not the product identity.

======================================================================
34. FINAL PRODUCT FLOW
======================================================================

The final interview flow should be extremely simple.

-------------------------------------
DEMO 1 — KONYA
-------------------------------------

Open application.

Konya baseline automatically appears.

Say:

“Bu, kazanan projemizin gerçek pilot bölgesi.”

Click:

SU -20%.

Click:

ÜRÜN DESENİNİ HESAPLA.

Show:

CURRENT
→
RECOMMENDED PATTERN.

Explain one binding constraint.

-------------------------------------
DEMO 2 — TÜRKİYE
-------------------------------------

Select another region.

Its official baseline automatically appears.

Run the same engine.

Show:

same method,
different conditions,
different pattern.

This proves transfer.

-------------------------------------
DEMO 3 — FUTURE NORTH
-------------------------------------

Switch:

GELECEK / KUZEY.

The app automatically loads:

future climate
candidate crops
known land/water context
available evidence.

Choose planning objective.

Click:

GELECEĞİN ÜRETİM DESENİNİ HESAPLA.

Show:

crop pattern
+
method
+
water source
+
resource use.

-------------------------------------
DEMO 4 — WHY TASE?
-------------------------------------

Click:

SAHA ARAŞTIRMASI.

Show:

“Kararı etkileyen ama saha gözlemi gerektiren
değişkenler bunlar.”

Show PWN / sample plan.

Then show an explicitly simulated
field-update demonstration:

MODEL VALUE
→
OBSERVATION
→
SAME ENGINE
→
decision changes / does not change.

Make clear the observation is simulated
until real TASE data exist.

======================================================================
35. PROJECT CONTINUITY STORY
======================================================================

The complete project lifecycle:

SEBEP

Climate change changes:
production suitability
and water reliability.

↓

GELİŞME 1

Konya:
Crop Pattern optimization.

↓

GELİŞME 2

Türkiye:
Regional simulator.

↓

GELİŞME 3

Future North:
Production System Pattern.

↓

GELİŞME 4

TASE:
real observations / physical samples.

↓

GELİŞME 5

Post-TASE:
same model with field evidence.

↓

GELİŞME 6

Controlled agriculture / hydroponic pilot:
real water + energy + production data.

↓

SONUÇ

A living,
field-updatable,
evidence-traceable
water-and-production decision-support platform.

Possible later research/application branches:

public planning
regional agriculture
farmer planning
climate-risk indicators
agricultural insurance research.

Do not implement insurance pricing now.

======================================================================
36. UPDATE THE SCIENTIFIC QUESTIONS
======================================================================

Preserve / refine the project around these questions:

RQ1
Under future climate conditions,
which climatically possible production options
remain feasible after water, land and energy constraints?

RQ2
What crop + production method + water-source pattern
best meets the selected transparent planning objective?

RQ3
Which uncertainties have the greatest effect
on that decision?

RQ4
For variables measurable during TASE,
how much does actual field observation alter
model error, uncertainty and/or the resulting decision?

RQ5 — CONTINUATION
When a controlled-production option is recommended,
how accurately do real pilot greenhouse/hydroponic
water, energy and yield measurements
match model assumptions?

RQ5 is future continuation,
not required before the interview.

======================================================================
37. DO NOT OVERCLAIM THE ARCTIC CONNECTION
======================================================================

Never state:

“TASE proves future Arctic agriculture.”

“TASE measures 2050 water supply.”

“PWN measures all agricultural water.”

“raw seawater will be used directly for crops.”

“We will grow the whole proposed crop pattern on the ship.”

Instead:

TASE provides real field evidence
for specific present-day physical water-system variables
that are used to evaluate model assumptions
and relevant water-source scenarios.

======================================================================
38. IMPLEMENTATION PRIORITY
======================================================================

Do NOT spend the next work period adding more random datasets or screens.

Priority:

1. Lock FINAL_PRODUCT_CONTRACT.md.
2. Simplify primary UX to the model described above.
3. Remove unnecessary input burden from Future North.
4. Add planning-objective abstraction.
5. Make candidate crop filtering data-driven.
6. Make Future Production Pattern the hero result.
7. Implement decision sensitivity / field-information-value analysis.
8. Integrate the Research Mission / TASE drawer.
9. Preserve PRE/POST same-engine comparison.
10. Improve visual hierarchy / domain styling.
11. Preserve all provenance and tests.
12. Research only missing data that materially affect the decision.

======================================================================
39. DO NOT FAKE MISSING SCIENCE TO COMPLETE THE DESIGN
======================================================================

If Future North still lacks:

hydrology
permafrost
crop-specific local energy
treatment chemistry
yield
or another critical input,

the UI should say:

DATA NEEDED.

Do NOT fill the blank with a plausible-looking number.

But also:

do not expose 30 empty technical fields to the user.

The system should:

automatically use what is known,

clearly identify what is missing,

and show why it matters.

======================================================================
40. ACCEPTANCE TEST — PRODUCT
======================================================================

The product is acceptable only if a new person can understand this
without us explaining the interface.

TEST A — TÜRKİYE

Open Konya.

Immediately understand:
these are the current crops.

Click:
Su -20%.

Click one calculate button.

Immediately understand:
this is the recommended new pattern
and this is why.

TEST B — FUTURE NORTH

Switch Future North.

Immediately understand:
these are the scientifically selected candidate crops
and resource conditions.

Choose a planning objective.

Click calculate.

Immediately understand:

this is the proposed future production pattern,
these are the methods,
these are the water sources,
and these are the limitations.

TEST C — TASE

Click Field Research.

Immediately understand:

what is currently based on models,
what we could measure during TASE,
what instrument/sample would obtain it,
and how the same model will be rerun afterwards.

If these three tests fail,
the product is still wrong.

======================================================================
41. ACCEPTANCE TEST — SCIENCE
======================================================================

Also verify:

- no marine profile is treated as terrestrial annual water supply;
- no future climate value is presented as field observation;
- no assumption appears as sourced data;
- no mathematical optimization is called trained AI;
- no Arctic crop is called locally validated without evidence;
- no PWN result exists before physical measurement;
- no field sample analysis is claimed before lab confirmation;
- no PRE/POST difference is guaranteed;
- model agreement is accepted as a valid result.

======================================================================
42. REQUIRED DOCUMENT UPDATES
======================================================================

Create/update:

docs/FINAL_PRODUCT_CONTRACT.md

docs/ARCTIC_RESEARCH_PROGRAM.md
- Field Package A
- Field Package B
- Field Package C
- optional adaptive sampling

docs/FIELD_INFORMATION_VALUE.md

docs/SOURCE_WATER_TO_GROWTH_VALIDATION.md

docs/FUTURE_NORTH_DECISION_MODEL.md

docs/FINAL_SIMULATOR_UX.md

docs/PROJECT_CONTINUITY.md

docs/DEMO_PLAN.md

docs/INTERVIEW_STORY.md

docs/JURY_QA.md

docs/EVIDENCE_MAP.md

docs/BUILD_STATUS.md

docs/ANA_CHAT_TESLIM.txt

Do not create redundant copies if equivalent documents already exist.
Consolidate where sensible.

======================================================================
43. CURRENT PHYSICAL PWN WORK REMAINS PARALLEL
======================================================================

Do not block software work on hardware.

Physical track remains:

parts
→ bench tests
→ homogeneous water
→ stratified column
→ real CSV
→ importer
→ real profile.

Once real PWN tank data exist,
the app replaces the default explanatory simulation
with:

KENDİ ÖLÇÜMÜMÜZ — KONTROLLÜ TANK DENEYİ

where appropriate.

It is never labelled Arctic field data.

======================================================================
44. NEXT HANDOFF
======================================================================

Increment the cumulative handoff to:

TESLİM 005.

The handoff must answer clearly:

1. What is the product now?
2. What did you remove/simplify from the old UX?
3. How does Türkiye simulation now work?
4. How does Future North decide candidate crops automatically?
5. What planning objectives exist?
6. What is the calculated Future Production System Pattern?
7. What data support it?
8. What critical data are still missing?
9. What does the Decision Information Value analysis show?
10. Which high-impact unknowns can TASE actually measure?
11. What exactly will PWN measure?
12. What physical samples are planned and why?
13. What is PRE-TASE vs POST-TASE?
14. What is the post-expedition hydroponic/source-water validation plan?
15. How does the hydroponic/greenhouse pilot continue the project?
16. What UI/visual changes were made?
17. What tests passed?
18. What screenshots prove the three acceptance tests?
19. What must WE physically do next?
20. What still requires researcher/KARE/TASE feedback?

Also include screenshots for:

- Konya baseline
- Konya water-stress result
- Türkiye second-region result
- Future North Scenario Lab
- Future Production System Pattern
- Field Research / information-value view
- PRE vs POST observation comparison

======================================================================
45. FINAL RULE
======================================================================

Do not build more because “more features look impressive.”

Every element must answer one of four questions:

WHAT DO WE KNOW?

WHAT SHOULD WE PRODUCE?

WHAT DO WE STILL NEED TO KNOW?

WHAT WILL THE ARCTIC EXPEDITION ALLOW US TO TEST?

That is the final product.

Implement it now.