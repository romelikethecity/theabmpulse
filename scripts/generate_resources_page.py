#!/usr/bin/env python3
"""Generate the ABM resources page using the site's native templates."""

import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

import templates
from templates import get_page_wrapper, write_page

templates.OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
templates.SKIP_OG = True

# ---------------------------------------------------------------------------
# Resource data
# ---------------------------------------------------------------------------

RESOURCE_DATA = {
    "title": "Best Resources for Account-Based Marketing in 2026",
    "slug": "best-abm-resources",
    "description": "Curated list of the best newsletters, communities, platforms, podcasts, and courses for account-based marketing practitioners.",
    "canonical": "https://thegtmindex.com/abm/",
    "intro": "Account-based marketing has matured from a buzzword into a standard operating model for B2B companies selling to enterprise accounts. The ecosystem of platforms, communities, and educational content has grown accordingly. But quality varies wildly.\n\nThis list focuses on the ABM resources that practitioners recommend. Platforms that actually work, communities with real practitioners (not just vendors selling), and content that teaches execution, not theory.",
    "sections": [
        {"title": "Blogs & Websites", "items": [
            {"name": "Demandbase Blog & Resources", "url": "https://www.demandbase.com/resources/", "desc": "State of ABM reports, webinars, and research from the leading ABM platform."},
            {"name": "6sense Blog", "url": "https://6sense.com/blog/", "desc": "ABM platform blog covering intent data, predictive analytics, and account-based strategies."},
            {"name": "MarTech ABM Section", "url": "https://martech.org/topic/account-based-marketing-abm/", "desc": "ABM news, trends, and how-to guides."},
            {"name": "ABM Pulse", "url": "https://theabmpulse.com/", "desc": "Account-based marketing intelligence and tool reviews.", "owned": True},
        ]},
        {"title": "Podcasts", "items": [
            {"name": "Account-Based Marketing Podcast (Momentum ITSMA)", "url": "https://podcasts.apple.com/us/podcast/account-based-marketing/id1463942306", "desc": "Monthly conversations with sales and marketing leaders sharing practical ABM tips."},
        ]},
        {"title": "Courses & Training", "items": [
            {"name": "Demandbase Academy", "url": "https://www.demandbase.com/resources/academy/", "desc": "Free ABM certifications and courses (GTM strategy, measurement). Self-paced, 4-6 hours each."},
            {"name": "Momentum ITSMA ABM Certification", "url": "https://momentumitsma.com/training-courses/", "desc": "Industry-leading ABM certification. 3,000+ professionals trained. Global standard for ABM training."},
        ]},
    ],
}


def build_body_content(data):
    """Build the resource page body content."""
    sections_html = ""
    schema_items = []
    position = 1

    for section in data["sections"]:
        if not section["items"]:
            continue
        items_html = ""
        for i, item in enumerate(section["items"], 1):
            owned_badge = ""
            if item.get("owned"):
                owned_badge = ' <span style="display:inline-block;background:#FEF3C7;color:#92400E;font-size:11px;padding:2px 8px;border-radius:4px;font-weight:600;vertical-align:middle;margin-left:4px;">OUR PICK</span>'
            items_html += f'''
            <div style="margin-bottom:24px;">
                <h3 style="font-size:16px;font-weight:600;margin-bottom:4px;">
                    {i}. <a href="{item['url']}" target="_blank" rel="noopener" style="text-decoration:underline;text-decoration-color:#E5E7EB;text-underline-offset:3px;">{item['name']}</a>{owned_badge}
                </h3>
                <p style="font-size:14px;color:#6B7280;line-height:1.6;">{item['desc']}</p>
            </div>'''
            schema_items.append({
                "@type": "ListItem",
                "position": position,
                "name": item["name"],
                "url": item["url"]
            })
            position += 1

        sections_html += f'''
        <section style="margin-bottom:48px;">
            <h2 style="font-size:22px;font-weight:700;margin-bottom:20px;padding-bottom:8px;border-bottom:2px solid #F3F4F6;">{section['title']}</h2>
            {items_html}
        </section>'''

    intro_html = "\n".join(f"<p style='font-size:16px;color:#4B5563;line-height:1.7;margin-bottom:12px;'>{p.strip()}</p>" for p in data["intro"].split("\n\n") if p.strip())

    body = f'''
    <div style="max-width:760px;margin:0 auto;padding:40px 24px 80px;">
        <nav style="font-size:13px;color:#6B7280;margin-bottom:24px;" aria-label="Breadcrumb">
            <a href="/" style="text-decoration:none;">Home</a> &rsaquo; <span>{data['title']}</span>
        </nav>

        <h1 style="font-size:32px;font-weight:700;line-height:1.2;margin-bottom:20px;letter-spacing:-0.5px;">{data['title']}</h1>

        <div style="margin-bottom:40px;">
            {intro_html}
        </div>

        {sections_html}

        <div style="margin-top:48px;padding:32px;background:#F9FAFB;border-radius:12px;border:1px solid #E5E7EB;">
            <h2 style="font-size:18px;font-weight:600;margin-bottom:12px;">How We Curated This List</h2>
            <p style="font-size:14px;color:#6B7280;line-height:1.7;">Three criteria. First, does this resource teach you something you can't learn from a Google search? Second, is it actively maintained and producing new content? Third, do practitioners in the role actually recommend it to peers? We don't accept payment for listings. We review and update this page quarterly.</p>
        </div>

        <p style="margin-top:32px;font-size:14px;color:#6B7280;">
            This page is part of <a href="https://thegtmindex.com/abm/" style="color:#EA580C;text-decoration:underline;">The GTM Index</a>, a cross-site directory of curated resources for go-to-market professionals.
        </p>
    </div>'''

    schema = f'''    <script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": [{"@type": "ItemList", "name": data["title"], "description": data["description"], "numberOfItems": len(schema_items), "itemListElement": schema_items}, {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://theabmpulse.com"}, {"@type": "ListItem", "position": 2, "name": data["title"], "item": data["canonical"]}]}]}, indent=2)}
    </script>
'''
    return body, schema


def main():
    data = RESOURCE_DATA
    body, schema = build_body_content(data)

    page = get_page_wrapper(
        data["title"],
        data["description"],
        f"/{data['slug']}/",
        body,
        extra_head=schema,
    )

    # Override the self-canonical with the cross-site canonical
    page = page.replace(
        f'<link rel="canonical" href="https://theabmpulse.com/{data["slug"]}/">',
        f'<link rel="canonical" href="{data["canonical"]}">'
    )

    write_page(f"{data['slug']}/index.html", page)
    print(f"  Built: {data['slug']}/index.html")


if __name__ == "__main__":
    main()
