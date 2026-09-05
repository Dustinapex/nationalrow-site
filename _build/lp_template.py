# -*- coding: utf-8 -*-
"""Reusable paid-traffic landing-page template.

A landing page is a CONFIG DICT, not code. To ship one for a new project,
copy the config block in build_lp.py, change the fields you care about, and
call render(cfg). Everything you leave out falls back to DEFAULTS below.

Section order is fixed and deliberate, and mirrors /offer-review/:

    header  ->  hero  ->  PROOF BAND  ->  compact route map
            ->  what you get  ->  CTA  ->  what a first offer leaves out
            ->  CTA  ->  form  ->  footer

There is deliberately NO address checker on a landing page. Paid traffic is
paid for on the click; a checker that answers "your address is not on the
route" throws that money away - and because the filed corridor is not the
final surveyed alignment, that answer would not even be reliable. The
interactive checker lives on the /projects/* information pages instead.

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
from chassis import head, FORM_SCRIPT, form_section, SITE_HEADER_NOLINK
from mapmod import MAP_HEAD, map_compact
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
    "hero_cta": CTA,                    # primary gold button -> the form
    "trust": ("On the property owner's side since the 1980s &nbsp;&middot;&nbsp; "
              "<b>We never represent the condemning agency</b> &nbsp;&middot;&nbsp; No upfront cost"),

    # --- proof band (sits directly under the hero) ----------------------
    "results": None,                    # None -> content.RESULTS_UTILITY
    "proof_headline": None,             # None -> content.PROOF_HEADLINE
    "proof_fine": None,                 # None -> content.PROOF_FINE
    "proof_note": "",                   # optional extra line under the band

    # --- compact route map (proof, NOT a qualifier - see module docstring)
    "project_ids": None,                # REQUIRED, Oncor CCN project_id list
    "map_heading": "The approved route",
    "map_blurb": ("Gold is the centerline the PUCT approved. Dashed grey is what was studied and not selected."),
    "map_detail_url": "",               # set both to "" for no exit link (default)
    "map_detail_label": "",

    # --- valuation vs legal counsel (content.versus_block) --------------
    "show_versus": True,

    # --- body -----------------------------------------------------------
    "get_heading": "What you actually get",
    "get_cards": [
        ("A senior consultant, not a call center",
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
         "outlives the check by decades."),
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
/* header CTA that replaces the email line on a landing page */
.site-head .hc-cta{display:inline-block;background:var(--gold);color:var(--navy);
  font-family:'Barlow Semi Condensed','Arial Narrow',Arial,sans-serif;font-size:16.5px;font-weight:800;
  letter-spacing:.2px;text-decoration:none;padding:10px 18px;border-radius:5px;white-space:nowrap;
  box-shadow:0 2px 8px rgba(201,162,39,.35);}
.site-head .hc-cta:hover{background:var(--navy);color:#fff;}
@media(max-width:420px){.site-head .hc-cta{font-size:15px;padding:9px 14px;white-space:normal;}}

/* --- valuation vs legal counsel (ported from /offer-review/) ------------ */
.lp-vs{background:#fff;padding:52px 22px;}
.lp-vs .container{max-width:1100px;}
.vc-sechead{margin-bottom:22px;}
.vc-eyebrow{font-family:'IBM Plex Mono',ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:1.9px;
  text-transform:uppercase;font-weight:600;color:var(--gold);margin-bottom:10px;}
.lp-vs h2{font-size:clamp(23px,3.1vw,35px);line-height:1.16;color:var(--text);margin:0;}
.vc-lead{font-size:17px;line-height:1.55;font-weight:500;color:var(--text);max-width:52ch;margin:0 0 4px;}
.vc-lead strong{font-weight:800;color:var(--navy);}
.vc-grid{display:grid;grid-template-columns:1.35fr 1fr;gap:18px;align-items:start;margin-top:26px;}
.vc-col{background:#fff;border:1px solid rgba(13,35,64,.2);border-radius:5px;padding:24px 22px;
  display:flex;flex-direction:column;gap:16px;}
.vc-col--us{background:var(--navy);border:2px solid var(--gold);}
.vc-head{padding-bottom:14px;border-bottom:1px solid rgba(13,35,64,.13);}
.vc-col--us .vc-head{border-bottom-color:rgba(201,162,39,.35);}
.vc-head h3{font-size:19px;font-weight:700;color:var(--text);margin:0 0 5px;}
.vc-col--us .vc-head h3{color:#fff;}
.vc-sub{font-family:'IBM Plex Mono',ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:1.5px;
  text-transform:uppercase;color:#79828a;display:block;}
.vc-col--us .vc-sub{color:var(--gold-light);}
.vc-list{list-style:none;display:flex;flex-direction:column;gap:10px;margin:0;padding:0;}
.vc-list li{display:flex;align-items:flex-start;gap:10px;font-size:15.5px;line-height:1.45;color:var(--text);}
.vc-list li::before{content:"";display:block;width:17px;height:17px;min-width:17px;margin-top:3px;
  background:url("data:image/svg+xml,%3Csvg viewBox='0 0 24 24' fill='none' stroke='%23c9a227' stroke-width='2.5' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20 6L9 17l-5-5'/%3E%3C/svg%3E") center/contain no-repeat;}
.vc-list--us li{color:#e8edf5;}
.vc-list--us li strong{color:#fff;}
.vc-note{text-align:center;margin:22px 0 0;font-family:'Barlow Semi Condensed','Arial Narrow',Arial,sans-serif;
  font-style:italic;font-size:17px;color:#4e565e;}
.vc-disclosure{background:#f4f6f9;border-left:3px solid var(--gold);padding:18px 22px;margin-top:26px;border-radius:0 4px 4px 0;}
.vc-disclosure p{font-size:14.5px;line-height:1.65;color:#4e565e;margin:0;max-width:80ch;}
@media(max-width:820px){.vc-grid{grid-template-columns:1fr;gap:14px;}}
@media(max-width:640px){.lp-vs{padding:38px 18px;}.vc-col{padding:20px 17px;}}
.lp-map{padding:38px 22px 34px;background:#f4f7fa;}
.lp-map .container{max-width:900px;}
.lp-map h2{text-align:center;font-size:clamp(21px,2.6vw,27px);margin:0 0 6px;}
.lp-map-sub{text-align:center;color:#5b6a7d;font-size:14.5px;line-height:1.6;margin:0 auto 18px;max-width:620px;}
.lp-map #routeMapC{height:300px;width:100%;background:#eef2f6;position:relative;}
.lp-map .map-legend{padding:9px 16px;font-size:12.5px;gap:14px;}
.lp-map .map-note{font-size:11.5px;padding:10px 16px;}
.lp-map-more{text-align:center;margin:14px 0 0;font-size:14px;}
.lp-map-more a{color:var(--navy);font-weight:700;}
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
  .lp-hero{padding:34px 18px 32px;}
  .lp-hero .acts .btn-gold,.lp-hero .acts .btn-outline{width:100%;text-align:center;}
  .lp-get,.miss{padding:38px 18px;}
  .lp-map{padding:28px 16px 26px;}
  .lp-map #routeMapC{height:210px;}
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
%s
<section class="lp-hero">
  <div class="container">
    %s<h1>%s%s</h1>
    <p class="sub">%s</p>
    <div class="acts">
      <a class="btn-gold" href="#contact">%s</a>
      <a class="btn-outline" href="tel:%s">Call or text %s</a>
    </div>
  </div>
</section>
<div class="lp-trust">%s</div>
""" % (SITE_HEADER_NOLINK, eyebrow, c["h1"], gold, c["sub"], c["hero_cta"], PHONE, PHONE_H, c["trust"]))

    # PROOF BAND — directly under the hero, above every ask.
    b.append(C.proof_band(results=c["results"], headline=c["proof_headline"], fine=c["proof_fine"]))
    if c["proof_note"]:
        b.append('<div class="lp-trust">%s</div>' % c["proof_note"])

    b.append(map_compact(c["project_ids"], c["map_heading"], c["map_blurb"],
                         VIEWER, c["map_detail_url"], c["map_detail_label"]))

    # valuation vs legal counsel - directly under the map, before the ask
    if c["show_versus"]:
        b.append(C.versus_block())

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
      <a href="mailto:info@nationalrow.com">info@nationalrow.com</a></p>
    <p class="nl">National ROW is a right-of-way and condemnation consulting firm representing property owners. We are not
      a law firm, we do not provide legal advice, and contacting us does not create an attorney-client relationship.
      When a matter needs condemnation counsel we say so and coordinate with an independent licensed attorney.
      %s &nbsp;<a href="/privacy-policy/">Privacy</a></p>
  </div>
</footer>
""" % (PHONE, PHONE_H, c["footer_note"]))

    b.append(FORM_SCRIPT)
    b.append("</body>\n</html>")

    html = "\n".join(b)
    if write:
        out = os.path.join(ROOT, c["slug"].strip("/"))
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
    return url, len(html)
