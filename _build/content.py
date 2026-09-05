# -*- coding: utf-8 -*-
"""Shared body content blocks for the 765 kV project pages."""

ACRES_PER_MILE = 200 * 5280 / 43560.0  # 200-ft ROW -> 24.24 acres per mile

COUNTY_SEATS = {
    "Somervell": "Glen Rose", "Hood": "Granbury", "Erath": "Stephenville",
    "Comanche": "Comanche", "Brown": "Brownwood", "Callahan": "Baird",
    "Coleman": "Coleman", "Taylor": "Abilene", "Runnels": "Ballinger",
    "Coke": "Robert Lee", "Sterling": "Sterling City", "Glasscock": "Garden City",
    "Howard": "Big Spring", "Martin": "Stanton", "Andrews": "Andrews",
    "Ector": "Odessa", "Winkler": "Kermit", "Loving": "Mentone",
    "Reeves": "Pecos", "Culberson": "Van Horn",
}


def county_grid(counties):
    chips = "".join(
        '<div class="county-chip">%s County<small>County seat: %s</small></div>' % (c, COUNTY_SEATS[c])
        for c in sorted(counties)
    )
    return '<div class="county-grid">%s</div>' % chips


EASEMENT_COST = """
<section>
  <div class="container container-narrow prose">
    <h2>What a 765 kV easement actually costs you</h2>
    <p>An easement is not a sale of your land. You keep title, you keep paying taxes on it, and in most cases you keep grazing or farming it. What you give up is control of a strip — permanently. Understanding exactly what you are giving up is what turns a number on a page into a number you can argue with.</p>

    <h3>The corridor is 200 feet wide</h3>
    <p>Oncor's published specification for its 765 kV lines is a <strong>200-foot right-of-way</strong>. For comparison, Oncor puts a single double-circuit 345 kV line at 160 feet, and notes that carrying the same power with 345 kV lines would take roughly 480 feet of corridor. So 765 kV is a wider strip than most Texas landowners have dealt with before, and it is the reason a single line can serve so much load.</p>
    <p>Two hundred feet is <strong>24.2 acres for every mile</strong> the line crosses your property. Half a mile across your place is roughly twelve acres encumbered forever.</p>

    <h3>Steel lattice towers, not wood poles</h3>
    <p>These lines are built on self-supporting steel lattice towers. Lattice structures sit on four legs with a footprint measured in tens of feet on a side, set in concrete foundations. They are not something you mow around. Where a tower lands on your property matters enormously — for pivot irrigation, for field patterns, for equipment turning room, and for what the place looks like from your house.</p>

    <h3>What you lose inside the strip</h3>
    <ul>
      <li><strong>Building rights.</strong> No structures, no barns, no houses, no shops inside the easement.</li>
      <li><strong>Trees and tall vegetation.</strong> Cleared at the outset and kept cleared for the life of the line.</li>
      <li><strong>Elevation and equipment height.</strong> Restrictions on how high you can build, stack, or operate under the conductors.</li>
      <li><strong>Access on your terms.</strong> The utility gets the right to come and go for construction, inspection, and repair — including with heavy equipment, including in wet conditions.</li>
      <li><strong>Aerial application.</strong> Crop dusting over and near a 765 kV line is a real operational problem, and pilots price it accordingly if they will fly it at all.</li>
    </ul>

    <h3>What you lose outside the strip — and this is where the money is</h3>
    <p>The strip itself is the easy part to value. The harder and usually larger question is what happens to the rest of your property: the <strong>remainder</strong>. A line that cuts a ranch into two pieces, that sits in the view from the homesite, that severs a field from its water, or that puts a tower in the middle of a pivot circle damages land the utility is not paying for by the acre.</p>
    <div class="urgency-box"><strong>The core principle:</strong> in Texas you are entitled to the value of the part taken <em>plus</em> the loss in value to everything you keep. Initial offers routinely price the first and shortchange the second.</div>
  </div>
</section>
"""


OFFER_ANATOMY = """
<section class="section-alt">
  <div class="container container-narrow prose">
    <h2>What the offer will look like — and what it usually leaves out</h2>
    <p>When the offer arrives it will not say "here is our opening bid." It will arrive as a package: a cover letter, an appraisal or a summary of one, a plat showing the part being acquired, an easement document already drafted, and in most cases a deadline. It is designed to look final. It is not final.</p>

    <h3>The three numbers every offer package contains</h3>
    <p>Every legitimate offer breaks down into the same three components. Find them, because the way they are weighted tells you where the offer is weak.</p>
    <table class="num-table">
      <thead><tr><th>Component</th><th>What it pays for</th><th>Typically</th></tr></thead>
      <tbody>
        <tr><td><strong>Value of the part acquired</strong></td><td>The strip itself, priced per acre against comparable sales</td><td>Largest single line</td></tr>
        <tr><td><strong>Damages to the remainder</strong></td><td>Lost value to everything you keep — severance, access, layout, view, marketability</td><td>Frequently understated</td></tr>
        <tr><td><strong>Cost to cure</strong></td><td>What it costs to fix what the taking broke — fences, gates, water lines, crossings, re-routed roads</td><td>Frequently omitted</td></tr>
      </tbody>
    </table>
    <p>How much does the back half matter? In one recent Texas offer package our team reviewed, <strong>damages to the remainder made up about 39% of the total offer and cost to cure another 29%</strong> — nearly seven of every ten dollars came from something other than the raw land price. That package was a highway acquisition rather than a transmission easement, so the specifics differ. The structure does not. If your offer is almost entirely a per-acre land number with little or nothing for damages and cure, that is not because your property has none. It is because nobody quantified them.</p>

    <div class="note-box"><strong>How to read your own package in ten minutes.</strong> Find the total. Find the per-acre figure and the acreage it is applied to. Multiply. Whatever is left over is what they are paying for damages and cure. If that leftover is small or zero, you have found your issue.</div>

    <h3>Things that are compensable and almost never volunteered</h3>
    <ul>
      <li>Temporary construction easements and the workspace outside the permanent strip</li>
      <li>Access roads built across your land to reach tower sites</li>
      <li>Damage to terraces, drainage, and soil compaction from construction</li>
      <li>Loss of a pivot circle or the cost to reconfigure irrigation</li>
      <li>Fence rebuilds, cattle guards, gates, and the labor to manage livestock during construction</li>
      <li>Timber and improved pasture actually destroyed, valued as what it was, not as raw acreage</li>
      <li>The effect on a homesite, hunting lease income, or a planned subdivision</li>
    </ul>
  </div>
</section>
"""


TIMELINE = """
<section>
  <div class="container container-narrow">
    <h2>What happens next, in order</h2>
    <p class="section-sub">Approval of the route is the beginning of the landowner phase, not the end of it. Here is the sequence, and where your leverage sits in it.</p>
    <ul class="timeline">
      <li class="done">
        <span class="when">Done — 2025</span>
        <h4>Study area, public meetings, and route alternatives</h4>
        <p>Oncor mapped a study area, held public meetings, and developed dozens of alternative route links. Landowner comments filed at this stage genuinely moved routes.</p>
      </li>
      <li class="done">
        <span class="when">Done</span>
        <h4>Application filed at the PUCT</h4>
        <p>Oncor filed for a Certificate of Convenience and Necessity. Landowners on the alternative routes received formal notice and could intervene.</p>
      </li>
      <li class="done">
        <span class="when">Done — August 28, 2026</span>
        <h4>PUCT approved a single route</h4>
        <p>The Commission selected one route from the alternatives. Route selection is now settled. What is <em>not</em> settled is what each landowner gets paid.</p>
      </li>
      <li>
        <span class="when">Now</span>
        <h4>Survey permission</h4>
        <p>A land agent asks to enter and survey. The form they hand you is a legal document. You can negotiate its terms — scope, notice, timing, repair of damage, gates left as found — and you are not required to sign it on the spot. Signing a broad permission form gives away more than most people realize, and it costs you nothing to have it read first.</p>
      </li>
      <li>
        <span class="when">Next</span>
        <h4>Appraisal</h4>
        <p>An appraiser hired by the utility values your property. This appraisal is the foundation of the offer. You are entitled to your own — and an independent appraisal that documents damages to the remainder is the single most effective tool for moving an offer.</p>
      </li>
      <li>
        <span class="when">Next</span>
        <h4>Written offer and the Landowner's Bill of Rights</h4>
        <p>Texas law requires the condemning entity to deliver a written offer and the Texas Landowner's Bill of Rights before it can proceed to condemnation. Read both. The offer will come with a response window — commonly 30 days — but a deadline in a letter is a negotiating posture, not a statute of limitations on your property.</p>
      </li>
      <li>
        <span class="when">If you cannot agree</span>
        <h4>Special commissioners</h4>
        <p>If negotiation fails, the utility files a condemnation petition and a judge appoints three special commissioners — local landowners — who hold a hearing and set an award. Both sides present evidence. Documented damages win here.</p>
      </li>
      <li>
        <span class="when">Last resort</span>
        <h4>Objection and trial</h4>
        <p>Either side may object to the commissioners' award and take the case to court for a jury determination of just compensation.</p>
      </li>
    </ul>
    <div class="urgency-box"><strong>Where the leverage actually is:</strong> almost all of it sits between survey permission and the written offer. Once you have signed an easement, it is done — easements of this kind run with the land, forever. The cheapest hour you will ever spend is the one before you sign anything.</div>
  </div>
</section>
"""


DAMAGES = """
<section class="section-alt">
  <div class="container">
    <h2>What their offer may miss</h2>
    <p class="section-sub">The utility's appraiser works for the utility. That does not make them dishonest — it makes them narrow. These are the categories that routinely go unquantified.</p>
    <div class="damages-grid">
      <div class="damage-card"><h4>Diminution in Land Value</h4><p>A 200-foot high-voltage corridor can reduce the market value of your whole tract, not just the strip. Buyers price the line in.</p></div>
      <div class="damage-card"><h4>Severance Damages</h4><p>If the corridor cuts your property into pieces, the pieces are worth less than the whole. That loss is compensable and is often the largest single item.</p></div>
      <div class="damage-card"><h4>Cost to Cure</h4><p>Fences, gates, cattle guards, water lines, field roads, and crossings that have to be rebuilt because of the taking.</p></div>
      <div class="damage-card"><h4>Crop &amp; Grazing Losses</h4><p>Construction access and permanent restrictions take acres out of production during and after the build.</p></div>
      <div class="damage-card"><h4>Irrigation &amp; Equipment Interference</h4><p>Towers in a pivot circle, restricted equipment height, and lost turning room have real, calculable cost.</p></div>
      <div class="damage-card"><h4>Timber &amp; Vegetation Removal</h4><p>Trees cleared for the corridor have value as timber and as shade, screening, and habitat — not as bare dirt.</p></div>
      <div class="damage-card"><h4>Proximity to Improvements</h4><p>Distance from your home, barns, or a planned homesite affects both livability and what the place sells for.</p></div>
      <div class="damage-card"><h4>Temporary Construction Easements</h4><p>Workspace outside the permanent strip is separately compensable and is easy to under-price or leave out entirely.</p></div>
    </div>
  </div>
</section>
"""


HOW = """
<section class="how-section">
  <div class="container">
    <h2>How we work — no upfront cost</h2>
    <p class="section-sub">We are on the owner's side of the right-of-way. We are paid out of the increase, which means we do not get paid unless you do better.</p>
    <div class="steps-grid">
      <div class="step"><div class="step-num">01</div><h4>Free case review</h4><p>Send us whatever they sent you — a survey permission form, a letter, an appraisal, an offer. We read it and tell you plainly where it is weak. No charge, no obligation.</p></div>
      <div class="step"><div class="step-num">02</div><h4>Independent appraisal</h4><p>We bring in independent, certified appraisers to value the part acquired and, critically, to document damages to the remainder and cost to cure.</p></div>
      <div class="step"><div class="step-num">03</div><h4>We negotiate</h4><p>We deal with the land agents and their appraisers directly, with documentation behind every number, so you are not negotiating alone against people who do this full time.</p></div>
      <div class="step"><div class="step-num">04</div><h4>You get paid more</h4><p>Our fee is a percentage of the increase above the original offer. If we do not improve it, you owe us nothing.</p></div>
    </div>
    <div class="note-box" style="background:rgba(255,255,255,.07);border-left-color:#c9a227;color:rgba(255,255,255,.8);margin-top:32px;">
      <strong style="color:#e8bf4a;">To be clear about what we are:</strong> National ROW is a right-of-way consulting firm. We are not a law firm and we do not give legal advice. Much of what a landowner needs in this process is valuation and negotiation work rather than litigation — that is what we do. When a case needs a lawyer, we say so and we coordinate with condemnation counsel.
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------- PROOF BAND
# Documented results, rendered high on the page (directly under the hero),
# mirroring the placement /offer-review/ uses. Every field is data, not prose:
# swap RESULTS / edit the caller's args and the band re-renders.
#
# Each result is a dict:
#   where : where and what kind of taking it was
#   frm   : first offer
#   to    : final
#   pct   : percentage increase
#   why   : OPTIONAL one line on why the number moved. Leave it out and the
#           "why the price increased" sub-block is omitted entirely — do not
#           invent one, these are advertised claims that need substantiation.

RESULTS_UTILITY = [
    {"where": "Utility easement &middot; Houston, TX", "frm": "$16,000", "to": "$138,000", "pct": "+762%"},
    {"where": "Utility easement &middot; Irving, TX",  "frm": "$12,000", "to": "$50,000",  "pct": "+317%"},
]

PROOF_HEADLINE = ("Almost every condemnation case is a fight about a number, "
                  "not about the law.")

PROOF_FINE = ("Individual documented matters, each traced from the original offer letter through to final settlement. "
              "They are not an average and not a prediction &mdash; every take is different, and when we look at yours "
              "and think the number is close to right, we tell you so. National ROW is a right-of-way consulting firm, "
              "not a law firm; nothing here is legal advice.")


def proof_band(results=None, headline=None, fine=None, act=None, heading="Our documented results"):
    """Gold results band. `act` is the third column: (h3, paragraph, link_html)."""
    results = RESULTS_UTILITY if results is None else results
    headline = PROOF_HEADLINE if headline is None else headline
    fine = PROOF_FINE if fine is None else fine
    if act is None:
        act = ("Text us the letter",
               "A photo of the offer is enough. A senior consultant reads it and tells you what we see.",
               '<a href="sms:+14694847960">Text (469) 484-7960 &rarr;</a>')

    cols = []
    for r in results:
        why = ""
        if r.get("why"):
            why = ('\n        <div class="why">Why the price increased</div>'
                   '\n        <div class="whytxt">%s</div>' % r["why"])
        cols.append("""      <div class="col">
        <div class="where">%s</div>
        <div class="nums">%s<span class="ar">&rarr;</span>%s</div>
        <div class="pct">%s</div>%s
      </div>""" % (r["where"], r["frm"], r["to"], r["pct"], why))

    cols.append("""      <div class="col act">
        <div class="why" style="margin-top:0">Free, no obligation</div>
        <h3>%s</h3>
        <p>%s</p>
        %s
      </div>""" % act)

    return """
<section class="proofband">
  <div class="inner">
    <p class="hl">%s</p>
    <div class="rule"></div>
    <h2>%s</h2>
    <div class="cols">
%s
    </div>
    <p class="fine">%s</p>
  </div>
</section>
""" % (headline, heading, "\n".join(cols), fine)


def cta_band(headline, body, label, href, show_phone=True):
    phone = ('\n    <p class="alt">Or call or text '
             '<a href="tel:+14694847960">(469) 484-7960</a> '
             '&mdash; a senior consultant answers owners the same day.</p>') if show_phone else ""
    return """
<section class="cta-band">
  <div class="inner">
    <h3>%s</h3>
    <p>%s</p>
    <a class="btn-gold" href="%s">%s</a>%s
  </div>
</section>
""" % (headline, body, href, label, phone)


def handoff(project_param, headline, sub):
    return """
<section class="handoff">
  <div class="container">
    <h2>%s</h2>
    <p>%s</p>
    <a class="btn-gold" href="/offer-review/?project=%s">Free review by a senior consultant →</a>
    <p style="margin-top:22px;font-size:15px;opacity:.7;">Or call <a href="tel:+14694847960" style="color:#e8bf4a;font-weight:700;">(469) 484-7960</a> — we answer owners the same day.</p>
  </div>
</section>
""" % (headline, sub, project_param)


def sources_block(items):
    lis = "".join("<li>%s</li>" % i for i in items)
    return """
<section>
  <div class="container container-narrow">
    <div class="sources">
      <h3>Sources</h3>
      <ol>%s</ol>
      <p style="font-size:13px;color:#64748b;margin-top:16px;line-height:1.7;">County lists and tract counts on this page were derived by measuring Oncor's own published approved-route geometry against public county boundaries and Oncor's public tract layer. They are close, not surveyed. Verify your specific parcel against the official filings before relying on anything here.</p>
    </div>
  </div>
</section>
""" % lis
