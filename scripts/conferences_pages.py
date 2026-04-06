# scripts/conferences_pages.py
# Conference index page generator for The ABM Pulse.

import os
import json

from nav_config import SITE_NAME, SITE_URL, CURRENT_YEAR
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       breadcrumb_html, newsletter_cta_html)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")


def load_conferences():
    with open(os.path.join(DATA_DIR, "conferences.json"), "r") as f:
        return json.load(f)


def build_conferences_index():
    """Build /conferences/ index page."""
    conferences = load_conferences()
    role = "Account-Based Marketing"
    title = f"Best {role} Conferences in {CURRENT_YEAR}"
    description = (
        f"Top {len(conferences)} conferences for ABM professionals in {CURRENT_YEAR}. "
        f"Events covering intent data, account targeting, orchestration, and ABM platform strategy."
    )

    crumbs = [("Home", "/"), ("Conferences", None)]
    bc_schema = get_breadcrumb_schema([("Home", "/"), (f"{role} Conferences", f"{SITE_URL}/conferences/")])
    bc_html = breadcrumb_html(crumbs)

    cards_html = ""
    for conf in conferences:
        tags_html = "".join(
            f'<span class="conference-tag">{tag}</span>' for tag in conf["relevance_tags"][:4]
        )
        attendees = f"{conf['typical_attendees']:,}" if conf['typical_attendees'] else "TBA"
        cards_html += f'''<div class="conference-card">
    <div class="conference-card-header">
        <h3><a href="{conf['website_url']}" target="_blank" rel="noopener">{conf['name']}</a></h3>
        <span class="conference-organizer">by {conf['organizer']}</span>
    </div>
    <p class="conference-description">{conf['description']}</p>
    <div class="conference-meta">
        <span class="conference-location">{conf['location']}</span>
        <span class="conference-attendees">{attendees} typical attendees</span>
    </div>
    <div class="conference-tags">{tags_html}</div>
    <a href="{conf['website_url']}" target="_blank" rel="noopener" class="conference-link">Visit website</a>
</div>
'''

    body = f'''{bc_html}
<section class="page-header">
    <h1>{title}</h1>
    <p class="page-subtitle">The events where ABM professionals learn targeting strategies, explore platforms, and connect with practitioners.</p>
</section>

<section class="content-section">
    <div class="content-body">
        <p>Account-based marketing has matured from an experimental tactic into a core go-to-market strategy for B2B companies. But the discipline is still evolving rapidly. Intent data capabilities expand every year. New orchestration patterns emerge. The line between ABM and demand gen continues to blur. Conferences are where you see the cutting edge of what ABM teams are actually doing, not just what vendors claim is possible.</p>

        <p>The best ABM conferences bring together practitioners who are running real programs with real budgets and real results. They share what account selection frameworks actually work, how they measure ABM impact beyond vanity metrics, and how they get sales teams to care about the target account list. That practitioner knowledge is what separates great ABM programs from mediocre ones.</p>

        <p>We curated this list of {len(conferences)} conferences based on their relevance to ABM professionals in {CURRENT_YEAR}. The list includes ABM-specific events, broader B2B marketing conferences with strong ABM tracks, and platform-specific gatherings from the major ABM vendors.</p>

        <h2>Picking the Right ABM Conference</h2>
        <p>ABM conferences break into a few categories. Vendor-led events like 6sense Breakthrough and Demandbase ABM Innovation Summit are essential if you use those platforms or are evaluating them. Research-led events like Forrester B2B Summit and ITSMA Marketing Vision provide strategic frameworks and maturity benchmarks. Community-driven events like FlipMyFunnel offer practitioner-to-practitioner knowledge sharing in a more intimate setting.</p>

        <p>If your ABM program is still getting started, broader events with strong ABM tracks give you the strategic context you need. If you are running a mature program and want to push into advanced orchestration, one-to-one ABM, or buying group targeting, the ABM-specific events will deliver more value per session.</p>

        <h2>Top {role} Conferences in {CURRENT_YEAR}</h2>
    </div>
</section>

<section class="conferences-grid">
    {cards_html}
</section>

<section class="content-section">
    <div class="content-body">
        <h2>Getting the Most From ABM Events</h2>
        <p>ABM is a cross-functional discipline, and the best conference experiences reflect that. If possible, bring a sales counterpart with you. Many ABM conference sessions cover sales-marketing alignment, and having both perspectives in the room makes the content immediately more actionable.</p>

        <p>Before you go, prepare a short list of the specific challenges your ABM program faces. Use those as conversation starters with other attendees. ABM practitioners are generally willing to share what they have learned, including their failures. Those candid peer conversations are often more valuable than any keynote session.</p>
    </div>
</section>

{newsletter_cta_html("Get conference recaps and ABM insights delivered weekly.")}
'''

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/conferences/",
        body_content=body,
        active_path="/conferences/",
        extra_head=bc_schema,
    )
    write_page("/conferences/index.html", page)
    print(f"  Built: /conferences/ ({len(conferences)} conferences)")
