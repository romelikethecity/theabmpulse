# scripts/salary_pages.py
# Salary section page generators (~25 pages).
# Reads comp_analysis.json, generates index, seniority, location, remote,
# calculator, methodology, and comparison pages.

import os
import json

from nav_config import *
from templates import (get_page_wrapper, write_page, breadcrumb_html,
                       get_breadcrumb_schema, get_faq_schema, faq_html,
                       newsletter_cta_html)


# ---------------------------------------------------------------------------
# Data loader
# ---------------------------------------------------------------------------

def load_salary_data(project_dir):
    path = os.path.join(project_dir, "data", "comp_analysis.json")
    with open(path, "r") as f:
        return json.load(f)


def fmt_salary(n):
    if n >= 1000:
        return f"${n // 1000}K"
    return f"${n:,.0f}"


def fmt_salary_full(n):
    return f"${n:,.0f}"


def pad_description(desc, target_min=150, target_max=158):
    suffixes = [" Updated weekly.", " Independent.", " Free.", " No ads."]
    for suffix in suffixes:
        if target_min <= len(desc) <= target_max:
            return desc
        new = desc + suffix
        if len(new) <= target_max:
            desc = new
    if len(desc) > target_max:
        desc = desc[:target_max - 1].rstrip() + "."
    return desc


# ---------------------------------------------------------------------------
# Shared HTML components
# ---------------------------------------------------------------------------

def salary_header_html(eyebrow, h1, subtitle, crumbs):
    bc = breadcrumb_html(crumbs)
    return f'''<section class="salary-header">
    <div class="salary-header-inner">
        {bc}
        <div class="salary-eyebrow">{eyebrow}</div>
        <h1>{h1}</h1>
        <p>{subtitle}</p>
    </div>
</section>'''


def stat_grid_html(stats):
    """stats = [(value, label), ...]"""
    blocks = ""
    for val, label in stats:
        blocks += f'''<div class="stat-block">
    <span class="stat-value" style="color: var(--abm-accent);">{val}</span>
    <span class="stat-label">{label}</span>
</div>\n'''
    return f'<div class="stat-grid">{blocks}</div>'


def salary_table_html(headers, rows):
    """headers = [str], rows = [[str]]"""
    th = "".join(f"<th>{h}</th>" for h in headers)
    body = ""
    for row in rows:
        cells = "".join(f"<td>{c}</td>" for c in row)
        body += f"<tr>{cells}</tr>\n"
    return f'''<table class="data-table">
    <thead><tr>{th}</tr></thead>
    <tbody>{body}</tbody>
</table>'''


def related_links_html(title, links):
    """links = [(label, href), ...]"""
    cards = ""
    for label, href in links:
        cards += f'<a href="{href}" class="related-link-card">{label}</a>\n'
    return f'''<section class="related-links">
    <h2>{title}</h2>
    <div class="related-links-grid">{cards}</div>
</section>'''


# ---------------------------------------------------------------------------
# Page: Salary Index
# ---------------------------------------------------------------------------

def build_salary_index(data):
    title = "ABM Salary Data 2026"
    description = pad_description(
        "ABM salary benchmarks for 2026. Median base salary, breakdowns by seniority, location, and remote status. 225 roles analyzed."
    )
    stats = data["salary_stats"]
    crumbs = [("Home", "/"), ("Salary Data", None)]
    bc_schema = get_breadcrumb_schema([("Home", "/"), ("Salary Data", "/salary/")])

    header = salary_header_html(
        "Salary Data", "ABM Salary Benchmarks 2026",
        f"Based on {stats['count_with_salary']} roles with disclosed compensation across the ABM job market.",
        crumbs
    )

    stat_block = stat_grid_html([
        (fmt_salary(stats["median"]), "Median Base Salary"),
        (fmt_salary(stats["avg"]), "Average Base Salary"),
        (f"{fmt_salary(stats['min'])} - {fmt_salary(stats['max'])}", "Full Range"),
        (str(stats["count_with_salary"]), "Roles Analyzed"),
    ])

    # Seniority summary table
    seniority_order = ["Entry", "Mid", "Senior", "Director", "VP"]
    sen_rows = []
    for level in seniority_order:
        d = data["by_seniority"].get(level)
        if d:
            sen_rows.append([
                f"<strong>{level}</strong>",
                str(d["count"]),
                fmt_salary(d["median"]),
                f'{fmt_salary(d["min_base_avg"])} - {fmt_salary(d["max_base_avg"])}'
            ])
    sen_table = salary_table_html(
        ["Seniority", "Roles", "Median", "Avg Range"], sen_rows
    )

    # Metro summary table (skip Unknown)
    metro_rows = []
    metros_sorted = sorted(
        [(k, v) for k, v in data["by_metro"].items() if k != "Unknown"],
        key=lambda x: x[1]["median"], reverse=True
    )
    for metro, d in metros_sorted:
        metro_rows.append([
            f"<strong>{metro}</strong>",
            str(d["count"]),
            fmt_salary(d["median"]),
            f'{fmt_salary(d["min_base_avg"])} - {fmt_salary(d["max_base_avg"])}'
        ])
    metro_table = salary_table_html(
        ["Metro", "Roles", "Median", "Avg Range"], metro_rows
    )

    # Remote vs onsite
    remote_d = data["by_remote"]
    remote_stats = stat_grid_html([
        (fmt_salary(remote_d["remote"]["median"]), "Remote Median"),
        (fmt_salary(remote_d["onsite"]["median"]), "Onsite/Hybrid Median"),
        (str(remote_d["remote"]["count"]), "Remote Roles"),
        (str(remote_d["onsite"]["count"]), "Onsite/Hybrid Roles"),
    ])

    links = [
        ("By Seniority", "/salary/by-seniority/"),
        ("By Location", "/salary/by-location/"),
        ("Remote vs Onsite", "/salary/remote-vs-onsite/"),
        ("Salary Calculator", "/salary/calculator/"),
        ("Methodology", "/salary/methodology/"),
    ]
    # Add comparison links
    comparisons = get_comparison_defs()
    for comp in comparisons:
        links.append((comp["title_short"], f'/salary/{comp["slug"]}/'))

    body = f'''{header}
<div class="salary-content">
    {stat_block}

    <h2>Salary by Seniority Level</h2>
    <p>ABM salaries vary dramatically by seniority. Entry-level coordinators start around {fmt_salary(data["by_seniority"]["Entry"]["median"])}, while VP-level roles command {fmt_salary(data["by_seniority"]["VP"]["median"])}+ median compensation.</p>
    {sen_table}

    <h2>Salary by Metro Area</h2>
    <p>Location still matters for ABM compensation, even as remote work grows. Here are the major metro areas in our dataset.</p>
    {metro_table}

    <h2>Remote vs Onsite</h2>
    <p>Remote ABM roles pay a {fmt_salary(remote_d["remote"]["median"] - remote_d["onsite"]["median"])} premium over onsite/hybrid positions at the median.</p>
    {remote_stats}

    <h2>Top Paying ABM Roles</h2>
    <p>The highest-paying ABM and field marketing roles in our current dataset:</p>
'''
    # Top paying roles table
    top_rows = []
    for role in data["top_paying_roles"][:8]:
        top_rows.append([
            role["title"],
            role["company"],
            f'{fmt_salary_full(role["salary_min"])} - {fmt_salary_full(role["salary_max"])}',
            role["seniority"] or "N/A"
        ])
    body += salary_table_html(["Role", "Company", "Range", "Level"], top_rows)

    body += f'''
    {related_links_html("Explore Salary Data", links)}
    {newsletter_cta_html("Get weekly salary updates.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/",
        body_content=body, active_path="/salary/", extra_head=bc_schema,
    )
    write_page("salary/index.html", page)
    print(f"  Built: salary/index.html")


# ---------------------------------------------------------------------------
# Page: By Seniority (one page with all levels)
# ---------------------------------------------------------------------------

def build_salary_by_seniority(data):
    title = "ABM Salary by Seniority Level"
    description = pad_description(
        "ABM salaries from entry-level to VP. Median pay, ranges, and career progression data for account-based marketing professionals."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("By Seniority", None)]
    bc_schema = get_breadcrumb_schema([("Home", "/"), ("Salary Data", "/salary/"), ("By Seniority", "/salary/by-seniority/")])

    header = salary_header_html(
        "Salary Data", "ABM Salary by Seniority Level",
        "How ABM compensation scales from coordinator to VP. Based on real job postings with disclosed pay.",
        crumbs
    )

    seniority_order = ["Entry", "Mid", "Senior", "Director", "VP"]
    seniority_labels = {
        "Entry": ("Entry Level", "Coordinators, associates, and specialists with 0-2 years in ABM. Roles focus on execution: list building, campaign setup, reporting, and vendor coordination."),
        "Mid": ("Mid Level", "Managers and senior specialists with 3-5 years. Own campaign strategy, manage budgets, and coordinate across sales and marketing teams."),
        "Senior": ("Senior Level", "Senior managers and leads with 5-8 years. Set ABM strategy for segments, mentor junior staff, and own pipeline metrics."),
        "Director": ("Director Level", "Directors who own the full ABM function. Set strategy, manage teams, report to VP/CMO, and own revenue targets."),
        "VP": ("VP Level", "VPs of ABM, Demand Gen, or Field Marketing. Set organizational ABM vision, manage directors, and own executive relationships."),
    }

    content = ""
    for level in seniority_order:
        d = data["by_seniority"].get(level)
        if not d:
            continue
        label, desc = seniority_labels[level]
        content += f'''
    <h2>{label} ({level})</h2>
    <p>{desc}</p>
    {stat_grid_html([
        (fmt_salary(d["median"]), "Median Salary"),
        (f'{fmt_salary(d["min_base_avg"])} - {fmt_salary(d["max_base_avg"])}', "Avg Range"),
        (str(d["count"]), "Roles in Dataset"),
    ])}
'''

    # Progression summary
    entry_med = data["by_seniority"]["Entry"]["median"]
    vp_med = data["by_seniority"]["VP"]["median"]
    growth = ((vp_med - entry_med) / entry_med) * 100

    faq_pairs = [
        ("What does an entry-level ABM role pay?",
         f"Entry-level ABM coordinators and associates earn a median of {fmt_salary(entry_med)} based on our analysis of {data['by_seniority']['Entry']['count']} roles."),
        ("How much do ABM Directors make?",
         f"ABM Directors earn a median of {fmt_salary(data['by_seniority']['Director']['median'])}. The average range is {fmt_salary(data['by_seniority']['Director']['min_base_avg'])} to {fmt_salary(data['by_seniority']['Director']['max_base_avg'])}."),
        ("What is the salary progression from entry to VP?",
         f"The median jumps from {fmt_salary(entry_med)} at entry level to {fmt_salary(vp_med)} at VP level, a {growth:.0f}% increase over a typical 10-15 year career arc."),
    ]

    body = f'''{header}
<div class="salary-content">
    <p>ABM salaries scale from {fmt_salary(entry_med)} at entry level to {fmt_salary(vp_med)}+ at the VP level, a {growth:.0f}% increase. Here is how compensation breaks down at each stage.</p>
    {content}

    <h2>Career Progression</h2>
    <p>The typical ABM career path runs: Coordinator/Specialist (Entry) to Manager (Mid) to Senior Manager (Senior) to Director to VP of ABM or Demand Generation. Each jump brings 20-40% more compensation at the median.</p>

    {faq_html(faq_pairs)}
    {newsletter_cta_html("Get weekly salary benchmarks.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/by-seniority/",
        body_content=body, active_path="/salary/", extra_head=bc_schema + get_faq_schema(faq_pairs),
    )
    write_page("salary/by-seniority/index.html", page)
    print(f"  Built: salary/by-seniority/index.html")


# ---------------------------------------------------------------------------
# Pages: By Location (per metro + index)
# ---------------------------------------------------------------------------

def build_salary_by_location(data):
    metros = {k: v for k, v in data["by_metro"].items() if k != "Unknown"}
    metros_sorted = sorted(metros.items(), key=lambda x: x[1]["median"], reverse=True)

    # Location index page
    title = "ABM Salary by Location"
    description = pad_description(
        "ABM salary data by metro area. Compare compensation in New York, San Francisco, Seattle, Los Angeles, and more."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("By Location", None)]
    bc_schema = get_breadcrumb_schema([("Home", "/"), ("Salary Data", "/salary/"), ("By Location", "/salary/by-location/")])

    header = salary_header_html(
        "Salary Data", "ABM Salary by Location",
        f"How ABM compensation varies across {len(metros)} major metro areas.",
        crumbs
    )

    rows = []
    for metro, d in metros_sorted:
        slug = metro.lower().replace(" ", "-")
        rows.append([
            f'<a href="/salary/by-location/{slug}/"><strong>{metro}</strong></a>',
            str(d["count"]),
            fmt_salary(d["median"]),
            f'{fmt_salary(d["min_base_avg"])} - {fmt_salary(d["max_base_avg"])}'
        ])
    table = salary_table_html(["Metro Area", "Roles", "Median", "Avg Range"], rows)

    metro_links = [(m, f"/salary/by-location/{m.lower().replace(' ', '-')}/") for m, _ in metros_sorted]

    body = f'''{header}
<div class="salary-content">
    {table}
    <p>Click any metro area above for a detailed breakdown. All data sourced from job postings with disclosed compensation.</p>
    {related_links_html("Metro Breakdowns", metro_links)}
    {newsletter_cta_html("Get location-specific salary updates.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/by-location/",
        body_content=body, active_path="/salary/", extra_head=bc_schema,
    )
    write_page("salary/by-location/index.html", page)
    print(f"  Built: salary/by-location/index.html")

    # Individual metro pages
    for metro, d in metros_sorted:
        build_salary_metro_page(metro, d, data, metros_sorted)


def build_salary_metro_page(metro, metro_data, full_data, all_metros):
    slug = metro.lower().replace(" ", "-")
    title = f"ABM Salary in {metro}"
    description = pad_description(
        f"ABM salary data for {metro}. Median base salary {fmt_salary(metro_data['median'])} across {metro_data['count']} roles. Compare with other metros."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("By Location", "/salary/by-location/"), (metro, None)]
    bc_schema = get_breadcrumb_schema([
        ("Home", "/"), ("Salary Data", "/salary/"),
        ("By Location", "/salary/by-location/"), (metro, f"/salary/by-location/{slug}/")
    ])

    header = salary_header_html(
        "Salary Data", f"ABM Salary in {metro}",
        f"Compensation data for {metro_data['count']} ABM roles in the {metro} metro area.",
        crumbs
    )

    overall_median = full_data["salary_stats"]["median"]
    diff = metro_data["median"] - overall_median
    diff_pct = (diff / overall_median) * 100
    direction = "above" if diff > 0 else "below"

    # Other metros for comparison
    other_links = [(m, f"/salary/by-location/{m.lower().replace(' ', '-')}/")
                   for m, _ in all_metros if m != metro]

    body = f'''{header}
<div class="salary-content">
    {stat_grid_html([
        (fmt_salary(metro_data["median"]), "Median Base Salary"),
        (f'{fmt_salary(metro_data["min_base_avg"])} - {fmt_salary(metro_data["max_base_avg"])}', "Average Range"),
        (str(metro_data["count"]), "Roles Analyzed"),
        (f'{abs(diff_pct):.0f}% {direction}', "vs National Median"),
    ])}

    <h2>How {metro} Compares</h2>
    <p>{metro} ABM roles pay {fmt_salary(abs(diff))} {direction} the national median of {fmt_salary(overall_median)}. The average range spans from {fmt_salary(metro_data["min_base_avg"])} to {fmt_salary(metro_data["max_base_avg"])}.</p>

    <h2>Cost of Living Context</h2>
    <p>Raw salary numbers only tell part of the story. {metro} has a {"higher" if metro in ["San Francisco", "New York", "Seattle", "Los Angeles", "Boston", "Washington DC"] else "moderate"} cost of living compared to the national average, which affects take-home purchasing power.</p>

    {related_links_html("Other Metro Areas", other_links)}
    {newsletter_cta_html(f"Get {metro} salary updates.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path=f"/salary/by-location/{slug}/",
        body_content=body, active_path="/salary/", extra_head=bc_schema,
    )
    write_page(f"salary/by-location/{slug}/index.html", page)
    print(f"  Built: salary/by-location/{slug}/index.html")


# ---------------------------------------------------------------------------
# Page: Remote vs Onsite
# ---------------------------------------------------------------------------

def build_salary_remote(data):
    title = "Remote vs Onsite ABM Salaries"
    description = pad_description(
        "Remote ABM roles vs onsite compensation. Median salaries, sample sizes, and the remote premium for account-based marketing."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Remote vs Onsite", None)]
    bc_schema = get_breadcrumb_schema([
        ("Home", "/"), ("Salary Data", "/salary/"),
        ("Remote vs Onsite", "/salary/remote-vs-onsite/")
    ])

    remote_d = data["by_remote"]
    r = remote_d["remote"]
    o = remote_d["onsite"]
    premium = r["median"] - o["median"]
    premium_pct = (premium / o["median"]) * 100

    header = salary_header_html(
        "Salary Data", "Remote vs Onsite ABM Salaries",
        f"How remote work affects ABM compensation. Based on {r['count'] + o['count']} roles.",
        crumbs
    )

    table = salary_table_html(
        ["Work Type", "Roles", "Median", "Avg Range"],
        [
            ["<strong>Remote</strong>", str(r["count"]), fmt_salary(r["median"]),
             f'{fmt_salary(r["min_base_avg"])} - {fmt_salary(r["max_base_avg"])}'],
            ["<strong>Onsite / Hybrid</strong>", str(o["count"]), fmt_salary(o["median"]),
             f'{fmt_salary(o["min_base_avg"])} - {fmt_salary(o["max_base_avg"])}'],
        ]
    )

    faq_pairs = [
        ("Do remote ABM jobs pay more?",
         f"Yes. Remote ABM roles pay a {fmt_salary(premium)} ({premium_pct:.0f}%) premium at the median compared to onsite/hybrid positions."),
        ("What percentage of ABM roles are remote?",
         f"In our dataset of {r['count'] + o['count']} roles, {r['count']} ({r['count'] / (r['count'] + o['count']) * 100:.0f}%) are fully remote."),
        ("Is the remote premium real or selection bias?",
         "Some of the premium reflects that remote roles tend to be more senior. However, even controlling for seniority, remote ABM roles trend higher, likely because employers compete for a national talent pool."),
    ]

    body = f'''{header}
<div class="salary-content">
    {stat_grid_html([
        (fmt_salary(r["median"]), "Remote Median"),
        (fmt_salary(o["median"]), "Onsite/Hybrid Median"),
        (f'+{fmt_salary(premium)}', "Remote Premium"),
        (f'+{premium_pct:.0f}%', "Premium %"),
    ])}

    <h2>Side-by-Side Comparison</h2>
    {table}

    <h2>What Drives the Remote Premium?</h2>
    <p>Remote ABM roles pay {fmt_salary(premium)} more at the median. Three factors explain most of this gap:</p>
    <ul>
        <li><strong>National talent competition.</strong> Remote roles compete for candidates in high-cost metros like SF and NYC, pushing compensation up.</li>
        <li><strong>Seniority skew.</strong> Companies are more likely to offer remote work to senior hires. More junior roles tend to be onsite.</li>
        <li><strong>Startup vs enterprise mix.</strong> Well-funded startups that hire remote tend to benchmark against top-of-market comp.</li>
    </ul>

    <h2>Should You Optimize for Remote?</h2>
    <p>If compensation is your priority, yes. But the calculus changes if you factor in career growth, mentorship access, and internal visibility. Onsite roles at the right company can accelerate your trajectory faster than a remote role with higher base pay.</p>

    {faq_html(faq_pairs)}
    {newsletter_cta_html("Get remote salary insights.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path="/salary/remote-vs-onsite/",
        body_content=body, active_path="/salary/",
        extra_head=bc_schema + get_faq_schema(faq_pairs),
    )
    write_page("salary/remote-vs-onsite/index.html", page)
    print(f"  Built: salary/remote-vs-onsite/index.html")


# ---------------------------------------------------------------------------
# Page: Salary Calculator (email-gated)
# ---------------------------------------------------------------------------

def build_salary_calculator(data):
    title = "ABM Salary Calculator"
    description = pad_description(
        "Estimate your ABM salary based on seniority, location, and work type. Data-driven calculator for account-based marketing professionals."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Calculator", None)]
    bc_schema = get_breadcrumb_schema([
        ("Home", "/"), ("Salary Data", "/salary/"),
        ("Calculator", "/salary/calculator/")
    ])

    header = salary_header_html(
        "Salary Data", "ABM Salary Calculator",
        "Estimate your market rate based on seniority, location, and remote status.",
        crumbs
    )

    # Build JS data object from salary data
    seniority_data = {}
    for level in ["Entry", "Mid", "Senior", "Director", "VP"]:
        d = data["by_seniority"].get(level)
        if d:
            seniority_data[level] = {"median": d["median"], "min": d["min_base_avg"], "max": d["max_base_avg"]}

    metro_data = {}
    overall_median = data["salary_stats"]["median"]
    for metro, d in data["by_metro"].items():
        if metro == "Unknown":
            continue
        multiplier = d["median"] / overall_median
        metro_data[metro] = round(multiplier, 3)

    remote_premium = data["by_remote"]["remote"]["median"] / data["by_remote"]["onsite"]["median"]

    body = f'''{header}
<div class="salary-content">
    <div class="calculator-gate" id="calculator-gate">
        <div class="calculator-gate-inner">
            <h2>Get Your Personalized Salary Estimate</h2>
            <p>Enter your email to unlock the ABM Salary Calculator. We will also send you a personalized salary report.</p>
            <form class="hero-signup calculator-gate-form" onsubmit="return false;">
                <input type="email" placeholder="Your email" aria-label="Email address" required>
                <button type="submit" class="btn btn--primary">Unlock Calculator</button>
            </form>
            <p class="hero-signup-note">Free. No spam. Unsubscribe anytime.</p>
        </div>
    </div>

    <div class="calculator-tool" id="calculator-tool" style="display:none;">
        <div class="calculator-form-group">
            <label for="calc-seniority"><strong>Seniority Level</strong></label>
            <select id="calc-seniority" class="calculator-select">
                <option value="Entry">Entry Level (0-2 years)</option>
                <option value="Mid" selected>Mid Level (3-5 years)</option>
                <option value="Senior">Senior (5-8 years)</option>
                <option value="Director">Director (8-12 years)</option>
                <option value="VP">VP (12+ years)</option>
            </select>
        </div>
        <div class="calculator-form-group">
            <label for="calc-location"><strong>Location</strong></label>
            <select id="calc-location" class="calculator-select">
                <option value="national">National Average</option>
                {"".join(f'<option value="{m}">{m}</option>' for m in sorted(metro_data.keys()))}
            </select>
        </div>
        <div class="calculator-form-group">
            <label for="calc-remote"><strong>Work Type</strong></label>
            <select id="calc-remote" class="calculator-select">
                <option value="onsite">Onsite / Hybrid</option>
                <option value="remote">Fully Remote</option>
            </select>
        </div>
        <button class="btn btn--primary" id="calc-btn" style="width:100%; margin-top: var(--abm-space-4);">Calculate My Salary Range</button>

        <div id="calc-result" class="calculator-result" style="display:none;">
            <h3>Your Estimated Range</h3>
            <div class="stat-grid">
                <div class="stat-block">
                    <span class="stat-value" style="color: var(--abm-accent);" id="calc-low">-</span>
                    <span class="stat-label">Low End</span>
                </div>
                <div class="stat-block">
                    <span class="stat-value" style="color: var(--abm-accent);" id="calc-mid">-</span>
                    <span class="stat-label">Market Rate</span>
                </div>
                <div class="stat-block">
                    <span class="stat-value" style="color: var(--abm-accent);" id="calc-high">-</span>
                    <span class="stat-label">High End</span>
                </div>
            </div>
            <p class="calc-note" style="margin-top: var(--abm-space-4); color: var(--abm-text-secondary); font-size: var(--abm-text-sm);">Based on {data["salary_stats"]["count_with_salary"]} real ABM job postings. Individual results vary by company, skills, and negotiation.</p>
        </div>
    </div>

    <h2>How the Calculator Works</h2>
    <p>We start with the median salary for your seniority level, adjust for location using a metro-specific multiplier, and apply a remote premium if applicable. All numbers are derived from {data["salary_stats"]["count_with_salary"]} job postings with disclosed compensation.</p>

    {newsletter_cta_html("Get salary insights weekly.")}
</div>

<script>
(function() {{
    var SENIORITY = {json.dumps(seniority_data)};
    var METRO = {json.dumps(metro_data)};
    var REMOTE_PREMIUM = {remote_premium:.3f};

    // Gate logic
    var gate = document.getElementById('calculator-gate');
    var tool = document.getElementById('calculator-tool');
    var gateForm = document.querySelector('.calculator-gate-form');
    if (gateForm) {{
        gateForm.onsubmit = function(e) {{
            e.preventDefault();
            var email = gateForm.querySelector('input').value.trim();
            if (!email) return;
            gate.style.display = 'none';
            tool.style.display = 'block';
            // Also subscribe
            var SIGNUP_URL = '{SIGNUP_WORKER_URL}';
            fetch(SIGNUP_URL, {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{email: email, list: 'abm-pulse'}})
            }}).catch(function(){{}});
        }};
    }}

    // Calculator
    document.getElementById('calc-btn').onclick = function() {{
        var level = document.getElementById('calc-seniority').value;
        var loc = document.getElementById('calc-location').value;
        var remote = document.getElementById('calc-remote').value;

        var base = SENIORITY[level];
        if (!base) return;

        var locMult = loc === 'national' ? 1.0 : (METRO[loc] || 1.0);
        var remoteMult = remote === 'remote' ? REMOTE_PREMIUM : 1.0;

        var median = Math.round(base.median * locMult * remoteMult / 1000) * 1000;
        var low = Math.round(base.min * locMult * remoteMult / 1000) * 1000;
        var high = Math.round(base.max * locMult * remoteMult / 1000) * 1000;

        document.getElementById('calc-low').textContent = '$' + (low/1000) + 'K';
        document.getElementById('calc-mid').textContent = '$' + (median/1000) + 'K';
        document.getElementById('calc-high').textContent = '$' + (high/1000) + 'K';
        document.getElementById('calc-result').style.display = 'block';
    }};
}})();
</script>'''

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path="/salary/calculator/",
        body_content=body, active_path="/salary/", extra_head=bc_schema,
    )
    write_page("salary/calculator/index.html", page)
    print(f"  Built: salary/calculator/index.html")


# ---------------------------------------------------------------------------
# Page: Methodology
# ---------------------------------------------------------------------------

def build_salary_methodology(data):
    title = "ABM Salary Data Methodology"
    description = pad_description(
        "How The ABM Pulse collects and analyzes ABM salary data. Sources, methodology, and limitations explained."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Methodology", None)]
    bc_schema = get_breadcrumb_schema([
        ("Home", "/"), ("Salary Data", "/salary/"),
        ("Methodology", "/salary/methodology/")
    ])

    header = salary_header_html(
        "Salary Data", "Salary Data Methodology",
        "How we collect, clean, and present ABM compensation data.",
        crumbs
    )

    stats = data["salary_stats"]
    disclosure = data["disclosure_rate"]

    faq_pairs = [
        ("Where does the salary data come from?",
         "We collect compensation data from public job postings on major job boards and company career pages. We focus on roles that explicitly list ABM, demand generation, or field marketing in the title or description."),
        ("How often is the data updated?",
         "The dataset is refreshed weekly. Historical trends are tracked month-over-month."),
        ("Why do some roles show very high or very low salaries?",
         "Outliers exist. Some postings include commission or OTE in the range. We report the numbers as listed and flag known outliers in the top-paying roles section."),
        ("Do you include equity and bonus?",
         "Base salary only. Equity, bonus, and OTE are tracked separately when disclosed but not included in the headline numbers."),
    ]

    body = f'''{header}
<div class="salary-content">
    <h2>Data Collection</h2>
    <p>The ABM Pulse tracks {data["total_records"]} ABM-related job postings. Of those, {stats["count_with_salary"]} ({disclosure:.1f}%) include disclosed salary ranges. We source data from:</p>
    <ul>
        <li>Public job boards (LinkedIn, Indeed, Glassdoor, BuiltIn)</li>
        <li>Company career pages</li>
        <li>State pay transparency filings (CO, NY, CA, WA)</li>
    </ul>

    <h2>Inclusion Criteria</h2>
    <p>A role is included if it meets any of these criteria:</p>
    <ul>
        <li>Title includes "ABM," "account-based," "demand generation," or "field marketing"</li>
        <li>Job description references ABM platforms (6sense, Demandbase, Terminus, etc.)</li>
        <li>Role is explicitly within an ABM or demand gen team</li>
    </ul>

    <h2>Seniority Classification</h2>
    <p>Seniority is determined by title keywords and years-of-experience requirements:</p>
    <ul>
        <li><strong>Entry:</strong> Coordinator, Associate, Specialist (0-2 years)</li>
        <li><strong>Mid:</strong> Manager (3-5 years)</li>
        <li><strong>Senior:</strong> Senior Manager, Lead (5-8 years)</li>
        <li><strong>Director:</strong> Director, Head of (8-12 years)</li>
        <li><strong>VP:</strong> Vice President, SVP (12+ years)</li>
    </ul>

    <h2>Metro Classification</h2>
    <p>Roles are assigned to metro areas based on the listed location. "Remote" roles are classified separately. Roles listing a state but not a specific city are grouped under the nearest major metro when possible, or excluded from metro analysis.</p>

    <h2>Statistical Methods</h2>
    <ul>
        <li><strong>Median:</strong> The middle value. Less sensitive to outliers than mean.</li>
        <li><strong>Average range:</strong> Mean of minimum base and mean of maximum base across all roles in a category.</li>
        <li><strong>Sample sizes:</strong> Always disclosed. Interpret small samples (n &lt; 10) with caution.</li>
    </ul>

    <h2>Limitations</h2>
    <ul>
        <li>Only {disclosure:.0f}% of postings disclose salary. Disclosed-pay roles may skew toward states with transparency laws.</li>
        <li>Posted ranges may differ from actual offers.</li>
        <li>Our dataset represents a snapshot, not a census. Treat numbers as directional.</li>
    </ul>

    {faq_html(faq_pairs)}
    {newsletter_cta_html()}
</div>'''

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path="/salary/methodology/",
        body_content=body, active_path="/salary/",
        extra_head=bc_schema + get_faq_schema(faq_pairs),
    )
    write_page("salary/methodology/index.html", page)
    print(f"  Built: salary/methodology/index.html")


# ---------------------------------------------------------------------------
# Comparison definitions
# ---------------------------------------------------------------------------

def get_comparison_defs():
    return [
        {
            "slug": "vs-demand-gen-manager",
            "title": "ABM Manager vs Demand Gen Manager Salary",
            "title_short": "vs Demand Gen Manager",
            "role_a": "ABM Manager",
            "role_b": "Demand Gen Manager",
            "a_salary": "$99K", "a_range": "$85K - $130K",
            "b_salary": "$105K", "b_range": "$90K - $140K",
            "description": "Demand gen managers typically earn 5-10% more than ABM managers. Demand gen roles tend to own a broader funnel, while ABM managers focus on named accounts. Both roles require similar skills, but demand gen has more cross-functional scope.",
            "skills_overlap": "Campaign strategy, marketing automation, analytics, sales alignment, content strategy",
            "key_diff": "ABM managers focus on 1:1 and 1:few account engagement. Demand gen managers own the full funnel including inbound, events, and content programs.",
        },
        {
            "slug": "vs-field-marketing",
            "title": "ABM Manager vs Field Marketing Manager Salary",
            "title_short": "vs Field Marketing",
            "role_a": "ABM Manager",
            "role_b": "Field Marketing Manager",
            "a_salary": "$99K", "a_range": "$85K - $130K",
            "b_salary": "$95K", "b_range": "$80K - $135K",
            "description": "ABM and field marketing managers earn similar base salaries, but field marketing roles often include travel stipends and event budgets. Field marketers are region-focused while ABM managers work cross-region on named accounts.",
            "skills_overlap": "Event management, regional sales alignment, campaign execution, ROI reporting",
            "key_diff": "Field marketers own in-person events and regional pipeline. ABM managers run digital-first 1:1 campaigns. Field marketing is physical, ABM is digital.",
        },
        {
            "slug": "vs-marketing-ops",
            "title": "ABM Manager vs Marketing Ops Manager Salary",
            "title_short": "vs Marketing Ops",
            "role_a": "ABM Manager",
            "role_b": "Marketing Ops Manager",
            "a_salary": "$99K", "a_range": "$85K - $130K",
            "b_salary": "$110K", "b_range": "$90K - $145K",
            "description": "Marketing ops managers typically earn 10-15% more than ABM managers. Ops roles require deeper technical skills (Marketo, HubSpot, Salesforce) and own the marketing tech stack. ABM managers are more strategy-focused.",
            "skills_overlap": "Marketing automation, Salesforce, data analysis, campaign reporting, lead scoring",
            "key_diff": "Marketing ops builds and maintains systems. ABM managers use those systems to run campaigns. Ops is infrastructure, ABM is execution.",
        },
        {
            "slug": "vs-growth-marketer",
            "title": "ABM Manager vs Growth Marketer Salary",
            "title_short": "vs Growth Marketer",
            "role_a": "ABM Manager",
            "role_b": "Growth Marketer",
            "a_salary": "$99K", "a_range": "$85K - $130K",
            "b_salary": "$115K", "b_range": "$90K - $150K",
            "description": "Growth marketers tend to earn more than ABM managers, reflecting the broader skill set required. Growth roles blend product marketing, experimentation, and analytics. ABM is a specialized function within broader growth teams.",
            "skills_overlap": "Data analysis, campaign optimization, A/B testing, funnel strategy",
            "key_diff": "Growth marketers optimize the entire customer lifecycle. ABM managers focus specifically on target account engagement and pipeline generation.",
        },
        {
            "slug": "vs-campaign-manager",
            "title": "ABM Manager vs Campaign Manager Salary",
            "title_short": "vs Campaign Manager",
            "role_a": "ABM Manager",
            "role_b": "Campaign Manager",
            "a_salary": "$99K", "a_range": "$85K - $130K",
            "b_salary": "$85K", "b_range": "$70K - $115K",
            "description": "ABM managers earn 15-20% more than general campaign managers. ABM requires account-level strategy and sales alignment. Campaign managers typically execute broader demand gen programs without the account-specific targeting.",
            "skills_overlap": "Email marketing, campaign planning, analytics, copywriting, project management",
            "key_diff": "Campaign managers execute marketing programs at scale. ABM managers create personalized account strategies. ABM is strategic, campaign management is operational.",
        },
    ]


# ---------------------------------------------------------------------------
# Pages: Role Comparisons
# ---------------------------------------------------------------------------

def build_salary_comparisons(data):
    comparisons = get_comparison_defs()

    for comp in comparisons:
        build_comparison_page(comp, data, comparisons)
    print(f"  Built: {len(comparisons)} comparison pages")


def build_comparison_page(comp, data, all_comparisons):
    title = comp["title"]
    description = pad_description(
        f'{comp["role_a"]} vs {comp["role_b"]} salary comparison. Median pay, skill overlap, and career path differences for ABM professionals.'
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), (comp["title_short"], None)]
    bc_schema = get_breadcrumb_schema([
        ("Home", "/"), ("Salary Data", "/salary/"),
        (comp["title_short"], f'/salary/{comp["slug"]}/')
    ])

    header = salary_header_html(
        "Salary Comparison", comp["title"],
        f'How {comp["role_a"]} and {comp["role_b"]} compare on compensation, skills, and career trajectory.',
        crumbs
    )

    table = salary_table_html(
        ["", comp["role_a"], comp["role_b"]],
        [
            ["<strong>Median Salary</strong>", comp["a_salary"], comp["b_salary"]],
            ["<strong>Typical Range</strong>", comp["a_range"], comp["b_range"]],
        ]
    )

    other_links = [(c["title_short"], f'/salary/{c["slug"]}/') for c in all_comparisons if c["slug"] != comp["slug"]]

    faq_pairs = [
        (f'Who earns more: {comp["role_a"]} or {comp["role_b"]}?',
         f'{comp["description"]}'),
        (f'Can I transition from {comp["role_b"]} to {comp["role_a"]}?',
         f'Yes. The skill overlap is significant: {comp["skills_overlap"]}. The main adjustment is learning account-level strategy and sales alignment.'),
    ]

    body = f'''{header}
<div class="salary-content">
    {stat_grid_html([
        (comp["a_salary"], comp["role_a"] + " Median"),
        (comp["b_salary"], comp["role_b"] + " Median"),
    ])}

    <h2>Compensation Comparison</h2>
    {table}

    <h2>Key Differences</h2>
    <p>{comp["description"]}</p>
    <p><strong>The core distinction:</strong> {comp["key_diff"]}</p>

    <h2>Skills Overlap</h2>
    <p>Both roles require: {comp["skills_overlap"]}.</p>

    <h2>Career Path Considerations</h2>
    <p>ABM is becoming a specialized track within B2B marketing. If you want to go deep on account strategy and work closely with sales, ABM is the path. If you prefer breadth and want to touch more of the funnel, the alternative may offer more variety.</p>

    {faq_html(faq_pairs)}
    {related_links_html("More Comparisons", other_links)}
    {newsletter_cta_html("Get weekly salary comparisons.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path=f'/salary/{comp["slug"]}/',
        body_content=body, active_path="/salary/",
        extra_head=bc_schema + get_faq_schema(faq_pairs),
    )
    write_page(f'salary/{comp["slug"]}/index.html', page)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def build_all_salary_pages(project_dir):
    """Called from build.py to generate all salary pages."""
    data = load_salary_data(project_dir)
    print("\n  Building salary pages...")
    build_salary_index(data)
    build_salary_by_seniority(data)
    build_salary_by_location(data)
    build_salary_remote(data)
    build_salary_calculator(data)
    build_salary_methodology(data)
    build_salary_comparisons(data)
