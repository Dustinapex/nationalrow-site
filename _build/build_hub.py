# -*- coding: utf-8 -*-
import json, os, sys, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chassis import head, TOPBAR_NAV, FOOTER, FORM_SCRIPT, form_section
from mapmod import MAP_HEAD, map_section
import content as C
from build import SEG, UPDATED, UPDATED_H, VIEWER, ROOT

SLUG = "ercot-765kv"
URL = "https://nationalrow.com/projects/ercot-765kv/"
TITLE = "Texas 765 kV Transmission Buildout — Approved Routes, Counties & Landowner Rights"
DESC = ("Texas is getting its first 765 kV transmission lines. The PUCT approved 424 miles of Oncor 765 kV line "
        "on August 28, 2026. See the approved routes, the 21 counties affected, and what the easement offer will look like.")

FAQ = [
 ("What is a 765 kV line and why is Texas building them now?",
  "765 kilovolts is the highest transmission voltage in common use in North America. Texas has run its grid backbone at 345 kV since the 1960s. The move to 765 kV is driven by load growth in West Texas — oil and gas electrification in the Permian Basin plus data centers and cryptocurrency mining — and by the fact that one 765 kV line moves roughly the power of three double-circuit 345 kV lines in a corridor about 200 feet wide instead of roughly 480 feet."),
 ("Which 765 kV projects have actually been approved?",
  "As of September 2026, the Public Utility Commission of Texas has approved two Oncor 765 kV projects, both on August 28, 2026: Dinosaur Switch to Longshore Switch (Docket 59315, Route 559, 242.6 miles) and Longshore Switch to Drill Hole Switch (Docket 59029, Route 476, 181.6 miles). Together that is 424 miles across 21 counties. Additional 765 kV segments, including Big Hill to Sand Lake, have been filed but not yet decided."),
 ("How much land does a 765 kV line take?",
  "Oncor specifies a 200-foot permanent right-of-way for its 765 kV lines, which is about 24.2 acres per mile. Across the 424 approved miles that is roughly 10,300 acres of private Texas land placed under permanent easement."),
 ("How do I find out if my property is on a route?",
  "Use the map on this page or on the individual project page, and confirm against Oncor's official interactive viewer and the filed constraints maps, which we link in the sources. If you have already received a letter, the project name is on it. If you are not sure which project a letter belongs to, send it to us and we will identify it."),
 ("Can I stop the line from crossing my property?",
  "Realistically, no. Once the PUCT has approved a route, the utility holds the power of eminent domain and the line will be built. Route selection is the phase where landowner input changes outcomes, and that phase is over for these two projects. What is still open — and it is worth real money — is what you are paid and what the easement document actually says."),
 ("Is National ROW a law firm?",
  "No. National ROW is a right-of-way and condemnation consulting firm representing property owners only. We do not provide legal advice and no attorney-client relationship is created by contacting us. When a case needs a lawyer, we say so and coordinate with condemnation counsel."),
]


def seg_card(slug, s):
    ac = int(round(s["miles"] * C.ACRES_PER_MILE))
    return """
<div class="seg-card">
  <div class="docket">PUCT Docket %s · Approved Aug 28, 2026</div>
  <h3>%s</h3>
  <p style="font-size:15px;color:#4b5563;line-height:1.7;">%s to %s.</p>
  <ul class="grow">
    <li>Approved route <b>Route %s</b></li>
    <li>Length <b>%s miles</b></li>
    <li>Counties crossed <b>%d</b></li>
    <li>Land under easement <b>~%s acres</b></li>
    <li>Estimated cost <b>%s</b></li>
    <li>Target in service <b>%s</b></li>
  </ul>
  <p style="font-size:13px;color:#64748b;line-height:1.6;margin-bottom:16px;"><strong style="color:#0d2340">Counties:</strong> %s</p>
  <a class="btn-gold" href="/projects/%s/" style="text-align:center;">Full project page &amp; route map →</a>
</div>""" % (s["docket"], s["short"], s["from_pt"][0].upper() + s["from_pt"][1:], s["to_pt"],
             s["route_no"], s["miles"], len(s["counties"]), "{:,}".format(ac),
             s["cost"], s["in_service"], ", ".join(sorted(s["counties"])), slug)


def build():
    schema_g = [
      {"@context":"https://schema.org","@type":"Article","headline":TITLE,"description":DESC,"url":URL,
       "datePublished":UPDATED,"dateModified":UPDATED,
       "author":{"@type":"Organization","name":"National ROW","url":"https://nationalrow.com/"},
       "publisher":{"@type":"Organization","name":"National ROW","url":"https://nationalrow.com/",
                    "logo":{"@type":"ImageObject","url":"https://nationalrow.com/national-row-logo.png"}}},
      {"@context":"https://schema.org","@type":"FAQPage",
       "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Projects","item":"https://nationalrow.com/projects/"},
        {"@type":"ListItem","position":2,"name":"Texas 765 kV Transmission","item":URL}]},
    ]

    all_counties = sorted(set(SEG["dinosaur-longshore-765kv"]["counties"]) |
                          set(SEG["longshore-drill-hole-765kv"]["counties"]))
    total_ac = int(round(424.2 * C.ACRES_PER_MILE))

    b = [TOPBAR_NAV]
    b.append('<div class="alert-banner">⚡ 424 miles of Texas 765 kV line approved August 28, 2026 — right-of-way acquisition is beginning across 21 counties.</div>')

    b.append("""
<section class="hero">
  <div class="container">
    <div class="hero-badge">Texas 765 kV Buildout · Updated %s</div>
    <h1>Texas Is Building Its First 765 kV Lines.<br><span class="gold">424 Miles Are Approved. Acquisition Starts Now.</span></h1>
    <div class="hero-accent"></div>
    <p class="hero-sub">On August 28, 2026 the Public Utility Commission of Texas approved two Oncor 765-kilovolt transmission projects running from Somervell County to the Culberson–Reeves county line. This page tracks what has been approved, which counties are affected, and what landowners in the corridor should expect next. We update it as the dockets move.</p>
    <div class="hero-btns">
      <a class="btn-gold" href="#segments">See the approved projects</a>
      <a class="btn-outline" href="#map">Check my property</a>
    </div>
    <div class="stats-row">
      <div class="stat"><div class="stat-num">424</div><div class="stat-label">Miles approved</div></div>
      <div class="stat"><div class="stat-num">21</div><div class="stat-label">Texas counties</div></div>
      <div class="stat"><div class="stat-num">~%s</div><div class="stat-label">Acres under permanent easement</div></div>
      <div class="stat"><div class="stat-num">$3.9B</div><div class="stat-label">Combined estimated cost</div></div>
    </div>
  </div>
</section>""" % (UPDATED_H, "{:,}".format(total_ac)))

    b.append("""
<section id="segments">
  <div class="container">
    <h2>The two approved projects</h2>
    <p class="section-sub">Both were approved on the same day, by the same order date, and they connect end to end at Longshore Switch in Howard County. If you own land anywhere along this corridor, one of these is yours.</p>
    <div class="seg-grid">%s%s</div>
  </div>
</section>""" % (seg_card("dinosaur-longshore-765kv", SEG["dinosaur-longshore-765kv"]),
                 seg_card("longshore-drill-hole-765kv", SEG["longshore-drill-hole-765kv"])))

    b.append(map_section([1015, 1019],
        "Both approved routes on one map",
        "Gold is what the PUCT approved. Dashed grey is what was studied and not selected. Enter an address to see roughly how far your property sits from the approved centerline. For the detail on a single project — timeline, offer anatomy, sources — open its own page above.",
        VIEWER, SEG["dinosaur-longshore-765kv"]["constraints"], "[32.05, -101.0]", 7))

    b.append("""
<section>
  <div class="container">
    <h2>Every county in the corridor</h2>
    <p class="section-sub">Twenty-one Texas counties, from the Brazos country west of Fort Worth all the way to the Permian Basin.</p>
    %s
  </div>
</section>""" % C.county_grid(all_counties))

    b.append("""
<section class="section-alt">
  <div class="container container-narrow prose">
    <h2>Why 765 kV, and why now</h2>
    <p>Texas has run its transmission backbone at 345 kilovolts since the 1960s. Nothing about that changed until the load did. Two things are happening at once in West Texas: the oil and gas industry is electrifying operations that used to run on gas engines, and an entirely separate wave of demand — data centers, cryptocurrency mining, industrial load — has arrived in places that never had it. ERCOT's planning work and the Permian Basin Reliability Plan both concluded the existing network cannot move that much power.</p>
    <p>The case for 765 kV is a land-use case as much as an engineering one. By Oncor's published figures, one 765 kV line carries the capacity of three double-circuit 345 kV lines. Doing the same job at 345 kV would take roughly 480 feet of corridor; the 765 kV line takes 200. Fewer corridors, fewer landowners affected in total — but each one affected more.</p>
    <p>This is Texas's first major voltage step in sixty years, and the technology itself is not experimental: there are more than 2,400 miles of 765 kV line already operating in the U.S. and Canada.</p>

    <h3>What this means if you are in the corridor</h3>
    <p>It means the line is going to be built. Landowners, county governments and conservation groups filed extensive protests in both dockets. The Texas Attorney General filed an amicus brief asking the Commission to hold off pending legislative review. The Commission approved both projects anyway, unanimously.</p>
    <p>We say that plainly because the alternative — telling you there is a fight left over whether the line crosses your place — would waste the months when you actually have leverage. Route selection is over. <strong>Compensation is not.</strong> That is where the remaining money is, and it is a lot of money: the difference between an offer that prices only the strip and one that properly accounts for severance damages and cost to cure is routinely a multiple, not a percentage.</p>
    <div class="urgency-box"><strong>The one thing to do right now:</strong> if a land agent has contacted you, do not sign the survey permission form until someone independent has read it. It is a legal document with negotiable terms, and signing the version they hand you gives away things you cannot get back.</div>
  </div>
</section>""")

    b.append("""
<section>
  <div class="container container-narrow prose">
    <h2>What is coming after these two</h2>
    <p>These two projects are not the end of it. Oncor's own public certificate mapping currently tracks twenty transmission projects — about half already filed with the Commission and about half still in the study phase where routes are being drawn. A third 765 kV segment, Big Hill to Sand Lake, has been filed and is awaiting decision.</p>
    <p>Practically, that means two different situations, and they call for two different responses:</p>
    <ul>
      <li><strong>If your land is on an approved route</strong> — Dinosaur–Longshore or Longshore–Drill Hole — your window is the compensation window. Survey permission, appraisal, offer.</li>
      <li><strong>If your land is in a study area or on a filed but undecided route</strong> — you still have the routing window, and it is genuinely worth using. Landowner comments and protests do move routes, and they moved several in these dockets. It is much cheaper to be routed around than to be paid for.</li>
    </ul>
    <p>We track the dockets either way. If you tell us where your property is, we will tell you which of these you are in.</p>
  </div>
</section>""")

    b.append(C.EASEMENT_COST)
    b.append(C.cta_band(
        "Want to know what your acreage is actually worth on this route?",
        "A senior consultant will walk your numbers with you &mdash; the easement acreage, what it does to the remainder, "
        "and the value the first offer tends to leave on the table. No cost and no obligation.",
        "Get my free senior review &rarr;", "#contact"))
    b.append(C.OFFER_ANATOMY)
    b.append(C.cta_band(
        "Not contacted yet? This is the best time to call.",
        "A senior consultant reads every one of these. Knowing what the first offer will look like <em>before</em> it "
        "lands is worth far more than anything you can do after you have signed something.",
        "Talk to a senior consultant &rarr;", "#contact"))
    b.append(C.DAMAGES)
    b.append(C.cta_band(
        "Already holding an offer letter?",
        "Send it over with their appraisal if they gave you one &mdash; a photo of the pages is enough. A senior consultant "
        "reads it and tells you what their number left out, what we would argue for, and whether it can be moved.",
        "Get my free senior review &rarr;", "/offer-review/?project=%s" % "Texas%20765kV"))
    b.append(C.HOW)
    b.append(C.cta_band(
        "Nothing out of pocket. Ever.",
        "A senior consultant reads every case that comes in and calls you back. If we look at your situation and do not "
        "think we can move the number, we tell you that too.",
        "Start my free senior review &rarr;", "#contact"))

    faq_html = "".join('<div class="faq-item"><h4>%s</h4><p>%s</p></div>' % (q, a) for q, a in FAQ)
    b.append('<section><div class="container container-narrow"><h2>Frequently asked questions</h2>%s</div></section>' % faq_html)

    b.append(C.handoff("Texas%20765kV",
        "Not sure which project your letter is about?",
        "Send it to us. We will tell you which docket it belongs to, where you sit on the route, and whether what they are offering is in the range it should be. Free, no obligation."))

    b.append(C.sources_block([
      'Public Utility Commission of Texas, Docket No. 59315 — <a href="%s" target="_blank" rel="noopener">order approving Oncor\'s Dinosaur–Longshore application (PDF)</a>, August 28, 2026.' % SEG["dinosaur-longshore-765kv"]["order_url"],
      'Public Utility Commission of Texas, Docket No. 59029 — <a href="%s" target="_blank" rel="noopener">order approving Oncor\'s Longshore–Drill Hole application (PDF)</a>, August 28, 2026.' % SEG["longshore-drill-hole-765kv"]["order_url"],
      'Oncor Electric Delivery — <a href="%s" target="_blank" rel="noopener">Dinosaur–Longshore project page</a> and <a href="%s" target="_blank" rel="noopener">Longshore–Drill Hole project page</a>.' % (SEG["dinosaur-longshore-765kv"]["oncor_url"], SEG["longshore-drill-hole-765kv"]["oncor_url"]),
      'Oncor Electric Delivery — <a href="%s" target="_blank" rel="noopener">public certificate-of-convenience-and-necessity map viewer</a> (approved and studied route geometry, project tract mapping).' % VIEWER,
      'Oncor Electric Delivery — 765 kV overview, June 2026: <a href="https://www.oncor.com/content/dam/oncorwww/documents/about-us/transmission-system/updated-step-one-pager/Oncor%20765kV%20One-Pager_June2026.pdf" target="_blank" rel="noopener">right-of-way width, capacity comparison, and existing 765 kV mileage in North America (PDF)</a>.',
      'The Dallas Express — <a href="https://dallasexpress.com/business-markets/texas-regulators-approve-424-miles-of-power-lines-despite-calls-to-wait/" target="_blank" rel="noopener">"Texas Regulators Approve 424 Miles Of Power Lines Despite Calls To Wait"</a>, August 30, 2026 (mileage, cost, and the Attorney General\'s amicus filing).',
      'Texas Landowner’s Bill of Rights — <a href="https://www2.texasattorneygeneral.gov/agency/landowners-bill-of-rights" target="_blank" rel="noopener">Office of the Texas Attorney General</a>.',
    ]))

    b.append(form_section("Texas 765kV", "Free review — Texas 765 kV corridor"))
    b.append(FOOTER)
    b.append(FORM_SCRIPT)
    b.append("</body>\n</html>")

    html = head(TITLE, DESC, URL, json.dumps(schema_g, ensure_ascii=False), MAP_HEAD) + "\n".join(b)
    out = os.path.join(ROOT, "projects", SLUG)
    os.makedirs(out, exist_ok=True)
    with io.open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return URL, len(html)


if __name__ == "__main__":
    print(build())
