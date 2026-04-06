# scripts/glossary_pages.py
# Glossary section page generators (45 terms + index).
# Each term gets a standalone page at /glossary/{slug}/ with breadcrumb schema,
# FAQ schema, related terms, and newsletter CTA.

import os
import re
import json

from nav_config import *
from templates import (get_page_wrapper, write_page, breadcrumb_html,
                       get_breadcrumb_schema, get_faq_schema, faq_html,
                       newsletter_cta_html)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(term):
    """Convert term name to URL slug."""
    s = term.lower()
    s = re.sub(r'\([^)]*\)', '', s)  # remove parenthetical abbreviations
    s = s.strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s


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
# Term database
# ---------------------------------------------------------------------------

GLOSSARY_TERMS = [
    {
        "term": "Account-Based Marketing (ABM)",
        "slug": "account-based-marketing",
        "short": "A B2B strategy that focuses sales and marketing resources on a defined set of target accounts.",
        "body": """<p>Account-based marketing (ABM) is a go-to-market strategy where sales and marketing teams collaborate to target specific high-value accounts rather than casting a wide net. Instead of generating a high volume of leads, ABM focuses on a curated list of companies that match your ideal customer profile and tailors campaigns to engage decision-makers within those accounts.</p>

<p>The approach flips the traditional demand generation funnel. Rather than attracting anonymous traffic and hoping some of it converts, ABM starts by identifying the accounts you want to win, then builds personalized experiences designed to move them through your pipeline.</p>

<p>ABM programs typically fall into three tiers. One-to-one ABM targets your highest-value accounts with fully customized campaigns. One-to-few groups similar accounts into clusters and delivers semi-personalized content. One-to-many (also called programmatic ABM) uses technology to scale personalized touches across hundreds or thousands of target accounts.</p>

<p>Successful ABM requires tight alignment between sales and marketing. Both teams need to agree on account selection criteria, engagement tactics, and success metrics. Common KPIs include account engagement scores, pipeline velocity, deal size, and win rate rather than traditional lead volume metrics.</p>

<p>The ABM technology stack has matured significantly. Platforms like 6sense, Demandbase, and Terminus offer end-to-end capabilities including account identification, intent data, advertising, and analytics. Most ABM teams also layer in personalization tools, direct mail platforms, and CRM integrations to orchestrate multi-channel campaigns.</p>

<p>ABM works best for B2B companies with high average contract values, long sales cycles, and buying committees with multiple stakeholders. Companies selling deals worth $50K or more annually see the strongest ROI from ABM investments.</p>""",
        "faq": [
            ("What is the difference between ABM and demand generation?", "Demand generation casts a wide net to attract leads from a broad audience. ABM targets specific accounts that match your ideal customer profile and builds personalized campaigns for each. ABM prioritizes quality over quantity."),
            ("How many accounts should an ABM program target?", "It depends on the tier. One-to-one programs typically cover 10-50 accounts. One-to-few programs target 50-500. Programmatic ABM can scale to thousands. Start small and expand as you prove results."),
            ("What tools do ABM teams use?", "Core ABM platforms include 6sense, Demandbase, Terminus, and RollWorks. Teams also use intent data providers like Bombora, personalization tools, direct mail platforms like Sendoso, and CRM systems like Salesforce or HubSpot."),
        ],
        "related": ["Account-Based Experience (ABX)", "Ideal Customer Profile (ICP)", "Target Account List (TAL)", "One-to-One ABM"],
    },
    {
        "term": "Account-Based Experience (ABX)",
        "slug": "account-based-experience",
        "short": "An evolution of ABM that centers the entire customer lifecycle around account-level experiences.",
        "body": """<p>Account-based experience (ABX) extends account-based marketing beyond the initial sale to encompass the full customer lifecycle. While ABM traditionally focuses on acquiring new accounts, ABX applies the same personalized, account-centric approach to onboarding, adoption, expansion, and renewal.</p>

<p>The shift from ABM to ABX reflects a broader industry recognition that winning a deal is only the beginning. B2B companies lose significant revenue through churn, failed expansions, and poor post-sale engagement. ABX addresses this by ensuring that every touchpoint, from first ad impression through long-term partnership, feels coordinated and relevant to the account.</p>

<p>In practice, ABX requires collaboration across more teams than traditional ABM. Marketing, sales, customer success, product, and support all contribute to the account experience. Shared data and shared goals replace siloed handoffs. An ABX program might orchestrate a renewal campaign that combines personalized product usage insights from CS, targeted content from marketing, and executive outreach from sales.</p>

<p>Technology plays a critical role. ABX platforms need to unify data from CRM, product analytics, support tickets, and marketing engagement to build a complete picture of each account. This unified view lets teams identify expansion opportunities, detect churn risk, and deliver the right message at the right time through the right channel.</p>

<p>Organizations adopting ABX typically see improvements in net revenue retention, expansion revenue, and customer lifetime value. The approach works especially well for companies with land-and-expand models, where initial deals are smaller and growth comes from deepening relationships over time.</p>

<p>ABX is not a separate strategy from ABM. It is ABM matured. Teams that have mastered account selection, personalization, and sales-marketing alignment are best positioned to extend those capabilities across the full customer journey.</p>""",
        "faq": [
            ("How is ABX different from ABM?", "ABM focuses primarily on acquiring new accounts. ABX extends the account-based approach across the entire customer lifecycle, including onboarding, adoption, expansion, and renewal. ABX involves more teams and covers more touchpoints."),
            ("Which teams are involved in ABX?", "ABX requires coordination across marketing, sales, customer success, product, and support. All teams share account data and align on account-level goals rather than working in silos."),
            ("When should a company move from ABM to ABX?", "Companies ready for ABX typically have a mature ABM program with strong sales-marketing alignment. If you are losing revenue to churn or missing expansion opportunities, ABX helps address those gaps by extending personalization post-sale."),
        ],
        "related": ["Account-Based Marketing (ABM)", "Orchestration", "Sales-Marketing Alignment", "Account Plan"],
    },
    {
        "term": "Target Account List (TAL)",
        "slug": "target-account-list",
        "short": "A curated list of companies that an ABM program will focus its resources on.",
        "body": """<p>A target account list (TAL) is the foundation of any account-based marketing program. It is a curated set of companies that your sales and marketing teams have agreed to prioritize. Every campaign, piece of content, and outreach effort in an ABM program flows from this list.</p>

<p>Building a strong TAL starts with your ideal customer profile. Firmographic criteria like industry, company size, revenue, and geography form the baseline. Technographic data adds another layer, identifying companies that use complementary or competing technologies. Intent data helps surface accounts actively researching solutions in your category.</p>

<p>The size of your TAL depends on your ABM tier. One-to-one programs might include 10 to 50 accounts. One-to-few programs typically range from 50 to 500. Programmatic ABM programs can target thousands. Regardless of size, every account on the list should meet your ICP criteria and have genuine revenue potential.</p>

<p>A common mistake is building a TAL that is too large or based on wishful thinking. Including aspirational accounts that will never buy wastes resources and dilutes campaign effectiveness. Better to start with a smaller, tightly qualified list and expand once you have validated your approach.</p>

<p>TALs should be living documents, not static spreadsheets. Review and refresh your list quarterly. Remove accounts that have been disqualified. Add new accounts based on fresh intent signals or market changes. Track engagement and pipeline metrics at the account level to understand which segments of your TAL are responding.</p>

<p>Sales input is non-negotiable. Marketing cannot build a TAL in isolation. Sales teams bring relationship context, competitive intelligence, and deal history that data alone cannot capture. The best TALs combine data-driven scoring with human judgment from both teams.</p>""",
        "faq": [
            ("How do you build a target account list?", "Start with your ideal customer profile criteria: industry, company size, revenue, and geography. Layer in technographic data and intent signals. Validate with sales input. Score and tier the list based on fit and engagement."),
            ("How often should you update your TAL?", "Review your target account list quarterly at minimum. Remove disqualified accounts, add new accounts based on intent signals, and re-tier based on engagement data. Some teams refresh monthly for dynamic segments."),
            ("How many accounts should be on a TAL?", "It depends on your ABM approach. One-to-one programs target 10-50 accounts. One-to-few covers 50-500. Programmatic ABM can scale to thousands. The key is ensuring every account genuinely fits your ICP and has revenue potential."),
        ],
        "related": ["Ideal Customer Profile (ICP)", "Account Tiering", "Account Scoring", "Intent Data"],
    },
    {
        "term": "Ideal Customer Profile (ICP)",
        "slug": "ideal-customer-profile",
        "short": "A description of the company attributes that make an account a great fit for your product or service.",
        "body": """<p>An ideal customer profile (ICP) defines the characteristics of companies that are the best fit for your product or service. Unlike buyer personas, which describe individual people, an ICP operates at the account level. It answers the question: which types of companies should we be selling to?</p>

<p>A well-defined ICP includes firmographic attributes like industry, employee count, annual revenue, and geography. It also incorporates technographic signals such as existing tools and platforms the company uses, as well as organizational traits like growth stage, funding status, and go-to-market model.</p>

<p>Building an ICP requires analyzing your existing customer base. Look at your best customers, specifically the ones with the highest lifetime value, fastest sales cycles, lowest churn, and strongest expansion revenue. Identify the attributes they share. Those common traits become your ICP criteria.</p>

<p>The ICP is the starting point for your target account list. Accounts that match your ICP get prioritized for ABM campaigns. Accounts that fall outside your ICP get deprioritized or excluded entirely, even if they express interest. This discipline is what makes ABM effective. Resources go where they will generate the best returns.</p>

<p>Avoid making your ICP too broad. An ICP that describes half the market is not useful. The goal is specificity. If your best customers are mid-market SaaS companies with 200 to 1,000 employees, a Series B or later, and a sales team of 20 or more, say that. Broad ICPs lead to wasted spend and diluted messaging.</p>

<p>Revisit your ICP at least annually. As your product evolves and your market position shifts, the types of companies that benefit most from your solution will change. Use win/loss analysis, customer health data, and expansion patterns to keep your ICP current.</p>""",
        "faq": [
            ("What is the difference between an ICP and a buyer persona?", "An ICP describes the ideal company (firmographics, technographics, organizational traits). A buyer persona describes the ideal individual within that company (role, goals, pain points). ABM uses both, but the ICP comes first."),
            ("How do you build an ICP?", "Analyze your best existing customers. Identify shared attributes across firmographics (industry, size, revenue), technographics (tools they use), and behavioral traits (fast sales cycles, high retention). Those patterns define your ICP."),
            ("How often should you update your ICP?", "Review your ICP at least annually. Use win/loss data, churn analysis, and expansion revenue patterns to refine it. As your product and market evolve, your ideal customer will shift."),
        ],
        "related": ["Target Account List (TAL)", "Buyer Persona", "Account Scoring", "Account Tiering"],
    },
    {
        "term": "Buying Committee",
        "slug": "buying-committee",
        "short": "The group of stakeholders within a target account who influence or make a purchase decision.",
        "body": """<p>A buying committee is the group of people within a target account who collectively influence or make a purchase decision. In B2B sales, especially for high-value deals, no single person has sole authority. Understanding and engaging the full buying committee is essential for ABM success.</p>

<p>Research from Gartner consistently shows that B2B buying committees have grown larger over the past decade. Enterprise deals now involve an average of 6 to 10 decision-makers. Each member brings a different perspective, set of priorities, and evaluation criteria. Failing to engage even one critical stakeholder can stall or kill a deal.</p>

<p>Buying committees typically include several roles. The economic buyer controls the budget and gives final approval. The champion advocates for your solution internally. The technical evaluator assesses product capabilities and integration requirements. The user buyer represents the team that will use the product daily. Influencers and blockers shape opinions without necessarily having formal authority.</p>

<p>ABM programs need to map the buying committee for each target account. This means identifying who the stakeholders are, understanding their individual priorities, and creating content and outreach tailored to each role. A CFO cares about ROI and total cost of ownership. A marketing director cares about campaign performance and ease of use. Generic messaging that tries to address everyone addresses no one.</p>

<p>Multi-threading is the practice of building relationships with multiple members of the buying committee simultaneously. Sales reps who rely on a single contact are vulnerable. If that contact changes roles, goes on leave, or loses internal influence, the deal stalls. Multi-threaded deals close at higher rates and with larger deal sizes.</p>

<p>Technology helps. ABM platforms can track engagement across multiple contacts within an account, showing which committee members are active and which are dark. This visibility lets teams focus outreach where it matters most and identify gaps in committee coverage before they become deal killers.</p>""",
        "faq": [
            ("How many people are typically on a B2B buying committee?", "Enterprise B2B buying committees average 6 to 10 decision-makers, according to Gartner. Complex purchases involving new technology categories or large budgets can involve even more stakeholders."),
            ("How do you identify buying committee members?", "Start with your CRM data and LinkedIn research. Map the organizational chart around the budget owner. Look for roles that will use, evaluate, approve, or influence the purchase. Sales conversations and intent data can reveal additional stakeholders."),
            ("Why is engaging the full buying committee important for ABM?", "Deals that engage only one contact are fragile. If that person leaves, changes priorities, or lacks internal influence, the deal stalls. Multi-threaded engagement with the full committee increases win rates and deal sizes."),
        ],
        "related": ["Multi-Threading", "Buyer Persona", "Account Penetration", "Coverage"],
    },
    {
        "term": "Buyer Persona",
        "slug": "buyer-persona",
        "short": "A semi-fictional profile of an individual decision-maker or influencer within your target accounts.",
        "body": """<p>A buyer persona is a semi-fictional representation of an individual decision-maker or influencer within your target accounts. While the ideal customer profile describes the right company, buyer personas describe the right people inside those companies. ABM programs need both to deliver effective personalization.</p>

<p>Each persona captures the role, responsibilities, goals, challenges, and evaluation criteria of a specific type of stakeholder. A VP of Marketing persona has different priorities than a CTO persona, even within the same account. The VP of Marketing might care about campaign ROI and team productivity. The CTO cares about data security, integrations, and technical scalability.</p>

<p>Building personas for ABM is different from traditional marketing persona work. Traditional personas often focus on demographics and psychographics. ABM personas are more functional. They need to capture how each role participates in the buying process, what information they need at each stage, and what objections they are likely to raise.</p>

<p>Most B2B companies need 3 to 5 buyer personas. Common ABM personas include the economic buyer (budget holder), the champion (internal advocate), the technical evaluator, and the end user. Some deals also involve legal, procurement, or security reviewers who need specific content and messaging.</p>

<p>Personas drive content strategy. Once you know which roles matter and what each role cares about, you can create content that speaks directly to their priorities. A technical whitepaper for the evaluator. An ROI calculator for the economic buyer. A customer story featuring a peer for the champion. This level of specificity is what separates ABM content from generic marketing.</p>

<p>Validate your personas with real data. Interview customers, analyze CRM notes from closed-won deals, and review engagement patterns across your existing accounts. Personas built from assumptions rather than evidence will lead to messaging that misses the mark.</p>""",
        "faq": [
            ("What is the difference between a buyer persona and an ICP?", "An ICP describes the ideal company (industry, size, revenue). A buyer persona describes the ideal person within that company (role, goals, pain points). ICPs help you pick accounts. Personas help you engage the right people inside those accounts."),
            ("How many buyer personas does an ABM program need?", "Most B2B companies need 3 to 5 personas covering the key roles in the buying committee: economic buyer, champion, technical evaluator, and end user. Avoid creating too many personas, as it dilutes your content strategy."),
            ("How do you validate buyer personas?", "Interview existing customers, analyze CRM data from closed-won deals, and review content engagement patterns. Real conversations with buyers reveal more than internal brainstorming sessions."),
        ],
        "related": ["Buying Committee", "Ideal Customer Profile (ICP)", "Personalization", "Multi-Threading"],
    },
    {
        "term": "Intent Data",
        "slug": "intent-data",
        "short": "Behavioral signals that indicate a company is actively researching a topic or considering a purchase.",
        "body": """<p>Intent data captures behavioral signals that suggest a company is actively researching a topic, evaluating solutions, or preparing to make a purchase. For ABM teams, intent data is a prioritization engine. It helps you focus resources on accounts that are showing buying behavior right now rather than guessing who might be ready.</p>

<p>There are two primary types of intent data. First-party intent comes from your own properties: website visits, content downloads, webinar attendance, and product usage data. Third-party intent comes from external sources that track research activity across the broader web, including publisher networks, review sites, and content syndication platforms.</p>

<p>Major third-party intent data providers include Bombora (which powers intent signals for many ABM platforms), G2 (buyer intent from software review activity), TrustRadius, and TechTarget. Each provider has a different methodology and data source, so signals vary in coverage and accuracy.</p>

<p>Intent data works best when combined with your ICP and account scoring model. A surge in research activity from an account that already matches your ICP is a strong signal. The same surge from an account outside your ICP might be noise. Context matters. Intent data tells you when an account is active. Your ICP tells you whether that account is worth pursuing.</p>

<p>Common use cases for intent data in ABM include prioritizing outreach to accounts showing buying signals, triggering personalized ad campaigns when accounts enter research phases, alerting sales reps to engage warm accounts, and identifying competitive evaluation activity before it is too late to influence the decision.</p>

<p>Intent data is not a silver bullet. Signal quality varies. Not every topic surge means an account is ready to buy. Some research is educational. Some is driven by a single employee with no purchasing authority. The best ABM teams treat intent data as one input among many, not a standalone decision-making tool.</p>""",
        "faq": [
            ("What is intent data in ABM?", "Intent data captures behavioral signals showing that a company is researching topics related to your solution. It helps ABM teams prioritize accounts that are actively in-market over those that are not showing buying behavior."),
            ("What is the difference between first-party and third-party intent data?", "First-party intent data comes from your own channels (website, content, product). Third-party intent data comes from external sources like publisher networks, review sites, and content syndication platforms that track research activity across the web."),
            ("How accurate is intent data?", "Accuracy varies by provider and methodology. Intent data is directional, not definitive. It works best as one signal in a broader scoring model that includes ICP fit, engagement, and sales input. Never rely on intent data alone to make targeting decisions."),
        ],
        "related": ["First-Party Intent", "Third-Party Intent", "Surge Score", "Account Scoring"],
    },
    {
        "term": "First-Party Intent",
        "slug": "first-party-intent",
        "short": "Buying signals collected from your own digital properties and interactions.",
        "body": """<p>First-party intent data consists of buying signals collected directly from your own digital properties and interactions. This includes website visits, content downloads, email engagement, webinar registrations, product trial activity, and any other behavioral data from channels you control.</p>

<p>First-party intent is generally considered more reliable than third-party intent because you know exactly where the data comes from and can validate it against your own systems. When a target account visits your pricing page three times in a week, that signal is concrete. You can see which pages they viewed, how long they stayed, and whether multiple people from the same account are engaging.</p>

<p>For ABM programs, first-party intent data is especially valuable because it shows direct interest in your solution. Third-party intent tells you an account is researching a category. First-party intent tells you an account is researching you specifically. That distinction matters when deciding where to allocate sales and marketing resources.</p>

<p>Collecting first-party intent requires the right infrastructure. You need account identification technology (often called reverse IP lookup or deanonymization) to connect anonymous website visitors to specific companies. You also need marketing automation and CRM integrations to stitch together engagement across email, content, events, and product.</p>

<p>Common first-party intent signals ranked by strength: pricing page visits, demo requests, product documentation views, case study downloads, repeated visits from multiple contacts at the same account, and email opens or clicks. Weaker signals include blog visits and social media engagement, though these still contribute to the overall engagement picture.</p>

<p>The limitation of first-party intent is that it only captures accounts already interacting with your brand. It misses the large number of accounts that are researching your category but have not yet found you. That is where third-party intent fills the gap, surfacing accounts in the early research phase before they visit your site.</p>""",
        "faq": [
            ("What counts as first-party intent data?", "First-party intent includes any buying signal from your own channels: website visits, content downloads, email clicks, webinar attendance, demo requests, and product trial usage. Anything you can track on properties you control."),
            ("Why is first-party intent more reliable than third-party?", "You know exactly where the data originates and can validate it against your own systems. The signal is specific to your brand rather than a broad topic. Pricing page visits from a target account are a stronger signal than general category research."),
            ("How do you collect first-party intent data?", "Use account identification technology to deanonymize website visitors, marketing automation to track email and content engagement, and product analytics to capture trial or usage behavior. Integrate these data sources into your CRM or ABM platform."),
        ],
        "related": ["Intent Data", "Third-Party Intent", "Account Engagement Score", "Signal"],
    },
    {
        "term": "Third-Party Intent",
        "slug": "third-party-intent",
        "short": "Buying signals collected from external sources across the broader web, outside your own properties.",
        "body": """<p>Third-party intent data captures buying signals from sources outside your owned channels. These signals come from publisher networks, B2B content syndication platforms, software review sites, industry forums, and other web properties where professionals research solutions and consume content.</p>

<p>The major third-party intent data providers include Bombora (the most widely used, integrated into 6sense, Demandbase, and others), G2 (which tracks software buyer activity on its review platform), TrustRadius, TechTarget (which captures intent from its network of technology media sites), and Bidstream data providers that analyze programmatic advertising bid data.</p>

<p>Third-party intent solves a critical gap in ABM. Your first-party data only shows accounts that have already found you. But research shows that B2B buyers complete 70% or more of their evaluation process before ever contacting a vendor. Third-party intent surfaces accounts that are in that invisible early research phase, giving your team a head start before competitors even know the account is active.</p>

<p>The data typically surfaces as topic-level signals. Rather than showing that an account visited a specific webpage, third-party intent shows that an account has increased its research activity around specific topics like "account-based marketing platforms" or "B2B intent data vendors." When research volume for a topic spikes above normal levels, that is flagged as a surge.</p>

<p>Quality varies significantly between providers. Bombora uses a cooperative data model with a large publisher network, providing broad coverage. G2 signals are more purchase-specific but limited to accounts actively comparing software. TechTarget signals are strong for technology purchases but narrow in scope. Most ABM teams layer multiple intent sources for better coverage.</p>

<p>Third-party intent works best when paired with ICP fit data. An intent surge from a company that matches your ICP is actionable. A surge from a company that does not match your ICP is often just noise. Use intent as a timing signal, not a qualification signal.</p>""",
        "faq": [
            ("Where does third-party intent data come from?", "Third-party intent data comes from publisher networks, B2B review sites (G2, TrustRadius), content syndication platforms, technology media properties, and programmatic ad bid data. Providers aggregate and anonymize this data at the account level."),
            ("Which third-party intent providers are best for ABM?", "Bombora is the most widely integrated. G2 is strong for software purchase signals. TechTarget covers technology buyers. Most mature ABM teams use multiple providers. The best choice depends on your industry and the topics that matter to your buyers."),
            ("How reliable is third-party intent data?", "It is directional, not precise. Third-party intent tells you an account is researching a topic, but it does not tell you who is researching or why. Use it as one input in a broader scoring model alongside ICP fit, first-party engagement, and sales input."),
        ],
        "related": ["Intent Data", "First-Party Intent", "Surge Score", "Bombora"],
    },
    {
        "term": "Surge Score",
        "slug": "surge-score",
        "short": "A metric that flags when an account's research activity on a topic spikes above its baseline.",
        "body": """<p>A surge score measures the degree to which an account's research activity on a specific topic has increased compared to its historical baseline. When the score crosses a threshold, it signals that the account may be entering an active buying cycle. ABM teams use surge scores to time their outreach and campaign activation.</p>

<p>The concept is straightforward. Every company has a normal level of content consumption around topics related to their business. A marketing technology company will always show some research activity around terms like "marketing automation" or "ABM." A surge score only fires when that activity increases meaningfully above the baseline, indicating a change in behavior rather than business as usual.</p>

<p>Most intent data providers calculate surge scores differently. Bombora uses a topic-level model that compares an account's current week of research against its trailing average. 6sense builds composite scores that blend multiple topic surges with other behavioral signals. The methodology matters because it affects how sensitive the score is and how many false positives it generates.</p>

<p>In practice, ABM teams use surge scores in several ways. High surge scores can trigger automated ad campaigns targeting the account. They can alert sales reps to prioritize outreach. They can move accounts into higher tiers for more personalized treatment. Some teams use surge scores as qualification criteria for one-to-one ABM programs.</p>

<p>The biggest pitfall with surge scores is over-reliance. A high surge score does not guarantee an account is ready to buy. The research could be educational. It could be driven by a junior employee with no purchasing authority. It could reflect a content marketing initiative rather than a buying decision. Smart teams use surge scores as timing signals, not as standalone qualification criteria.</p>

<p>Combine surge scores with ICP fit and first-party engagement for the most accurate picture. An account that matches your ICP, shows a high surge score, and is engaging with your own content is a much stronger signal than a surge score alone.</p>""",
        "faq": [
            ("What is a good surge score?", "It depends on the provider. Most intent platforms use relative scoring that compares current activity to baseline. A meaningful surge is typically 2x to 3x above normal levels. The threshold depends on your conversion data and how many false positives you can tolerate."),
            ("How should ABM teams use surge scores?", "Use surge scores to time outreach and campaign activation. High surges can trigger ad campaigns, alert sales reps, or escalate accounts to higher ABM tiers. Always combine surge data with ICP fit and first-party engagement for accuracy."),
            ("Do surge scores predict purchases?", "Surge scores are correlated with buying activity but do not predict purchases with certainty. They indicate increased research, which may or may not lead to a buying decision. Treat them as one signal among many."),
        ],
        "related": ["Intent Data", "Third-Party Intent", "Account Scoring", "Signal"],
    },
    {
        "term": "Account Scoring",
        "slug": "account-scoring",
        "short": "A framework for ranking target accounts based on fit, intent, and engagement signals.",
        "body": """<p>Account scoring is a framework for ranking and prioritizing target accounts based on a combination of fit, intent, and engagement signals. Unlike traditional lead scoring, which evaluates individual contacts, account scoring operates at the company level and aggregates signals across all known contacts and anonymous visitors within an account.</p>

<p>A typical account scoring model combines three dimensions. Fit score measures how closely an account matches your ideal customer profile based on firmographic and technographic data. Intent score captures buying signals from first-party and third-party sources. Engagement score tracks actual interactions with your brand, such as website visits, content downloads, ad clicks, email opens, and event attendance.</p>

<p>The weights assigned to each dimension depend on your business. Some companies find that ICP fit is the strongest predictor of success and weight it heavily. Others find that intent signals are more actionable. The right balance comes from analyzing your historical win/loss data and correlating account attributes with conversion outcomes.</p>

<p>Most ABM platforms offer built-in account scoring. 6sense uses AI to generate predictive scores based on buying stage and account fit. Demandbase provides customizable scoring that blends multiple data sources. RollWorks offers scoring that emphasizes advertising engagement. These platform scores are a good starting point, but many teams customize them based on their specific sales motion.</p>

<p>Account scores drive operational decisions across the GTM team. Marketing uses them to determine which accounts receive personalized campaigns versus scaled programs. Sales uses them to prioritize outreach and allocate rep time. Customer success uses them to identify expansion opportunities in existing accounts.</p>

<p>Review your scoring model regularly. Models degrade over time as market conditions and buying behaviors shift. Quarterly reviews that compare scoring predictions against actual outcomes will keep your model accurate and actionable.</p>""",
        "faq": [
            ("How is account scoring different from lead scoring?", "Lead scoring evaluates individual contacts based on their attributes and behavior. Account scoring evaluates entire companies by aggregating signals across all contacts, anonymous visitors, and external intent data within an account."),
            ("What data goes into an account score?", "Account scores typically combine three dimensions: ICP fit (firmographics, technographics), intent signals (first-party and third-party research activity), and engagement (website visits, content consumption, email interactions, ad clicks)."),
            ("How often should you update your account scoring model?", "Review your model quarterly. Compare predicted high-scoring accounts against actual pipeline and revenue outcomes. Adjust weights and thresholds based on what the data shows."),
        ],
        "related": ["Account Tiering", "Ideal Customer Profile (ICP)", "Intent Data", "Account Engagement Score"],
    },
    {
        "term": "Account Tiering",
        "slug": "account-tiering",
        "short": "The practice of segmenting target accounts into tiers that determine the level of investment each receives.",
        "body": """<p>Account tiering is the practice of segmenting your target account list into distinct tiers based on each account's potential value and strategic importance. Each tier receives a different level of investment in terms of personalization, channel mix, and human attention. Tiering ensures that your most valuable accounts get the most resources while still covering a broader set of opportunities efficiently.</p>

<p>The most common tiering model uses three levels. Tier 1 accounts are your highest-value targets. They get one-to-one treatment with fully customized campaigns, dedicated account teams, and personalized content. Tier 2 accounts are grouped into clusters based on shared characteristics and receive one-to-few campaigns with semi-personalized messaging. Tier 3 accounts are reached through programmatic ABM with scaled, automated touches.</p>

<p>Tiering criteria typically combine ICP fit, revenue potential, intent signals, and strategic value. A Fortune 500 company in your core industry with active intent signals belongs in Tier 1. A mid-market company that matches your ICP but shows no intent might start in Tier 3 and move up as engagement increases.</p>

<p>The resource allocation differences between tiers are significant. A Tier 1 account might receive custom research reports, personalized landing pages, executive dinner invitations, and direct mail. A Tier 3 account might receive targeted display ads, automated email sequences, and standard webinar invitations. The investment per account can differ by 10x or more between tiers.</p>

<p>Dynamic tiering is a best practice. Accounts should move between tiers as their situation changes. An account showing a sudden intent surge deserves promotion to a higher tier. An account that has gone dark after months of engagement might drop down. Static tiering based on annual planning alone misses these real-time signals.</p>

<p>Tiering decisions should involve both sales and marketing. Sales brings relationship context and pipeline intelligence. Marketing brings engagement data and intent signals. When both teams agree on the tiering framework, alignment on resource allocation and campaign strategy follows naturally.</p>""",
        "faq": [
            ("What is account tiering in ABM?", "Account tiering segments your target accounts into levels (usually 3) based on value and strategic importance. Each tier gets a different level of investment. Tier 1 accounts receive personalized, high-touch treatment. Lower tiers receive scaled, automated programs."),
            ("How many tiers should an ABM program have?", "Three tiers is the standard approach. Tier 1 for one-to-one ABM (10-50 accounts), Tier 2 for one-to-few (50-500 accounts), and Tier 3 for programmatic ABM (500+ accounts). Some organizations add a fourth tier for broad awareness."),
            ("How do you decide which tier an account belongs in?", "Tier assignment combines ICP fit score, revenue potential, intent signal strength, engagement level, and strategic value. Accounts should move between tiers dynamically based on changing signals rather than staying fixed in annual plans."),
        ],
        "related": ["Target Account List (TAL)", "Account Scoring", "One-to-One ABM", "One-to-Few ABM"],
    },
    {
        "term": "One-to-One ABM",
        "slug": "one-to-one-abm",
        "short": "The most personalized ABM tier, with fully customized campaigns for individual high-value accounts.",
        "body": """<p>One-to-one ABM is the highest-touch tier of account-based marketing. Each target account receives a fully customized campaign built around its specific business challenges, organizational structure, and buying committee. This approach delivers the deepest personalization but requires the most resources per account.</p>

<p>A one-to-one ABM program typically covers 10 to 50 accounts. These are your highest-value opportunities: large enterprises with significant revenue potential, strategic logos that would transform your market position, or key accounts at risk of churning. The investment per account can reach thousands or tens of thousands of dollars in campaign spend, content creation, and sales time.</p>

<p>The campaign elements for one-to-one ABM are highly customized. Custom research reports analyzing the account's industry challenges. Personalized landing pages that speak to the account by name and reference their specific situation. Account-specific ad creative. Executive briefings tailored to the company's strategic priorities. Direct mail packages designed around the interests of individual buying committee members.</p>

<p>Success in one-to-one ABM requires deep account research. Teams build detailed account plans that map the organizational structure, identify key stakeholders, document strategic priorities and challenges, track competitive relationships, and outline engagement strategies for each buying committee member. This research takes time but is essential for genuine personalization.</p>

<p>The ROI math for one-to-one ABM works because deal sizes are proportionally large. If your average deal size is $500K or more, investing $20K in a custom campaign for a single account can still deliver strong returns. Companies with smaller deal sizes are better served by one-to-few or programmatic approaches.</p>

<p>Measurement for one-to-one ABM focuses on account-level metrics: engagement depth across the buying committee, pipeline creation and velocity, deal size, and win rate. Traditional marketing metrics like MQLs and lead volume are not relevant at this tier.</p>""",
        "faq": [
            ("How many accounts should be in a one-to-one ABM program?", "Typically 10 to 50 accounts. The exact number depends on your team's capacity to deliver truly personalized campaigns. It is better to do 15 accounts well than 50 accounts with watered-down personalization."),
            ("What budget does one-to-one ABM require?", "Investment per account ranges from $5K to $50K+ depending on the tactics used. The total program budget depends on the number of accounts. One-to-one ABM only makes sense when deal sizes are large enough to justify the per-account investment."),
            ("What makes one-to-one ABM different from regular ABM?", "One-to-one ABM creates completely custom campaigns for each account. Custom research, personalized content, account-specific ad creative, and tailored executive outreach. Other ABM tiers use templated or semi-personalized approaches for efficiency."),
        ],
        "related": ["One-to-Few ABM", "One-to-Many ABM", "Account Tiering", "Account Plan"],
    },
    {
        "term": "One-to-Few ABM",
        "slug": "one-to-few-abm",
        "short": "An ABM approach that groups similar accounts into clusters and delivers semi-personalized campaigns.",
        "body": """<p>One-to-few ABM (also called cluster-based ABM) groups similar target accounts into segments and delivers semi-personalized campaigns to each cluster. It sits between the fully custom one-to-one approach and the scaled programmatic approach, balancing personalization with efficiency.</p>

<p>Clusters are typically formed around shared attributes: industry vertical, company size, business challenge, or technology stack. A one-to-few campaign might target 15 mid-market fintech companies that all use Salesforce and are expanding their sales teams. The content and messaging are tailored to that specific cluster's situation without being customized for each individual account.</p>

<p>One-to-few programs typically cover 50 to 500 accounts divided into 5 to 20 clusters of 10 to 50 accounts each. The investment per account is lower than one-to-one but significantly higher than programmatic ABM. Campaigns include cluster-specific landing pages, targeted ad creative, industry-relevant content, and personalized email sequences.</p>

<p>The key advantage of one-to-few is scalability without sacrificing relevance. You cannot build a custom research report for 200 accounts. But you can build 10 industry-specific campaign packages that feel personalized to each cluster. The accounts in each cluster share enough context that the messaging resonates even without account-level customization.</p>

<p>Effective clustering requires good data. You need firmographic, technographic, and behavioral data to identify meaningful groupings. Clusters based on surface-level attributes like industry alone produce generic campaigns. The best clusters combine multiple attributes that predict shared needs and buying behavior.</p>

<p>Many ABM programs start with one-to-few before adding one-to-one or programmatic tiers. It is a practical starting point because it delivers measurable results without the heavy resource requirements of one-to-one ABM. Teams can prove the value of account-based approaches and then invest in higher-touch programs for top accounts.</p>""",
        "faq": [
            ("What is one-to-few ABM?", "One-to-few ABM groups similar target accounts into clusters based on shared attributes (industry, size, challenges) and delivers semi-personalized campaigns to each cluster. It balances personalization with efficiency."),
            ("How many accounts fit in a one-to-few program?", "Typically 50 to 500 accounts divided into 5 to 20 clusters. Each cluster contains 10 to 50 accounts that share meaningful attributes. The exact size depends on your team capacity and market segmentation."),
            ("How do you create account clusters?", "Combine firmographic data (industry, size), technographic data (tools used), and behavioral signals (shared challenges, buying patterns) to identify groups with common needs. Avoid clustering on a single dimension like industry alone."),
        ],
        "related": ["One-to-One ABM", "One-to-Many ABM", "Account Tiering", "Personalization"],
    },
    {
        "term": "One-to-Many ABM",
        "slug": "one-to-many-abm",
        "short": "A scaled ABM approach that uses technology to deliver personalized touches across hundreds or thousands of accounts.",
        "body": """<p>One-to-many ABM (also called programmatic ABM) uses technology to deliver account-level personalization at scale across hundreds or thousands of target accounts. It is the broadest tier of ABM, relying on automation, dynamic content, and advertising technology to reach a large audience with relevant messaging without manual customization.</p>

<p>The approach typically targets Tier 3 accounts that match your ICP but do not warrant the investment of one-to-one or one-to-few treatment. These accounts have legitimate revenue potential, but the deal sizes or strategic importance do not justify high-touch campaigns. Programmatic ABM keeps them engaged and moves them through your pipeline efficiently.</p>

<p>Common one-to-many tactics include account-based display advertising (targeting ads to specific companies using IP-based or cookie-based matching), dynamic website personalization (showing different content based on the visitor's company), personalized email sequences triggered by engagement signals, and retargeting campaigns that follow target account visitors across the web.</p>

<p>Technology is the enabler. ABM platforms like Demandbase, 6sense, and RollWorks offer programmatic ABM capabilities that automate audience building, ad targeting, and content personalization. These platforms can dynamically insert company names, industry references, and role-specific messaging into templates without manual effort.</p>

<p>The personalization depth is lighter than other ABM tiers. Instead of custom content per account, programmatic ABM uses templates with dynamic variables. Instead of dedicated account teams, it relies on automated workflows. The goal is relevance at scale, not the deep customization of one-to-one programs.</p>

<p>Measurement at this tier looks more like traditional demand generation metrics with an account-level lens. Track account reach (how many target accounts saw your campaigns), engagement rate (how many took action), and pipeline influence (how many generated or accelerated opportunities). The ROI model works because per-account costs are low and the volume is high.</p>""",
        "faq": [
            ("What is programmatic ABM?", "Programmatic ABM (one-to-many) uses technology to deliver account-level personalization at scale. It targets hundreds or thousands of accounts with automated, template-based personalization rather than custom campaigns for each account."),
            ("How is one-to-many ABM different from demand generation?", "One-to-many ABM still targets a defined list of accounts that match your ICP. Demand generation targets broad audiences. The personalization is lighter than other ABM tiers, but the targeting is still account-specific rather than audience-based."),
            ("What technology do you need for programmatic ABM?", "An ABM platform with advertising and personalization capabilities (6sense, Demandbase, RollWorks), marketing automation for triggered email sequences, and a CRM to track account-level engagement and pipeline impact."),
        ],
        "related": ["One-to-One ABM", "One-to-Few ABM", "Account-Based Advertising", "Dynamic Content"],
    },
    {
        "term": "Programmatic ABM",
        "slug": "programmatic-abm",
        "short": "Technology-driven ABM that automates personalized outreach to a large volume of target accounts.",
        "body": """<p>Programmatic ABM is a technology-driven approach to account-based marketing that automates personalized outreach across a large volume of target accounts. It is functionally synonymous with one-to-many ABM and represents the most scalable tier of account-based strategy.</p>

<p>The term "programmatic" comes from its reliance on programmatic advertising technology and marketing automation. Rather than manually building campaigns for individual accounts, programmatic ABM uses rules, triggers, and dynamic content to deliver relevant experiences at scale. When an account shows intent signals, the system automatically activates advertising, sends personalized emails, and adjusts website content without human intervention.</p>

<p>Programmatic ABM platforms typically offer several automated capabilities. Audience building pulls target account lists from your CRM or ABM platform and syncs them to advertising channels. Dynamic creative inserts account-specific or segment-specific details into ad templates. Triggered workflows launch multi-step campaigns based on engagement or intent signals. Analytics track performance at the account level across all channels.</p>

<p>The economics of programmatic ABM make it accessible to companies with smaller deal sizes. Because per-account costs are low (typically $50 to $500 per account annually in media spend), the approach works even when individual deal values are in the $10K to $50K range. This makes ABM viable for a broader set of B2B companies than the one-to-one tier, which requires large deal sizes to justify the investment.</p>

<p>Effective programmatic ABM still requires a well-defined target account list, clear ICP criteria, and strong data hygiene. Automation amplifies both good and bad inputs. If your TAL includes poorly qualified accounts or your messaging is generic, programmatic ABM will scale those problems.</p>

<p>Most ABM programs use programmatic ABM as the foundation and layer higher-touch approaches on top. Tier 3 accounts get programmatic treatment. Accounts that engage and show buying signals graduate to one-to-few or one-to-one programs. This graduated approach ensures that resources flow to accounts with the highest probability of conversion.</p>""",
        "faq": [
            ("Is programmatic ABM the same as one-to-many ABM?", "Yes. Programmatic ABM and one-to-many ABM refer to the same approach: using technology to deliver account-level personalization at scale across hundreds or thousands of target accounts."),
            ("What budget does programmatic ABM require?", "Per-account media spend typically ranges from $50 to $500 annually. Total program costs depend on the number of target accounts and the technology stack. It is the most cost-efficient ABM tier on a per-account basis."),
            ("Can programmatic ABM work without an ABM platform?", "It is difficult. ABM platforms provide the account matching, audience syncing, and analytics needed to run programmatic ABM effectively. Without one, you would need to cobble together manual processes that defeat the purpose of automation."),
        ],
        "related": ["One-to-Many ABM", "Account-Based Advertising", "Dynamic Content", "Orchestration"],
    },
    {
        "term": "Account Engagement Score",
        "slug": "account-engagement-score",
        "short": "A composite metric that measures how actively a target account is interacting with your brand.",
        "body": """<p>An account engagement score is a composite metric that quantifies how actively a target account is interacting with your brand across all channels and touchpoints. Unlike individual lead scores, account engagement scores aggregate activity from every known contact and anonymous visitor associated with an account to provide a company-level view of interest.</p>

<p>The score typically incorporates multiple signal types weighted by their predictive value. High-weight signals include demo requests, pricing page visits, and direct sales inquiries. Medium-weight signals include content downloads, webinar attendance, and email engagement. Lower-weight signals include social media interactions, blog visits, and ad impressions. The exact weights depend on your sales motion and what historically correlates with conversion.</p>

<p>Account engagement scores serve multiple operational purposes. Marketing uses them to identify accounts ready for sales handoff. Sales uses them to prioritize outreach and allocate time across their book of accounts. Leadership uses them to forecast pipeline health and measure campaign effectiveness. Customer success teams use them to monitor account health and identify expansion or churn risk.</p>

<p>A key differentiator from traditional lead scoring is the aggregation across contacts. If five people from the same account each do a small amount of research, an individual lead scoring model might not flag any of them. An account engagement model recognizes that five engaged contacts from one company is a much stronger signal than one highly engaged individual. This matters in B2B, where buying decisions involve committees.</p>

<p>Most ABM platforms calculate engagement scores automatically. 6sense, Demandbase, and Terminus all offer engagement scoring as core functionality. These platform scores are a useful starting point, but teams with mature ABM programs often customize the scoring model to reflect their specific buying journey and conversion patterns.</p>

<p>Track engagement score trends over time, not just current values. An account that has been steadily increasing engagement over four weeks is a better outreach target than an account with a high score that is trending downward. Momentum matters as much as the absolute number.</p>""",
        "faq": [
            ("What is an account engagement score?", "An account engagement score is a composite metric that aggregates all interactions between a target account and your brand. It combines signals from website visits, content downloads, email engagement, ad interactions, and sales touches into a single account-level number."),
            ("How is account engagement scoring different from lead scoring?", "Lead scoring evaluates individual contacts. Account engagement scoring aggregates signals from all contacts and anonymous visitors within a company. This matters because B2B buying involves committees, and multiple moderate signals from one account often indicate stronger intent than one high signal."),
            ("What signals should an engagement score include?", "Weight signals by predictive value. High-weight: demo requests, pricing page visits. Medium-weight: content downloads, webinar attendance, email clicks. Lower-weight: blog visits, social engagement, ad impressions. Calibrate weights based on your conversion data."),
        ],
        "related": ["Account Scoring", "Intent Data", "Signal", "Coverage"],
    },
    {
        "term": "Multi-Threading",
        "slug": "multi-threading",
        "short": "The practice of building relationships with multiple stakeholders in a target account simultaneously.",
        "body": """<p>Multi-threading is the practice of building relationships with multiple stakeholders within a target account simultaneously rather than relying on a single point of contact. In ABM and enterprise sales, multi-threading is essential because B2B purchase decisions involve buying committees with 6 to 10 or more members. A single-threaded deal is fragile.</p>

<p>The risks of single-threading are well-documented. If your sole contact changes jobs, goes on leave, gets reorganized, or simply loses internal influence, your deal is dead. Research from sales analytics platforms consistently shows that multi-threaded deals close at 2 to 3 times the rate of single-threaded deals and produce larger deal sizes.</p>

<p>Effective multi-threading requires coordinated outreach across both sales and marketing. Sales builds direct relationships through meetings, calls, and personalized outreach. Marketing supports by running account-targeted campaigns that engage additional stakeholders through advertising, content, events, and direct mail. The combination ensures that your message reaches the full buying committee.</p>

<p>The key stakeholders to thread include the economic buyer (budget authority), the champion (internal advocate), technical evaluators, end users, and potential blockers. Each needs different messaging and content. A CTO needs technical depth. A CFO needs ROI data. A frontline manager needs implementation details. Multi-threading without role-specific personalization is just spam at scale.</p>

<p>ABM platforms help by providing visibility into account-level engagement across contacts. You can see which buying committee members are engaging with your content and which are dark. This visibility lets you target your multi-threading efforts where they will have the most impact. If the technical evaluator is engaged but the economic buyer has not been reached, that gap becomes a clear action item.</p>

<p>A practical starting point is the "3x3 rule": engage at least 3 contacts from 3 different departments or levels within each target account. This provides enough breadth to survive contact changes and enough depth to build genuine organizational awareness of your solution.</p>""",
        "faq": [
            ("What is multi-threading in ABM?", "Multi-threading means building relationships with multiple stakeholders in a target account at the same time. Instead of relying on one contact, you engage several members of the buying committee to increase deal resilience and win rates."),
            ("How many contacts should you engage per account?", "A practical minimum is 3 contacts from 3 different departments or levels (the 3x3 rule). Enterprise deals benefit from engaging 5 to 10 stakeholders across the buying committee. The right number depends on deal complexity and committee size."),
            ("How does multi-threading improve win rates?", "Multi-threaded deals close at 2 to 3 times the rate of single-threaded deals. Multiple relationships reduce dependency on any single contact, build broader organizational consensus, and give your team more paths to influence the decision."),
        ],
        "related": ["Buying Committee", "Account Penetration", "Coverage", "Account Plan"],
    },
    {
        "term": "Air Cover",
        "slug": "air-cover",
        "short": "Marketing campaigns that surround a target account with brand awareness to support sales outreach.",
        "body": """<p>Air cover refers to marketing campaigns that surround a target account with brand awareness, thought leadership, and relevant content to create a favorable environment for sales outreach. The metaphor comes from military strategy: just as air support makes ground operations more effective, marketing air cover makes sales conversations more productive.</p>

<p>When a sales rep reaches out to a cold account, the response rate is low. When that same rep reaches out to an account that has been seeing targeted ads, receiving relevant content, and encountering the brand across multiple channels for weeks, the response rate increases substantially. Air cover creates familiarity and credibility before the first sales touch.</p>

<p>Common air cover tactics include account-targeted display advertising on LinkedIn and programmatic networks, sponsored content in the account's industry publications, retargeting campaigns that follow known visitors from the account, thought leadership content distributed through social channels, and targeted social posts that address the account's industry challenges.</p>

<p>The timing of air cover is critical. The best ABM programs activate air cover 2 to 4 weeks before sales outreach begins. This gives the campaign enough time to build familiarity without losing momentum. Launching outreach simultaneously with air cover misses the awareness-building window. Waiting too long after air cover means the initial impressions have faded.</p>

<p>Measuring air cover effectiveness requires account-level attribution. Track whether accounts receiving air cover show higher email open rates, meeting acceptance rates, and pipeline conversion compared to accounts without air cover. Most ABM platforms provide this comparison through control group functionality.</p>

<p>Air cover is especially important for breaking into new accounts where you have no existing relationships. It is less necessary for expansion within existing customers, where your brand is already known. Allocate your air cover budget toward accounts in the earliest stages of engagement, where brand awareness will have the greatest impact on sales effectiveness.</p>""",
        "faq": [
            ("What is air cover in ABM?", "Air cover is marketing activity that builds brand awareness and familiarity with a target account before or during sales outreach. It includes targeted ads, content distribution, and retargeting campaigns that make sales conversations more productive."),
            ("When should you start air cover before sales outreach?", "Activate air cover 2 to 4 weeks before sales begins outreach. This gives enough time to build multiple ad impressions and content touches without losing momentum. The exact timing depends on your sales cycle length and campaign channels."),
            ("How do you measure air cover effectiveness?", "Compare accounts that received air cover against those that did not. Measure differences in email response rates, meeting acceptance, pipeline creation, and win rates. ABM platforms with control group features can automate this comparison."),
        ],
        "related": ["Account-Based Advertising", "Orchestration", "Retargeting", "Sales-Marketing Alignment"],
    },
    {
        "term": "Orchestration",
        "slug": "orchestration",
        "short": "The coordination of multi-channel campaign activities across sales and marketing for target accounts.",
        "body": """<p>Orchestration in ABM is the coordination of multi-channel campaign activities across sales and marketing to deliver a cohesive, timed experience to target accounts. It ensures that every touchpoint, from advertising to email to sales outreach to direct mail, works together as a unified campaign rather than a collection of disconnected tactics.</p>

<p>Without orchestration, ABM breaks down into silos. Marketing runs ads. Sales sends emails. Events teams plan dinners. Each team operates independently, and the account receives a disjointed experience. Orchestration brings these activities into a single timeline with clear sequencing, so the account experiences a logical progression of touches that build on each other.</p>

<p>A typical orchestrated ABM sequence might look like this: Week 1-2, launch account-targeted ads to build awareness. Week 2-3, deliver thought leadership content through email and social. Week 3-4, sales rep sends a personalized outreach referencing the content theme. Week 4-5, follow up with a direct mail piece to key stakeholders. Week 5-6, invite the champion to an executive event. Each step reinforces the previous one.</p>

<p>Technology enables orchestration at scale. ABM platforms and marketing automation tools allow teams to build orchestrated workflows that trigger activities based on account behavior. If an account clicks an ad, it triggers a content delivery. If a contact opens the content email, it triggers a sales alert. If the account visits the pricing page, it accelerates the next outreach step.</p>

<p>The biggest challenge in orchestration is cross-team coordination. Sales and marketing need to operate from the same playbook with shared visibility into the account timeline. This requires regular synchronization meetings, shared dashboards, and clear ownership of each touchpoint. Technology alone cannot solve coordination problems rooted in organizational misalignment.</p>

<p>Effective orchestration also means knowing when to pause or adapt. If an account responds early in the sequence, skip the remaining awareness steps and move to engagement. If an account goes dark, shift to a re-engagement play. Rigid playbooks that ignore real-time signals waste budget and annoy buyers.</p>""",
        "faq": [
            ("What is ABM orchestration?", "ABM orchestration is the coordination of multi-channel activities across sales and marketing to deliver a cohesive, timed experience to target accounts. It ensures ads, emails, sales outreach, and direct mail work together as a unified campaign."),
            ("What tools support ABM orchestration?", "ABM platforms (6sense, Demandbase, Terminus), marketing automation (Marketo, HubSpot), and sales engagement platforms (Outreach, Salesloft) all contribute. The key is integration between systems so triggers and data flow across tools."),
            ("How do you build an ABM orchestration playbook?", "Map the desired account journey from awareness to opportunity. Assign each touchpoint to a team and channel. Define timing and triggers. Build in decision points where the sequence adapts based on account behavior. Test with a small group before scaling."),
        ],
        "related": ["Play", "Campaign", "Sales-Marketing Alignment", "Air Cover"],
    },
    {
        "term": "Personalization",
        "slug": "personalization",
        "short": "Tailoring marketing content and experiences to the specific context of a target account or buyer.",
        "body": """<p>Personalization in ABM is the practice of tailoring marketing content, messaging, and experiences to the specific context of a target account or individual buyer. Unlike mass marketing, which delivers the same message to everyone, ABM personalization adapts content based on the account's industry, challenges, buying stage, and the roles of specific stakeholders.</p>

<p>Personalization exists on a spectrum. At the basic level, you insert the company name and industry into template content. At the mid-level, you create segment-specific content for account clusters that share common attributes. At the advanced level, you build fully custom content for individual accounts, including custom landing pages, personalized video, and bespoke research reports.</p>

<p>The depth of personalization should match your ABM tier. Tier 1 (one-to-one) accounts deserve deep, custom personalization. Tier 2 (one-to-few) accounts get segment-level personalization. Tier 3 (programmatic) accounts get template-based personalization with dynamic variables. Applying one-to-one personalization to thousands of accounts is neither feasible nor necessary.</p>

<p>Effective personalization requires knowledge of the account. You need to understand the company's industry challenges, competitive landscape, technology stack, organizational priorities, and the roles and interests of buying committee members. This intelligence fuels the content strategy and ensures that personalization feels relevant rather than superficial.</p>

<p>Common personalized ABM assets include custom landing pages that reference the account's situation, personalized ad creative with industry-specific messaging, tailored email sequences that address role-specific pain points, dynamic website experiences that adapt based on the visitor's company, and custom presentations for executive meetings.</p>

<p>The line between personalization and creepiness is real. Mentioning a company's recent earnings call in a relevant context adds value. Referencing a prospect's personal social media activity does not. The best personalization demonstrates that you understand the account's business challenges and can help solve them, without feeling invasive.</p>""",
        "faq": [
            ("What does personalization mean in ABM?", "ABM personalization means tailoring content, messaging, and experiences to a target account's specific context. This includes adapting content based on industry, company challenges, buying stage, and the roles of individual stakeholders within the buying committee."),
            ("How deep should ABM personalization go?", "Match personalization depth to your ABM tier. Tier 1 gets fully custom content. Tier 2 gets segment-specific content. Tier 3 gets template-based personalization with dynamic variables. Deeper personalization requires more research and resources per account."),
            ("What are the most effective personalized ABM assets?", "Custom landing pages, personalized ad creative, tailored email sequences, dynamic website experiences, and custom executive presentations deliver the strongest results. The most effective assets demonstrate understanding of the account's business situation."),
        ],
        "related": ["Dynamic Content", "One-to-One ABM", "Account Plan", "Account-Based Advertising"],
    },
    {
        "term": "Dynamic Content",
        "slug": "dynamic-content",
        "short": "Content that automatically adapts based on the viewer's company, role, industry, or behavior.",
        "body": """<p>Dynamic content refers to marketing assets that automatically adapt their messaging, imagery, or structure based on the viewer's attributes such as company, role, industry, or behavioral signals. In ABM, dynamic content enables personalization at scale by allowing a single asset to serve multiple audiences with relevant variations.</p>

<p>The most common application is dynamic website personalization. When a visitor from a target account lands on your site, the page automatically adjusts to show industry-relevant case studies, company-specific messaging, or role-appropriate calls to action. A visitor from a healthcare company sees healthcare examples. A visitor from financial services sees fintech case studies. The page structure stays the same, but the content adapts.</p>

<p>Dynamic content extends beyond websites. Email templates can swap subject lines, body copy, and CTAs based on the recipient's account tier, engagement level, or buying stage. Display ad creative can insert company names, industry references, or persona-specific messages. Landing pages can adapt headlines and proof points based on the campaign that drove the click.</p>

<p>Technology requirements for dynamic content include a content management system or website personalization tool that supports rule-based or AI-driven content swapping, integration with your ABM platform or CDP for account identification, and a content library with enough variations to make the personalization meaningful. Tools like Mutiny, Intellimize, and the personalization features within Demandbase and 6sense are common choices.</p>

<p>The content creation challenge is real. Dynamic content requires building and maintaining multiple content variations. If you have 5 industry segments and 3 persona types, you theoretically need 15 variations of each key message. Start with the highest-impact pages (homepage, pricing page, key landing pages) and the most meaningful segmentation dimensions before expanding.</p>

<p>Measure the impact of dynamic content by comparing conversion rates, engagement time, and bounce rates between personalized and non-personalized experiences. Most personalization tools offer built-in A/B testing to quantify the lift from dynamic content against a static baseline.</p>""",
        "faq": [
            ("What is dynamic content in ABM?", "Dynamic content automatically adapts its messaging, imagery, or structure based on the viewer's attributes. In ABM, this means showing different content to visitors based on their company, industry, role, or engagement level without creating separate pages for each audience."),
            ("What tools enable dynamic content for ABM?", "Website personalization tools like Mutiny and Intellimize, ABM platforms with built-in personalization (Demandbase, 6sense), marketing automation for dynamic emails (Marketo, HubSpot), and CDPs for audience data. The key is integration with your account identification data."),
            ("How do you measure dynamic content effectiveness?", "Compare conversion rates, time on page, and bounce rates between personalized and non-personalized experiences. Most personalization tools include A/B testing capabilities. Track account-level engagement lift from dynamic content across your ABM program."),
        ],
        "related": ["Personalization", "One-to-Many ABM", "IP Targeting", "Account-Based Advertising"],
    },
    {
        "term": "Account-Based Advertising",
        "slug": "account-based-advertising",
        "short": "Targeted advertising that delivers ads to specific companies on your target account list.",
        "body": """<p>Account-based advertising (ABA) delivers digital ads to specific companies on your target account list rather than broad demographic or interest-based audiences. It is one of the most widely used ABM tactics because it provides scalable reach to target accounts across display, social, and programmatic channels.</p>

<p>The targeting mechanism varies by channel. LinkedIn allows direct company targeting by name. Programmatic display networks use IP-to-company matching to serve ads to employees of specific companies. Some platforms use cookie-based matching tied to business email addresses. Each method has different reach, accuracy, and privacy implications.</p>

<p>Common account-based advertising use cases include awareness campaigns for new accounts that do not know your brand, air cover to warm accounts before sales outreach, retargeting campaigns for accounts that have visited your website, and competitive displacement campaigns targeting accounts that use a competitor's product.</p>

<p>The major ABA platforms include Demandbase (which operates its own B2B DSP), 6sense (which integrates with programmatic networks), RollWorks (built on the AdRoll advertising platform), Terminus (multi-channel ad capabilities), and LinkedIn's native account targeting. Each platform offers different strengths in reach, targeting precision, and analytics.</p>

<p>Measurement for account-based advertising differs from traditional display advertising. Instead of tracking individual clicks and conversions, ABA focuses on account-level lift metrics: did the targeted accounts show increased website visits, content engagement, sales meetings, and pipeline creation compared to non-targeted accounts? Impressions and click-through rates matter less than downstream business impact.</p>

<p>Budget allocation for ABA depends on your list size and campaign duration. Most programs spend $10 to $50 per account per month on display advertising, with higher CPMs for LinkedIn. A 500-account programmatic campaign running for 6 months might cost $30K to $150K in media spend. The investment is justified when account-level engagement and pipeline metrics improve.</p>""",
        "faq": [
            ("What is account-based advertising?", "Account-based advertising delivers digital ads to specific companies on your target account list. Instead of targeting demographics or interests, it targets named companies through IP matching, LinkedIn company targeting, or cookie-based matching."),
            ("How much does account-based advertising cost?", "Typical spending ranges from $10 to $50 per account per month for programmatic display, with LinkedIn CPMs running higher. Total program cost depends on list size and campaign duration. A 500-account program for 6 months might run $30K to $150K."),
            ("How do you measure account-based ad effectiveness?", "Focus on account-level lift metrics rather than click-through rates. Compare website visits, content engagement, meeting rates, and pipeline creation between targeted and non-targeted accounts. Most ABM ad platforms provide lift reporting."),
        ],
        "related": ["IP Targeting", "Retargeting", "Air Cover", "One-to-Many ABM"],
    },
    {
        "term": "IP Targeting",
        "slug": "ip-targeting",
        "short": "An advertising technique that serves ads to devices associated with a specific company's IP addresses.",
        "body": """<p>IP targeting is an advertising technique that identifies and serves ads to devices connected to a specific company's IP address range. It is one of the primary mechanisms behind account-based advertising, allowing marketers to reach employees of target companies as they browse the web without requiring personally identifiable information.</p>

<p>The process works by matching corporate IP addresses to company names. When an employee at a target account browses a website that serves programmatic ads, the ad platform recognizes the IP address as belonging to that company and serves an account-targeted ad instead of a generic one. This happens in real time through the programmatic bidding process.</p>

<p>IP targeting accuracy depends on the quality of the IP-to-company mapping database. Major ABM platforms maintain their own databases or license them from providers. Accuracy is generally strong for large enterprises with dedicated IP ranges but weaker for smaller companies that share IP addresses through ISPs or cloud services. Remote work has further complicated accuracy, as employees working from home use residential IPs that are harder to associate with their employer.</p>

<p>The rise of remote work has been the biggest challenge for IP targeting. When most employees worked from office locations with known corporate IP ranges, targeting accuracy was high. With distributed workforces, many impressions go undelivered because the platform cannot identify home network IPs. ABM platforms have responded by supplementing IP targeting with cookie-based and email-based matching approaches.</p>

<p>Best practices for IP targeting include focusing on larger companies where IP databases are more accurate, supplementing with other targeting methods (LinkedIn, email match, cookie-based) for broader coverage, monitoring viewability and frequency to avoid wasting impressions, and using IP targeting as one channel within a multi-channel ABM strategy rather than relying on it exclusively.</p>

<p>Privacy regulations affect IP targeting. GDPR and similar frameworks classify IP addresses as personal data in some contexts. Ensure your ABM advertising vendor complies with applicable privacy laws and provides transparency about their data sources and targeting methodology.</p>""",
        "faq": [
            ("How does IP targeting work for ABM?", "IP targeting matches corporate IP addresses to company names. When an employee at a target account browses a website with programmatic ads, the platform recognizes the IP and serves an account-specific ad. It enables reaching target accounts without personal data."),
            ("How accurate is IP targeting?", "Accuracy is strong for large enterprises with dedicated IP ranges (80-90%+) but drops for smaller companies and remote workers. The shift to remote work has reduced overall IP targeting effectiveness, pushing ABM platforms to supplement with cookie and email-based matching."),
            ("Does IP targeting still work with remote employees?", "It is less effective for remote workers since home IPs are harder to map to employers. ABM platforms now combine IP targeting with cookie matching, email-based audiences, and LinkedIn targeting to maintain account-level reach in hybrid work environments."),
        ],
        "related": ["Account-Based Advertising", "Retargeting", "Dynamic Content", "Programmatic ABM"],
    },
    {
        "term": "Retargeting",
        "slug": "retargeting",
        "short": "Serving ads to people who have previously visited your website or engaged with your content.",
        "body": """<p>Retargeting (also called remarketing) serves ads to people who have previously visited your website, engaged with your content, or interacted with your brand in some way. In ABM, retargeting is particularly valuable because it keeps your brand visible to target account visitors who showed interest but did not convert on their first visit.</p>

<p>ABM retargeting differs from standard retargeting in one important way: it applies account-level filters. Standard retargeting shows ads to any past visitor. ABM retargeting only retargets visitors who belong to companies on your target account list. This prevents wasting budget on visitors from companies you do not want to sell to, such as competitors, students, or companies outside your ICP.</p>

<p>The most common ABM retargeting scenario targets accounts that visited high-intent pages. If someone from a target account visited your pricing page, product comparison page, or demo request page but did not convert, retargeting keeps your brand in front of them as they browse other sites. The ad creative often addresses the specific interest shown: "Still evaluating ABM platforms? See how we compare."</p>

<p>Retargeting works across multiple channels. Display retargeting serves banner ads across programmatic networks. Social retargeting shows sponsored content on LinkedIn, Facebook, or Twitter. Search retargeting bids on keywords when known target account visitors search for relevant terms. Video retargeting serves pre-roll ads on YouTube and other video platforms.</p>

<p>Frequency management matters in retargeting. Seeing the same ad 50 times in a week annoys people and damages your brand. Most ABM teams cap retargeting frequency at 3 to 7 impressions per day per person. Rotate creative regularly to maintain freshness. Use sequential messaging that evolves the story rather than repeating the same message.</p>

<p>Combine retargeting with other ABM tactics for maximum impact. Retarget target account visitors who attended a webinar with follow-up content. Retarget accounts that opened a direct mail piece with digital reinforcement. Retarget accounts where sales has an active opportunity with case studies relevant to their evaluation criteria. The integration of retargeting with the broader ABM orchestration plan drives the best results.</p>""",
        "faq": [
            ("How is ABM retargeting different from standard retargeting?", "ABM retargeting applies account-level filters, only retargeting visitors from companies on your target account list. Standard retargeting shows ads to any past visitor regardless of company, which wastes budget on audiences outside your ICP."),
            ("What is a good frequency cap for retargeting?", "Most ABM programs cap retargeting at 3 to 7 impressions per person per day. Rotate creative regularly and use sequential messaging that evolves the story. Over-frequency damages brand perception and wastes budget."),
            ("Which channels work best for ABM retargeting?", "LinkedIn retargeting is strong for B2B because of its professional targeting data. Programmatic display provides broad reach. Video retargeting on YouTube is effective for awareness. Use multiple channels based on where your target audience spends time online."),
        ],
        "related": ["Account-Based Advertising", "IP Targeting", "Air Cover", "Dynamic Content"],
    },
    {
        "term": "Direct Mail",
        "slug": "direct-mail",
        "short": "Physical mail or packages sent to specific contacts at target accounts as part of an ABM campaign.",
        "body": """<p>Direct mail in ABM refers to physical mail or packages sent to specific contacts at target accounts as part of a coordinated account-based campaign. In a digital-first marketing world, physical mail cuts through inbox noise and creates a tangible brand experience that digital channels cannot replicate.</p>

<p>ABM direct mail ranges from simple branded items to elaborate custom packages. At the basic level, teams send handwritten notes, branded merchandise, or relevant books. At the premium level, packages might include custom gifts related to the account's interests, high-end food items, or experience vouchers. The common thread is that the item is personalized, relevant, and tied to a broader campaign strategy.</p>

<p>The most effective ABM direct mail is not random gift-sending. It is integrated into the orchestration plan. A direct mail piece might follow up on a webinar the contact attended, reinforce a theme from recent ad campaigns, or serve as an icebreaker before a critical meeting. The package should reference something specific about the account or the contact's role to show genuine thought behind the gesture.</p>

<p>Major ABM direct mail platforms include Sendoso, Reachdesk, PFL, and Alyce. These platforms integrate with CRM and marketing automation systems, allowing teams to trigger mail sends based on engagement signals and track whether the package was delivered, opened, and followed up on. They also handle procurement, warehouse, and shipping logistics.</p>

<p>ROI measurement for direct mail requires tracking downstream outcomes. Did the contact respond to follow-up outreach? Did the account progress in the pipeline? Did the deal close? Per-piece costs are higher than digital channels ($20 to $200+ per send), so the business case depends on deal sizes and conversion rates at the accounts that receive mail.</p>

<p>Best practices include sending to verified physical addresses (office addresses work better than home addresses for B2B), timing mail to arrive before a scheduled meeting or call, personalizing beyond just the name (reference their role, challenge, or recent activity), and always pairing direct mail with digital follow-up. A package without a timely follow-up is a missed opportunity.</p>""",
        "faq": [
            ("How effective is direct mail in ABM?", "Direct mail response rates in ABM programs range from 5% to 20%, significantly higher than email. Its effectiveness comes from cutting through digital noise and creating a physical touchpoint. ROI depends on deal sizes and proper integration with the campaign sequence."),
            ("What should ABM direct mail include?", "The best direct mail is personalized and tied to the campaign theme. Options range from handwritten notes and relevant books to custom branded packages. Always reference something specific about the account or contact's role rather than sending generic gifts."),
            ("Which platforms handle ABM direct mail?", "Major platforms include Sendoso, Reachdesk, PFL, and Alyce. They integrate with CRM and marketing automation for triggered sends, handle logistics, and track delivery and engagement. Most offer catalogs of gift options plus custom package capabilities."),
        ],
        "related": ["Gifting", "Orchestration", "One-to-One ABM", "Multi-Threading"],
    },
    {
        "term": "Gifting",
        "slug": "gifting",
        "short": "Sending personalized gifts to contacts at target accounts to build relationships and drive engagement.",
        "body": """<p>Gifting in ABM is the practice of sending personalized gifts to contacts at target accounts to build relationships, break through digital noise, and drive engagement. It overlaps with direct mail but focuses specifically on the gift-giving element, often incorporating recipient choice and experience-based options rather than just branded merchandise.</p>

<p>Modern ABM gifting has moved beyond generic swag boxes. The trend is toward giving recipients choice. Platforms like Sendoso, Alyce, and Reachdesk allow you to send a gift selection where the contact chooses what they want, swaps for a different item, or donates the value to charity. This approach increases acceptance rates and avoids the waste of sending unwanted items.</p>

<p>Common gifting use cases in ABM include meeting incentives (gift card or coffee delivery for agreeing to a discovery call), event attendance drivers (premium gift for joining an executive dinner), deal acceleration (gift timed to a key decision point), and relationship building (thoughtful gift tied to a personal interest or milestone). Each use case requires different gift values and personalization levels.</p>

<p>Gift value guidelines vary by context. Meeting incentives typically run $25 to $75. Relationship-building gifts range from $50 to $150. Executive-level gifts can reach $200 or more. Many companies have gift acceptance policies that limit what employees can receive, so research the target account's policy before sending high-value items. When in doubt, lower-value but highly personalized gifts outperform expensive generic ones.</p>

<p>The ethics and effectiveness of gifting depend on execution. Gifts that feel transactional or manipulative backfire. A $50 gift card with a message that says "Let me have 15 minutes of your time" feels like a bribe. A thoughtful book on a topic the contact cares about, sent with a genuine note about why you thought they would find it valuable, builds authentic connection.</p>

<p>Track gifting ROI by measuring downstream engagement. Did gift recipients convert to meetings at a higher rate? Did gifted accounts progress through the pipeline faster? Did deal sizes increase? The per-touch cost is higher than digital channels, so the ROI case must be grounded in measurable outcomes.</p>""",
        "faq": [
            ("How much should ABM gifts cost?", "Meeting incentives: $25-$75. Relationship building: $50-$150. Executive gifts: $150-$200+. Check target companies' gift acceptance policies. Personalization matters more than cost. A thoughtful $30 gift often outperforms a generic $100 one."),
            ("What gifting platforms do ABM teams use?", "Sendoso, Alyce, and Reachdesk are the most common. They offer recipient choice (pick a gift, swap, or donate), CRM integration, triggered sending, and delivery tracking. Alyce pioneered the recipient-choice model that improves acceptance rates."),
            ("When should you send gifts in ABM?", "Common triggers include booking a meeting, attending an event, reaching a deal milestone, or recognizing a contact's promotion. Always tie the gift to the broader campaign and follow up promptly. A gift without context or follow-up misses the point."),
        ],
        "related": ["Direct Mail", "One-to-One ABM", "Multi-Threading", "Orchestration"],
    },
    {
        "term": "Sales-Marketing Alignment",
        "slug": "sales-marketing-alignment",
        "short": "The coordination of sales and marketing teams around shared accounts, goals, and campaign execution.",
        "body": """<p>Sales-marketing alignment is the coordination of sales and marketing teams around shared target accounts, shared goals, shared data, and coordinated campaign execution. In ABM, alignment is not optional. The entire strategy depends on both teams working from the same account list, agreeing on priorities, and executing campaigns together.</p>

<p>Misalignment between sales and marketing is the most common reason ABM programs fail. When marketing targets one set of accounts and sales pursues another, resources are wasted. When sales does not know what campaigns marketing is running, outreach feels disconnected. When the teams measure success differently, conflict over ROI and attribution becomes inevitable.</p>

<p>Practical alignment starts with shared account selection. Sales and marketing should jointly build the target account list, agree on tiering criteria, and sign off on which accounts receive which level of investment. This single step eliminates the most common source of conflict: "marketing is giving us bad leads" versus "sales is not following up on our leads."</p>

<p>Shared metrics are equally important. ABM teams aligned on account-level KPIs like engagement rate, pipeline velocity, deal size, and win rate collaborate better than teams where marketing optimizes for MQLs and sales optimizes for closed revenue. When both teams win or lose together, alignment follows naturally.</p>

<p>Operational alignment requires regular coordination. Weekly or bi-weekly "ABM syncs" where sales and marketing review target account engagement, discuss upcoming plays, and adjust priorities keep both teams on the same page. These meetings should be short and action-oriented. Dashboards that show account-level activity from both teams provide the shared visibility needed for effective collaboration.</p>

<p>Technology supports alignment but does not create it. CRM systems, ABM platforms, and sales engagement tools can share data between teams. But if the teams do not agree on goals, processes, and accountability, no tool will fix the problem. Start with the human alignment: shared goals, shared accounts, and shared accountability. Then use technology to operationalize those agreements.</p>""",
        "faq": [
            ("Why is sales-marketing alignment critical for ABM?", "ABM requires both teams working the same accounts with coordinated campaigns. Misalignment wastes resources and creates a disjointed experience for target accounts. It is the most common reason ABM programs fail."),
            ("How do you align sales and marketing for ABM?", "Start with jointly building the target account list and agreeing on tiering. Share account-level metrics (engagement, pipeline, win rate) rather than separate KPIs. Hold regular ABM syncs to review account activity and adjust priorities."),
            ("What metrics should aligned ABM teams share?", "Account engagement rate, pipeline velocity, deal size, win rate, and account penetration. Avoid separate metrics where marketing optimizes for MQLs and sales optimizes for closed revenue. Shared metrics create shared accountability."),
        ],
        "related": ["Orchestration", "Account Plan", "Buying Committee", "Multi-Threading"],
    },
    {
        "term": "Pipeline Velocity",
        "slug": "pipeline-velocity",
        "short": "The speed at which opportunities move through your sales pipeline from creation to close.",
        "body": """<p>Pipeline velocity measures the speed at which opportunities move through your sales pipeline from creation to close. It is a critical ABM metric because one of the primary goals of account-based marketing is to accelerate deals, not just create more of them. Faster pipeline velocity means shorter sales cycles, more efficient resource use, and faster revenue realization.</p>

<p>The standard pipeline velocity formula is: (Number of Opportunities x Average Deal Size x Win Rate) / Average Sales Cycle Length. This produces a dollar-per-day figure that represents how much revenue your pipeline generates daily. ABM programs should track this metric for ABM-influenced deals separately from the overall pipeline to measure program impact.</p>

<p>ABM improves pipeline velocity in several ways. Personalized engagement with the full buying committee reduces internal consensus-building time. Intent-based timing ensures outreach reaches accounts when they are actively evaluating. Multi-threaded relationships reduce the risk of deals stalling when a single contact becomes unavailable. Air cover builds familiarity that shortens early-stage conversations.</p>

<p>Benchmarking pipeline velocity requires segmentation. Compare ABM-influenced deals against non-ABM deals to quantify the acceleration effect. Also segment by deal size, industry, and sales rep to identify where ABM has the greatest velocity impact. Some ABM programs reduce sales cycle length by 20 to 30 percent for target accounts, which can represent millions in accelerated revenue.</p>

<p>Improving pipeline velocity is not just about moving faster. It is also about removing friction points. Analyze your pipeline stages to identify where deals stall. Common bottlenecks include legal review, procurement processes, technical evaluation, and budget approval. ABM can address many of these by engaging the right stakeholders early and providing the information needed for each stage before it becomes a blocker.</p>

<p>Track pipeline velocity as a trend, not a snapshot. Quarterly comparisons show whether your ABM program is genuinely accelerating deals over time. One-time improvements might reflect deal-level factors. Sustained improvements indicate that your program is driving systemic change in how target accounts buy from you.</p>""",
        "faq": [
            ("How do you calculate pipeline velocity?", "Pipeline velocity = (Number of Opportunities x Average Deal Size x Win Rate) / Average Sales Cycle Length. The result is a dollar-per-day figure representing how much revenue your pipeline produces daily."),
            ("How does ABM improve pipeline velocity?", "ABM accelerates deals through personalized buying committee engagement, intent-based timing, multi-threaded relationships, and air cover that builds familiarity. These factors reduce internal consensus time and remove friction at each pipeline stage."),
            ("What is a good pipeline velocity improvement from ABM?", "Strong ABM programs reduce sales cycle length by 20 to 30 percent for target accounts. The exact improvement depends on baseline cycle length, deal complexity, and program maturity. Track the trend over multiple quarters."),
        ],
        "related": ["Deal Velocity", "Influenced Pipeline", "Sourced Pipeline", "Pipeline-to-Revenue"],
    },
    {
        "term": "Deal Velocity",
        "slug": "deal-velocity",
        "short": "The speed at which an individual deal progresses from opportunity creation to closed-won.",
        "body": """<p>Deal velocity measures the speed at which an individual deal progresses from opportunity creation to closed-won. While pipeline velocity is an aggregate metric across all deals, deal velocity zooms in on specific opportunities to understand what makes some deals move fast and others stall. For ABM teams, comparing deal velocity between ABM-influenced and non-ABM deals reveals the impact of account-based programs on sales efficiency.</p>

<p>The simplest deal velocity calculation is the number of days between opportunity creation and close. More sophisticated models track velocity through each pipeline stage: how long does the average deal spend in discovery, evaluation, negotiation, and procurement? Stage-level analysis reveals specific bottlenecks that ABM campaigns can address.</p>

<p>ABM programs typically improve deal velocity by engaging the full buying committee earlier in the process. When marketing builds awareness and engagement with multiple stakeholders before the opportunity is created, the sales team does not need to start from scratch with each new contact. Deals where marketing has already engaged 3 or more buying committee members close significantly faster than deals where sales must build all relationships from zero.</p>

<p>Tracking deal velocity by account tier reveals whether higher-touch ABM investments are paying off. Tier 1 accounts that receive one-to-one treatment should show faster deal velocity than Tier 3 accounts that receive only programmatic touches. If the data does not show this pattern, the personalization and account planning for Tier 1 may need improvement.</p>

<p>External factors influence deal velocity in ways ABM cannot control. Budget cycles, organizational changes, competitive evaluations, and procurement processes all affect timing. When analyzing ABM's impact on deal velocity, control for these factors by comparing similar deals with and without ABM influence rather than looking at raw averages.</p>

<p>Use deal velocity data to improve your ABM playbooks. If deals consistently slow down at the technical evaluation stage, create assets and campaigns that address technical concerns earlier. If procurement bottlenecks are common, engage procurement stakeholders as part of your multi-threading strategy. Every slow point is an opportunity to redesign your approach.</p>""",
        "faq": [
            ("What is deal velocity?", "Deal velocity is the speed at which an individual opportunity moves from creation to closed-won. It measures the number of days in the sales cycle and can be tracked at each pipeline stage to identify bottlenecks."),
            ("How does ABM affect deal velocity?", "ABM typically improves deal velocity by engaging buying committee members before the opportunity is created, building awareness that shortens early conversations, and providing relevant content that accelerates evaluation stages."),
            ("How should you track deal velocity for ABM?", "Compare velocity between ABM-influenced and non-ABM deals. Segment by account tier, deal size, and industry. Track stage-level velocity to identify specific bottlenecks. Control for external factors when analyzing the data."),
        ],
        "related": ["Pipeline Velocity", "Influenced Pipeline", "Buying Committee", "Multi-Threading"],
    },
    {
        "term": "Influenced Pipeline",
        "slug": "influenced-pipeline",
        "short": "Pipeline value where marketing ABM activities touched the deal at any point in the buying journey.",
        "body": """<p>Influenced pipeline measures the total dollar value of sales opportunities where ABM marketing activities touched the deal at any point in the buying journey. Unlike sourced pipeline, which credits marketing only for creating the opportunity, influenced pipeline captures the broader impact of ABM campaigns that engaged the account before, during, or after opportunity creation.</p>

<p>The distinction matters because ABM rarely operates in isolation. A deal might be sourced by a sales rep who made a cold call. But if that account had been seeing targeted ads for three weeks, received a direct mail piece, and had two contacts download content, marketing influenced the deal even though it did not source it. Influenced pipeline captures this multi-touch reality.</p>

<p>Calculating influenced pipeline requires attribution modeling. The simplest approach credits any deal where at least one ABM touchpoint occurred within a defined window (typically 90 to 180 days before opportunity creation). More sophisticated models weight the influence based on the number, type, and timing of touchpoints. Multi-touch attribution models distribute credit across all contributing activities.</p>

<p>The challenge with influenced pipeline is that it can be gamed. If your definition is broad enough, marketing can claim influence on nearly every deal. This inflates the metric and erodes trust with sales and leadership. Guard against this by setting clear rules: define which activities count, establish minimum engagement thresholds, and apply time windows that reflect your actual sales cycle.</p>

<p>ABM programs should track both influenced and sourced pipeline. Sourced pipeline shows marketing's ability to create new opportunities. Influenced pipeline shows marketing's ability to accelerate and support existing opportunities. Both are valuable. A mature ABM program delivers strong numbers on both metrics.</p>

<p>Use influenced pipeline data to optimize your campaign mix. If certain ABM tactics (advertising, direct mail, events) consistently appear in the influence path of closed-won deals, allocate more budget to those tactics. If other activities appear in influence paths but deals still lose, investigate whether those touches are actually contributing or just coincidental.</p>""",
        "faq": [
            ("What is influenced pipeline?", "Influenced pipeline is the total dollar value of deals where ABM marketing activities touched the account at any point in the buying journey. It captures the multi-touch impact of campaigns that contribute to deals even when marketing did not source the opportunity directly."),
            ("How is influenced pipeline different from sourced pipeline?", "Sourced pipeline credits marketing only for creating the opportunity (first touch or lead source). Influenced pipeline credits marketing whenever ABM activities engaged the account at any stage. Influenced is broader and captures the supportive role of campaigns."),
            ("How do you prevent influenced pipeline from being inflated?", "Set clear rules: define which activities count as influence, establish minimum engagement thresholds, and apply time windows that reflect your sales cycle. Require meaningful engagement (not just an ad impression) and validate with sales feedback."),
        ],
        "related": ["Sourced Pipeline", "Pipeline Velocity", "Pipeline-to-Revenue", "Account Engagement Score"],
    },
    {
        "term": "Sourced Pipeline",
        "slug": "sourced-pipeline",
        "short": "Pipeline value where marketing ABM activities directly created the opportunity.",
        "body": """<p>Sourced pipeline measures the total dollar value of sales opportunities that were directly created by marketing ABM activities. An opportunity is "sourced" by marketing when the initial engagement or conversion that led to the deal came from an ABM campaign, inbound content, event, or other marketing-driven touchpoint rather than outbound sales effort.</p>

<p>Common scenarios that generate sourced pipeline include a target account contact who responded to an ABM email campaign and booked a meeting, an account that clicked through an ABM ad and submitted a demo request, a buying committee member who attended a marketing-hosted event and converted to an opportunity, and an inbound lead from a target account who found your content through organic search.</p>

<p>Sourced pipeline is a more conservative metric than influenced pipeline. It only credits marketing when there is a clear, direct line from marketing activity to opportunity creation. This makes it harder to inflate and more credible with sales leadership and executives who are skeptical of broad attribution claims.</p>

<p>The challenge with sourced pipeline is that it undervalues marketing's contribution in complex B2B sales. Many deals involve a combination of marketing and sales touches before an opportunity is created. If marketing ran targeted ads and sent personalized content for weeks, but a sales rep ultimately booked the first meeting through a cold call, the deal is typically sourced by sales even though marketing played a significant role.</p>

<p>Mature ABM organizations track both sourced and influenced pipeline. Sourced pipeline demonstrates marketing's ability to independently create opportunities. Influenced pipeline captures the full scope of marketing's impact. Together, they tell the complete story of how ABM contributes to revenue.</p>

<p>To increase sourced pipeline from ABM, focus on campaigns with clear conversion paths. Content offers, event registrations, demo requests, and assessment tools give target account contacts a reason to self-identify and engage directly. Pair these conversion opportunities with account-targeted advertising and email campaigns that drive traffic to high-intent pages.</p>""",
        "faq": [
            ("What is sourced pipeline?", "Sourced pipeline is the dollar value of opportunities directly created by marketing activities. Marketing gets credit when an ABM campaign, content piece, or event generates the initial engagement that leads to an opportunity, without relying on outbound sales to initiate the relationship."),
            ("Why is sourced pipeline important for ABM?", "Sourced pipeline demonstrates marketing's ability to independently create new opportunities from target accounts. It is a conservative, credible metric that resonates with sales leadership and executives because the attribution is clear and direct."),
            ("How do you increase sourced pipeline from ABM?", "Create campaigns with clear conversion paths: content offers, event registrations, demo requests, and assessment tools. Pair these with targeted advertising and email that drive target account traffic to high-intent landing pages."),
        ],
        "related": ["Influenced Pipeline", "Pipeline Velocity", "Pipeline-to-Revenue", "Campaign"],
    },
    {
        "term": "Account Penetration",
        "slug": "account-penetration",
        "short": "The breadth and depth of your engagement across contacts and departments within a target account.",
        "body": """<p>Account penetration measures the breadth and depth of your engagement across contacts and departments within a target account. It answers the question: how much of the buying committee and broader organization have we reached? High account penetration means you are engaged with multiple stakeholders across different functions and levels. Low penetration means you are relying on one or two contacts.</p>

<p>Penetration metrics typically track several dimensions. Contact coverage: how many known contacts do you have at the account compared to the estimated buying committee size? Department coverage: how many relevant departments (marketing, sales, IT, finance, executive) are represented in your contact database? Engagement depth: among your known contacts, how many are actively engaging with your brand?</p>

<p>ABM programs need account penetration because B2B buying decisions are made by committees, not individuals. If your CRM contains 2 contacts at a 10-person buying committee, you are missing 80% of the decision-making group. Deals with low penetration are more likely to stall, get blocked by unknown stakeholders, or lose to competitors who have built broader relationships.</p>

<p>Increasing account penetration is a joint effort between sales and marketing. Sales builds direct relationships through outreach, meetings, and referrals within the account. Marketing expands reach through targeted advertising that generates new contacts, content campaigns that attract additional stakeholders, and events that bring multiple people from the same account together.</p>

<p>Track penetration at each account tier. Tier 1 accounts should have the highest penetration because they receive the most investment. If a Tier 1 account shows low penetration after months of one-to-one ABM treatment, the program is not reaching the right people and needs adjustment.</p>

<p>Account penetration is a leading indicator of deal health. Deals where penetration increases over time are progressing. Deals where penetration flatlines or declines are at risk. Use penetration trends to identify deals that need intervention before they stall completely.</p>""",
        "faq": [
            ("What is account penetration in ABM?", "Account penetration measures how broadly and deeply you are engaged within a target account. It tracks the number of known contacts, departments represented, and engagement depth across the buying committee and broader organization."),
            ("Why does account penetration matter?", "B2B buying decisions involve committees of 6 to 10+ people. Low penetration means you are missing most decision-makers, which increases the risk of deal stalls, unknown blockers, and competitive losses. Higher penetration correlates with higher win rates."),
            ("How do you increase account penetration?", "Sales builds relationships through outreach and referrals. Marketing expands reach through targeted ads, content campaigns, and events. Together, they systematically engage new contacts and departments within target accounts."),
        ],
        "related": ["Coverage", "Multi-Threading", "Buying Committee", "Engagement Rate"],
    },
    {
        "term": "Coverage",
        "slug": "coverage",
        "short": "The percentage of target accounts or buying committee roles that your ABM program has successfully reached.",
        "body": """<p>Coverage in ABM refers to the percentage of target accounts, or buying committee roles within those accounts, that your program has successfully reached and engaged. It is a top-of-funnel ABM metric that answers the fundamental question: are we actually reaching the accounts and people we intend to reach?</p>

<p>Coverage operates at two levels. Account-level coverage measures what percentage of your target account list has been reached by at least one ABM touchpoint (ad impression, email, website visit, event attendance, or sales outreach). Contact-level coverage measures how many of the relevant buying committee roles at each account have been engaged.</p>

<p>Low coverage means your ABM program has a reach problem. If only 40% of your target accounts have seen your ads or received outreach, the other 60% do not know you exist. Before optimizing engagement rates or conversion metrics, you need to solve the coverage gap. You cannot convert accounts you have not reached.</p>

<p>Improving account-level coverage typically starts with advertising. Account-based display ads and LinkedIn campaigns can reach the broadest set of target accounts with the least human effort. Layer in email campaigns, content syndication, and event invitations to add additional coverage channels. Track which accounts remain unreached and investigate whether the issue is targeting accuracy, contact data quality, or channel selection.</p>

<p>Contact-level coverage is harder to achieve. You need to know who the buying committee members are at each account and have ways to reach them. This requires building contact databases from LinkedIn research, lead generation campaigns, and sales prospecting. ABM platforms that provide contact-level data (ZoomInfo, Apollo, Cognism) help fill coverage gaps at the contact level.</p>

<p>Set coverage targets by tier. Tier 1 accounts should have 80%+ buying committee coverage. Tier 2 should aim for 50-70%. Tier 3 coverage targets focus on account reach rather than buying committee depth. Review coverage metrics monthly and investigate any target accounts that remain unreached after 60 to 90 days of program activity.</p>""",
        "faq": [
            ("What is coverage in ABM?", "Coverage measures the percentage of target accounts and buying committee roles your ABM program has reached. Account-level coverage tracks which companies received touchpoints. Contact-level coverage tracks which individuals within those companies have been engaged."),
            ("What is a good coverage rate for ABM?", "Tier 1 accounts should reach 80%+ buying committee coverage. Tier 2 targets 50-70%. Tier 3 focuses on account-level reach. At the account level, aim to reach 90%+ of your target list within the first 90 days of program activity."),
            ("How do you improve ABM coverage?", "Start with advertising for broad account-level reach. Layer in email, content syndication, and events. For contact-level coverage, build databases from LinkedIn research, lead gen campaigns, and contact data providers. Investigate unreached accounts to identify gaps."),
        ],
        "related": ["Account Penetration", "Multi-Threading", "Account-Based Advertising", "Buying Committee"],
    },
    {
        "term": "Engagement Rate",
        "slug": "engagement-rate",
        "short": "The percentage of target accounts actively interacting with your ABM campaigns and content.",
        "body": """<p>Engagement rate in ABM measures the percentage of target accounts that are actively interacting with your campaigns, content, and brand. It goes beyond coverage (which tracks reach) to measure whether accounts are taking meaningful actions in response to your ABM efforts.</p>

<p>The definition of "engagement" varies by team, but common qualifying actions include website visits to key pages, content downloads, email clicks, ad clicks, webinar registrations, event attendance, direct mail responses, and sales meeting bookings. Most ABM platforms let you define custom engagement rules that match your specific campaign goals.</p>

<p>Engagement rate is calculated as: (Number of Engaged Target Accounts / Total Target Accounts) x 100. If your target account list has 500 accounts and 175 have taken qualifying actions, your engagement rate is 35%. Segment this metric by tier, industry, and campaign to identify where engagement is strongest and weakest.</p>

<p>Benchmarks for ABM engagement rates depend on how engagement is defined and how long the program has been running. A new program might see 15-25% engagement in the first quarter. Mature programs targeting well-qualified accounts often achieve 40-60% engagement rates. If your rate is below 20% after 90 days, investigate whether the issue is targeting accuracy, messaging relevance, or channel selection.</p>

<p>Improving engagement rate requires diagnosing the root cause of non-engagement. Are non-engaged accounts seeing your campaigns but not responding (messaging problem)? Are they not seeing your campaigns at all (coverage problem)? Are they the wrong accounts (targeting problem)? Each cause requires a different solution.</p>

<p>Track engagement trends over time at the account level. Accounts that show increasing engagement are moving toward pipeline. Accounts with declining engagement may be losing interest or have chosen a competitor. Flat engagement over extended periods suggests your content and campaigns are not resonating with that segment.</p>""",
        "faq": [
            ("What is a good ABM engagement rate?", "New programs typically see 15-25% engagement in the first quarter. Mature programs achieve 40-60%. The exact benchmark depends on how you define engagement and the quality of your target account list. Engagement below 20% after 90 days signals a problem."),
            ("How do you calculate ABM engagement rate?", "Engagement rate = (Engaged Target Accounts / Total Target Accounts) x 100. Define engaged as accounts that have taken qualifying actions like website visits, content downloads, email clicks, or meeting bookings within a specified time period."),
            ("How can ABM teams improve engagement rates?", "Diagnose the root cause: coverage problem (accounts not seeing campaigns), messaging problem (seeing but not responding), or targeting problem (wrong accounts). Then address the specific issue with channel adjustments, content changes, or list refinement."),
        ],
        "related": ["Account Engagement Score", "Coverage", "Account Penetration", "Campaign"],
    },
    {
        "term": "Meeting Rate",
        "slug": "meeting-rate",
        "short": "The percentage of target accounts that convert from engagement to a scheduled sales meeting.",
        "body": """<p>Meeting rate measures the percentage of target accounts that convert from marketing engagement to a scheduled sales meeting. It is a critical handoff metric between marketing and sales in ABM programs. Marketing drives awareness and engagement; meeting rate shows how effectively that engagement converts to direct sales conversations.</p>

<p>The formula is straightforward: (Number of Target Accounts with Meetings Booked / Number of Engaged Target Accounts) x 100. If 175 accounts are engaged and 28 have booked meetings, the meeting rate is 16%. Some teams calculate meeting rate against the total target list rather than engaged accounts only, which produces a lower but still useful number.</p>

<p>ABM programs typically improve meeting rates compared to traditional outbound because the accounts have been warmed by marketing before sales outreach. An account that has seen targeted ads, consumed relevant content, and received personalized direct mail is more likely to accept a meeting request than a cold account. This is the air cover effect in action.</p>

<p>Benchmarks for meeting rates vary by industry, deal size, and outreach method. Cold outbound meeting rates typically range from 1-3%. ABM-warmed accounts commonly achieve 5-15% meeting rates, a significant improvement. Tier 1 accounts with extensive personalization can reach 20-30% meeting rates due to the depth of engagement before outreach.</p>

<p>Improving meeting rates requires collaboration between sales and marketing. Marketing can improve the quality of accounts passed to sales by refining ICP criteria and engagement thresholds. Sales can improve conversion by timing outreach to engagement signals, personalizing the meeting request based on the account's content consumption, and following up persistently with multiple contacts.</p>

<p>Track meeting rate by ABM tier and campaign to understand which programs drive the best conversion. If Tier 2 accounts convert to meetings at a higher rate than Tier 1, the Tier 1 campaign may need more relevant content or the Tier 1 list may need qualification refinement. The data should guide resource allocation across tiers.</p>""",
        "faq": [
            ("What is a good meeting rate for ABM?", "ABM-warmed accounts typically achieve 5-15% meeting rates, compared to 1-3% for cold outbound. Tier 1 accounts with deep personalization can reach 20-30%. The benchmark depends on your industry, deal size, and how you define engagement."),
            ("How do you calculate meeting rate?", "Meeting rate = (Target Accounts with Meetings / Engaged Target Accounts) x 100. Some teams calculate against the total target list for a more conservative number. Track by tier and campaign for actionable insights."),
            ("How does ABM improve meeting rates?", "ABM warms accounts through targeted advertising, content delivery, and personalized outreach before sales reaches out. Accounts that recognize your brand and have consumed relevant content are significantly more likely to accept meeting requests."),
        ],
        "related": ["Engagement Rate", "Sales-Marketing Alignment", "Air Cover", "Pipeline Velocity"],
    },
    {
        "term": "Pipeline-to-Revenue",
        "slug": "pipeline-to-revenue",
        "short": "The conversion rate from pipeline creation to closed-won revenue in an ABM program.",
        "body": """<p>Pipeline-to-revenue measures the conversion rate from pipeline creation to actual closed-won revenue. It answers the ultimate ROI question for ABM programs: of the pipeline we generated and influenced, how much turned into real bookings? This metric connects ABM activity to the revenue number that executives and boards care about.</p>

<p>The calculation is: (Closed-Won Revenue from ABM Pipeline / Total ABM Pipeline Created) x 100. If your ABM program created $5M in pipeline and $1.5M closed, the pipeline-to-revenue rate is 30%. Compare this against your non-ABM pipeline-to-revenue rate to demonstrate ABM's impact on conversion efficiency.</p>

<p>ABM programs should show a higher pipeline-to-revenue rate than non-ABM programs for two reasons. First, the accounts in ABM pipeline are pre-qualified against your ICP, so they are better fits for your product. Second, the multi-channel engagement from ABM campaigns builds deeper relationships and stronger consensus within the buying committee, which improves close rates.</p>

<p>Typical B2B pipeline-to-revenue rates range from 15-30%, depending on deal size, industry, and sales cycle complexity. ABM-influenced pipeline often converts at a 5-15 percentage point premium over non-ABM pipeline. If your ABM pipeline converts at the same rate or worse than non-ABM pipeline, your program has a quality problem: either the accounts are not well-qualified or the engagement is not translating to buying behavior.</p>

<p>The time dimension matters. Pipeline-to-revenue requires patience because B2B sales cycles are long. A pipeline deal created in Q1 might not close until Q3 or Q4. Track cohort-based conversion: what percentage of Q1 pipeline has converted by Q2, Q3, and Q4? This reveals the true velocity of your ABM pipeline and sets realistic expectations for stakeholders.</p>

<p>Use pipeline-to-revenue data to refine your ABM program. If certain account segments convert at higher rates, expand your targeting into similar accounts. If specific campaign types consistently appear in the influence path of converted deals, invest more in those tactics. The revenue outcome is the final validation of every upstream ABM decision.</p>""",
        "faq": [
            ("What is a good pipeline-to-revenue rate for ABM?", "B2B pipeline-to-revenue rates typically range from 15-30%. ABM-influenced pipeline often converts 5-15 percentage points higher than non-ABM pipeline. If ABM pipeline does not outperform, investigate account qualification and engagement quality."),
            ("How do you calculate pipeline-to-revenue?", "Pipeline-to-revenue = (Closed-Won Revenue from ABM Pipeline / Total ABM Pipeline Created) x 100. Track on a cohort basis (by quarter of pipeline creation) to account for long sales cycles."),
            ("Why is pipeline-to-revenue the ultimate ABM metric?", "Pipeline-to-revenue connects ABM activity directly to bookings. While engagement, coverage, and pipeline creation are important leading indicators, revenue is what validates the entire program. It proves that ABM is not just generating activity but driving business outcomes."),
        ],
        "related": ["Pipeline Velocity", "Influenced Pipeline", "Sourced Pipeline", "Deal Velocity"],
    },
    {
        "term": "Account Plan",
        "slug": "account-plan",
        "short": "A strategic document that outlines the engagement strategy for a specific high-value target account.",
        "body": """<p>An account plan is a strategic document that outlines the engagement strategy, key stakeholders, competitive dynamics, and tactical roadmap for a specific high-value target account. In one-to-one ABM, account plans are essential. They transform generic sales outreach into a coordinated, research-driven campaign designed around the account's specific situation.</p>

<p>A comprehensive account plan typically includes several components. Account overview: company background, strategic priorities, recent news, and market position. Buying committee map: key stakeholders with their roles, priorities, and engagement status. Competitive landscape: which competitors have relationships at the account and what their strengths and weaknesses are. Revenue opportunity: estimated deal size, timeline, and growth potential.</p>

<p>The plan also includes the engagement strategy. This details which campaigns will run, which channels will be used, what content will be created, and how sales and marketing touchpoints will be sequenced. It identifies the champion you plan to build, the economic buyer you need to reach, and the potential blockers you need to neutralize or convert.</p>

<p>Building account plans is time-intensive, which is why they are reserved for Tier 1 accounts. A thorough account plan might take 4 to 8 hours of research and planning. This investment is justified when the potential deal size is large enough: $100K+ annual contracts typically warrant dedicated account planning. For smaller deals, the one-to-few or programmatic approach is more efficient.</p>

<p>Account plans should be living documents, not static reports that get filed away. Update them monthly with new intelligence: stakeholder changes, competitive moves, engagement data, and pipeline developments. The plan should drive weekly actions for the account team and serve as the foundation for regular account review meetings between sales and marketing.</p>

<p>The best account plans are co-created by sales and marketing. Sales brings relationship intelligence and deal context. Marketing brings engagement data, content strategy, and campaign capabilities. Together, they build a plan that leverages both teams' strengths and ensures coordinated execution across all touchpoints.</p>""",
        "faq": [
            ("What should an ABM account plan include?", "An account plan should cover the company overview, buying committee map with stakeholder roles, competitive landscape, revenue opportunity sizing, engagement strategy, channel and content plan, and timeline for campaign execution."),
            ("How long does it take to create an account plan?", "A thorough account plan takes 4 to 8 hours of research and strategic planning. This investment is justified for Tier 1 accounts with $100K+ deal potential. Smaller accounts should be covered through one-to-few or programmatic ABM approaches."),
            ("How often should account plans be updated?", "Update account plans monthly with new stakeholder intelligence, competitive moves, engagement data, and pipeline developments. Plans that are not actively maintained lose their value quickly as the account's situation evolves."),
        ],
        "related": ["One-to-One ABM", "Buying Committee", "Multi-Threading", "Orchestration"],
    },
    {
        "term": "Play",
        "slug": "play",
        "short": "A repeatable, triggered sequence of ABM actions designed to move accounts through a specific stage.",
        "body": """<p>A play in ABM is a repeatable, triggered sequence of actions designed to move target accounts through a specific stage of the buying journey. Plays standardize best practices into reusable templates that can be activated consistently across multiple accounts. Think of them as playbooks for specific situations rather than one-off campaigns.</p>

<p>Common ABM plays include the new account awareness play (activate ads and content for accounts newly added to the target list), the intent surge play (trigger personalized outreach when an account shows a spike in research activity), the stalled deal play (re-engage accounts where pipeline has gone quiet), the competitive displacement play (target accounts using a competitor with switch-focused messaging), and the expansion play (identify and engage new buying centers within existing customers).</p>

<p>Each play has a defined trigger, a sequence of actions, and success criteria. The trigger is the condition that activates the play: an intent signal, a pipeline stage change, a time-based threshold, or a sales request. The actions are the specific marketing and sales touches in sequence: ad activation, email send, sales outreach, direct mail, event invitation. The success criteria define what outcome signals that the play worked: meeting booked, pipeline created, deal advanced.</p>

<p>The value of plays is consistency and scalability. Instead of reinventing the approach for each account, the team follows a tested playbook. New team members can execute proven plays without extensive training. And play performance can be measured and optimized over time because the approach is standardized.</p>

<p>Build your play library incrementally. Start with 3 to 5 plays that address your most common ABM scenarios. Test each play on a small set of accounts, measure results, and refine before scaling. Over time, expand to cover more scenarios and account segments. A mature ABM program might have 10 to 20 plays covering the full range of account situations.</p>

<p>Document each play with clear instructions for both sales and marketing. Include the trigger criteria, step-by-step actions with timing, content and assets to use, and expected outcomes. When both teams can execute the play without additional coordination meetings, you have achieved true operational efficiency.</p>""",
        "faq": [
            ("What is a play in ABM?", "A play is a repeatable sequence of ABM actions triggered by specific conditions. It standardizes how teams respond to account situations like intent surges, stalled deals, or competitive threats. Plays combine marketing and sales activities into a coordinated, tested workflow."),
            ("What are the most common ABM plays?", "Common plays include awareness (new accounts), intent surge (active research detected), stalled deal (re-engagement), competitive displacement (accounts using competitors), and expansion (new buying centers in existing customers). Start with 3-5 plays for your most frequent scenarios."),
            ("How do you build an ABM play?", "Define the trigger condition, sequence the marketing and sales actions with timing, assign content and assets for each step, and set success criteria. Test on a small group, measure results, refine, and then scale. Document everything for team execution."),
        ],
        "related": ["Campaign", "Orchestration", "Account Plan", "Signal"],
    },
    {
        "term": "Campaign",
        "slug": "campaign",
        "short": "A coordinated set of ABM marketing activities aimed at engaging target accounts around a specific theme.",
        "body": """<p>A campaign in ABM is a coordinated set of marketing activities designed to engage target accounts around a specific theme, value proposition, or business outcome. Unlike traditional marketing campaigns that target broad audiences, ABM campaigns are built for defined account segments and personalized to the specific challenges and interests of those accounts.</p>

<p>ABM campaigns differ from plays in scope and duration. A play is a short, triggered sequence for a specific situation. A campaign is a broader initiative that may incorporate multiple plays across a longer timeframe. A campaign might run for a full quarter and include awareness advertising, content delivery, event invitations, direct mail, and sales outreach, all unified around a central theme.</p>

<p>Effective ABM campaigns start with a clear objective tied to a business outcome. Instead of "generate leads," the objective might be "create pipeline in 30 Tier 2 healthcare accounts" or "accelerate 15 stalled opportunities in the financial services segment." Specific objectives drive specific tactics and enable clear measurement.</p>

<p>Campaign components typically include a target account segment (defined by tier, industry, or shared attributes), a content theme that addresses the segment's primary challenge, multi-channel activation across advertising, email, social, and sales outreach, and measurement criteria that track account-level engagement, pipeline creation, and revenue impact.</p>

<p>Channel mix varies by campaign objective and account tier. Awareness campaigns lean on advertising and content syndication. Engagement campaigns add email, webinars, and events. Conversion campaigns emphasize sales outreach, direct mail, and executive events. The right mix depends on where your target accounts are in their buying journey and how they prefer to consume information.</p>

<p>Measure campaigns at the account level, not the individual level. Track how many target accounts engaged, progressed in pipeline, or converted to revenue as a result of the campaign. Compare against a control group of similar accounts that did not receive the campaign to isolate its impact. This account-level lens is what makes ABM measurement different from traditional marketing.</p>""",
        "faq": [
            ("How is an ABM campaign different from a traditional campaign?", "ABM campaigns target defined account segments with personalized content and multi-channel coordination. Traditional campaigns target broad audiences with generic messaging. ABM campaigns measure success at the account level rather than by lead volume."),
            ("What makes an ABM campaign effective?", "Clear objectives tied to business outcomes, a well-defined account segment, a compelling content theme, coordinated multi-channel execution, and account-level measurement. The best campaigns combine marketing air cover with coordinated sales outreach."),
            ("How long should an ABM campaign run?", "Most ABM campaigns run 8 to 12 weeks to allow enough time for multi-touch engagement. Shorter campaigns work for time-sensitive triggers. Longer campaigns work for building awareness in new markets. Match duration to your sales cycle and engagement goals."),
        ],
        "related": ["Play", "Orchestration", "Air Cover", "Engagement Rate"],
    },
    {
        "term": "Demand Unit",
        "slug": "demand-unit",
        "short": "A group within a company that has its own budget, decision-making authority, and buying process.",
        "body": """<p>A demand unit is a group within a company that has its own budget, decision-making authority, and buying process for a specific category of purchases. The concept, introduced by SiriusDecisions (now Forrester), recognizes that large enterprises are not monolithic buying entities. Different departments, divisions, and business units make independent purchasing decisions, each with their own buying committee.</p>

<p>For ABM teams, demand units matter because treating a large enterprise as a single account misses the complexity. A Fortune 500 company might have a marketing department evaluating ABM tools, an IT department evaluating data platforms, and a sales operations team evaluating CRM add-ons. Each is a separate demand unit with its own budget, stakeholders, and evaluation criteria. A single ABM approach cannot effectively engage all three.</p>

<p>Identifying demand units within target accounts requires organizational research. Look for divisions with independent P&L responsibility, business units with dedicated leadership, functional teams with their own technology budgets, and geographic regions that make autonomous purchasing decisions. Your CRM should reflect demand unit structure, not just the parent company.</p>

<p>Campaign strategy shifts when you think in demand units. Instead of one campaign per account, you might run separate campaigns for each demand unit within a large account. The messaging, content, and stakeholders differ for each unit. This is especially relevant for land-and-expand strategies, where you win one demand unit first and then expand to others over time.</p>

<p>Demand unit thinking also changes how you measure ABM performance. Pipeline and revenue should be tracked at the demand unit level, not just the account level. An account might show low overall engagement while one demand unit within it is highly active. Account-level metrics alone would miss this opportunity.</p>

<p>Not every ABM program needs to operate at the demand unit level. For mid-market accounts where purchasing is centralized, the account-level view is sufficient. Demand unit segmentation matters most for enterprise accounts with $1B+ revenue and complex organizational structures where multiple independent buying processes exist simultaneously.</p>""",
        "faq": [
            ("What is a demand unit?", "A demand unit is a group within a company with its own budget, decision-making authority, and buying process. Large enterprises often have multiple demand units making independent purchasing decisions across departments, divisions, or regions."),
            ("When should ABM teams think about demand units?", "Demand unit thinking is most relevant for enterprise accounts with $1B+ revenue and complex structures. Mid-market accounts with centralized purchasing can be managed at the account level. Consider demand units when you see multiple independent buying processes within a single company."),
            ("How do demand units affect ABM strategy?", "Each demand unit needs its own campaign, messaging, and buying committee map. Track pipeline per demand unit rather than per account. Use demand unit insights for land-and-expand strategies where you win one unit and expand to others."),
        ],
        "related": ["Buying Group", "Buying Committee", "Account Plan", "One-to-One ABM"],
    },
    {
        "term": "Buying Group",
        "slug": "buying-group",
        "short": "The specific set of stakeholders within a demand unit who are involved in a particular purchase decision.",
        "body": """<p>A buying group is the specific set of stakeholders within a demand unit or organization who are actively involved in a particular purchase decision. While a buying committee describes the typical roles that participate in purchasing decisions, a buying group is the actual, named set of people involved in a live deal. The distinction matters for execution: you campaign to buying committee profiles, but you sell to buying groups.</p>

<p>The buying group concept has gained traction in ABM because it bridges the gap between marketing's account-level targeting and sales' contact-level selling. Marketing campaigns target accounts and buying committee roles. But when an opportunity is active, there is a specific buying group of 3 to 12 individuals who will make or influence the decision. Knowing who they are and where they stand is essential.</p>

<p>Buying groups are dynamic. Members enter and exit the evaluation process. A technical evaluator might be involved early but step back once technical requirements are met. A procurement contact joins late in the process. An executive sponsor appears only at the final approval stage. Tracking these movements requires ongoing attention from both sales and marketing.</p>

<p>Mapping the buying group for an active deal means identifying each member, understanding their role in the decision (decision-maker, influencer, champion, blocker, user), assessing their sentiment toward your solution (positive, neutral, negative), and tracking their engagement with your content and outreach. This map guides tactical decisions: who to call next, what content to send, and where the deal is vulnerable.</p>

<p>ABM platforms are increasingly building buying group features. Demandbase, 6sense, and others now offer buying group identification and engagement tracking as core capabilities. These features use AI and data signals to suggest likely buying group members even before they are known to your sales team.</p>

<p>For ABM marketers, buying group awareness means creating content and campaigns that address each role's perspective. Rather than generic account-level messaging, develop assets for each buying group role: business cases for decision-makers, technical documentation for evaluators, implementation guides for users, and compliance information for legal and procurement.</p>""",
        "faq": [
            ("What is the difference between a buying group and a buying committee?", "A buying committee describes the typical roles involved in purchase decisions at a company. A buying group is the actual set of named individuals participating in a specific deal. Buying committees are abstract profiles. Buying groups are real people in live opportunities."),
            ("How do you identify buying group members?", "Combine CRM data, LinkedIn research, sales conversations, and ABM platform insights. Look for people in roles that typically influence purchases in your category. ABM platforms increasingly use AI to suggest probable buying group members based on data signals."),
            ("Why do buying groups matter for ABM?", "ABM targets accounts, but deals are won by engaging the specific people in the buying group. Understanding who they are, what they care about, and where they stand determines whether your account-level campaigns translate into actual revenue."),
        ],
        "related": ["Buying Committee", "Demand Unit", "Multi-Threading", "Account Penetration"],
    },
    {
        "term": "Signal",
        "slug": "signal",
        "short": "A data point or behavior that indicates a target account's readiness to buy or engage.",
        "body": """<p>A signal in ABM is any data point or behavior that indicates a target account's readiness to buy, evaluate solutions, or engage with your brand. Signals are the inputs that drive ABM decision-making: when to launch a campaign, which accounts to prioritize, when to engage sales, and how to personalize outreach.</p>

<p>Signals come from multiple sources. Intent signals show accounts researching relevant topics. Engagement signals show accounts interacting with your content and campaigns. Technographic signals reveal technology changes like new tool installations or contract renewals. Firmographic signals capture events like funding rounds, leadership changes, or acquisitions. Each signal type adds a different dimension to your account intelligence.</p>

<p>Not all signals are created equal. A pricing page visit from a target account is a stronger signal than a blog post view. An intent surge across multiple buying-related topics is stronger than a spike in a single generic topic. A combination of first-party engagement and third-party intent is stronger than either alone. The art of ABM is weighting signals appropriately and acting on the right combinations.</p>

<p>Signal-based workflows automate the response to account behavior. When a target account triggers a high-priority signal (such as visiting the pricing page plus showing intent surge), the system can automatically activate an ad campaign, alert the assigned sales rep, and trigger a personalized email sequence. This ensures rapid response to buying signals without manual monitoring.</p>

<p>The challenge with signals is noise. In a world of abundant data, every ABM platform generates hundreds of signals daily. Without clear prioritization and threshold-setting, teams drown in alerts and lose the ability to distinguish real buying behavior from background noise. Define which signal combinations warrant immediate action versus ongoing monitoring.</p>

<p>Build a signal hierarchy for your team. Tier 1 signals (pricing page visit + intent surge + multiple engaged contacts) trigger immediate sales action. Tier 2 signals (content engagement + moderate intent) trigger marketing campaign activation. Tier 3 signals (single ad click or blog visit) feed the engagement model but do not trigger specific actions. This hierarchy prevents alert fatigue and focuses attention where it matters.</p>""",
        "faq": [
            ("What is a signal in ABM?", "A signal is any data point or behavior indicating a target account's readiness to buy or engage. Signals come from intent data, website behavior, content engagement, technology changes, and firmographic events like funding or leadership changes."),
            ("How should ABM teams prioritize signals?", "Build a signal hierarchy. High-priority signals (pricing page visits + intent surges) trigger immediate sales action. Medium signals (content engagement) activate marketing campaigns. Low signals (blog visits, ad impressions) feed scoring models. Not every signal warrants an immediate response."),
            ("What is the difference between signals and intent data?", "Intent data is a type of signal focused on research behavior. Signals are broader and include engagement data, technographic changes, firmographic events, and any other indicator of buying readiness. Intent data is one important signal source among many."),
        ],
        "related": ["Intent Data", "Surge Score", "Dark Funnel", "Account Engagement Score"],
    },
    {
        "term": "Dark Funnel",
        "slug": "dark-funnel",
        "short": "The invisible research and evaluation activities that buyers conduct before engaging with your brand.",
        "body": """<p>The dark funnel refers to the buyer research and evaluation activities that happen outside your tracking and attribution systems. It includes the conversations, content consumption, peer recommendations, community discussions, and independent research that influence buying decisions but are invisible to your marketing technology stack.</p>

<p>Research consistently shows that B2B buyers complete 60 to 80 percent of their evaluation process before ever contacting a vendor. Much of that research happens in the dark funnel: reading independent reviews, asking peers in Slack communities, attending industry events, watching video content, and consuming analyst reports. None of these activities show up in your first-party engagement data.</p>

<p>The dark funnel challenges traditional attribution models. If a buyer consumed 20 pieces of content about your category, discussed your product in three private Slack groups, and read five peer reviews before visiting your website and requesting a demo, your attribution system sees only the last-touch website visit. The 28 earlier touchpoints that actually drove the decision are invisible.</p>

<p>For ABM teams, the dark funnel has several implications. First, do not over-index on first-party engagement data. An account with low tracked engagement might be deeply engaged through dark funnel channels. Second, invest in making your brand visible in dark funnel environments: community conversations, review sites, industry events, and peer networks. Third, use third-party intent data to illuminate some dark funnel activity by detecting topic-level research patterns.</p>

<p>Self-reported attribution helps address the dark funnel. Simply asking new leads "How did you hear about us?" or "What influenced your decision to reach out?" reveals dark funnel touchpoints that your tracking cannot capture. Many companies find that word of mouth, podcasts, and community recommendations are among the top sources, even though these never appear in marketing analytics.</p>

<p>The dark funnel is not a problem to solve. It is a reality to acknowledge. Buyers will always do private research that you cannot track. The best response is to ensure your brand shows up positively wherever buyers are looking, even when you cannot measure it. Build a reputation through content quality, community presence, and customer advocacy that works regardless of attribution visibility.</p>""",
        "faq": [
            ("What is the dark funnel?", "The dark funnel is buyer research activity that happens outside your tracking systems: peer conversations, community discussions, independent reviews, analyst reports, and other evaluation steps that influence decisions but are invisible to your marketing analytics."),
            ("Why does the dark funnel matter for ABM?", "B2B buyers complete 60-80% of their evaluation before contacting vendors. Most of that research happens in dark funnel channels. ABM programs that only rely on tracked engagement miss the majority of the buying journey."),
            ("How do you address the dark funnel?", "Use self-reported attribution to surface hidden touchpoints. Invest in brand visibility in dark funnel channels (communities, review sites, events). Use third-party intent data to detect research patterns. Accept that not everything can be tracked and focus on being present where buyers look."),
        ],
        "related": ["Signal", "Intent Data", "Third-Party Intent", "Full-Funnel ABM"],
    },
    {
        "term": "Full-Funnel ABM",
        "slug": "full-funnel-abm",
        "short": "An ABM approach that coordinates campaigns across every stage of the buying journey, from awareness to close.",
        "body": """<p>Full-funnel ABM coordinates campaigns and tactics across every stage of the buying journey: awareness, consideration, evaluation, decision, and post-sale expansion. Rather than focusing ABM efforts on a single stage (typically top-of-funnel awareness or bottom-of-funnel sales acceleration), full-funnel ABM ensures that target accounts receive relevant, stage-appropriate engagement throughout their entire journey.</p>

<p>At the top of the funnel, full-funnel ABM runs awareness campaigns: account-based advertising, thought leadership content, and social visibility to build brand recognition with target accounts that are not yet engaged. In the middle of the funnel, it delivers educational content, webinars, and personalized experiences that help engaged accounts evaluate solutions. At the bottom of the funnel, it supports active deals with case studies, ROI analysis, competitive comparisons, and buying committee-specific content.</p>

<p>The full-funnel approach extends beyond the initial sale. Post-sale, ABM programs support onboarding, drive adoption, identify expansion opportunities, and prevent churn. This aligns with the ABX (account-based experience) philosophy that the customer relationship does not end at closed-won. Expansion revenue from existing accounts is often more efficient than new logo acquisition.</p>

<p>Full-funnel ABM requires more content, more channels, and more coordination than single-stage approaches. You need stage-specific content for each buying committee role at each tier. You need channel strategies that match each stage: advertising for awareness, email and events for consideration, sales outreach and direct mail for decision. And you need orchestration that moves accounts from one stage to the next based on engagement signals.</p>

<p>The benefit of full-funnel ABM is that it eliminates the handoff gaps where accounts fall through cracks. When marketing only covers awareness and sales only covers the close, the consideration and evaluation stages are orphaned. Full-funnel programs own every stage, ensuring continuous engagement that prevents accounts from going dark between marketing and sales touches.</p>

<p>Start with the stages where you have the most obvious gaps. If your team generates awareness but struggles to convert to meetings, focus on building mid-funnel engagement programs. If you win deals but lose customers, invest in post-sale ABM. Full-funnel does not mean building everything at once. It means having a plan for every stage and systematically filling gaps.</p>""",
        "faq": [
            ("What is full-funnel ABM?", "Full-funnel ABM coordinates campaigns across every stage of the buying journey: awareness, consideration, evaluation, decision, and post-sale. It ensures target accounts receive stage-appropriate engagement throughout their entire relationship with your company."),
            ("How is full-funnel ABM different from standard ABM?", "Many ABM programs focus on a single stage, usually top-of-funnel awareness or bottom-of-funnel deal acceleration. Full-funnel ABM covers every stage, eliminating handoff gaps where accounts fall through cracks between marketing and sales."),
            ("Where should you start with full-funnel ABM?", "Start with your biggest gap. If you generate awareness but cannot convert to meetings, build mid-funnel programs. If you win deals but churn customers, invest in post-sale ABM. Build incrementally rather than trying to cover all stages at once."),
        ],
        "related": ["Account-Based Experience (ABX)", "Orchestration", "Campaign", "Dark Funnel"],
    },
]


# ---------------------------------------------------------------------------
# Helpers for related-term linking
# ---------------------------------------------------------------------------

def _build_slug_map():
    """Return {term_name: slug} for cross-referencing."""
    return {t["term"]: t["slug"] for t in GLOSSARY_TERMS}


def related_terms_html(related, slug_map):
    """Render related terms as linked pills."""
    links = []
    for term_name in related:
        slug = slug_map.get(term_name)
        if slug:
            links.append(f'<a href="/glossary/{slug}/" class="related-term">{term_name}</a>')
        else:
            links.append(f'<span class="related-term">{term_name}</span>')
    return f'<div class="related-terms"><h3>Related Terms</h3><div class="related-terms-grid">{"".join(links)}</div></div>'


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def build_glossary_index():
    """Build /glossary/ index page listing all terms."""
    title = "ABM Glossary"
    description = pad_description(
        "45 account-based marketing terms defined. Clear definitions for ABM professionals covering intent data, account scoring, buying committees, and more."
    )

    crumbs = [("Home", "/"), ("Glossary", None)]
    bc_html = breadcrumb_html(crumbs)
    bc_schema = get_breadcrumb_schema([("Home", "/"), ("Glossary", "/glossary/")])

    # Group terms alphabetically
    sorted_terms = sorted(GLOSSARY_TERMS, key=lambda t: t["term"].lower())
    groups = {}
    for t in sorted_terms:
        letter = t["term"][0].upper()
        if letter not in groups:
            groups[letter] = []
        groups[letter].append(t)

    term_list_html = ""
    for letter in sorted(groups.keys()):
        term_list_html += f'<div class="glossary-group"><h2 class="glossary-letter">{letter}</h2><ul class="glossary-list">'
        for t in groups[letter]:
            term_list_html += f'<li><a href="/glossary/{t["slug"]}/">{t["term"]}</a><span class="glossary-short">{t["short"]}</span></li>'
        term_list_html += '</ul></div>'

    body = f'''<div class="page-header container">
    {bc_html}
    <h1>ABM Glossary</h1>
    <p class="lead">45 account-based marketing terms defined clearly for practitioners. No jargon, no fluff.</p>
</div>
<div class="glossary-index container">
    {term_list_html}
</div>
'''
    body += newsletter_cta_html("Stay sharp on ABM terminology and strategy.")

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/glossary/",
        body_content=body, active_path="/glossary/", extra_head=bc_schema,
    )
    write_page("glossary/index.html", page)
    print(f"  Built: glossary/index.html")


def build_glossary_term_page(term_data, slug_map):
    """Build a single glossary term page at /glossary/{slug}/."""
    term = term_data["term"]
    slug = term_data["slug"]
    short = term_data["short"]
    body_content = term_data["body"]
    faq_pairs = term_data["faq"]
    related = term_data["related"]

    title = f"What Is {term}?"
    description = pad_description(
        f"{term}: {short} Learn how ABM professionals use this concept in practice."
    )

    crumbs = [("Home", "/"), ("Glossary", "/glossary/"), (term, None)]
    bc_html = breadcrumb_html(crumbs)
    bc_schema = get_breadcrumb_schema([
        ("Home", "/"),
        ("Glossary", "/glossary/"),
        (term, f"/glossary/{slug}/"),
    ])
    faq_schema = get_faq_schema(faq_pairs)

    faq_section = faq_html(faq_pairs)
    related_section = related_terms_html(related, slug_map)

    body = f'''<article class="glossary-article container">
    {bc_html}
    <h1>What Is {term}?</h1>
    <p class="glossary-tldr">{short}</p>
    <div class="glossary-body">
        {body_content}
    </div>
    {related_section}
    {faq_section}
</article>
'''
    body += newsletter_cta_html("Get ABM insights delivered weekly.")

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path=f"/glossary/{slug}/",
        body_content=body, active_path="/glossary/",
        extra_head=bc_schema + faq_schema,
    )
    write_page(f"glossary/{slug}/index.html", page)


def build_all_glossary_pages(project_dir):
    """Build glossary index + all term pages."""
    print(f"\n  Building glossary pages ({len(GLOSSARY_TERMS)} terms)...")
    slug_map = _build_slug_map()

    build_glossary_index()

    for term_data in GLOSSARY_TERMS:
        build_glossary_term_page(term_data, slug_map)

    print(f"  Built: {len(GLOSSARY_TERMS)} glossary term pages")
