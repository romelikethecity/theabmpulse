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

SIGNUP_WORKER_URL = "https://newsletter-subscribe.rome-workers.workers.dev/subscribe"

GA_MEASUREMENT_ID = "G-22S8BL6YFY"
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
            {"href": "/salary/remote-vs-onsite/", "label": "Remote vs Onsite"},
            {"href": "/salary/calculator/", "label": "Salary Calculator"},
            {"href": "/salary/methodology/", "label": "Methodology"},
        ],
    },
    {
        "href": "/tools/",
        "label": "Tools",
        "children": [
            {"href": "/tools/", "label": "Tools Index"},
            {"href": "/tools/category/abm-platforms/", "label": "ABM Platforms"},
            {"href": "/tools/category/intent-data/", "label": "Intent Data"},
            {"href": "/tools/category/personalization/", "label": "Personalization"},
            {"href": "/tools/category/direct-mail/", "label": "Direct Mail"},
            {"href": "/tools/best-abm-platforms/", "label": "Best ABM Platforms"},
        ],
    },
    {
        "href": "/careers/",
        "label": "Careers",
        "children": [
            {"href": "/careers/", "label": "Career Guides"},
            {"href": "/careers/how-to-become-abm-strategist/", "label": "How to Break In"},
            {"href": "/companies/", "label": "Companies Hiring"},
        ],
    },
    {"href": "/glossary/", "label": "Glossary"},
    {
        "href": "/insights/",
        "label": "Resources",
        "children": [
            {"href": "/insights/", "label": "Insights"},
            {"href": "/comparisons/", "label": "Comparisons"},
        ],
    },
]

FOOTER_COLUMNS = {
    "Salary Data": [
        {"href": "/salary/", "label": "Salary Index"},
        {"href": "/salary/by-seniority/", "label": "By Seniority"},
        {"href": "/salary/by-location/", "label": "By Location"},
        {"href": "/salary/remote-vs-onsite/", "label": "Remote vs Onsite"},
        {"href": "/salary/calculator/", "label": "Salary Calculator"},
        {"href": "/salary/methodology/", "label": "Methodology"},
    ],
    "Tools": [
        {"href": "/tools/", "label": "All Tools"},
        {"href": "/tools/category/abm-platforms/", "label": "ABM Platforms"},
        {"href": "/tools/category/intent-data/", "label": "Intent Data"},
        {"href": "/tools/category/personalization/", "label": "Personalization"},
        {"href": "/tools/category/direct-mail/", "label": "Direct Mail"},
        {"href": "/tools/best-abm-platforms/", "label": "Best ABM Platforms"},
    ],
    "Resources": [
        {"href": "/careers/", "label": "Career Guides"},
        {"href": "/glossary/", "label": "Glossary"},
        {"href": "/insights/", "label": "Insights"},
        {"href": "/comparisons/", "label": "Comparisons"},
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
