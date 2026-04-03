# scripts/nav_config.py
# Site constants, navigation, and footer configuration.
# Pure data — zero logic, zero imports.

SITE_NAME = "The ABM Pulse"
SITE_URL = "https://theabmpulse.com"
SITE_TAGLINE = "Career intelligence for account-based marketing professionals"
COPYRIGHT_YEAR = "2026"
CURRENT_YEAR = 2026
CSS_VERSION = "1"

CTA_HREF = "/newsletter/"
CTA_LABEL = "Get the Weekly Pulse"

SIGNUP_WORKER_URL = "https://abm-newsletter-signup.rome-workers.workers.dev/subscribe"

GA_MEASUREMENT_ID = ""
GOOGLE_SITE_VERIFICATION = ""
GOOGLE_SITE_VERIFICATION_META = ""

NAV_ITEMS = [
    {
        "href": "/salary/",
        "label": "Salary Data",
        "children": [
            {"href": "/salary/", "label": "Salary Index"},
            {"href": "/salary/by-seniority/", "label": "By Seniority"},
            {"href": "/salary/by-location/", "label": "By Location"},
            {"href": "/salary/by-company-stage/", "label": "By Company Stage"},
            {"href": "/salary/comparisons/", "label": "Comparisons"},
        ],
    },
    {
        "href": "/tools/",
        "label": "Tools",
        "children": [
            {"href": "/tools/", "label": "Tools Index"},
            {"href": "/tools/category/intent-data/", "label": "Tool Categories"},
            {"href": "/tools/6sense-review/", "label": "Tool Reviews"},
        ],
    },
    {
        "href": "/careers/",
        "label": "Careers",
        "children": [
            {"href": "/careers/", "label": "Career Guides"},
            {"href": "/careers/how-to-become-abm-strategist/", "label": "How to Break In"},
        ],
    },
    {"href": "/glossary/", "label": "Glossary"},
    {
        "href": "/blog/",
        "label": "Resources",
        "children": [
            {"href": "/blog/", "label": "Blog"},
            {"href": "/insights/", "label": "Insights"},
            {"href": "/comparisons/", "label": "Comparisons"},
            {"href": "/jobs/", "label": "Job Board"},
        ],
    },
]

FOOTER_COLUMNS = {
    "Salary Data": [
        {"href": "/salary/", "label": "Salary Index"},
        {"href": "/salary/by-seniority/", "label": "By Seniority"},
        {"href": "/salary/by-location/", "label": "By Location"},
        {"href": "/salary/by-company-stage/", "label": "By Stage"},
        {"href": "/salary/comparisons/", "label": "Comparisons"},
    ],
    "Resources": [
        {"href": "/tools/", "label": "ABM Tools"},
        {"href": "/tools/category/intent-data/", "label": "Tool Categories"},
        {"href": "/comparisons/", "label": "Comparisons"},
        {"href": "/careers/", "label": "Career Guides"},
        {"href": "/glossary/", "label": "Glossary"},
        {"href": "/jobs/", "label": "Job Board"},
        {"href": "/blog/", "label": "Blog"},
        {"href": "/insights/", "label": "Insights"},
        {"href": "/newsletter/", "label": "Newsletter"},
        {"href": "/about/", "label": "About"},
    ],
    "Site": [
        {"href": "/privacy/", "label": "Privacy Policy"},
        {"href": "/terms/", "label": "Terms of Service"},
    ],
    "ABM Tools & Resources": [
        {"href": "https://gtmepulse.com", "label": "GTME Pulse", "external": True},
        {"href": "https://therevopsreport.com", "label": "RevOps Report", "external": True},
        {"href": "https://b2bsalestools.com", "label": "B2B Sales Tools", "external": True},
        {"href": "https://datastackguide.com", "label": "DataStack Guide", "external": True},
    ],
}
