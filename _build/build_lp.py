# -*- coding: utf-8 -*-
"""765 kV paid-traffic landing page -> /765kv-landowner/index.html

Deliberately NOT an SEO page:
  * noindex,follow  (does not compete with /projects/*-765kv/ for the same terms)
  * kept out of sitemap.xml
  * no site nav — logo, phone and the form are the only exits
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chassis import head, FOOTER, FORM_SCRIPT, form_section
from mapmod import MAP_HEAD, map_section
import content as C
from build import VIEWER, ROOT

SLUG = "765kv-landowner"
URL = "https://nationalrow.com/765kv-landowner/"
TITLE = "Is Your Land on Oncor's 765 kV Route? | Free Senior Review | National ROW"
DESC = ("Texas approved 424 miles of Oncor 765 kV line on August 28, 2026. Check your address against the "
        "approved centerline in seconds, then have a senior consultant review what you are offered.")

LP_CSS = """
.lp-head{position:sticky;top:0;z-index:900;background:var(--navy);border-bottom:2px solid var(--gold);
  display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 22px;flex-wrap:wrap;}
.lp-head .brand-logo{display:block;width:132px;height:40px;background:url('/national-row-logo.png') left center/contain no-repeat;}
.lp-head .r{display:flex;align-items:center;gap:16px;flex-wrap:wrap;}
.lp-head .ph{color:var(--gold);font-weight:900;font-size:19px;text-decoration:none;white-space:nowrap;}
.lp-head .ph small{display:block;font-size:11px;font-weight:600;color:rgba(255,255,255,.62);letter-spacing:.3px;}
.lp-hero{background:linear-gradient(135deg,#0a1c33,#1a3a5c);color:#fff;padding:52px 22px 46px;text-align:center;}
.lp-hero .eyebrow{display:inline-block;background:rgba(201,162,39,.16);border:1px solid rgba(201,162,39,.5);
  color:var(--gold);font-weight:800;font-size:12.5px;letter-spacing:1.1px;text-transform:uppercase;padding:7px 15px;border-radius:3px;margin-bottom:20px;}
.lp-hero h1{color:#fff;font-size:clamp(27px,4.4vw,45px);line-height:1.14;margin:0 auto 18px;max-width:880px;}
.lp-hero h1 .gold{color:var(--gold);}
.lp-hero p.sub{color:rgba(255,255,255,.87);font-size:clamp(16px,1.9vw,19px);line-height:1.65;max-width:660px;margin:0 auto 26px;}
.lp-hero .acts{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;}
.lp-trust{background:#0d2340;color:rgba(255,255,255,.8);font-size:14px;padding:13px 22px;text-align:center;
  border-top:1px solid rgba(255,255,255,.08);}
.lp-trust b{color:var(--gold);}
.lp-get{padding:52px 22px;background:#fff;}
.lp-get .grid{max-width:1000px;margin:26px auto 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(258px,1fr));gap:22px;}
.lp-get .card{border:1px solid #e2e8f0;border-left:4px solid var(--gold);border-radius:5px;padding:22px 20px;background:#fbfcfd;}
.lp-get .card h3{font-size:17px;color:var(--navy);margin:0 0 9px;}
.lp-get .card p{font-size:15px;line-height:1.7;color:#475569;margin:0;}
.res{background:var(--navy);padding:56px 22px;}
.res h2{color:#fff;text-align:center;margin-bottom:8px;}
.res .lede{color:rgba(255,255,255,.7);text-align:center;font-size:16px;max-width:640px;margin:0 auto 30px;}
.res .rows{max-width:880px;margin:0 auto;display:grid;gap:16px;}
.res .row{background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.12);border-radius:6px;padding:20px 22px;
  display:grid;grid-template-columns:1fr auto;gap:14px;align-items:center;}
.res .where{color:rgba(255,255,255,.62);font-size:13px;letter-spacing:.7px;text-transform:uppercase;font-weight:700;margin-bottom:7px;}
.res .nums{color:#fff;font-size:clamp(19px,2.5vw,25px);font-weight:900;letter-spacing:-.3px;}
.res .nums .ar{color:var(--gold);margin:0 9px;}
.res .pct{background:var(--gold);color:var(--navy);font-weight:900;font-size:clamp(17px,2.2vw,22px);
  padding:9px 17px;border-radius:4px;white-space:nowrap;}
.res .biggest{color:rgba(255,255,255,.78);font-size:15px;line-height:1.7;max-width:880px;margin:18px auto 0;
  border-left:3px solid var(--gold);padding:4px 0 4px 16px;}
.res .fine{color:rgba(255,255,255,.5);font-size:12.5px;line-height:1.75;max-width:880px;margin:24px auto 0;}
.miss{background:#fbf7ec;padding:54px 22px;}
.miss ul{max-width:760px;margin:22px auto 0;padding:0;list-style:none;}
.miss li{background:#fff;border:1px solid #e6dcc2;border-radius:5px;padding:17px 20px;margin-bottom:12px;
  font-size:16px;line-height:1.7;color:#3d4a5c;}
.miss li b{color:var(--navy);display:block;margin-bottom:3px;font-size:16.5px;}
.lp-foot{background:#08182c;color:rgba(255,255,255,.5);font-size:13px;line-height:1.8;padding:34px 22px;text-align:center;}
.lp-foot a{color:rgba(255,255,255,.72);}
.lp-foot .nl{max-width:820px;margin:14px auto 0;font-size:12.5px;color:rgba(255,255,255,.42);}
@media(max-width:560px){.res .row{grid-template-columns:1fr;}.lp-head{padding:10px 16px;}.lp-head .ph{font-size:17px;}}
"""

RESULTS = [
    ("Utility easement &middot; Houston, TX", "$16,000", "$138,000", "+762%"),
    ("Utility easement &middot; Irving, TX",  "$12,000", "$50,000",  "+317%"),
]

def results_block():
    rows = "".join("""
    <div class="row">
      <div>
        <div class="where">%s</div>
        <div class="nums">%s<span class="ar">&rarr;</span>%s</div>
      </div>
      <div class="pct">%s</div>
    </div>""" % r for r in RESULTS)
    return """
<section class="res">
  <div class="container">
    <h2>Our documented results</h2>
    <p class="lede">Both of these were utility easements &mdash; the same kind of taking Oncor is about to ask you for.</p>
    <div class="rows">%s</div>
    <p class="biggest">Our largest increase on file is <b style="color:#fff">+1,825%%</b> &mdash; an I&#8209;35 expansion taking in
      McLennan County that went from $20,000 to $385,000. That one was a highway condemnation rather than a utility easement,
      but the reason the number moved was the same: the agency's appraisal left value out.</p>
    <p class="fine">Individual documented matters, each traced from the original offer letter through to final settlement.
      They are not a forecast and not a promise. What any particular property is worth depends on the land, the taking,
      the remainder and the agency involved, and some offers are already fair. National ROW is a right-of-way consulting
      firm, not a law firm; nothing here is legal advice.</p>
  </div>
</section>
"""


def build():
    schema = {
      "@context": "https://schema.org",
      "@type": "Service",
      "name": "765 kV Transmission Easement Review for Texas Landowners",
      "serviceType": "Right-of-way and condemnation consulting",
      "provider": {"@type": "Organization", "name": "National ROW", "url": "https://nationalrow.com",
                   "telephone": "+1-469-484-7960"},
      "areaServed": {"@type": "State", "name": "Texas"},
      "description": DESC,
    }

    b = []
    b.append(head(TITLE, DESC, URL, json.dumps(schema, indent=2),
                  extra_head=MAP_HEAD + '<meta name="robots" content="noindex,follow">\n<style>%s</style>' % LP_CSS))

    b.append("""
<header class="lp-head">
  <a href="/" aria-label="National ROW"><span class="brand-logo"></span></a>
  <div class="r">
    <a class="ph" href="tel:+14694847960">(469) 484-7960<small>SPEAK TO A SENIOR CONSULTANT</small></a>
    <a class="btn-gold" href="#contact">Free senior review &rarr;</a>
  </div>
</header>

<section class="lp-hero">
  <div class="container">
    <span class="eyebrow">424 miles approved &middot; August 28, 2026</span>
    <h1>Oncor's 765 kV line is coming through 21 Texas counties.<br><span class="gold">Find out if it crosses your land.</span></h1>
    <p class="sub">Type your address below and we will measure it against the approved centerline &mdash; the actual route
      the PUCT signed off on, not an estimate. Then a senior consultant will tell you what the easement is worth
      before you are asked to sign anything.</p>
    <div class="acts">
      <a class="btn-gold" href="#corridor-check">Check my address &rarr;</a>
      <a class="btn-outline" href="tel:+14694847960">Or call (469) 484-7960</a>
    </div>
  </div>
</section>
<div class="lp-trust">On the property owner's side since the 1980s &nbsp;&middot;&nbsp; <b>We never represent the condemning agency</b>
  &nbsp;&middot;&nbsp; No upfront cost</div>
""")

    b.append('<div id="corridor-check"></div>')
    b.append(map_section(
        [1015, 1019],
        "Is your property on an approved 765 kV route?",
        "The gold line is the centerline the PUCT approved. Dashed grey lines are routes that were studied and not "
        "selected. Enter an address and we will tell you how far your property sits from the approved line, and which "
        "docket it falls under.",
        VIEWER, None, [31.6, -100.4], 7))

    b.append("""
<section class="lp-get">
  <div class="container">
    <h2 style="text-align:center;">What you actually get</h2>
    <div class="grid">
      <div class="card"><h3>A senior consultant, not a call centre</h3>
        <p>A senior consultant reads every one of these and calls you back within the hour, 8am&ndash;6pm Central,
           Monday to Friday. Outside those hours, first thing the next morning.</p></div>
      <div class="card"><h3>What their number left out</h3>
        <p>Easement acreage, damage to the remainder, access, temporary workspace, and the things agency appraisals
           routinely undercount. We tell you where the value is.</p></div>
      <div class="card"><h3>Nothing out of pocket</h3>
        <p>We are paid out of the increase. If we look at your situation and do not believe we can move the number,
           we tell you that too &mdash; and you owe nothing either way.</p></div>
    </div>
  </div>
</section>
""")

    b.append(C.cta_band(
        "You do not have to wait for the letter.",
        "Right-of-way agents are working these two routes now. The best time to understand what your land is worth is "
        "before the first offer is in front of you with a signature line under it.",
        "Get my free senior review &rarr;", "#contact"))

    b.append(results_block())

    b.append("""
<section class="miss">
  <div class="container">
    <h2 style="text-align:center;">What a first offer usually leaves out</h2>
    <ul>
      <li><b>Damage to the remainder</b>A 200-foot corridor does not just take the acres under it. It splits fields,
        strands corners, moves your building envelope and follows you into every future appraisal of the whole tract.</li>
      <li><b>Access and crossings</b>Where they can enter, how often, which roads they build, who maintains them, and
        whether you can still cross your own easement with equipment.</li>
      <li><b>Temporary construction easement</b>Work space outside the permanent corridor is a separate taking with its
        own value, and it is frequently folded in for free.</li>
      <li><b>The easement language itself</b>Width, height, vegetation control, future additional circuits, assignment
        to third parties. The document outlives the cheque by decades.</li>
    </ul>
  </div>
</section>
""")

    b.append(C.cta_band(
        "Already have an offer letter in hand?",
        "Send it over with their appraisal if they gave you one &mdash; a photo of the pages is enough. A senior "
        "consultant reads it and tells you what their number left out and whether it can be moved.",
        "Have a senior consultant read it &rarr;", "#contact"))

    fs = form_section("765 kV Landing Page", "Free senior review &mdash; Oncor 765 kV")
    fs = fs.replace('<input type="hidden" name="_template" value="table">',
                    '<input type="hidden" name="_template" value="table">\n'
                    '          <input type="hidden" name="source" value="765kv_lp">')
    b.append(fs)

    b.append("""
<footer class="lp-foot">
  <div class="container">
    <p><b style="color:rgba(255,255,255,.8)">National ROW</b> &middot; Nationwide service, HQ in Texas<br>
      <a href="tel:+14694847960">(469) 484-7960</a> &nbsp;&middot;&nbsp;
      <a href="tel:+19563634144">(956) 363-4144</a> &nbsp;&middot;&nbsp;
      <a href="mailto:info@nationalrow.com">info@nationalrow.com</a></p>
    <p class="nl">National ROW is a right-of-way and condemnation consulting firm representing property owners. We are not
      a law firm, we do not provide legal advice, and contacting us does not create an attorney-client relationship.
      When a matter needs condemnation counsel we say so and coordinate with an independent licensed attorney.
      Route geometry shown on this page is published by Oncor Electric Delivery; confirm against the official filings
      before relying on it. &nbsp;<a href="/privacy-policy/">Privacy</a></p>
  </div>
</footer>
""")
    b.append(FORM_SCRIPT)
    b.append("</body>\n</html>")

    out = os.path.join(ROOT, SLUG)
    os.makedirs(out, exist_ok=True)
    html = "\n".join(b)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print((URL, len(html)))


if __name__ == "__main__":
    build()
