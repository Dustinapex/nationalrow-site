# -*- coding: utf-8 -*-
"""Landing pages. THIS FILE IS CONFIG, NOT CODE.

To ship a landing page for a new project:
  1. copy one block below,
  2. change the fields,
  3. run `python3 build_lp.py`.

Anything you leave out falls back to lp_template.DEFAULTS, so a minimal page
is just: slug, title, desc, h1, sub, project_ids, form_source.

Remember for every new landing page:
  * it is noindex,follow on purpose - do NOT add it to sitemap.xml
  * give it its own form_source so the lead source is traceable
  * results shown must be documented matters you can substantiate
"""
from lp_template import render

PAGES = [

    # ------------------------------------------------------------------
    # Oncor 765 kV Import Path 1  (PUCT 59315 Dinosaur-Longshore,
    #                              PUCT 59029 Longshore-Drill Hole)
    # ------------------------------------------------------------------
    {
        "slug": "765kv-landowner",
        "title": "Is Your Land on Oncor's 765 kV Route? | Free Senior Review | National ROW",
        "desc": ("Texas approved 424 miles of Oncor 765 kV line on August 28, 2026. Check your address against "
                 "the approved centerline in seconds, then have a senior consultant review what you are offered."),
        "schema_name": "765 kV Transmission Easement Review for Texas Landowners",

        "eyebrow": "424 miles approved &middot; August 28, 2026",
        "h1": "Oncor is running 765,000 volts across Texas.",
        "h1_gold": "Your land may be on the route.",
        "sub": ("They have a team &mdash; appraisers, right-of-way agents and lawyers who do this every day. If the "
                "line crosses your property you will find out by letter, and their number will already be written. "
                "Find out what your side of it is worth first."),

        "project_ids": [1015, 1019],
        "map_heading": "The two approved 765 kV routes",
        "map_blurb": ("Gold is the centerline the PUCT approved on August 28, 2026. Dashed grey is what was studied "
                      "and not selected. The easement corridor runs roughly 200 feet wide along the gold line."),
        "map_detail_url": "/projects/ercot-765kv/",
        "map_detail_label": "See the full route, both dockets and an address checker &rarr;",

        "cta_1": ("You do not have to wait for the letter.",
                  "Right-of-way agents are working these two routes now. The best time to understand what your land "
                  "is worth is before the first offer is in front of you with a signature line under it."),
        "miss": [
            ("Damage to the remainder",
             "A 200-foot corridor does not just take the acres under it. It splits fields, strands corners, moves "
             "your building envelope and follows you into every future appraisal of the whole tract."),
            ("Access and crossings",
             "Where they can enter, how often, which roads they build, who maintains them, and whether you can "
             "still cross your own easement with equipment."),
            ("Temporary construction easement",
             "Work space outside the permanent corridor is a separate taking with its own value, and it is "
             "frequently folded in for free."),
            ("The easement language itself",
             "Width, height, vegetation control, future additional circuits, assignment to third parties. The "
             "document outlives the check by decades."),
        ],

        "form_source": "765kv_lp",
        "form_project": "765 kV Landing Page",
        "form_heading": "Free review by a senior consultant &mdash; Oncor 765 kV",
        "footer_note": ("Route geometry shown on this page is published by Oncor Electric Delivery; confirm against "
                        "the official filings before relying on it."),
    },

    # ------------------------------------------------------------------
    # NEXT LANDING PAGE - copy the block above, change these seven fields
    # and delete this comment:
    #   slug, title, desc, h1, sub, project_ids, form_source
    # ------------------------------------------------------------------

]


def build():
    return [render(p) for p in PAGES]


if __name__ == "__main__":
    for url, n in build():
        print((url, n))
