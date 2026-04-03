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
        <a href="/jobs/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128188;</span></div>
            <h3>Job Board</h3>
            <p>Curated ABM roles from B2B companies. Updated twice a week from 2,500+ tracked postings.</p>
            <span class="preview-link">View all jobs &rarr;</span>
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
    content = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Built: robots.txt")


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

    print("\n  Building meta files...")
    build_sitemap()
    build_robots()

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
