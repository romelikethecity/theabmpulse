# scripts/build.py
# Main build pipeline: generates all pages, sitemap, robots, CNAME.
# Data + page generators live here. HTML shell lives in templates.py.
# Site constants live in nav_config.py.

import os
import sys
import re
import shutil
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import *
import templates
from templates import (get_page_wrapper, write_page, get_homepage_schema,
                       get_breadcrumb_schema, get_faq_schema,
                       get_article_schema,
                       breadcrumb_html, newsletter_cta_html, faq_html, ALL_PAGES)
from salary_pages import build_all_salary_pages
from tool_pages import build_all_tool_pages, TOOL_COMPARISONS, ROUNDUPS
from glossary_pages import build_all_glossary_pages
from build_companies import build_all_company_pages
from report_pages import build_all_report_pages
from conferences_pages import build_conferences_index

# OG image generation state
OG_PAGES = []
SKIP_OG = "--skip-og" in sys.argv


# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
BUILD_DATE = datetime.now().strftime("%Y-%m-%d")

# Wire up templates module
templates.OUTPUT_DIR = OUTPUT_DIR
templates.SKIP_OG = SKIP_OG


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def pad_description(desc, target_min=150, target_max=158):
    """Ensure description is within 150-158 chars by appending filler."""
    suffixes = [" Updated weekly.", " Independent.", " Free.", " No ads."]
    used = set()
    for suffix in suffixes:
        if target_min <= len(desc) <= target_max:
            return desc
        if suffix in used:
            continue
        new = desc + suffix
        if len(new) <= target_max:
            desc = new
            used.add(suffix)
    if len(desc) > target_max:
        desc = desc[:target_max - 1].rstrip() + "."
    return desc


def fmt_salary(n):
    """Format salary number: 132000 -> '$132K'"""
    return f"${n // 1000}K"


# ---------------------------------------------------------------------------
# Page Generators
# ---------------------------------------------------------------------------

def build_homepage():
    """Generate the homepage with Organization+WebSite schema."""
    title = "ABM Salary and Career Intelligence"
    description = pad_description(
        "Salary benchmarks, tool reviews, and career data for ABM professionals."
        " Vendor-neutral and data-driven. For strategists, managers, and directors."
    )

    body = '''<section class="hero">
    <div class="hero-inner">
        <h1>Account-Based Marketing, Finally Mapped Out</h1>
        <p class="hero-subtitle">Salary data, tool reviews, career paths, and job listings for ABM professionals. The resource hub this space has been missing.</p>
        <div class="stat-grid">
            <div class="stat-block">
                <span class="stat-value">2,500+</span>
                <span class="stat-label">Roles Tracked</span>
            </div>
            <div class="stat-block">
                <span class="stat-value">$85K&#8209;$220K+</span>
                <span class="stat-label">Salary Range</span>
            </div>
            <div class="stat-block">
                <span class="stat-value">68%</span>
                <span class="stat-label">YoY Growth</span>
            </div>
        </div>
        <form class="hero-signup" onsubmit="return false;">
            <input type="email" placeholder="Your email" aria-label="Email address" required>
            <button type="submit" class="btn btn--primary">Get the Weekly Pulse</button>
        </form>
        <p class="hero-signup-note">Free weekly newsletter. Salary shifts, tool intel, job data.</p>
    </div>
</section>

<section class="logo-bar">
    <p class="logo-bar-label">Tracking hiring data from companies using</p>
    <div class="logo-bar-row">
        <span class="logo-name">6sense</span>
        <span class="logo-name">Demandbase</span>
        <span class="logo-name">Terminus</span>
        <span class="logo-name">RollWorks</span>
        <span class="logo-name">Sendoso</span>
        <span class="logo-name">Reachdesk</span>
        <span class="logo-name">Bombora</span>
        <span class="logo-name">HubSpot</span>
        <span class="logo-name">Salesforce</span>
        <span class="logo-name">Marketo</span>
    </div>
</section>

<section class="section-previews">
    <h2 class="section-previews-heading">Explore ABM Career Intelligence</h2>
    <div class="preview-grid">
        <a href="/salary/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128176;</span></div>
            <h3>Salary Data</h3>
            <p>Breakdowns by seniority, location, and company stage. See where ABM strategists, managers, and directors land.</p>
            <span class="preview-link">Browse salary data &rarr;</span>
        </a>
        <a href="/tools/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128295;</span></div>
            <h3>Tool Reviews</h3>
            <p>Practitioner-tested reviews of 6sense, Demandbase, Terminus, and more. Honest scores, no pay-to-play.</p>
            <span class="preview-link">Browse tools &rarr;</span>
        </a>
        <a href="/careers/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128200;</span></div>
            <h3>Career Guides</h3>
            <p>How to break into ABM, level up, and negotiate. Interview prep, skill maps, and role comparisons.</p>
            <span class="preview-link">Browse guides &rarr;</span>
        </a>
        <a href="/comparisons/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#9878;</span></div>
            <h3>Tool Comparisons</h3>
            <p>Head-to-head breakdowns of 6sense vs Demandbase, Terminus vs RollWorks, and more. Side-by-side verdicts.</p>
            <span class="preview-link">Browse comparisons &rarr;</span>
        </a>
        <a href="/glossary/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128218;</span></div>
            <h3>ABM Glossary</h3>
            <p>Clear definitions for ABM terms. Intent signals, account scoring, buying committees, and more.</p>
            <span class="preview-link">Browse glossary &rarr;</span>
        </a>
        <a href="/newsletter/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128232;</span></div>
            <h3>Weekly Newsletter</h3>
            <p>Salary shifts, tool intel, and hiring trends delivered every Monday.</p>
            <span class="preview-link">Get the weekly pulse &rarr;</span>
        </a>
    </div>
</section>

'''
    body += newsletter_cta_html()

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/",
        body_content=body,
        active_path="/",
        extra_head=get_homepage_schema(),
        body_class="page-home",
    )
    write_page("index.html", page)
    print(f"  Built: index.html")


def build_about_page():
    """Generate the about page."""
    title = "About The ABM Pulse"
    description = pad_description(
        "The ABM Pulse offers vendor-neutral salary benchmarks, tool reviews, and career data"
        " for account-based marketing professionals."
    )

    crumbs = [("Home", "/"), ("About", None)]
    bc_html = breadcrumb_html(crumbs)
    bc_schema = get_breadcrumb_schema([("Home", "/"), ("About", "/about/")])

    body = f'''<div class="page-header container">
    {bc_html}
    <h1>About The ABM Pulse</h1>
    <p>The ABM Pulse is an independent resource hub for account-based marketing professionals. We track salary data, review tools, and analyze the ABM job market so you can make informed career decisions.</p>
    <h2>What We Cover</h2>
    <ul>
        <li><strong>Salary data</strong> broken down by seniority, location, and company stage</li>
        <li><strong>Tool reviews</strong> of platforms like 6sense, Demandbase, Terminus, and RollWorks</li>
        <li><strong>Career guides</strong> for ABM strategists, managers, and directors</li>
        <li><strong>Job board</strong> with curated ABM roles updated twice weekly</li>
        <li><strong>Weekly newsletter</strong> with salary shifts, tool intel, and market data</li>
    </ul>
    <h2>Who We Are</h2>
    <p>Built by <strong>Rome Thorndike</strong>. All content is vendor-neutral and based on real market data. We don't accept pay-to-play reviews or sponsored rankings.</p>
    <p>Questions? Reach out at <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a>.</p>
</div>'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/about/",
        body_content=body, active_path="/about/", extra_head=bc_schema,
    )
    write_page("about/index.html", page)
    print(f"  Built: about/index.html")


def build_newsletter_page():
    """Generate the newsletter signup page."""
    title = "The ABM Pulse Newsletter"
    description = pad_description(
        "Weekly ABM salary shifts, tool intel, and job market data. Free newsletter for account-based marketing professionals."
    )

    body = '''<div class="newsletter-page">
    <h1>The ABM Pulse Newsletter</h1>
    <p class="lead">Weekly salary shifts, tool intel, and ABM job market data. Free, every Monday.</p>
    <ul class="newsletter-features">
        <li>ABM salary benchmarks and week-over-week changes</li>
        <li>Tool adoption trends across 6sense, Demandbase, Terminus, and more</li>
        <li>New ABM job postings with salary transparency</li>
        <li>Career moves and hiring signals from the ABM market</li>
    </ul>
    <form class="hero-signup" onsubmit="return false;">
        <input type="email" placeholder="Your email" aria-label="Email address" required>
        <button type="submit" class="btn btn--primary">Get the Weekly Pulse</button>
    </form>
    <p class="hero-signup-note">No spam. Unsubscribe anytime.</p>
</div>'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/newsletter/",
        body_content=body, active_path="/newsletter/",
    )
    write_page("newsletter/index.html", page)
    print(f"  Built: newsletter/index.html")


def build_privacy_page():
    """Generate privacy policy page."""
    title = "Privacy Policy"
    description = pad_description(
        f"Privacy policy for {SITE_NAME}. How we collect, use, and protect your data."
    )

    body = f'''<div class="legal-content">
    <h1>Privacy Policy</h1>
    <p><em>Last updated: {BUILD_DATE}</em></p>
    <h2>Information We Collect</h2>
    <p>{SITE_NAME} ("we," "us," or "our") collects minimal data to operate this website and newsletter:</p>
    <ul>
        <li><strong>Email address</strong> when you subscribe to our newsletter (via Resend)</li>
        <li><strong>Analytics data</strong> through Google Analytics (page views, device type, referral source)</li>
    </ul>
    <h2>How We Use Your Data</h2>
    <ul>
        <li>To send our weekly newsletter (you can unsubscribe anytime)</li>
        <li>To understand site usage and improve content</li>
    </ul>
    <h2>Third-Party Services</h2>
    <ul>
        <li><strong>Resend</strong> for email delivery and subscriber management</li>
        <li><strong>Cloudflare</strong> for DNS, CDN, and worker hosting</li>
        <li><strong>GitHub Pages</strong> for site hosting</li>
        <li><strong>Google Analytics</strong> for anonymized usage metrics</li>
    </ul>
    <h2>Your Rights</h2>
    <p>You can request deletion of your data at any time by emailing <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a>.</p>
    <h2>Contact</h2>
    <p>Questions about this policy? Email <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a>.</p>
</div>'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/privacy/",
        body_content=body,
    )
    write_page("privacy/index.html", page)
    print(f"  Built: privacy/index.html")


def build_terms_page():
    """Generate terms of service page."""
    title = "Terms of Service"
    description = pad_description(
        f"Terms of service for {SITE_NAME}. Usage terms for our website and newsletter."
    )

    body = f'''<div class="legal-content">
    <h1>Terms of Service</h1>
    <p><em>Last updated: {BUILD_DATE}</em></p>
    <h2>Acceptance of Terms</h2>
    <p>By accessing {SITE_NAME} ({SITE_URL}), you agree to these terms. If you disagree, do not use the site.</p>
    <h2>Content</h2>
    <p>All salary data, tool reviews, and career guides are provided for informational purposes only. We strive for accuracy but do not guarantee completeness. Salary figures are estimates based on market research and should not be treated as binding offers.</p>
    <h2>Affiliate Links</h2>
    <p>Some tool review pages contain affiliate links. We earn a commission if you purchase through them. This does not affect our review scores or rankings. All reviews reflect honest practitioner opinions.</p>
    <h2>Newsletter</h2>
    <p>By subscribing to our newsletter, you consent to receive weekly emails. You can unsubscribe at any time via the link in every email.</p>
    <h2>Intellectual Property</h2>
    <p>All content on {SITE_NAME} is owned by us unless otherwise noted. You may not reproduce, distribute, or create derivative works without permission.</p>
    <h2>Contact</h2>
    <p>Questions? Email <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a>.</p>
</div>'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/terms/",
        body_content=body,
    )
    write_page("terms/index.html", page)
    print(f"  Built: terms/index.html")


def build_404_page():
    """Generate 404 error page."""
    body = '''<div class="error-page">
    <div class="error-code">404</div>
    <h1>Page not found</h1>
    <p>The page you're looking for doesn't exist or has been moved.</p>
    <a href="/" class="btn btn--primary">Back to homepage</a>
</div>'''

    page = get_page_wrapper(
        title="Page Not Found",
        description="This page could not be found.",
        canonical_path="/404.html",
        body_content=body,
        body_class="page-404",
    )
    write_page("404.html", page)
    print(f"  Built: 404.html")


def build_careers_index():
    """Generate the careers index page."""
    title = "ABM Career Guides"
    description = pad_description(
        "Career guides for account-based marketing professionals. Paths, skills, certifications, and salary expectations for ABM roles."
    )

    crumbs = [("Home", "/"), ("Careers", None)]
    bc_html = breadcrumb_html(crumbs)
    bc_schema = get_breadcrumb_schema([("Home", "/"), ("Careers", "/careers/")])

    body = f'''<div class="page-header container">
    {bc_html}
    <h1>ABM Career Guides</h1>
    <p class="lead">Everything you need to break into account-based marketing, level up in your current role, or transition from adjacent fields. Practical guidance backed by real hiring data.</p>
</div>

<div class="salary-content">
    <h2>Why ABM Is a Career Worth Pursuing</h2>
    <p>Account-based marketing has gone from a niche tactic to a core strategy at most B2B companies with deal sizes above $50K. That shift created a new class of specialized roles that did not exist five years ago. ABM strategists, ABM managers, and directors of ABM are now standard titles at mid-market and enterprise companies across SaaS, financial services, cybersecurity, and healthcare IT.</p>
    <p>The talent gap is real. Companies need people who can run multi-channel programs targeting named accounts, and there are not enough practitioners with hands-on experience. That supply-demand imbalance means competitive salaries, faster promotions, and strong negotiating leverage for people with the right skills.</p>

    <h2>Career Paths in ABM</h2>
    <p>Most ABM professionals enter through one of three doors:</p>
    <ul>
        <li><strong>Demand generation:</strong> You already run campaigns and understand pipeline metrics. ABM narrows your focus from broad audiences to specific accounts, which often means higher conversion rates and more strategic work.</li>
        <li><strong>Field marketing or sales development:</strong> You know the accounts, the personas, and what sales needs. ABM gives you a framework to scale that knowledge across channels.</li>
        <li><strong>Marketing operations:</strong> You built the tech stack and scoring models. ABM roles let you apply that infrastructure expertise to a more targeted, measurable program.</li>
    </ul>

    <h2>Core Skills Every ABM Professional Needs</h2>
    <div class="preview-grid" style="grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));">
        <div class="preview-card" style="cursor: default;">
            <h3>Account Selection</h3>
            <p>Building ideal customer profiles, scoring accounts with intent and firmographic data, and aligning target lists with sales.</p>
        </div>
        <div class="preview-card" style="cursor: default;">
            <h3>Multi-Channel Orchestration</h3>
            <p>Running coordinated plays across display ads, email, direct mail, events, and web personalization for the same account list.</p>
        </div>
        <div class="preview-card" style="cursor: default;">
            <h3>Platform Proficiency</h3>
            <p>Hands-on experience with at least one ABM platform (6sense, Demandbase, Terminus, or RollWorks) plus your marketing automation system.</p>
        </div>
        <div class="preview-card" style="cursor: default;">
            <h3>Sales Alignment</h3>
            <p>Working directly with sales on account intelligence, play design, and feedback loops. ABM without sales buy-in is just marketing.</p>
        </div>
        <div class="preview-card" style="cursor: default;">
            <h3>Measurement and Attribution</h3>
            <p>Tracking account engagement, pipeline influence, and revenue attribution. Knowing what to measure and how to present it to leadership.</p>
        </div>
        <div class="preview-card" style="cursor: default;">
            <h3>Content Strategy</h3>
            <p>Creating or commissioning content for specific verticals, personas, and buying stages. One-size-fits-all content does not work in ABM.</p>
        </div>
    </div>

    <h2>Explore Career Guides</h2>
    <div class="related-links-grid">
        <a href="/careers/how-to-become-abm-strategist/" class="related-link-card">How to Become an ABM Strategist</a>
        <a href="/salary/" class="related-link-card">ABM Salary Data</a>
        <a href="/tools/" class="related-link-card">ABM Tools and Platforms</a>
    </div>

    <h2>Salary Expectations</h2>
    <p>ABM roles consistently pay above general marketing positions at the same level. Entry-level ABM coordinators start around $65K-$80K. Mid-level ABM managers land between $100K-$140K. Senior directors and VPs of ABM at enterprise companies can reach $180K-$220K+ with equity. See our full <a href="/salary/">salary data section</a> for breakdowns by seniority, location, and company stage.</p>

    {newsletter_cta_html("Get weekly ABM career intelligence.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/",
        body_content=body, active_path="/careers/", extra_head=bc_schema,
    )
    write_page("careers/index.html", page)
    print(f"  Built: careers/index.html")


def build_careers_abm_strategist():
    """Generate the How to Become an ABM Strategist guide."""
    title = "How to Become an ABM Strategist"
    description = pad_description(
        "Complete guide to becoming an ABM strategist. Career paths, required skills, certifications, tools, and salary expectations for 2026."
    )

    crumbs = [("Home", "/"), ("Careers", "/careers/"), ("How to Become an ABM Strategist", None)]
    bc_html = breadcrumb_html(crumbs)
    bc_schema = get_breadcrumb_schema([
        ("Home", "/"),
        ("Careers", "/careers/"),
        ("How to Become an ABM Strategist", "/careers/how-to-become-abm-strategist/"),
    ])

    faq_pairs = [
        ("What degree do I need to become an ABM strategist?",
         "No specific degree is required. Most ABM strategists have backgrounds in marketing, business, or communications. What matters more is hands-on experience with ABM platforms, demand generation campaigns, and sales alignment. Certifications from Demandbase University or 6sense carry more weight in interviews than a specific degree."),
        ("How long does it take to become an ABM strategist?",
         "If you are already in B2B marketing (demand gen, field marketing, or marketing ops), you can transition into an ABM-focused role within 6 to 12 months by building platform skills and running a pilot program. Starting from scratch with no marketing background, expect 2 to 3 years to build the foundation."),
        ("What is the average salary for an ABM strategist?",
         "ABM strategist salaries range from $85K to $130K depending on location, company size, and experience. Senior ABM strategists at enterprise companies can earn $130K to $160K. See our salary data section for detailed breakdowns."),
        ("Is ABM a good career path in 2026?",
         "Yes. ABM adoption continues to grow as B2B companies shift budget from broad demand gen to targeted account programs. The talent shortage means strong negotiating leverage and faster career progression for qualified practitioners."),
    ]

    faq_section = faq_html(faq_pairs)
    faq_schema = get_faq_schema(faq_pairs)

    body = f'''<div class="page-header container">
    {bc_html}
    <h1>How to Become an ABM Strategist</h1>
    <p class="lead">A practical guide to breaking into account-based marketing. Career paths, the skills that actually matter, certifications worth your time, the tools you need to know, and what to expect on compensation.</p>
</div>

<div class="salary-content">
    <h2>What Does an ABM Strategist Do?</h2>
    <p>An ABM strategist designs and executes account-based marketing programs that target specific high-value accounts rather than broad audiences. The role sits at the intersection of marketing, sales, and data. On any given day, you might be building a target account list with intent data, designing a multi-channel play for a tier-1 account, briefing sales on account engagement signals, or analyzing pipeline influence from your latest campaign.</p>
    <p>Unlike generalist marketing roles, ABM strategists own the full lifecycle for their account segments. You select the accounts, design the plays, coordinate the channels, and measure the results. That end-to-end ownership is what makes the role both demanding and rewarding.</p>
    <p>Common responsibilities include:</p>
    <ul>
        <li>Building and maintaining ideal customer profiles (ICPs) and target account lists</li>
        <li>Designing multi-channel plays (ads, email, direct mail, events, web personalization)</li>
        <li>Configuring and managing ABM platforms (6sense, Demandbase, Terminus, or RollWorks)</li>
        <li>Collaborating with sales on account intelligence and play execution</li>
        <li>Analyzing account engagement, pipeline velocity, and revenue attribution</li>
        <li>Reporting program performance to marketing leadership</li>
    </ul>

    <h2>Career Paths Into ABM</h2>
    <h3>From Demand Generation</h3>
    <p>This is the most common path. If you are running lead gen campaigns, you already understand pipeline metrics, campaign operations, and marketing automation. The transition to ABM means narrowing your targeting from broad audiences to named accounts and shifting your success metrics from MQLs to account engagement and pipeline influence.</p>
    <p>What to do: Volunteer to run an ABM pilot at your current company. Pick 50 accounts, build a multi-channel play, and measure the results against your standard demand gen programs. That pilot becomes your case study for ABM roles.</p>

    <h3>From Field Marketing or Sales Development</h3>
    <p>Field marketers and SDRs have deep account knowledge and direct relationships with sales. You understand which accounts matter, what messaging resonates, and how deals actually progress. ABM gives you a structured framework to scale that knowledge.</p>
    <p>What to do: Start documenting the account-specific tactics you already use. Build a one-to-few ABM play for your top 10 accounts using existing tools. Show the results to marketing leadership as proof of concept.</p>

    <h3>From Marketing Operations</h3>
    <p>Marketing ops professionals built the infrastructure that ABM runs on: the CRM, the marketing automation platform, the data integrations, the scoring models. ABM roles let you move from building the pipes to designing what flows through them.</p>
    <p>What to do: Get hands-on with an ABM platform trial. Demandbase and RollWorks both offer sandbox environments. Build an integration between the ABM platform and your existing tech stack, then propose an ABM pilot to your team.</p>

    <h2>Skills That Actually Matter</h2>
    <h3>Must-Have Skills</h3>
    <ul>
        <li><strong>Account selection and tiering:</strong> Building ICPs using firmographic, technographic, and intent data. Scoring and prioritizing accounts into tiers (1:1, 1:few, 1:many).</li>
        <li><strong>ABM platform proficiency:</strong> At least one platform deeply (6sense, Demandbase, Terminus, or RollWorks). Knowing how to configure audiences, build segments, activate ads, and pull reports.</li>
        <li><strong>Multi-channel orchestration:</strong> Coordinating display ads, email sequences, direct mail, events, and web personalization for the same account list without message fatigue.</li>
        <li><strong>Sales alignment:</strong> Running account reviews, sharing engagement data with sales in formats they actually use, and building feedback loops that improve targeting over time.</li>
        <li><strong>Analytics and attribution:</strong> Measuring account engagement scores, pipeline influence, deal velocity, and revenue attribution. Knowing the difference between self-reported and multi-touch attribution.</li>
    </ul>

    <h3>Nice-to-Have Skills</h3>
    <ul>
        <li><strong>Intent data interpretation:</strong> Understanding surge scores, topic clusters, and how to separate signal from noise in intent data feeds from Bombora, G2, or first-party sources.</li>
        <li><strong>Content strategy:</strong> Creating or commissioning account-specific content (personalized landing pages, vertical case studies, exec-level briefings).</li>
        <li><strong>Marketing automation:</strong> HubSpot or Marketo proficiency for building ABM-specific nurture flows and scoring models.</li>
        <li><strong>Data analysis:</strong> SQL or basic data manipulation for building custom reports beyond what ABM platforms offer out of the box.</li>
        <li><strong>Budget management:</strong> Allocating spend across channels and tiers based on expected pipeline impact.</li>
    </ul>

    <h2>Certifications Worth Your Time</h2>
    <p>Not all certifications carry equal weight. Here are the ones that hiring managers actually look for:</p>

    <h3>High Value</h3>
    <ul>
        <li><strong>Demandbase University:</strong> Free certification program covering ABM fundamentals, platform usage, and program design. The most recognized ABM-specific credential in the market. Completing it signals you understand the Demandbase ecosystem and ABM best practices.</li>
        <li><strong>6sense Certifications:</strong> 6sense offers role-based certifications for marketers, sales teams, and administrators. The marketer certification covers intent data interpretation, audience building, and campaign activation. Particularly valuable if you are targeting companies that run 6sense.</li>
    </ul>

    <h3>Moderate Value</h3>
    <ul>
        <li><strong>HubSpot ABM Certification:</strong> Free course covering ABM strategy within the HubSpot ecosystem. Good foundational knowledge, though less recognized than Demandbase or 6sense certs for dedicated ABM roles.</li>
        <li><strong>Terminus ABM Certification:</strong> Platform-specific certification. Useful if you are targeting companies that use Terminus, but the platform's market position has shifted since the DemandScience acquisition.</li>
        <li><strong>ITSMA/Momentum ABM Certification:</strong> The most strategic (and expensive) ABM certification. Focused on enterprise 1:1 ABM. Best for senior practitioners moving into director-level roles.</li>
    </ul>

    <h3>Supporting Certifications</h3>
    <ul>
        <li><strong>Salesforce Administrator:</strong> Understanding CRM architecture is critical for ABM. A Salesforce admin cert shows you can work with the data layer that ABM depends on.</li>
        <li><strong>Google Analytics:</strong> Basic analytics competency. Not ABM-specific, but table stakes for any marketing role.</li>
    </ul>

    <h2>Tools You Need to Know</h2>
    <table class="data-table">
        <thead><tr><th>Category</th><th>Tools</th><th>Why It Matters</th></tr></thead>
        <tbody>
            <tr><td>ABM Platforms</td><td>6sense, Demandbase, Terminus, RollWorks</td><td>Core platform for account targeting, intent data, and orchestration</td></tr>
            <tr><td>Intent Data</td><td>Bombora, G2 Buyer Intent, TrustRadius</td><td>Identifies which accounts are actively researching your category</td></tr>
            <tr><td>Marketing Automation</td><td>HubSpot, Marketo, Pardot</td><td>Email nurtures, scoring, and campaign operations</td></tr>
            <tr><td>CRM</td><td>Salesforce, HubSpot CRM</td><td>Account and opportunity data, sales alignment</td></tr>
            <tr><td>Personalization</td><td>Mutiny, Intellimize, PathFactory</td><td>Tailoring web experiences for target accounts</td></tr>
            <tr><td>Direct Mail</td><td>Sendoso, Reachdesk, Alyce</td><td>Physical touchpoints that cut through digital noise</td></tr>
            <tr><td>Analytics</td><td>Salesforce Reports, Tableau, Looker</td><td>Pipeline attribution and program reporting</td></tr>
        </tbody>
    </table>
    <p>You do not need to master every tool. Focus on one ABM platform deeply and have working knowledge of the supporting categories. See our <a href="/tools/">full tool reviews</a> for detailed breakdowns.</p>

    <h2>Salary Expectations</h2>
    <p>ABM roles pay above general marketing positions at equivalent seniority levels. Here is what to expect in 2026:</p>
    <table class="data-table">
        <thead><tr><th>Role</th><th>Salary Range</th><th>Notes</th></tr></thead>
        <tbody>
            <tr><td>ABM Coordinator / Associate</td><td>$65K - $85K</td><td>Entry-level, supports ABM manager</td></tr>
            <tr><td>ABM Strategist</td><td>$85K - $130K</td><td>Owns program design and execution</td></tr>
            <tr><td>Senior ABM Strategist</td><td>$120K - $160K</td><td>Leads strategy for multiple segments</td></tr>
            <tr><td>ABM Manager</td><td>$110K - $150K</td><td>Manages team and program budget</td></tr>
            <tr><td>Director of ABM</td><td>$150K - $200K</td><td>Sets strategy, reports to VP/CMO</td></tr>
            <tr><td>VP of ABM</td><td>$180K - $220K+</td><td>Enterprise companies, often includes equity</td></tr>
        </tbody>
    </table>
    <p>Location matters. San Francisco, New York, and Boston pay 15-25% above these ranges. Remote roles typically benchmark to the national median. See our <a href="/salary/">salary data</a> for full breakdowns by location and company stage.</p>

    <h2>How to Get Your First ABM Role</h2>
    <ol>
        <li><strong>Run a pilot at your current company.</strong> Pick 25-50 accounts, design a multi-channel play, and measure the results over 90 days. Document everything.</li>
        <li><strong>Get certified.</strong> Complete Demandbase University and one 6sense certification. Both are free. This takes about 20 hours total.</li>
        <li><strong>Build your case study.</strong> Write up your pilot results: accounts targeted, channels used, engagement lift, pipeline generated. This becomes the centerpiece of your resume and interviews.</li>
        <li><strong>Target the right companies.</strong> Look for companies that already use ABM platforms (check their job postings for tool requirements). They value practitioners over theorists.</li>
        <li><strong>Network in ABM communities.</strong> Join the ABM Leadership Alliance, FlipMyFunnel community, and LinkedIn ABM groups. Many ABM roles are filled through referrals before they hit job boards.</li>
    </ol>

    {faq_section}

    {newsletter_cta_html("Get weekly ABM career intelligence.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/how-to-become-abm-strategist/",
        body_content=body, active_path="/careers/", extra_head=bc_schema + faq_schema,
    )
    write_page("careers/how-to-become-abm-strategist/index.html", page)
    print(f"  Built: careers/how-to-become-abm-strategist/index.html")


def build_insights_page():
    """Generate the insights hub page."""
    title = "ABM Insights"
    description = pad_description(
        "Analysis and insights on account-based marketing trends, strategies, and best practices for B2B professionals."
    )

    crumbs = [("Home", "/"), ("Insights", None)]
    bc_html = breadcrumb_html(crumbs)
    bc_schema = get_breadcrumb_schema([("Home", "/"), ("Insights", "/insights/")])

    body = f'''<div class="page-header container">
    {bc_html}
    <h1>ABM Insights</h1>
    <p class="lead">Analysis and practical guidance on account-based marketing strategies, trends, and best practices. Written for practitioners, not executives who need a buzzword glossary.</p>
</div>

<div class="salary-content">
    <h2>What You Will Find Here</h2>
    <p>The Insights section is where we publish analysis that goes deeper than our data pages. Think of it as the editorial layer on top of our salary benchmarks, tool reviews, and career guides.</p>
    <ul>
        <li><strong>Strategy breakdowns:</strong> How to structure ABM programs at different company stages and deal sizes</li>
        <li><strong>Trend analysis:</strong> What is actually changing in ABM hiring, tooling, and budgets based on real data</li>
        <li><strong>Practitioner interviews:</strong> Conversations with ABM leaders about what works and what does not</li>
        <li><strong>Playbook teardowns:</strong> Detailed walkthroughs of ABM plays that generated measurable pipeline</li>
    </ul>

    <h2>Explore Related Sections</h2>
    <div class="related-links-grid">
        <a href="/salary/" class="related-link-card">Salary Data</a>
        <a href="/tools/" class="related-link-card">Tool Reviews</a>
        <a href="/comparisons/" class="related-link-card">Tool Comparisons</a>
        <a href="/careers/" class="related-link-card">Career Guides</a>
        <a href="/glossary/" class="related-link-card">ABM Glossary</a>
    </div>

    <p>New insights are published weekly. Subscribe to get them in your inbox every Monday.</p>

    {newsletter_cta_html("Get weekly ABM insights.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/insights/",
        body_content=body, active_path="/insights/", extra_head=bc_schema,
    )
    write_page("insights/index.html", page)
    print(f"  Built: insights/index.html")


def build_blog_redirect():
    """Generate /blog/ as a redirect to /insights/."""
    redirect_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url=/insights/">
    <link rel="canonical" href="{SITE_URL}/insights/">
    <title>Redirecting to Insights</title>
</head>
<body>
    <p>Redirecting to <a href="/insights/">Insights</a>...</p>
</body>
</html>'''
    full_path = os.path.join(OUTPUT_DIR, "blog", "index.html")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(redirect_html)
    # Don't add to ALL_PAGES / sitemap since it's a redirect
    print(f"  Built: blog/index.html (redirect to /insights/)")


def build_comparisons_index():
    """Generate the comparisons index page listing all compare pages."""
    title = "ABM Tool Comparisons"
    description = pad_description(
        "Head-to-head comparisons of ABM tools. 6sense vs Demandbase, Terminus vs RollWorks, and more. Side-by-side verdicts."
    )

    crumbs = [("Home", "/"), ("Comparisons", None)]
    bc_html = breadcrumb_html(crumbs)
    bc_schema = get_breadcrumb_schema([("Home", "/"), ("Comparisons", "/comparisons/")])

    # Build comparison cards from tool_pages data
    comp_cards = ""
    for comp in TOOL_COMPARISONS:
        comp_cards += f'''<a href="/tools/compare/{comp["slug"]}/" class="preview-card">
    <h3>{comp["title"]}</h3>
    <p>{comp["summary"]}</p>
    <span class="preview-link">Read comparison &rarr;</span>
</a>
'''

    # Build roundup cards
    roundup_cards = ""
    for r in ROUNDUPS:
        roundup_cards += f'''<a href="/tools/{r["slug"]}/" class="preview-card">
    <h3>{r["title"]}</h3>
    <p>{r["description"]}</p>
    <span class="preview-link">Read roundup &rarr;</span>
</a>
'''

    body = f'''<div class="page-header container">
    {bc_html}
    <h1>ABM Tool Comparisons</h1>
    <p class="lead">Side-by-side breakdowns of the major ABM platforms and tools. Honest verdicts based on features, pricing, and real practitioner experience.</p>
</div>

<div class="salary-content">
    <h2>Head-to-Head Comparisons</h2>
    <div class="preview-grid" style="grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));">
        {comp_cards}
    </div>

    <h2>Category Roundups</h2>
    <div class="preview-grid" style="grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));">
        {roundup_cards}
    </div>

    <h2>How We Compare Tools</h2>
    <p>Every comparison on The ABM Pulse is based on hands-on evaluation, public documentation, community feedback, and real hiring data. We do not accept payment for rankings or favorable reviews. If a tool has weaknesses, we name them.</p>
    <p>Our evaluations consider:</p>
    <ul>
        <li><strong>Feature depth:</strong> What the tool actually does versus what the marketing site claims</li>
        <li><strong>Pricing transparency:</strong> Real-world pricing ranges, not just "contact us"</li>
        <li><strong>Implementation effort:</strong> How long it takes to get value, not just how long the trial lasts</li>
        <li><strong>Job market signal:</strong> How frequently each tool appears in ABM job postings as a required or preferred skill</li>
        <li><strong>Practitioner feedback:</strong> What actual users say in communities, reviews, and conversations</li>
    </ul>

    {newsletter_cta_html("Get weekly tool comparisons.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/comparisons/",
        body_content=body, active_path="/comparisons/", extra_head=bc_schema,
    )
    write_page("comparisons/index.html", page)
    print(f"  Built: comparisons/index.html")


# ---------------------------------------------------------------------------
# Sitemap, Robots, CNAME
# ---------------------------------------------------------------------------

def build_sitemap():
    urls = ""
    for page_path in ALL_PAGES:
        clean = page_path.replace("index.html", "")
        if not clean.startswith("/"):
            clean = "/" + clean
        if not clean.endswith("/"):
            clean += "/"
        if clean == "//":
            clean = "/"
        urls += f"  <url>\n    <loc>{SITE_URL}{clean}</loc>\n    <lastmod>{BUILD_DATE}</lastmod>\n  </url>\n"

    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"  Built: sitemap.xml ({len(ALL_PAGES)} URLs)")


def build_robots():
    content = f"""User-agent: *
Allow: /

# AI/LLM crawlers - explicitly allowed for AI search citations
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: GoogleOther
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Built: robots.txt")


def build_llms_txt():
    content = """# The ABM Pulse

> Career intelligence for account-based marketing professionals. Salary benchmarks, tool reviews, company hiring profiles, and career guides for ABM strategists, managers, and directors. Vendor-neutral and data-driven.

The ABM Pulse tracks ABM salaries across seniority levels and locations, reviews 20+ ABM tools (platforms, intent data providers, personalization, direct mail, analytics), publishes head-to-head comparisons, and profiles companies actively hiring ABM professionals. The site also covers ABM conferences, glossary terms, and career advancement guides.

## Core Pages

- [Homepage](https://theabmpulse.com/): ABM salary and career intelligence
- [Salary Index](https://theabmpulse.com/salary/): ABM salary data and benchmarks
- [Tools Index](https://theabmpulse.com/tools/): ABM tool reviews and comparisons
- [Companies Hiring](https://theabmpulse.com/companies/): Companies with active ABM roles
- [Career Guides](https://theabmpulse.com/careers/): ABM career development resources
- [Blog](https://theabmpulse.com/blog/): ABM industry analysis and insights
- [About](https://theabmpulse.com/about/): About The ABM Pulse

## Salary Data

- [Salary by Seniority](https://theabmpulse.com/salary/by-seniority/): ABM pay by experience level
- [Salary by Location](https://theabmpulse.com/salary/by-location/): ABM pay by city and region
- [Remote vs Onsite](https://theabmpulse.com/salary/remote-vs-onsite/): Remote ABM salary comparison
- [Salary Calculator](https://theabmpulse.com/salary/calculator/): Estimate your ABM market rate
- [Salary Methodology](https://theabmpulse.com/salary/methodology/): How we source salary data
- [ABM vs Demand Gen Manager](https://theabmpulse.com/salary/vs-demand-gen-manager/): Salary comparison
- [ABM vs Marketing Ops](https://theabmpulse.com/salary/vs-marketing-ops/): Salary comparison
- [ABM vs Campaign Manager](https://theabmpulse.com/salary/vs-campaign-manager/): Salary comparison
- [ABM vs Field Marketing](https://theabmpulse.com/salary/vs-field-marketing/): Salary comparison
- [ABM vs Growth Marketer](https://theabmpulse.com/salary/vs-growth-marketer/): Salary comparison

## Tool Reviews

- [6sense Review](https://theabmpulse.com/tools/6sense-review/): ABM platform review
- [Demandbase Review](https://theabmpulse.com/tools/demandbase-review/): ABM platform review
- [Terminus Review](https://theabmpulse.com/tools/terminus-review/): ABM platform review
- [RollWorks Review](https://theabmpulse.com/tools/rollworks-review/): ABM platform review
- [Triblio Review](https://theabmpulse.com/tools/triblio-review/): ABM platform review
- [Madison Logic Review](https://theabmpulse.com/tools/madison-logic-review/): ABM platform review
- [Bombora Review](https://theabmpulse.com/tools/bombora-review/): Intent data provider review
- [G2 Intent Review](https://theabmpulse.com/tools/g2-intent-review/): Intent data review
- [ZoomInfo Intent Review](https://theabmpulse.com/tools/zoominfo-intent-review/): Intent data review
- [TrustRadius Intent Review](https://theabmpulse.com/tools/trustradius-intent-review/): Intent data review
- [Mutiny Review](https://theabmpulse.com/tools/mutiny-review/): Personalization platform review
- [Intellimize Review](https://theabmpulse.com/tools/intellimize-review/): Personalization review
- [Folloze Review](https://theabmpulse.com/tools/folloze-review/): Content experience review
- [PathFactory Review](https://theabmpulse.com/tools/pathfactory-review/): Content experience review
- [Sendoso Review](https://theabmpulse.com/tools/sendoso-review/): Direct mail platform review
- [Reachdesk Review](https://theabmpulse.com/tools/reachdesk-review/): Direct mail review
- [Alyce Review](https://theabmpulse.com/tools/alyce-review/): Gifting platform review
- [PFL Review](https://theabmpulse.com/tools/pfl-review/): Direct mail review
- [HubSpot Review](https://theabmpulse.com/tools/hubspot-review/): Marketing automation for ABM
- [Marketo Review](https://theabmpulse.com/tools/marketo-review/): Marketing automation review
- [Pardot Review](https://theabmpulse.com/tools/pardot-review/): Salesforce marketing cloud review

## Tool Comparisons

- [6sense vs Demandbase](https://theabmpulse.com/tools/compare/6sense-vs-demandbase/): ABM platform comparison
- [Terminus vs RollWorks](https://theabmpulse.com/tools/compare/terminus-vs-rollworks/): Mid-market ABM comparison
- [Bombora vs G2 Intent](https://theabmpulse.com/tools/compare/bombora-vs-g2-intent/): Intent data comparison
- [Sendoso vs Reachdesk](https://theabmpulse.com/tools/compare/sendoso-vs-reachdesk/): Direct mail comparison
- [HubSpot vs Marketo](https://theabmpulse.com/tools/compare/hubspot-vs-marketo/): Marketing automation comparison
- [Mutiny vs Intellimize](https://theabmpulse.com/tools/compare/mutiny-vs-intellimize/): Personalization comparison

## Best Of Lists

- [Best ABM Platforms](https://theabmpulse.com/tools/best-abm-platforms/): Platform rankings
- [Best Intent Data Providers](https://theabmpulse.com/tools/best-intent-data-providers/): Intent data rankings
- [Best Direct Mail for ABM](https://theabmpulse.com/tools/best-direct-mail-abm/): Direct mail rankings
- [Best Personalization Tools](https://theabmpulse.com/tools/best-personalization-tools/): Personalization rankings

## Tool Categories

- [ABM Platforms](https://theabmpulse.com/tools/category/abm-platforms/): Full ABM platform category
- [Intent Data Providers](https://theabmpulse.com/tools/category/intent-data/): Intent data category
- [Personalization Tools](https://theabmpulse.com/tools/category/personalization/): Website personalization
- [Direct Mail Platforms](https://theabmpulse.com/tools/category/direct-mail/): Corporate gifting and mail
- [Marketing Automation](https://theabmpulse.com/tools/category/marketing-automation/): MAP tools for ABM
- [Analytics](https://theabmpulse.com/tools/category/analytics/): ABM analytics and reporting

## Career Resources

- [How to Become an ABM Strategist](https://theabmpulse.com/careers/how-to-become-abm-strategist/): Career guide
- [ABM Conferences](https://theabmpulse.com/conferences/): ABM events and conferences
- [Best ABM Resources](https://theabmpulse.com/best-abm-resources/): Books, podcasts, communities
- [ABM Glossary](https://theabmpulse.com/glossary/): ABM terminology defined

## Reports

- [ABM Salary Report](https://theabmpulse.com/reports/salary-report/): Annual salary benchmarks
- [ABM Tool Stack Report](https://theabmpulse.com/reports/tool-stack-report/): Tool adoption data
"""
    with open(os.path.join(OUTPUT_DIR, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Built: llms.txt")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"=== The ABM Pulse Build ({BUILD_DATE}) ===\n")

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    print("  Cleaned output/")

    shutil.copytree(ASSETS_DIR, os.path.join(OUTPUT_DIR, "assets"))
    print("  Copied assets/")

    print("\n  Building core pages...")
    build_homepage()
    build_about_page()
    build_newsletter_page()
    build_privacy_page()
    build_terms_page()
    build_404_page()

    # Career guides
    build_careers_index()
    build_careers_abm_strategist()

    # Insights and blog redirect
    build_insights_page()
    build_blog_redirect()

    # Comparisons index
    build_comparisons_index()

    # Salary section (~25 pages)
    build_all_salary_pages(PROJECT_DIR)

    # Tool reviews section (~40 pages)
    build_all_tool_pages(PROJECT_DIR)

    # Glossary section (45 terms + index)
    build_all_glossary_pages(PROJECT_DIR)

    build_all_company_pages(PROJECT_DIR)

    build_all_report_pages(PROJECT_DIR)

    build_conferences_index()

    print("\n  Building meta files...")
    build_sitemap()
    build_robots()
    build_llms_txt()

    with open(os.path.join(OUTPUT_DIR, "CNAME"), "w", encoding="utf-8") as f:
        f.write("theabmpulse.com\n")
    print("  Built: CNAME")

    # Google Search Console verification file
    if GOOGLE_SITE_VERIFICATION:
        verification_path = os.path.join(OUTPUT_DIR, GOOGLE_SITE_VERIFICATION)
        with open(verification_path, "w", encoding="utf-8") as f:
            f.write(f"google-site-verification: {GOOGLE_SITE_VERIFICATION}")
        print(f"  Generated {GOOGLE_SITE_VERIFICATION}")

    print(f"\n=== Build complete: {len(ALL_PAGES)} pages ===")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Preview: cd output && python3 -m http.server 8090")


if __name__ == "__main__":
    main()
