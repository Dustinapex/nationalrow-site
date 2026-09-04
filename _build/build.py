# -*- coding: utf-8 -*-
import json, os, sys, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chassis import head, TOPBAR_NAV, FOOTER, FORM_SCRIPT, form_section
from mapmod import MAP_HEAD, map_section
import content as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = "2026-09-04"
UPDATED_H = "September 4, 2026"

VIEWER = "https://experience.arcgis.com/experience/2a2ca9b3206a4bfbbd1ae875e8abb9d7"

SEG = {
  "dinosaur-longshore-765kv": dict(
    pid=1015,
    name="Dinosaur Switch – Longshore Switch 765 kV",
    short="Dinosaur–Longshore 765 kV",
    param="Dinosaur-Longshore%20765kV",
    param_plain="Dinosaur-Longshore 765kV",
    docket="59315",
    order_url="https://interchange.puc.texas.gov/Documents/59315_5819_1678289.PDF",
    filings_url="https://interchange.puc.texas.gov/search/filings/?UtilityType=A&ControlNumber=59315&ItemMatch=Equal&DocumentType=ALL&SortOrder=Ascending",
    oncor_url="https://www.oncor.com/content/oncorwww/us/en/home/about-us/transmission-systems/current-transmission-line-projects/dinosaur-to-longshore-765-kv-transmission-line-project.html",
    viewer=VIEWER + "/page/Dinosaur_Longshore",
    constraints="https://www.oncor.com/content/dam/oncorwww/documents/about-us/transmission-system/current-trasmission-line-projects/dinosaur-%E2%80%93-longshore-765-kv-transmission-line-project/updated-maps/Dinosaur%20-%20Longshore%20Filing%20Constraint%20Map%202.11.2026.pdf",
    filed="February 19, 2026",
    route_no="559",
    miles=242.6,
    cost="$2.24 billion",
    in_service="2028",
    from_pt="Dinosaur Switch, about 3 miles north of Glen Rose in Somervell County",
    to_pt="Longshore Switch, about 4.5 miles west of Forsan in Howard County",
    counties=["Somervell","Hood","Erath","Comanche","Brown","Callahan","Coleman",
              "Taylor","Runnels","Coke","Sterling","Glasscock","Howard"],
    tracts=500,
    oncor_phone="214.486.5841",
    meetings=[("June 2, 2025","Big Spring — Ryan Hall"),
              ("June 3, 2025","Sweetwater — Marqueza Conference Center"),
              ("June 4, 2025","Stephenville — Cross Timbers Legacy Center")],
    center="[32.14, -99.6]", zoom=8,
    aliases="Also searched as: Oncor 765 kV Glen Rose, Dinosaur to Longshore power line, ERCOT 765 kV Somervell County, Big Spring transmission line.",
  ),
  "longshore-drill-hole-765kv": dict(
    pid=1019,
    name="Longshore Switch – Drill Hole Switch 765 kV",
    short="Longshore–Drill Hole 765 kV",
    param="Longshore-DrillHole%20765kV",
    param_plain="Longshore-DrillHole 765kV",
    docket="59029",
    order_url="https://interchange.puc.texas.gov/Documents/59029_503_1678287.PDF",
    filings_url="https://interchange.puc.texas.gov/search/filings/?UtilityType=A&ControlNumber=59029&ItemMatch=Equal&DocumentType=ALL&SortOrder=Ascending",
    oncor_url="https://www.oncor.com/content/oncorwww/us/en/home/about-us/transmission-systems/current-transmission-line-projects/longshore-switch---drill-hole-switch-765-kv-transmission-line-pr.html",
    viewer=VIEWER + "/page/Longshore_DrillHole",
    constraints="https://www.oncor.com/content/dam/oncorwww/documents/about-us/transmission-system/current-trasmission-line-projects/longshore-switch-%E2%80%93-drill-hole-switch-765-kv-transmission-line-project/update-map/Longshore%20-%20Drill%20Hole%20Filing%20Appendix%20G%20Constraints%20Map%2011.26.25.pdf",
    filed="December 11, 2025",
    route_no="476",
    miles=181.6,
    cost="$1.70 billion",
    in_service="2029",
    from_pt="Longshore Switch, about 4.5 miles west of Forsan in Howard County",
    to_pt="Drill Hole Switch, about 6 miles west of US 285 near the Culberson–Reeves county line",
    counties=["Howard","Martin","Andrews","Ector","Winkler","Loving","Reeves","Culberson"],
    tracts=200,
    oncor_phone="469-822-6787",
    meetings=[("May 19, 2025","Big Spring — Ryan Hall"),
              ("May 20, 2025","Odessa — Lawndale Community Center"),
              ("May 21, 2025","Kermit — Kermit Civic Center")],
    center="[31.98, -102.8]", zoom=8,
    aliases="Also searched as: Oncor 765 kV Permian Basin, Longshore to Drill Hole power line, 765 kV Reeves County, Odessa transmission line right of way.",
  ),
}


def faqs(s):
    ac = int(round(s["miles"] * C.ACRES_PER_MILE))
    return [
      ("Has this route been approved, or can it still change?",
       "The Public Utility Commission of Texas approved Route %s for this project on August 28, 2026, in Docket No. %s. The corridor is settled. The exact centerline can still shift somewhat within the approved corridor when Oncor completes final survey and engineering, so a property near the edge of the corridor should confirm its status directly." % (s["route_no"], s["docket"])),
      ("How wide is the easement and how much of my land does it take?",
       "Oncor specifies a 200-foot right-of-way for its 765 kV lines. That works out to about 24.2 acres for every mile of line. Across the full %s-mile route that is roughly %s acres of private land placed under permanent easement." % (s["miles"], "{:,}".format(ac))),
      ("Do I have to let them survey my property?",
       "A land agent will ask you to sign a survey permission form. That form is a negotiable legal document — its scope, notice requirements, what happens to gates and fences, and who pays for damage are all terms you can change. You are not required to sign it the day it is handed to you, and refusing to sign immediately does not forfeit any right. Have it reviewed first."),
      ("Do I have to accept the offer they make?",
       "No. A written offer is an opening position. Under Texas law a condemning entity must make a bona fide offer and deliver the Texas Landowner's Bill of Rights before it can condemn, and you are entitled to just compensation — which includes the value of the part taken plus damages to the remainder of your property. Most offers can be negotiated. The response deadline in the letter is the utility's schedule, not a legal cutoff on your rights."),
      ("Can they take my land if I say no?",
       "Ultimately, yes. A utility holding a certificate from the PUCT has the power of eminent domain, so the question is almost never whether the line gets built — it is how much you are paid and on what terms. That is exactly why the negotiation matters, and why what goes into the easement document matters as much as the dollar figure."),
      ("What is my property actually worth to them?",
       "It depends on the part acquired, what the corridor does to the rest of your property, and what it costs to fix what the taking breaks. Two neighbors with identical acreage can be owed very different amounts because one loses a pivot circle and a field road and the other loses a strip of pasture along a fence line. Anyone who quotes you a per-acre rate without seeing your property is guessing."),
      ("How long do I have?",
       "There is no single deadline, but the practical answer is that your leverage is highest before you sign anything and drops sharply afterward. Survey permission, the appraisal, and the written offer all happen over a period of months. Once an easement is executed it runs with the land permanently and is extremely difficult to modify."),
      ("Is National ROW a law firm?",
       "No. National ROW is a right-of-way and condemnation consulting firm, and we represent property owners only — never the utility. We do not provide legal advice and no attorney-client relationship is created by contacting us. Much of what this process requires is valuation and negotiation work. When a case needs a lawyer, we say so and coordinate with condemnation counsel."),
      ("What does it cost to have you look at my offer?",
       "The review is free. If you engage us, we work on contingency — our fee is a percentage of the increase we secure above the original offer. If we do not improve your offer, you owe us nothing."),
      ("Where can I read the actual filings myself?",
       "Everything is public. The complete docket, including Oncor's application, the routing study, landowner protests and the final order, is on the PUCT Interchange under Control Number %s. We link to it directly in the sources at the bottom of this page, and we encourage you to read it." % s["docket"]),
    ]


def schema(s, url, title, desc, fq):
    g = [
      {"@context":"https://schema.org","@type":"Article",
       "headline":title,"description":desc,"url":url,
       "datePublished":UPDATED,"dateModified":UPDATED,
       "author":{"@type":"Organization","name":"National ROW","url":"https://nationalrow.com/"},
       "publisher":{"@type":"Organization","name":"National ROW","url":"https://nationalrow.com/",
                    "logo":{"@type":"ImageObject","url":"https://nationalrow.com/national-row-logo.png"}},
       "about":{"@type":"Thing","name":s["name"]},
       "isBasedOn":s["order_url"]},
      {"@context":"https://schema.org","@type":"FAQPage",
       "mainEntity":[{"@type":"Question","name":q,
                      "acceptedAnswer":{"@type":"Answer","text":a}} for q,a in fq]},
      {"@context":"https://schema.org","@type":"Service",
       "name":"Landowner representation — " + s["name"],
       "serviceType":"Eminent domain and right-of-way consulting for property owners",
       "provider":{"@type":"Organization","name":"National ROW","url":"https://nationalrow.com/",
                   "telephone":"+1-469-484-7960"},
       "areaServed":[{"@type":"AdministrativeArea","name":c + " County, Texas"} for c in sorted(s["counties"])],
       "url":url},
    ]
    return json.dumps(g, ensure_ascii=False, indent=None)


def build_segment(slug, s):
    url = "https://nationalrow.com/projects/%s/" % slug
    ac = int(round(s["miles"] * C.ACRES_PER_MILE))
    ncty = len(s["counties"])
    title = "%s — Docket %s | Approved Route, Counties & Landowner Rights" % (s["short"], s["docket"])
    desc = ("PUCT approved Route %s for Oncor's %s line on August 28, 2026 — %s miles across %d Texas counties. "
            "See the approved route map, check whether your property is in the corridor, and understand what the easement offer will and won't include."
            % (s["route_no"], s["short"], s["miles"], ncty))
    fq = faqs(s)

    body = []
    body.append(TOPBAR_NAV)
    body.append('<div class="alert-banner">⚡ Docket %s approved August 28, 2026 — right-of-way acquisition on this route is beginning now. Do not sign a survey form or an easement without an independent review.</div>' % s["docket"])

    # HERO
    body.append("""
<section class="hero">
  <div class="container">
    <div class="hero-badge">PUCT Docket %s · Route %s · Approved</div>
    <h1>The %s Line<br><span class="gold">Has Been Approved. Here Is What It Means For Your Land.</span></h1>
    <div class="hero-accent"></div>
    <p class="hero-sub">On August 28, 2026 the Public Utility Commission of Texas approved Oncor's %s-mile, 765-kilovolt transmission line from %s to %s. The route is set. Right-of-way acquisition across %d counties starts now. This page explains the project, shows you the approved route, and tells you plainly what the offer will look like when it arrives.</p>
    <div class="hero-btns">
      <a class="btn-gold" href="#map">See the approved route</a>
      <a class="btn-outline" href="#contact">Have us review your offer</a>
    </div>
    <div class="stats-row">
      <div class="stat"><div class="stat-num">%s</div><div class="stat-label">Miles of new 765 kV line</div></div>
      <div class="stat"><div class="stat-num">%d</div><div class="stat-label">Texas counties crossed</div></div>
      <div class="stat"><div class="stat-num">200 ft</div><div class="stat-label">Permanent easement width</div></div>
      <div class="stat"><div class="stat-num">~%s</div><div class="stat-label">Acres placed under easement</div></div>
    </div>
  </div>
</section>""" % (s["docket"], s["route_no"], s["short"], s["miles"], s["from_pt"], s["to_pt"],
                 ncty, s["miles"], ncty, "{:,}".format(ac)))

    # STATUS
    meetings = "<br>".join("%s — %s" % (d, p) for d, p in s["meetings"])
    body.append("""
<section>
  <div class="container container-narrow">
    <div class="status-block">
      <div class="status-head">
        <h3>Project status</h3>
        <span class="status-date">Last verified %s</span>
      </div>
      <span class="status-pill">Approved — ROW acquisition beginning</span>
      <table class="project-table">
        <tr><td>Official project name</td><td>%s Transmission Line Project</td></tr>
        <tr><td>Applicant</td><td>Oncor Electric Delivery Company LLC</td></tr>
        <tr><td>PUCT docket</td><td>No. %s &nbsp;·&nbsp; <a href="%s" target="_blank" rel="noopener">all filings</a></td></tr>
        <tr><td>Application filed</td><td>%s</td></tr>
        <tr><td>Approved</td><td>August 28, 2026 &nbsp;·&nbsp; <a href="%s" target="_blank" rel="noopener">read the order (PDF)</a></td></tr>
        <tr><td>Approved route</td><td>Route %s</td></tr>
        <tr><td>Length</td><td>%s miles</td></tr>
        <tr><td>From</td><td>%s</td></tr>
        <tr><td>To</td><td>%s</td></tr>
        <tr><td>Voltage &amp; structures</td><td>765 kV single circuit on self-supporting steel lattice towers</td></tr>
        <tr><td>Right-of-way width</td><td>200 feet (about 24.2 acres per mile)</td></tr>
        <tr><td>Estimated cost</td><td>%s</td></tr>
        <tr><td>Target in service</td><td>%s</td></tr>
        <tr><td>Oncor project line</td><td>%s</td></tr>
        <tr><td>Public meetings held</td><td>%s</td></tr>
      </table>
    </div>
    <p style="font-size:13px;color:#64748b;line-height:1.7;">%s</p>
  </div>
</section>""" % (UPDATED_H, s["name"], s["docket"], s["filings_url"], s["filed"], s["order_url"],
                 s["route_no"], s["miles"], s["from_pt"], s["to_pt"], s["cost"], s["in_service"],
                 s["oncor_phone"], meetings, s["aliases"]))

    # MAP
    body.append(map_section(
        [s["pid"]],
        "Is your property on the approved route?",
        "The gold line is the route the PUCT approved. The dashed grey lines are the alternative routes that were studied and not selected — useful if you were notified during the docket but are no longer on the chosen route. Enter an address to see roughly how far you are from the centerline.",
        s["viewer"], s["constraints"], s["center"], s["zoom"]))

    # COUNTIES
    body.append("""
<section>
  <div class="container">
    <h2>Counties on the approved route</h2>
    <p class="section-sub">The approved centerline crosses %d Texas counties. If your county is on this list and your property sits anywhere near the corridor, expect contact from a land agent.</p>
    %s
    <p style="font-size:14px;color:#64748b;margin-top:20px;line-height:1.7;">Measured against Oncor's own published tract mapping, the approved centerline crosses more than %d individual land tracts. Every one of those is a separate negotiation, and no two are worth the same.</p>
  </div>
</section>""" % (ncty, C.county_grid(s["counties"]), s["tracts"]))

    # WHY
    body.append("""
<section class="section-alt">
  <div class="container container-narrow prose">
    <h2>Why this line is being built</h2>
    <p>Texas has never had a 765-kilovolt transmission line. The state's backbone has been built at 345 kV since the 1960s. The push to 765 kV comes from a straightforward problem: West Texas is generating and consuming far more power than the existing network can move, and the load growth is not slowing down.</p>
    <p>The drivers the Commission cited are oil and gas electrification in the Permian Basin, plus rapid growth in load that has nothing to do with oil and gas — data centers and cryptocurrency mining in particular. The Permian Basin Reliability Plan and ERCOT's long-range planning work identified a 765 kV backbone as the way to move that power without carving up even more land: Oncor's published figures put one 765 kV line at the same capacity as three double-circuit 345 kV lines, in a 200-foot corridor instead of roughly 480 feet.</p>
    <p>That argument is a real one, and it is worth understanding, because it explains why opposition to the project as a whole has not succeeded. It also explains why the money conversation is the one that is still open. The line is going to be built. What each landowner is paid for it is not settled.</p>
    <div class="note-box">Landowners, county governments and conservation groups filed extensive protests in this docket, and the Texas Attorney General filed an amicus brief asking the Commission to wait for legislative review. The Commission approved the projects anyway. If you filed a protest and are wondering what happened, the order linked above is the answer, and it is worth reading.</div>
  </div>
</section>""")

    body.append(C.TIMELINE)
    body.append(C.EASEMENT_COST)
    body.append(C.OFFER_ANATOMY)
    body.append(C.DAMAGES)
    body.append(C.HOW)

    # FAQ
    faq_html = "".join('<div class="faq-item"><h4>%s</h4><p>%s</p></div>' % (q, a) for q, a in fq)
    body.append("""
<section>
  <div class="container container-narrow">
    <h2>Questions landowners on this project are asking</h2>
    %s
  </div>
</section>""" % faq_html)

    body.append(C.handoff(s["param"],
        "Send us what they sent you.",
        "Survey permission form, letter, appraisal, easement draft, offer — whatever stage you are at, we will read it and tell you where it is weak. Free, and there is no obligation to go further."))

    body.append(C.sources_block([
      'Public Utility Commission of Texas, Docket No. %s — <a href="%s" target="_blank" rel="noopener">order approving the application (PDF)</a>, signed August 28, 2026.' % (s["docket"], s["order_url"]),
      'Public Utility Commission of Texas — <a href="%s" target="_blank" rel="noopener">complete filings in Control Number %s</a>, PUCT Interchange.' % (s["filings_url"], s["docket"]),
      'Oncor Electric Delivery — <a href="%s" target="_blank" rel="noopener">%s project page</a> (project description, schedule, public meeting record, contact).' % (s["oncor_url"], s["short"]),
      'Oncor Electric Delivery — <a href="%s" target="_blank" rel="noopener">official interactive route map</a> and <a href="%s" target="_blank" rel="noopener">filed land use constraints map (PDF)</a>.' % (s["viewer"], s["constraints"]),
      'Oncor Electric Delivery — 765 kV overview, June 2026: <a href="https://www.oncor.com/content/dam/oncorwww/documents/about-us/transmission-system/updated-step-one-pager/Oncor%20765kV%20One-Pager_June2026.pdf" target="_blank" rel="noopener">right-of-way width and capacity comparison (PDF)</a>.',
      'Reported mileage and cost figures for both approved projects: The Dallas Express, <a href="https://dallasexpress.com/business-markets/texas-regulators-approve-424-miles-of-power-lines-despite-calls-to-wait/" target="_blank" rel="noopener">"Texas Regulators Approve 424 Miles Of Power Lines Despite Calls To Wait"</a>, August 30, 2026.',
      'Texas Landowner’s Bill of Rights — <a href="https://www2.texasattorneygeneral.gov/agency/landowners-bill-of-rights" target="_blank" rel="noopener">Office of the Texas Attorney General</a>.',
    ]))

    body.append('<section class="section-alt"><div class="container container-narrow prose"><h2>Related</h2><ul>'
        '<li><a href="/projects/ercot-765kv/">The Texas 765 kV buildout — both approved Oncor segments and what is coming next</a></li>'
        '<li><a href="/blog/damages-to-the-remainder/">What are damages to the remainder?</a></li>'
        '<li><a href="/blog/easement-vs-fee-taking/">Easement vs. fee taking — what is the difference?</a></li>'
        '<li><a href="/blog/transmission-line-easement-valuation-negotiation/">How transmission line easements are valued and negotiated</a></li>'
        '<li><a href="/blog/what-to-do-when-you-get-condemnation-notice/">What to do the day you get a condemnation notice</a></li>'
        '<li><a href="/states/texas/">Texas eminent domain — landowner overview</a></li>'
        '</ul></div></section>')

    body.append(form_section(s["param_plain"], "Free review — %s" % s["short"]))
    body.append(FOOTER)
    body.append(FORM_SCRIPT)
    body.append("</body>\n</html>")

    html = head(title, desc, url, schema(s, url, title, desc, fq), MAP_HEAD) + "\n".join(body)
    out = os.path.join(ROOT, "projects", slug)
    os.makedirs(out, exist_ok=True)
    with io.open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return url, len(html)


if __name__ == "__main__":
    for slug, s in SEG.items():
        print(build_segment(slug, s))
