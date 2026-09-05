# -*- coding: utf-8 -*-
"""Reusable paid-traffic landing-page template.

A landing page is a CONFIG DICT, not code. To ship one for a new project,
copy the config block in build_lp.py, change the fields you care about, and
call render(cfg). Everything you leave out falls back to DEFAULTS below.

Section order is fixed and deliberate, and mirrors /offer-review/:

    header  ->  hero  ->  PROOF BAND  ->  address checker + map
            ->  what you get  ->  CTA  ->  what a first offer leaves out
            ->  CTA  ->  form  ->  footer

Proof sits directly under the hero, above every ask. Credibility comes before
you make the visitor do work.

These pages are deliberately NOT SEO pages:
  * noindex,follow  (they must not compete with /projects/* for the same terms)
  * kept out of sitemap.xml
  * no site nav - logo, phone and the form are the only exits

MINIMUM CONFIG for a new page:
    slug, title, desc, h1, h1_gold, sub, project_ids, form_source
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chassis import head, FORM_SCRIPT, form_section
from mapmod import MAP_HEAD, map_section
import content as C
from build import VIEWER, ROOT

PHONE = "+14694847960"
PHONE_H = "(469) 484-7960"
PHONE2 = "+19563634144"
PHONE2_H = "(956) 363-4144"
CTA = "Free review by a senior consultant &rarr;"

DEFAULTS = {
    # --- identity -------------------------------------------------------
    "slug": None,                       # REQUIRED, e.g. "765kv-landowner"
    "title": None,                      # REQUIRED, <title>
    "desc": None,                       # REQUIRED, meta description
    "schema_name": "Transmission Easement Review for Landowners",
    "schema_area": "Texas",

    # --- hero -----------------------------------------------------------
    "eyebrow": "",                      # small gold badge, omit to hide
    "h1": None,                         # REQUIRED, white line
    "h1_gold": "",                      # gold second line, omit to hide
    "sub": None,                        # REQUIRED, paragraph under the H1
    "hero_cta": "Check my address &rarr;",
    "trust": ("On the property owner's side since the 1980s &nbsp;&middot;&nbsp; "
              "<b>We never represent the condemning agency</b> &nbsp;&middot;&nbsp; No upfront cost"),

    # --- proof band (sits directly under the hero) ----------------------
    "results": None,                    # None -> content.RESULTS_UTILITY
    "proof_headline": None,             # None -> content.PROOF_HEADLINE
    "proof_fine": None,                 # None -> content.PROOF_FINE
    "proof_note": "",                   # optional extra line under the band

    # --- map / address checker ------------------------------------------
    "project_ids": None,                # REQUIRED, Oncor CCN project_id list
    "map_heading": "Is your property on the approved route?",
    "map_blurb": ("The gold line is the centerline the PUCT approved. Dashed grey lines are routes that were "
                  "studied and not selected. Enter an address and we will tell you how far your property sits "
                  "from the approved line."),
    "map_center": [31.6, -100.4],
    "map_zoom": 7,

    # --- body -----------------------------------------------------------
    "get_heading": "What you actually get",
    "get_cards": [
        ("A senior consultant, not a call centre",
         "A senior consultant reads every one of these and calls you back within the hour, 8am&ndash;6pm Central, "
         "Monday to Friday. Outside those hours, first thing the next morning."),
        ("What their number left out",
         "Easement acreage, damage to the remainder, access, temporary workspace, and the things agency appraisals "
         "routinely undercount. We tell you where the value is."),
        ("Nothing out of pocket",
         "We are paid out of the increase. If we look at your situation and do not believe we can move the number, "
         "we tell you that too &mdash; and you owe nothing either way."),
    ],
    "cta_1": ("You do not have to wait for the letter.",
              "Right-of-way agents are working this route now. The best time to understand what your land is worth "
              "is before the first offer is in front of you with a signature line under it."),
    "miss_heading": "What a first offer usually leaves out",
    "miss": [
        ("Damage to the remainder",
         "A transmission corridor does not just take the acres under it. It splits fields, strands corners, moves "
         "your building envelope and follows you into every future appraisal of the whole tract."),
        ("Access and crossings",
         "Where they can enter, how often, which roads they build, who maintains them, and whether you can still "
         "cross your own easement with equipment."),
        ("Temporary construction easement",
         "Work space outside the permanent corridor is a separate taking with its own value, and it is frequently "
         "folded in for free."),
        ("The easement language itself",
         "Width, height, vegetation control, future additional circuits, assignment to third parties. The document "
         "outlives the cheque by decades."),
    ],
    "cta_2": ("Already have an offer letter in hand?",
              "Send it over with their appraisal if they gave you one &mdash; a photo of the pages is enough. "
              "A senior consultant reads it and tells you what their number left out and whether it can be moved."),

    # --- form + footer ---------------------------------------------------
    "form_source": None,                # REQUIRED, hidden `source` field value
    "form_project": None,               # None -> derived from title
    "form_heading": "Free review by a senior consultant",
    "footer_note": ("Route geometry shown on this page is published by the utility; confirm against the official "
                    "filings before relying on it."),
}

LP_CSS = """
.lp-head{position:sticky;top:0;z-index:900;background:var(--navy);border-bottom:2px solid var(--gold);
  display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 22px;flex-wrap:wrap;}
.lp-head .brand-logo{display:block;height:38px;aspect-ratio:760/420;background:var(--logo) center/contain no-repeat;background-color:#fff;border-radius:9px;padding:5px 9px;box-sizing:content-box;}
.lp-head .r{display:flex;align-items:center;gap:16px;flex-wrap:wrap;}
.lp-head .ph{color:var(--gold);font-weight:900;font-size:19px;text-decoration:none;white-space:nowrap;}
.lp-head .ph small{display:block;font-size:11.5px;font-weight:600;color:rgba(255,255,255,.62);letter-spacing:.3px;}
.lp-hero{background:linear-gradient(135deg,#0a1c33,#1a3a5c);color:#fff;padding:52px 22px 46px;text-align:center;}
.lp-hero .eyebrow{display:inline-block;background:rgba(201,162,39,.16);border:1px solid rgba(201,162,39,.5);
  color:var(--gold);font-weight:800;font-size:12.5px;letter-spacing:1.1px;text-transform:uppercase;padding:7px 15px;border-radius:3px;margin-bottom:20px;}
.lp-hero h1{color:#fff;font-size:clamp(27px,4.4vw,45px);line-height:1.14;margin:0 auto 18px;max-width:880px;}
.lp-hero h1 .gold{color:var(--gold);}
.lp-hero p.sub{color:rgba(255,255,255,.87);font-size:clamp(16px,1.9vw,19px);line-height:1.65;max-width:660px;margin:0 auto 26px;}
.lp-hero .acts{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;}
.lp-trust{background:#0d2340;color:rgba(255,255,255,.8);font-size:14px;padding:13px 22px;text-align:center;
  border-top:1px solid rgba(255,255,255,.08);line-height:1.7;}
.lp-trust b{color:var(--gold);}
.lp-get{padding:52px 22px;background:#fff;}
.lp-get .grid{max-width:1000px;margin:26px auto 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(258px,1fr));gap:22px;}
.lp-get .card{border:1px solid #e2e8f0;border-left:4px solid var(--gold);border-radius:5px;padding:22px 20px;background:#fbfcfd;}
.lp-get .card h3{font-size:17px;color:var(--navy);margin:0 0 9px;}
.lp-get .card p{font-size:15px;line-height:1.7;color:#475569;margin:0;}
.miss{background:#fbf7ec;padding:54px 22px;}
.miss ul{max-width:860px;margin:26px auto 0;padding:0;list-style:none;}
.miss li{background:#fff;border:1px solid #e6dcc2;border-radius:5px;padding:17px 20px;margin-bottom:12px;
  font-size:16px;line-height:1.7;color:#3d4a5c;}
.miss li b{color:var(--navy);display:block;margin-bottom:3px;font-size:16.5px;}
.lp-foot{background:#08182c;color:rgba(255,255,255,.5);font-size:13px;line-height:1.8;padding:34px 22px;text-align:center;}
.lp-foot a{color:rgba(255,255,255,.72);}
.lp-foot .nl{max-width:820px;margin:14px auto 0;font-size:12.5px;color:rgba(255,255,255,.46);}
@media(max-width:640px){
  .lp-head{padding:10px 16px;gap:10px;justify-content:center;}
  .lp-head .r{width:100%;justify-content:center;gap:12px;}
  .lp-head .ph{font-size:20px;text-align:center;}
  .lp-head .btn-gold{width:100%;text-align:center;}
  .lp-hero{padding:34px 18px 32px;}
  .lp-hero .acts .btn-gold,.lp-hero .acts .btn-outline{width:100%;text-align:center;}
  .lp-get,.miss{padding:38px 18px;}
}
"""


def _cfg(user):
    c = dict(DEFAULTS)
    c.update(user)
    for k in ("slug", "title", "desc", "h1", "sub", "project_ids", "form_source"):
        if not c.get(k):
            raise ValueError("landing page config is missing required field: %s" % k)
    if not c.get("form_project"):
        c["form_project"] = c["title"].split("|")[0].strip()
    return c


def render(user_cfg, write=True):
    c = _cfg(user_cfg)
    url = "https://nationalrow.com/%s/" % c["slug"].strip("/")

    schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": c["schema_name"],
        "serviceType": "Right-of-way and condemnation consulting",
        "provider": {"@type": "Organization", "name": "National ROW",
                     "url": "https://nationalrow.com", "telephone": "+1-469-484-7960"},
        "areaServed": {"@type": "State", "name": c["schema_area"]},
        "description": c["desc"],
    }

    b = [head(c["title"], c["desc"], url, json.dumps(schema, indent=2),
              extra_head=MAP_HEAD + '<meta name="robots" content="noindex,follow">\n<style>%s</style>' % LP_CSS)]

    eyebrow = '<span class="eyebrow">%s</span>\n    ' % c["eyebrow"] if c["eyebrow"] else ""
    gold = '<br><span class="gold">%s</span>' % c["h1_gold"] if c["h1_gold"] else ""

    b.append("""
<header class="lp-head">
  <a href="/" aria-label="National ROW"><span class="brand-logo"></span></a>
  <div class="r">
    <a class="ph" href="tel:%s">%s<small>CALL OR TEXT A SENIOR CONSULTANT</small></a>
    <a class="btn-gold" href="#contact">%s</a>
  </div>
</header>

<section class="lp-hero">
  <div class="container">
    %s<h1>%s%s</h1>
    <p class="sub">%s</p>
    <div class="acts">
      <a class="btn-gold" href="#corridor-check">%s</a>
      <a class="btn-outline" href="#contact">%s</a>
    </div>
  </div>
</section>
<div class="lp-trust">%s</div>
""" % (PHONE, PHONE_H, CTA, eyebrow, c["h1"], gold, c["sub"], c["hero_cta"], CTA, c["trust"]))

    # PROOF BAND — directly under the hero, above every ask.
    b.append(C.proof_band(results=c["results"], headline=c["proof_headline"], fine=c["proof_fine"]))
    if c["proof_note"]:
        b.append('<div class="lp-trust">%s</div>' % c["proof_note"])

    b.append('<div id="corridor-check"></div>')
    b.append(map_section(c["project_ids"], c["map_heading"], c["map_blurb"],
                         VIEWER, None, c["map_center"], c["map_zoom"]))

    cards = "\n      ".join(
        '<div class="card"><h3>%s</h3>\n        <p>%s</p></div>' % (h, p) for h, p in c["get_cards"])
    b.append("""
<section class="lp-get">
  <div class="container">
    <h2 style="text-align:center;">%s</h2>
    <div class="grid">
      %s
    </div>
  </div>
</section>
""" % (c["get_heading"], cards))

    b.append(C.cta_band(c["cta_1"][0], c["cta_1"][1], CTA, "#contact"))

    items = "\n      ".join('<li><b>%s</b>%s</li>' % (h, p) for h, p in c["miss"])
    b.append("""
<section class="miss">
  <div class="container">
    <h2 style="text-align:center;">%s</h2>
    <ul>
      %s
    </ul>
  </div>
</section>
""" % (c["miss_heading"], items))

    b.append(C.cta_band(c["cta_2"][0], c["cta_2"][1], CTA, "#contact"))

    fs = form_section(c["form_project"], c["form_heading"])
    fs = fs.replace('<input type="hidden" name="_template" value="table">',
                    '<input type="hidden" name="_template" value="table">\n'
                    '          <input type="hidden" name="source" value="%s">' % c["form_source"])
    b.append(fs)

    b.append("""
<footer class="lp-foot">
  <div class="container">
    <p><b style="color:rgba(255,255,255,.8)">National ROW</b> &middot; Nationwide service, HQ in Texas<br>
      Call or text <a href="tel:%s">%s</a> &nbsp;&middot;&nbsp;
      <a href="tel:%s">%s</a> &nbsp;&middot;&nbsp;
      <a href="mailto:info@nationalrow.com">info@nationalrow.com</a></p>
    <p class="nl">National ROW is a right-of-way and condemnation consulting firm representing property owners. We are not
      a law firm, we do not provide legal advice, and contacting us does not create an attorney-client relationship.
      When a matter needs condemnation counsel we say so and coordinate with an independent licensed attorney.
      %s &nbsp;<a href="/privacy-policy/">Privacy</a></p>
  </div>
</footer>
""" % (PHONE, PHONE_H, PHONE2, PHONE2_H, c["footer_note"]))

    b.append(FORM_SCRIPT)
    b.append("</body>\n</html>")

    html = "\n".join(b)
    if write:
        out = os.path.join(ROOT, c["slug"].strip("/"))
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
    return url, len(html)
