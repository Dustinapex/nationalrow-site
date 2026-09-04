# -*- coding: utf-8 -*-
"""Wire the new 765 kV pages into the site: projects index, sitemap, llms.txt,
and add ?project= / ?county= prefill to the /offer-review/ landing page."""
import io, os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TODAY = "2026-09-04"

NEW = [
    ("dinosaur-longshore-765kv", "Dinosaur&ndash;Longshore 765kV",
     "Dinosaur–Longshore 765kV", "Texas &middot; Docket 59315 &mdash; approved &rsaquo;"),
    ("longshore-drill-hole-765kv", "Longshore&ndash;Drill Hole 765kV",
     "Longshore–Drill Hole 765kV", "Texas &middot; Docket 59029 &mdash; approved &rsaquo;"),
]


def rd(p):
    return io.open(p, encoding="utf-8").read()


def wr(p, s):
    io.open(p, "w", encoding="utf-8").write(s)


# ---------- 1. projects/index.html ----------
h = rd("projects/index.html")

anchor = '<a href="/projects/ercot-765kv/" class="state-card"><span class="state-card-name">ERCOT 765kV Transmission</span><span class="state-card-tag">Texas &rsaquo;</span></a>'
assert anchor in h, "projects index anchor card not found"

new_anchor = ('<a href="/projects/ercot-765kv/" class="state-card">'
              '<span class="state-card-name">Texas 765kV Buildout</span>'
              '<span class="state-card-tag">Texas &middot; 424 miles approved &rsaquo;</span></a>')
cards = "".join(
    '\n      <a href="/projects/%s/" class="state-card">'
    '<span class="state-card-name">%s</span>'
    '<span class="state-card-tag">%s</span></a>' % (slug, label, tag)
    for slug, label, _plain, tag in NEW
)
h = h.replace(anchor, new_anchor + cards, 1)

# ItemList schema: rename item 1 and append the two new pages
m = re.search(r'<script type="application/ld\+json">(\{"@context": "https://schema\.org", "@type": "ItemList".*?\})</script>', h, re.S)
assert m, "ItemList schema not found"
data = json.loads(m.group(1))
data["itemListElement"][0]["name"] = "Texas 765kV Transmission Buildout"
n = len(data["itemListElement"])
for i, (slug, _label, plain, _tag) in enumerate(NEW, start=1):
    data["itemListElement"].append({
        "@type": "ListItem", "position": n + i, "name": plain,
        "url": "https://nationalrow.com/projects/%s/" % slug})
h = h[:m.start(1)] + json.dumps(data, ensure_ascii=False) + h[m.end(1):]

h = h.replace(
    "Seventeen active acquisitions across Texas and Oklahoma.",
    "Nineteen active acquisitions across Texas and Oklahoma, including the two Oncor 765 kV routes the PUCT approved on August 28, 2026.")
wr("projects/index.html", h)
print("projects/index.html wired")

# ---------- 2. sitemap.xml ----------
s = rd("sitemap.xml")
s = re.sub(r'(<url><loc>https://nationalrow\.com/projects/ercot-765kv/</loc><lastmod>)[0-9-]+(</lastmod>)',
           r'\g<1>%s\g<2>' % TODAY, s)
add = "".join(
    '<url><loc>https://nationalrow.com/projects/%s/</loc><lastmod>%s</lastmod>'
    '<changefreq>weekly</changefreq><priority>0.9</priority></url>\n' % (slug, TODAY)
    for slug, _l, _p, _t in NEW)
assert "</urlset>" in s
s = s.replace("</urlset>", add + "</urlset>")
wr("sitemap.xml", s)
print("sitemap.xml wired (ercot lastmod -> %s, 2 urls added)" % TODAY)

# ---------- 3. llms.txt ----------
L = rd("llms.txt")
block = """
## Texas 765 kV transmission buildout (updated %s)
The Public Utility Commission of Texas approved two Oncor 765-kilovolt transmission projects on August 28, 2026 — Texas's first 765 kV lines. Together they total 424 miles across 21 counties, with a 200-foot permanent easement (about 24.2 acres per mile).
- Dinosaur Switch to Longshore Switch — PUCT Docket 59315, approved Route 559, 242.6 miles, ~$2.24 billion, target in service 2028. Counties: Brown, Callahan, Coke, Coleman, Comanche, Erath, Glasscock, Hood, Howard, Runnels, Somervell, Sterling, Taylor. Detail: [nationalrow.com/projects/dinosaur-longshore-765kv/](https://nationalrow.com/projects/dinosaur-longshore-765kv/)
- Longshore Switch to Drill Hole Switch — PUCT Docket 59029, approved Route 476, 181.6 miles, ~$1.70 billion, target in service 2029. Counties: Andrews, Culberson, Ector, Howard, Loving, Martin, Reeves, Winkler. Detail: [nationalrow.com/projects/longshore-drill-hole-765kv/](https://nationalrow.com/projects/longshore-drill-hole-765kv/)
- Overview of both, with route maps and a property proximity check: [nationalrow.com/projects/ercot-765kv/](https://nationalrow.com/projects/ercot-765kv/)
Landowners on these routes should expect survey permission requests, an appraisal, and a written offer. Route selection is final; compensation is not. National ROW represents the landowner in that negotiation and is not a law firm.
""" % TODAY

if "## Texas 765 kV transmission buildout" in L:
    L = re.sub(r"\n## Texas 765 kV transmission buildout.*?(?=\n## |\Z)", block, L, flags=re.S)
else:
    marker = "\n## Core guides"
    L = L.replace(marker, block + marker, 1) if marker in L else L + block
wr("llms.txt", L)
print("llms.txt wired")

# ---------- 4. /offer-review/ ValueTrack prefill ----------
o = rd("offer-review/index.html")
SNIPPET = """
<!-- ValueTrack / campaign prefill: /offer-review/?project=...&county=... -->
<script>
(function(){
  try{
    var p = new URLSearchParams(location.search);
    function set(param, id){
      var v = p.get(param);
      if(!v) return;
      var el = document.getElementById(id);
      if(!el) return;
      el.value = v.replace(/\\+/g,' ').slice(0,120);
      el.setAttribute('data-prefilled','1');
    }
    set('project','project');
    set('county','county');
    var src = document.querySelector('[name="source"]');
    if(src && p.get('utm_source')) src.value = (src.value ? src.value + ' | ' : '') + p.get('utm_source');
  }catch(e){}
})();
</script>
"""
if "ValueTrack / campaign prefill" in o:
    o = re.sub(r"\n<!-- ValueTrack / campaign prefill.*?</script>\n", SNIPPET, o, flags=re.S)
    print("offer-review prefill updated")
else:
    assert "</body>" in o
    o = o.replace("</body>", SNIPPET + "</body>", 1)
    print("offer-review prefill added")
wr("offer-review/index.html", o)
