# scripts/tool_pages.py
# Tool review section page generators (~40 pages).
# Uses market_intelligence.json for mention counts. Generates reviews,
# category pages, comparisons, and roundups.

import os
import json

from nav_config import *
from templates import (get_page_wrapper, write_page, breadcrumb_html,
                       get_breadcrumb_schema, get_faq_schema, faq_html,
                       get_software_application_schema, newsletter_cta_html)


# ---------------------------------------------------------------------------
# Tool database (curated content for ABM tools)
# ---------------------------------------------------------------------------

TOOL_DATABASE = {
    # ABM Platforms
    "6sense": {
        "name": "6sense", "slug": "6sense-review",
        "category": "abm-platforms", "category_label": "ABM Platforms",
        "tagline": "AI-powered ABM platform for intent data and predictive analytics",
        "description": "6sense is an account engagement platform that uses AI and intent data to identify accounts in-market for your solution. It helps ABM teams prioritize accounts, personalize outreach, and measure pipeline impact.",
        "founded": "2013", "hq": "San Francisco, CA",
        "pricing": "Enterprise pricing, typically $60K-$120K/year",
        "best_for": "Enterprise B2B companies with complex sales cycles and dedicated ABM teams",
        "strengths": ["Best-in-class intent data from Bombora partnership", "AI-powered account scoring and prioritization", "Strong Salesforce and HubSpot integrations", "Predictive analytics for buying stage identification", "Robust audience segmentation for advertising"],
        "weaknesses": ["Steep learning curve for new users", "Enterprise pricing excludes mid-market", "Intent data accuracy varies by industry", "Long implementation timeline (3-6 months)", "Requires dedicated admin for ongoing optimization"],
        "alternatives": ["Demandbase", "Terminus", "RollWorks"],
        "rating": {"value": 4.2, "count": 342},
        "url": "https://6sense.com",
    },
    "demandbase": {
        "name": "Demandbase", "slug": "demandbase-review",
        "category": "abm-platforms", "category_label": "ABM Platforms",
        "tagline": "All-in-one ABM platform combining advertising, intent, and sales intelligence",
        "description": "Demandbase (formerly Demandbase + Engagio) is an ABM platform that combines account identification, intent data, advertising, and sales intelligence in a single platform. Known for its Demandbase One suite.",
        "founded": "2006", "hq": "San Francisco, CA",
        "pricing": "Enterprise pricing, typically $50K-$100K/year",
        "best_for": "Mid-market to enterprise companies running multi-channel ABM programs",
        "strengths": ["Unified platform (advertising + intent + sales intel)", "Strong account identification via IP-to-account matching", "Native B2B advertising DSP", "Good onboarding and customer success", "Comprehensive analytics and attribution"],
        "weaknesses": ["Interface can feel overwhelming", "Advertising CPMs are higher than general DSPs", "Some feature overlap since Engagio merger", "Account matching accuracy varies by region (US-centric)", "Requires significant data hygiene to get value"],
        "alternatives": ["6sense", "Terminus", "RollWorks"],
        "rating": {"value": 4.1, "count": 287},
        "url": "https://demandbase.com",
    },
    "terminus": {
        "name": "Terminus", "slug": "terminus-review",
        "category": "abm-platforms", "category_label": "ABM Platforms",
        "tagline": "Multi-channel ABM platform with strong advertising capabilities",
        "description": "Terminus is an ABM platform focused on multi-channel account engagement. It offers display advertising, email experiences, web personalization, and chat for targeted accounts. Acquired by DemandScience in 2023.",
        "founded": "2014", "hq": "Atlanta, GA",
        "pricing": "Starting at $30K/year for core platform",
        "best_for": "Mid-market B2B companies starting their ABM journey",
        "strengths": ["Lower entry price than 6sense/Demandbase", "Strong multi-channel engagement (ads, email, web, chat)", "Good for ABM beginners with guided playbooks", "Solid Salesforce integration", "Account-level chat capabilities"],
        "weaknesses": ["Intent data less robust than 6sense", "Advertising reach is narrower", "Feature depth lags behind 6sense and Demandbase", "Company ownership changes create uncertainty", "Reporting could be more granular"],
        "alternatives": ["6sense", "Demandbase", "RollWorks"],
        "rating": {"value": 3.9, "count": 198},
        "url": "https://terminus.com",
    },
    "rollworks": {
        "name": "RollWorks", "slug": "rollworks-review",
        "category": "abm-platforms", "category_label": "ABM Platforms",
        "tagline": "Account-based platform from NextRoll, focused on advertising and ABM",
        "description": "RollWorks is the B2B division of NextRoll (formerly AdRoll). It offers account-based advertising, intent data, and account scoring. Best known for accessible pricing and strong ad capabilities.",
        "founded": "2018 (B2B spinoff)", "hq": "San Francisco, CA",
        "pricing": "Starting at $12K/year, more accessible than enterprise ABM platforms",
        "best_for": "SMB and mid-market teams that want ABM advertising without enterprise pricing",
        "strengths": ["Most accessible pricing in the ABM platform category", "Strong display and social advertising", "Quick implementation (weeks, not months)", "Good for teams just starting ABM", "Solid account scoring and prioritization"],
        "weaknesses": ["Less sophisticated intent data than 6sense", "Limited personalization capabilities", "Smaller ecosystem of integrations", "Ad-centric, less full-funnel than competitors", "Reporting is basic compared to enterprise platforms"],
        "alternatives": ["6sense", "Demandbase", "Terminus"],
        "rating": {"value": 3.8, "count": 156},
        "url": "https://rollworks.com",
    },
    "triblio": {
        "name": "Triblio", "slug": "triblio-review",
        "category": "abm-platforms", "category_label": "ABM Platforms",
        "tagline": "ABM platform for orchestrating multi-channel account campaigns",
        "description": "Triblio (now part of IDG/Foundry) is an ABM platform that combines web personalization, advertising, and sales activation. Known for its orchestration capabilities and content syndication network via IDG.",
        "founded": "2014", "hq": "Reston, VA",
        "pricing": "Contact for pricing, mid-market positioning",
        "best_for": "Companies that value content syndication alongside ABM execution",
        "strengths": ["Strong content syndication through IDG network", "Web personalization for target accounts", "Good orchestration across channels", "Reasonable pricing for mid-market", "Strong sales activation features"],
        "weaknesses": ["Smaller market presence than top 3 platforms", "Less third-party integration support", "Intent data relies on IDG network", "Fewer case studies and social proof", "Learning resources are limited"],
        "alternatives": ["Terminus", "RollWorks", "Madison Logic"],
        "rating": {"value": 3.7, "count": 89},
        "url": "https://triblio.com",
    },
    "madison-logic": {
        "name": "Madison Logic", "slug": "madison-logic-review",
        "category": "abm-platforms", "category_label": "ABM Platforms",
        "tagline": "ABM platform focused on content syndication and intent-based advertising",
        "description": "Madison Logic is an ABM media activation platform that uses intent data to deliver targeted content syndication, display advertising, and LinkedIn advertising to in-market accounts.",
        "founded": "2005", "hq": "New York, NY",
        "pricing": "Enterprise pricing, typically $40K-$80K/year",
        "best_for": "Enterprise teams focused on content syndication and lead generation",
        "strengths": ["Strong content syndication network", "Proprietary intent data (ML Insights)", "LinkedIn advertising integration", "Good for lead generation at scale", "Established player with long track record"],
        "weaknesses": ["More lead-gen focused than full ABM", "Less account engagement features", "Pricing favors enterprise budgets", "Platform UX could be modernized", "Analytics less comprehensive than 6sense"],
        "alternatives": ["Triblio", "6sense", "Demandbase"],
        "rating": {"value": 3.8, "count": 134},
        "url": "https://madisonlogic.com",
    },

    # Intent Data
    "bombora": {
        "name": "Bombora", "slug": "bombora-review",
        "category": "intent-data", "category_label": "Intent Data",
        "tagline": "B2B intent data cooperative powering account-based marketing",
        "description": "Bombora operates the largest B2B intent data cooperative, tracking content consumption across 5,000+ B2B websites. Their Company Surge data identifies accounts researching topics relevant to your solution.",
        "founded": "2014", "hq": "New York, NY",
        "pricing": "Starting at $25K/year, enterprise tiers available",
        "best_for": "Any B2B company that wants to know which accounts are actively researching their category",
        "strengths": ["Largest B2B intent data cooperative (5,000+ sites)", "Powers intent data for 6sense, Salesforce, and others", "Proprietary Company Surge scoring", "Good topic-level granularity", "Strong privacy compliance (no cookies, cooperative model)"],
        "weaknesses": ["Intent signals can be noisy", "Cooperative model means competitors see similar data", "Topic taxonomy requires careful setup", "Latency of 7-14 days on some signals", "Requires integration work to activate"],
        "alternatives": ["G2 Intent", "TrustRadius Intent", "ZoomInfo Intent"],
        "rating": {"value": 4.0, "count": 223},
        "url": "https://bombora.com",
    },
    "g2-intent": {
        "name": "G2 Buyer Intent", "slug": "g2-intent-review",
        "category": "intent-data", "category_label": "Intent Data",
        "tagline": "Intent signals from the world's largest B2B software marketplace",
        "description": "G2 Buyer Intent captures signals from G2.com, where millions of B2B buyers research and compare software. When a target account views your G2 profile or category, G2 sends real-time intent signals.",
        "founded": "2012 (G2 overall)", "hq": "Chicago, IL",
        "pricing": "Bundled with G2 Marketing Solutions, starting at $15K/year",
        "best_for": "Software companies listed on G2 that want to identify active buyers",
        "strengths": ["High-intent signals (active buyers comparing software)", "Real-time notifications when accounts visit your profile", "Category-level intent (accounts researching your market)", "Strong Salesforce and HubSpot integrations", "Trusted by buyers (70M+ annual visitors)"],
        "weaknesses": ["Only captures G2 traffic, not broader web", "Limited to software buyers (not all B2B)", "Requires active G2 profile and reviews", "Signal volume depends on your category size", "Premium pricing for best features"],
        "alternatives": ["Bombora", "TrustRadius Intent", "ZoomInfo Intent"],
        "rating": {"value": 4.1, "count": 178},
        "url": "https://sell.g2.com/intent",
    },
    "trustradius-intent": {
        "name": "TrustRadius Intent", "slug": "trustradius-intent-review",
        "category": "intent-data", "category_label": "Intent Data",
        "tagline": "Downstream intent data from verified B2B buyers",
        "description": "TrustRadius offers buyer intent data from its review platform, where B2B buyers research, compare, and shortlist software. Their downstream intent signals indicate accounts deep in the buying journey.",
        "founded": "2012", "hq": "Austin, TX",
        "pricing": "Bundled with TrustRadius for Vendors, starting at $10K/year",
        "best_for": "Software companies that want deep-funnel intent signals from verified buyers",
        "strengths": ["Downstream intent (comparison, pricing, shortlist signals)", "Verified reviews add credibility", "Lower price point than G2 and Bombora", "Good for identifying late-stage buyers", "Strong integration with Salesforce and 6sense"],
        "weaknesses": ["Smaller traffic base than G2", "Less category coverage", "Signal volume is lower", "Platform awareness lower among buyers", "Review volume varies by category"],
        "alternatives": ["G2 Intent", "Bombora", "ZoomInfo Intent"],
        "rating": {"value": 3.8, "count": 112},
        "url": "https://trustradius.com/for-vendors",
    },
    "zoominfo-intent": {
        "name": "ZoomInfo Intent", "slug": "zoominfo-intent-review",
        "category": "intent-data", "category_label": "Intent Data",
        "tagline": "Intent data integrated into the ZoomInfo sales intelligence platform",
        "description": "ZoomInfo Intent combines web content consumption signals with ZoomInfo's contact database. It identifies accounts researching relevant topics and surfaces contacts at those accounts for outreach.",
        "founded": "2000 (ZoomInfo overall)", "hq": "Vancouver, WA",
        "pricing": "Bundled with ZoomInfo plans, $15K-$40K/year range",
        "best_for": "Teams already using ZoomInfo that want intent data without a separate vendor",
        "strengths": ["Integrated with ZoomInfo's massive contact database", "Easy to activate (contacts already available)", "Combines intent with technographics and firmographics", "No additional vendor to manage", "Good for sales-led ABM workflows"],
        "weaknesses": ["Intent data quality trails Bombora and G2", "Bundled pricing makes it hard to evaluate standalone", "Signal sources less transparent", "Topic taxonomy less granular", "Can be noisy without careful configuration"],
        "alternatives": ["Bombora", "G2 Intent", "TrustRadius Intent"],
        "rating": {"value": 3.7, "count": 145},
        "url": "https://zoominfo.com",
    },

    # Personalization
    "mutiny": {
        "name": "Mutiny", "slug": "mutiny-review",
        "category": "personalization", "category_label": "Personalization",
        "tagline": "AI-powered website personalization for B2B companies",
        "description": "Mutiny is a no-code website personalization platform built for B2B marketers. It uses firmographic data, intent signals, and visitor behavior to show personalized website experiences to target accounts and segments.",
        "founded": "2018", "hq": "San Francisco, CA",
        "pricing": "Starting at $18K/year, scales with traffic",
        "best_for": "B2B marketing teams that want to personalize their website without engineering resources",
        "strengths": ["No-code visual editor for personalization", "Strong ABM integrations (6sense, Clearbit, Demandbase)", "AI-powered content suggestions", "Easy A/B testing for personalized experiences", "Good for account-specific landing pages"],
        "weaknesses": ["Pricing scales with traffic (can get expensive)", "Personalization limited to web (no email/ads)", "Requires quality traffic to see results", "Setup requires clear ICP definition", "Attribution can be tricky to isolate"],
        "alternatives": ["Intellimize", "PathFactory", "Folloze"],
        "rating": {"value": 4.3, "count": 167},
        "url": "https://mutinyhq.com",
    },
    "intellimize": {
        "name": "Intellimize", "slug": "intellimize-review",
        "category": "personalization", "category_label": "Personalization",
        "tagline": "AI optimization platform for website conversion",
        "description": "Intellimize uses machine learning to automatically test and optimize website experiences. It goes beyond A/B testing by simultaneously testing multiple variations and personalizing for different audience segments.",
        "founded": "2016", "hq": "San Mateo, CA",
        "pricing": "Starting at $30K/year, enterprise pricing for high traffic",
        "best_for": "High-traffic B2B websites that want automated conversion optimization",
        "strengths": ["AI-driven multivariate testing at scale", "Automatic optimization without manual analysis", "Strong conversion rate optimization", "Good for teams without dedicated CRO resources", "Machine learning improves over time"],
        "weaknesses": ["Higher price point than Mutiny for similar features", "Requires significant traffic volume to work", "Less ABM-specific than Mutiny", "Black box AI can be hard to explain", "Implementation needs engineering support"],
        "alternatives": ["Mutiny", "PathFactory", "Optimizely"],
        "rating": {"value": 4.0, "count": 98},
        "url": "https://intellimize.com",
    },
    "pathfactory": {
        "name": "PathFactory", "slug": "pathfactory-review",
        "category": "personalization", "category_label": "Personalization",
        "tagline": "Content intelligence and activation platform for B2B",
        "description": "PathFactory is a content experience platform that tracks how buyers engage with content and uses that data to serve personalized content journeys. It replaces static resource pages with intelligent content tracks.",
        "founded": "2012", "hq": "Toronto, Canada",
        "pricing": "Starting at $20K/year",
        "best_for": "Content-heavy B2B organizations with large asset libraries",
        "strengths": ["Content engagement analytics (time spent, binge rate)", "Personalized content tracks based on behavior", "Removes form gates for better buyer experience", "Good integration with Marketo and Eloqua", "Content recommendations powered by AI"],
        "weaknesses": ["Niche tool, content-specific only", "Requires large content library to see ROI", "Can be complex to set up content tracks", "Less useful for companies with few content assets", "Pricing is premium for a content-only tool"],
        "alternatives": ["Mutiny", "Folloze", "Uberflip"],
        "rating": {"value": 4.1, "count": 134},
        "url": "https://pathfactory.com",
    },
    "folloze": {
        "name": "Folloze", "slug": "folloze-review",
        "category": "personalization", "category_label": "Personalization",
        "tagline": "Buyer experience platform for personalized content boards",
        "description": "Folloze enables sales and marketing teams to create personalized content boards (microsites) for target accounts. Each board is a curated collection of content tailored to a specific account's interests and buying stage.",
        "founded": "2013", "hq": "San Mateo, CA",
        "pricing": "Starting at $15K/year",
        "best_for": "Sales-led organizations that want to create account-specific content experiences",
        "strengths": ["Easy to create account-specific content boards", "Sales reps can personalize without marketing help", "Good engagement tracking per account", "Integrates with CRM and marketing automation", "Lower price point than competitors"],
        "weaknesses": ["Less AI/automation than Mutiny or Intellimize", "More sales tool than marketing platform", "Content boards require manual curation", "Analytics less sophisticated", "Smaller customer base and community"],
        "alternatives": ["Mutiny", "PathFactory", "Highspot"],
        "rating": {"value": 3.9, "count": 87},
        "url": "https://folloze.com",
    },

    # Direct Mail
    "sendoso": {
        "name": "Sendoso", "slug": "sendoso-review",
        "category": "direct-mail", "category_label": "Direct Mail",
        "tagline": "Sending platform for direct mail, gifts, and eGifts in B2B",
        "description": "Sendoso is a sending platform that enables B2B teams to send physical gifts, direct mail, branded items, and eGifts to prospects and customers. It integrates with CRM and marketing automation to trigger sends based on account behavior.",
        "founded": "2016", "hq": "San Francisco, CA",
        "pricing": "Platform fee starting at $20K/year plus per-send costs",
        "best_for": "Enterprise sales and ABM teams running high-value account campaigns",
        "strengths": ["Largest marketplace of sending options (gifts, swag, food, experiences)", "Strong CRM integrations (Salesforce, HubSpot, Outreach)", "Good analytics on send engagement", "Address verification reduces waste", "Trigger-based sends from ABM platforms"],
        "weaknesses": ["Total cost (platform + sends) adds up quickly", "Warehouse and fulfillment can have delays", "International sending is limited and expensive", "ROI tracking requires attribution setup", "Some gift options have long lead times"],
        "alternatives": ["Reachdesk", "PFL", "Alyce"],
        "rating": {"value": 4.0, "count": 189},
        "url": "https://sendoso.com",
    },
    "reachdesk": {
        "name": "Reachdesk", "slug": "reachdesk-review",
        "category": "direct-mail", "category_label": "Direct Mail",
        "tagline": "Global gifting and direct mail platform for B2B",
        "description": "Reachdesk is a B2B gifting and direct mail platform with strong international capabilities. It enables sales and marketing teams to send personalized gifts, handwritten notes, and branded items globally.",
        "founded": "2018", "hq": "London, UK",
        "pricing": "Starting at $15K/year plus per-send costs",
        "best_for": "Global B2B teams that need international sending capabilities",
        "strengths": ["Best international coverage (US, UK, EU, APAC)", "eGift marketplace with global brands", "Handwritten note capabilities", "Good Salesforce and HubSpot integrations", "More affordable than Sendoso for international sends"],
        "weaknesses": ["Smaller US marketplace than Sendoso", "Less brand awareness in North America", "Analytics less sophisticated than competitors", "Fewer trigger-based automation options", "Customer support varies by region"],
        "alternatives": ["Sendoso", "PFL", "Alyce"],
        "rating": {"value": 3.9, "count": 112},
        "url": "https://reachdesk.com",
    },
    "pfl": {
        "name": "PFL", "slug": "pfl-review",
        "category": "direct-mail", "category_label": "Direct Mail",
        "tagline": "Tactile marketing automation for direct mail at scale",
        "description": "PFL (formerly PrintingForLess) specializes in tactile marketing automation, combining direct mail with marketing automation triggers. Known for high-quality print and fulfillment capabilities.",
        "founded": "1996", "hq": "Livingston, MT",
        "pricing": "Contact for pricing, enterprise positioning",
        "best_for": "Companies that prioritize print quality and direct mail at scale",
        "strengths": ["Highest print quality in the category", "In-house printing and fulfillment", "Strong Marketo and Eloqua integrations", "Good for high-volume direct mail programs", "Established company with long track record"],
        "weaknesses": ["Less digital gifting options", "Platform interface is dated", "Fewer eGift options than Sendoso/Reachdesk", "International capabilities are limited", "Setup and campaign creation takes longer"],
        "alternatives": ["Sendoso", "Reachdesk", "Alyce"],
        "rating": {"value": 3.7, "count": 78},
        "url": "https://pfl.com",
    },
    "alyce": {
        "name": "Alyce", "slug": "alyce-review",
        "category": "direct-mail", "category_label": "Direct Mail",
        "tagline": "Personal gifting platform for B2B sales and marketing",
        "description": "Alyce is a personal experience platform that uses AI to recommend gifts based on recipient interests. It analyzes social profiles to suggest gifts the recipient will actually want, rather than generic swag.",
        "founded": "2015", "hq": "Boston, MA",
        "pricing": "Starting at $20K/year plus per-gift costs",
        "best_for": "Teams that want highly personalized, 1:1 gifting for high-value prospects",
        "strengths": ["AI-powered gift recommendations based on recipient interests", "Recipients choose their own gift (higher acceptance rates)", "Strong personalization differentiates from generic swag", "Good for high-value 1:1 ABM campaigns", "Integrates with Salesforce, Outreach, and ABM platforms"],
        "weaknesses": ["Higher per-gift cost than generic sending", "Best suited for small-volume, high-value campaigns", "Less effective for high-volume programs", "Gift acceptance tracking can be imperfect", "Newer platform, smaller customer base"],
        "alternatives": ["Sendoso", "Reachdesk", "PFL"],
        "rating": {"value": 4.1, "count": 95},
        "url": "https://alyce.com",
    },

    # Marketing Automation
    "hubspot": {
        "name": "HubSpot", "slug": "hubspot-review",
        "category": "marketing-automation", "category_label": "Marketing Automation",
        "tagline": "All-in-one CRM, marketing, and sales platform",
        "description": "HubSpot is a comprehensive CRM and marketing platform that serves as the foundation for many ABM programs. While not ABM-native, its Marketing Hub Enterprise includes ABM features like target account lists, company scoring, and account-based reporting.",
        "founded": "2006", "hq": "Cambridge, MA",
        "pricing": "Free CRM, Marketing Hub Enterprise at $3,600/mo for ABM features",
        "best_for": "Mid-market companies that want ABM capabilities within an all-in-one platform",
        "strengths": ["All-in-one platform (CRM + marketing + sales + service)", "Native ABM features in Enterprise tier", "Massive integration ecosystem", "Excellent documentation and academy", "Strong community and support"],
        "weaknesses": ["ABM features lag behind dedicated platforms", "Enterprise pricing required for ABM features", "Account-level reporting is basic", "Intent data requires third-party integration", "Can be limiting for complex enterprise ABM"],
        "alternatives": ["Marketo", "Pardot", "ActiveCampaign"],
        "rating": {"value": 4.4, "count": 1243},
        "url": "https://hubspot.com",
    },
    "marketo": {
        "name": "Marketo", "slug": "marketo-review",
        "category": "marketing-automation", "category_label": "Marketing Automation",
        "tagline": "Enterprise marketing automation from Adobe",
        "description": "Marketo Engage (now part of Adobe) is the marketing automation platform of choice for many enterprise ABM teams. It offers advanced lead scoring, nurturing, campaign orchestration, and deep integration with Salesforce.",
        "founded": "2006", "hq": "San Mateo, CA (Adobe)",
        "pricing": "Starting at $895/mo, enterprise pricing for advanced features",
        "best_for": "Enterprise B2B companies with complex multi-touch campaigns and Salesforce",
        "strengths": ["Deep Salesforce integration", "Advanced lead and account scoring", "Sophisticated campaign orchestration", "Strong ABM platform integrations (6sense, Demandbase)", "Battle-tested at enterprise scale"],
        "weaknesses": ["Steep learning curve", "Dated UI compared to HubSpot", "Expensive for smaller teams", "Requires Marketo-certified admin", "Landing page builder is limited"],
        "alternatives": ["HubSpot", "Pardot", "Eloqua"],
        "rating": {"value": 4.0, "count": 876},
        "url": "https://business.adobe.com/products/marketo/adobe-marketo.html",
    },
    "pardot": {
        "name": "Pardot (Account Engagement)", "slug": "pardot-review",
        "category": "marketing-automation", "category_label": "Marketing Automation",
        "tagline": "Salesforce-native marketing automation for B2B",
        "description": "Pardot (now Salesforce Account Engagement) is a B2B marketing automation platform native to the Salesforce ecosystem. It offers email marketing, lead scoring, campaign management, and account-based features within Salesforce.",
        "founded": "2007", "hq": "Atlanta, GA (Salesforce)",
        "pricing": "Starting at $1,250/mo, bundled with Salesforce",
        "best_for": "Salesforce-centric organizations that want marketing automation in their existing ecosystem",
        "strengths": ["Native Salesforce integration (no sync issues)", "Account-based reporting within Salesforce", "Einstein AI features for scoring and insights", "Good for Salesforce-first organizations", "Strong B2B email capabilities"],
        "weaknesses": ["Limited outside the Salesforce ecosystem", "Fewer third-party integrations than HubSpot", "UI is Salesforce-native (not always intuitive)", "Less flexible than Marketo for complex campaigns", "Pricing requires Salesforce investment"],
        "alternatives": ["Marketo", "HubSpot", "Eloqua"],
        "rating": {"value": 3.8, "count": 654},
        "url": "https://salesforce.com/marketing/automation/",
    },

    # Analytics
    "tableau": {
        "name": "Tableau", "slug": "tableau-review",
        "category": "analytics", "category_label": "Analytics",
        "tagline": "Visual analytics platform for ABM reporting and dashboards",
        "description": "Tableau (Salesforce) is a visual analytics platform that ABM teams use to build custom dashboards, track account engagement, and report on pipeline impact. It connects to CRM, marketing automation, and ABM platforms.",
        "founded": "2003", "hq": "Seattle, WA (Salesforce)",
        "pricing": "Creator at $75/user/mo, Viewer at $15/user/mo",
        "best_for": "ABM teams that need custom reporting beyond what their ABM platform provides",
        "strengths": ["Best-in-class data visualization", "Connects to virtually any data source", "Account-level dashboards for ABM reporting", "Strong community and template library", "Salesforce integration for unified reporting"],
        "weaknesses": ["Requires analyst skills to build dashboards", "Licensing costs add up with many users", "Not ABM-specific, requires custom setup", "Can be slow with large datasets", "Mobile experience is limited"],
        "alternatives": ["Looker", "Power BI", "Domo"],
        "rating": {"value": 4.3, "count": 2156},
        "url": "https://tableau.com",
    },
    "looker": {
        "name": "Looker", "slug": "looker-review",
        "category": "analytics", "category_label": "Analytics",
        "tagline": "Google Cloud BI platform for data-driven ABM teams",
        "description": "Looker (Google Cloud) is a business intelligence platform that ABM teams use for custom metrics, embedded analytics, and data modeling. Its LookML modeling layer makes it strong for teams with engineering support.",
        "founded": "2012", "hq": "Santa Cruz, CA (Google)",
        "pricing": "Contact for pricing, enterprise positioning",
        "best_for": "Data-driven ABM teams with engineering resources and Google Cloud infrastructure",
        "strengths": ["LookML data modeling for consistent metrics", "Strong for embedded analytics", "Good for creating custom ABM metrics", "Integrates with BigQuery and Google Cloud", "Version-controlled data models"],
        "weaknesses": ["Requires LookML knowledge (developer dependency)", "Less intuitive for non-technical users", "Google Cloud bias in integrations", "Higher learning curve than Tableau", "Fewer out-of-the-box templates"],
        "alternatives": ["Tableau", "Power BI", "Amplitude"],
        "rating": {"value": 4.0, "count": 876},
        "url": "https://looker.com",
    },
    "amplitude": {
        "name": "Amplitude", "slug": "amplitude-review",
        "category": "analytics", "category_label": "Analytics",
        "tagline": "Product analytics platform for understanding account behavior",
        "description": "Amplitude is a product analytics platform that ABM teams use to understand how target accounts engage with their product. It tracks feature usage, activation metrics, and account-level product engagement.",
        "founded": "2012", "hq": "San Francisco, CA",
        "pricing": "Free tier available, Growth at $49/mo, Enterprise pricing",
        "best_for": "Product-led growth companies running ABM alongside PLG motions",
        "strengths": ["Best-in-class product analytics", "Account-level engagement tracking", "Cohort analysis for ABM segments", "Good for PLG + ABM hybrid motions", "Free tier for getting started"],
        "weaknesses": ["Product analytics, not marketing analytics", "Requires product instrumentation", "Less useful for sales-led organizations", "Account-level features need Enterprise plan", "Learning curve for behavioral analytics"],
        "alternatives": ["Mixpanel", "Heap", "Pendo"],
        "rating": {"value": 4.2, "count": 567},
        "url": "https://amplitude.com",
    },
}

# ---------------------------------------------------------------------------
# Category definitions
# ---------------------------------------------------------------------------

CATEGORIES = {
    "abm-platforms": {
        "name": "ABM Platforms",
        "slug": "abm-platforms",
        "description": "Full-stack ABM platforms that combine account identification, intent data, advertising, and orchestration. These are the core platforms ABM teams build their programs around.",
        "tools": ["6sense", "demandbase", "terminus", "rollworks", "triblio", "madison-logic"],
    },
    "intent-data": {
        "name": "Intent Data Providers",
        "slug": "intent-data",
        "description": "Intent data platforms that identify accounts actively researching your category. They track content consumption signals across the web to surface in-market accounts.",
        "tools": ["bombora", "g2-intent", "trustradius-intent", "zoominfo-intent"],
    },
    "personalization": {
        "name": "Personalization Tools",
        "slug": "personalization",
        "description": "Website personalization and content experience platforms that help ABM teams deliver tailored experiences to target accounts and segments.",
        "tools": ["mutiny", "intellimize", "pathfactory", "folloze"],
    },
    "direct-mail": {
        "name": "Direct Mail Platforms",
        "slug": "direct-mail",
        "description": "Gifting and direct mail platforms that enable ABM teams to send physical gifts, swag, and personalized items to target accounts.",
        "tools": ["sendoso", "reachdesk", "pfl", "alyce"],
    },
    "marketing-automation": {
        "name": "Marketing Automation",
        "slug": "marketing-automation",
        "description": "Marketing automation platforms that serve as the execution layer for ABM campaigns. They handle email, lead scoring, nurturing, and campaign orchestration.",
        "tools": ["hubspot", "marketo", "pardot"],
    },
    "analytics": {
        "name": "Analytics Platforms",
        "slug": "analytics",
        "description": "Business intelligence and analytics platforms that ABM teams use for reporting, dashboards, and data-driven decision making.",
        "tools": ["tableau", "looker", "amplitude"],
    },
}

# ---------------------------------------------------------------------------
# Comparison definitions
# ---------------------------------------------------------------------------

TOOL_COMPARISONS = [
    {
        "slug": "6sense-vs-demandbase",
        "tool_a": "6sense", "tool_b": "demandbase",
        "title": "6sense vs Demandbase",
        "summary": "The two dominant ABM platforms go head-to-head. 6sense leads on AI-powered intent data and predictive scoring. Demandbase leads on advertising and its unified platform approach. Both are enterprise-priced.",
        "winner_intent": "6sense", "winner_ads": "Demandbase", "winner_ease": "Demandbase",
        "verdict": "Choose 6sense if intent data accuracy and AI-driven prioritization are your top priorities. Choose Demandbase if you want a unified platform with strong native advertising.",
    },
    {
        "slug": "terminus-vs-rollworks",
        "tool_a": "terminus", "tool_b": "rollworks",
        "title": "Terminus vs RollWorks",
        "summary": "The mid-market ABM platforms. Terminus offers more engagement channels (ads, email, web, chat). RollWorks has better pricing and is easier to start with. Both are good first ABM platforms.",
        "winner_intent": "Terminus", "winner_ads": "RollWorks", "winner_ease": "RollWorks",
        "verdict": "Choose Terminus for multi-channel engagement. Choose RollWorks for accessible pricing and quick setup. Both are better fits for mid-market than 6sense or Demandbase.",
    },
    {
        "slug": "sendoso-vs-reachdesk",
        "tool_a": "sendoso", "tool_b": "reachdesk",
        "title": "Sendoso vs Reachdesk",
        "summary": "The top direct mail platforms for ABM. Sendoso has the largest US marketplace and best integrations. Reachdesk has superior international coverage and lower pricing for global teams.",
        "winner_intent": "N/A", "winner_ads": "N/A", "winner_ease": "Reachdesk",
        "verdict": "Choose Sendoso if you are US-focused and want the broadest gift marketplace. Choose Reachdesk if you need strong international sending or are budget-conscious.",
    },
    {
        "slug": "mutiny-vs-intellimize",
        "tool_a": "mutiny", "tool_b": "intellimize",
        "title": "Mutiny vs Intellimize",
        "summary": "The personalization tools for B2B. Mutiny is ABM-native with no-code editing. Intellimize uses ML for automatic optimization but requires more traffic. Both improve website conversion for target accounts.",
        "winner_intent": "N/A", "winner_ads": "N/A", "winner_ease": "Mutiny",
        "verdict": "Choose Mutiny if you want ABM-specific personalization with a no-code builder. Choose Intellimize if you have high traffic and want AI-driven conversion optimization.",
    },
    {
        "slug": "hubspot-vs-marketo",
        "tool_a": "hubspot", "tool_b": "marketo",
        "title": "HubSpot vs Marketo for ABM",
        "summary": "HubSpot is the all-in-one platform that added ABM features. Marketo is the enterprise marketing automation platform that ABM teams have used for years. HubSpot is easier, Marketo is deeper.",
        "winner_intent": "Marketo", "winner_ads": "HubSpot", "winner_ease": "HubSpot",
        "verdict": "Choose HubSpot if you want ABM within an all-in-one platform and value ease of use. Choose Marketo if you need enterprise-grade orchestration and already use Salesforce.",
    },
    {
        "slug": "bombora-vs-g2-intent",
        "tool_a": "bombora", "tool_b": "g2-intent",
        "title": "Bombora vs G2 Buyer Intent",
        "summary": "Bombora tracks content consumption across 5,000+ B2B sites for broad category intent. G2 captures high-intent signals from active software buyers. Different signal types, often used together.",
        "winner_intent": "Bombora (breadth), G2 (depth)", "winner_ads": "Bombora", "winner_ease": "G2",
        "verdict": "Use Bombora for broad category intent across the buying journey. Use G2 for high-intent signals from active buyers. Many teams use both for full-funnel coverage.",
    },
]

# ---------------------------------------------------------------------------
# Roundup definitions
# ---------------------------------------------------------------------------

ROUNDUPS = [
    {
        "slug": "best-abm-platforms",
        "title": "Best ABM Platforms for 2026",
        "description": "Ranked comparison of the top ABM platforms. We evaluate 6sense, Demandbase, Terminus, RollWorks, Triblio, and Madison Logic on features, pricing, and fit.",
        "tools": ["6sense", "demandbase", "terminus", "rollworks", "triblio", "madison-logic"],
        "intro": "ABM platforms are the foundation of any account-based marketing program. They combine account identification, intent data, advertising, and orchestration into a single platform. Here is how the top options compare in 2026.",
    },
    {
        "slug": "best-intent-data-providers",
        "title": "Best Intent Data Providers for 2026",
        "description": "Ranked comparison of B2B intent data providers. We evaluate Bombora, G2 Buyer Intent, TrustRadius, and ZoomInfo Intent on signal quality, coverage, and pricing.",
        "tools": ["bombora", "g2-intent", "trustradius-intent", "zoominfo-intent"],
        "intro": "Intent data tells you which accounts are actively researching your category. It is the fuel that makes ABM targeting work. Here are the best intent data providers for ABM teams in 2026.",
    },
    {
        "slug": "best-personalization-tools",
        "title": "Best Personalization Tools for ABM",
        "description": "Ranked comparison of website personalization tools for ABM. We evaluate Mutiny, Intellimize, PathFactory, and Folloze on ease of use, ABM features, and ROI.",
        "tools": ["mutiny", "intellimize", "pathfactory", "folloze"],
        "intro": "Personalization turns your website into a 1:1 experience for target accounts. Instead of showing the same page to everyone, these tools let you tailor headlines, CTAs, and content to specific accounts and segments.",
    },
    {
        "slug": "best-direct-mail-abm",
        "title": "Best Direct Mail Platforms for ABM",
        "description": "Ranked comparison of B2B gifting and direct mail platforms for ABM. We evaluate Sendoso, Reachdesk, PFL, and Alyce on marketplace, integrations, and pricing.",
        "tools": ["sendoso", "reachdesk", "pfl", "alyce"],
        "intro": "Direct mail cuts through digital noise. When every decision-maker gets 100+ emails per day, a well-timed physical gift gets attention. Here are the best platforms for ABM teams running direct mail programs.",
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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


def load_market_data(project_dir):
    path = os.path.join(project_dir, "data", "market_intelligence.json")
    with open(path, "r") as f:
        return json.load(f)


def get_mention_count(market_data, tool_name):
    """Get mention count from market_intelligence.json."""
    tools = market_data.get("tools", {})
    # Try exact match, then case-insensitive
    for key, count in tools.items():
        if key.lower() == tool_name.lower():
            return count
    return 0


def star_rating_html(value):
    """Render star rating as HTML."""
    full = int(value)
    half = 1 if value - full >= 0.3 else 0
    empty = 5 - full - half
    stars = '<span style="color: var(--abm-accent);">' + ("&#9733;" * full)
    if half:
        stars += "&#9733;"  # simplified, just use full star for .3+
    stars += ('&#9734;' * empty) + '</span>'
    return f'{stars} <strong>{value}/5</strong>'


def tool_header_html(tool, mention_count, crumbs):
    bc = breadcrumb_html(crumbs)
    mentions_text = f' | <strong>{mention_count}</strong> mentions in ABM job postings' if mention_count > 0 else ''
    return f'''<section class="salary-header">
    <div class="salary-header-inner">
        {bc}
        <div class="salary-eyebrow">{tool["category_label"]}</div>
        <h1>{tool["name"]} Review</h1>
        <p>{tool["tagline"]}</p>
        <p style="font-size: var(--abm-text-sm); margin-top: var(--abm-space-2);">{star_rating_html(tool["rating"]["value"])} ({tool["rating"]["count"]} reviews){mentions_text}</p>
    </div>
</section>'''


# ---------------------------------------------------------------------------
# Page: Tools Index
# ---------------------------------------------------------------------------

def build_tools_index(market_data):
    title = "ABM Tool Reviews"
    description = pad_description(
        "Honest reviews of ABM tools. 6sense, Demandbase, Terminus, Sendoso, Mutiny, and more. No pay-to-play rankings."
    )
    crumbs = [("Home", "/"), ("Tools", None)]
    bc_schema = get_breadcrumb_schema([("Home", "/"), ("Tools", "/tools/")])

    header = f'''<section class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <div class="salary-eyebrow">Tool Reviews</div>
        <h1>ABM Tool Reviews</h1>
        <p>Vendor-neutral reviews of every major ABM tool. Real practitioner perspectives, no pay-to-play rankings.</p>
    </div>
</section>'''

    # Category cards
    cat_cards = ""
    for cat_key, cat in CATEGORIES.items():
        tool_names = [TOOL_DATABASE[t]["name"] for t in cat["tools"][:4]]
        tools_text = ", ".join(tool_names)
        cat_cards += f'''<a href="/tools/category/{cat["slug"]}/" class="preview-card">
    <h3>{cat["name"]}</h3>
    <p>{tools_text}</p>
    <span class="preview-link">View all &rarr;</span>
</a>\n'''

    # All tools list
    all_tools_rows = []
    for key, tool in sorted(TOOL_DATABASE.items(), key=lambda x: x[1]["rating"]["value"], reverse=True):
        mc = get_mention_count(market_data, tool["name"].split(" ")[0])
        all_tools_rows.append([
            f'<a href="/tools/{tool["slug"]}/"><strong>{tool["name"]}</strong></a>',
            tool["category_label"],
            f'{tool["rating"]["value"]}/5',
            str(mc) if mc > 0 else "-",
        ])

    from templates import newsletter_cta_html as ncta
    body = f'''{header}
<div class="salary-content">
    <h2>Browse by Category</h2>
    <div class="preview-grid" style="grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));">
        {cat_cards}
    </div>

    <h2>All Tools ({len(TOOL_DATABASE)})</h2>
    <table class="data-table">
        <thead><tr><th>Tool</th><th>Category</th><th>Rating</th><th>Job Mentions</th></tr></thead>
        <tbody>{"".join(f"<tr>{''.join(f'<td>{c}</td>' for c in row)}</tr>" for row in all_tools_rows)}</tbody>
    </table>

    <h2>Comparisons</h2>
    <div class="related-links-grid">
        {"".join(f'<a href="/tools/compare/{c["slug"]}/" class="related-link-card">{c["title"]}</a>' for c in TOOL_COMPARISONS)}
    </div>

    <h2>Roundups</h2>
    <div class="related-links-grid">
        {"".join(f'<a href="/tools/{r["slug"]}/" class="related-link-card">{r["title"]}</a>' for r in ROUNDUPS)}
    </div>

    {ncta("Get weekly tool intel.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/tools/",
        body_content=body, active_path="/tools/", extra_head=bc_schema,
    )
    write_page("tools/index.html", page)
    print(f"  Built: tools/index.html")


# ---------------------------------------------------------------------------
# Page: Individual Tool Reviews
# ---------------------------------------------------------------------------

def build_tool_review(tool_key, tool, market_data, all_comparisons):
    mc = get_mention_count(market_data, tool["name"].split(" ")[0])
    title = f'{tool["name"]} Review for ABM Teams'
    description = pad_description(
        f'{tool["name"]} review. {tool["tagline"]}. Strengths, weaknesses, pricing, and alternatives for ABM professionals.'
    )
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (tool["name"], None)]
    bc_schema = get_breadcrumb_schema([
        ("Home", "/"), ("Tools", "/tools/"), (tool["name"], f'/tools/{tool["slug"]}/')
    ])

    schema = get_software_application_schema({
        "name": tool["name"],
        "description": tool["description"],
        "category": "BusinessApplication",
        "url": tool["url"],
        "price_range": tool["pricing"],
        "rating": tool["rating"],
    })

    header = tool_header_html(tool, mc, crumbs)

    strengths = "\n".join(f"<li>{s}</li>" for s in tool["strengths"])
    weaknesses = "\n".join(f"<li>{w}</li>" for w in tool["weaknesses"])
    alternatives_html = "\n".join(
        f'<a href="/tools/{TOOL_DATABASE[a.lower().replace(" ", "-")]["slug"]}/" class="related-link-card">{a}</a>'
        for a in tool["alternatives"]
        if a.lower().replace(" ", "-") in TOOL_DATABASE
    )

    # Related comparisons
    related_comps = [c for c in all_comparisons if tool_key in [c["tool_a"], c["tool_b"]]]
    comp_links = ""
    if related_comps:
        comp_links = '<h2>Comparisons</h2><div class="related-links-grid">'
        for c in related_comps:
            comp_links += f'<a href="/tools/compare/{c["slug"]}/" class="related-link-card">{c["title"]}</a>\n'
        comp_links += '</div>'

    faq_pairs = [
        (f'How much does {tool["name"]} cost?',
         tool["pricing"]),
        (f'What are the best alternatives to {tool["name"]}?',
         f'The top alternatives are {", ".join(tool["alternatives"])}. Each has different strengths depending on your team size, budget, and ABM maturity.'),
        (f'Is {tool["name"]} good for ABM?',
         f'{tool["best_for"]}'),
    ]

    body = f'''{header}
<div class="salary-content">
    <h2>Overview</h2>
    <p>{tool["description"]}</p>

    <div class="stat-grid" style="margin: var(--abm-space-8) 0;">
        <div class="stat-block">
            <span class="stat-value" style="color: var(--abm-accent);">{tool["rating"]["value"]}/5</span>
            <span class="stat-label">Rating</span>
        </div>
        <div class="stat-block">
            <span class="stat-value" style="color: var(--abm-accent);">{tool["founded"]}</span>
            <span class="stat-label">Founded</span>
        </div>
        <div class="stat-block">
            <span class="stat-value" style="color: var(--abm-accent);">{mc if mc > 0 else "N/A"}</span>
            <span class="stat-label">Job Mentions</span>
        </div>
    </div>

    <h2>Best For</h2>
    <p>{tool["best_for"]}</p>

    <h2>Pricing</h2>
    <p>{tool["pricing"]}</p>

    <h2>Strengths</h2>
    <ul>{strengths}</ul>

    <h2>Weaknesses</h2>
    <ul>{weaknesses}</ul>

    <h2>Alternatives</h2>
    <div class="related-links-grid">{alternatives_html}</div>

    {comp_links}

    {faq_html(faq_pairs)}
    {newsletter_cta_html("Get weekly tool reviews.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path=f'/tools/{tool["slug"]}/',
        body_content=body, active_path="/tools/",
        extra_head=bc_schema + schema + get_faq_schema(faq_pairs),
    )
    write_page(f'tools/{tool["slug"]}/index.html', page)


# ---------------------------------------------------------------------------
# Page: Category Pages
# ---------------------------------------------------------------------------

def build_category_page(cat_key, cat, market_data):
    title = f'Best {cat["name"]} for ABM'
    description = pad_description(
        f'{cat["name"]} for ABM teams. Reviews and comparisons of {", ".join(TOOL_DATABASE[t]["name"] for t in cat["tools"][:3])}, and more.'
    )
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (cat["name"], None)]
    bc_schema = get_breadcrumb_schema([
        ("Home", "/"), ("Tools", "/tools/"),
        (cat["name"], f'/tools/category/{cat["slug"]}/')
    ])

    header = f'''<section class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <div class="salary-eyebrow">Tool Category</div>
        <h1>{cat["name"]}</h1>
        <p>{cat["description"]}</p>
    </div>
</section>'''

    # Tool cards
    tool_cards = ""
    for tool_key in cat["tools"]:
        tool = TOOL_DATABASE[tool_key]
        mc = get_mention_count(market_data, tool["name"].split(" ")[0])
        mc_text = f" | {mc} job mentions" if mc > 0 else ""
        tool_cards += f'''<a href="/tools/{tool["slug"]}/" class="preview-card" style="min-height: auto;">
    <h3>{tool["name"]}</h3>
    <p style="font-size: var(--abm-text-sm); color: var(--abm-text-secondary);">{star_rating_html(tool["rating"]["value"])}{mc_text}</p>
    <p>{tool["tagline"]}</p>
    <p style="font-size: var(--abm-text-sm);"><strong>Best for:</strong> {tool["best_for"]}</p>
    <p style="font-size: var(--abm-text-sm);"><strong>Pricing:</strong> {tool["pricing"]}</p>
    <span class="preview-link">Read full review &rarr;</span>
</a>\n'''

    # Comparison table
    rows = []
    for tool_key in cat["tools"]:
        tool = TOOL_DATABASE[tool_key]
        rows.append([
            f'<a href="/tools/{tool["slug"]}/"><strong>{tool["name"]}</strong></a>',
            f'{tool["rating"]["value"]}/5',
            tool["pricing"].split(",")[0],
            tool["best_for"][:80] + "...",
        ])

    table = f'''<table class="data-table">
    <thead><tr><th>Tool</th><th>Rating</th><th>Starting Price</th><th>Best For</th></tr></thead>
    <tbody>{"".join(f"<tr>{''.join(f'<td>{c}</td>' for c in row)}</tr>" for row in rows)}</tbody>
</table>'''

    body = f'''{header}
<div class="salary-content">
    <div class="preview-grid" style="grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));">
        {tool_cards}
    </div>

    <h2>Quick Comparison</h2>
    {table}

    {newsletter_cta_html(f"Get weekly {cat['name'].lower()} updates.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path=f'/tools/category/{cat["slug"]}/',
        body_content=body, active_path="/tools/", extra_head=bc_schema,
    )
    write_page(f'tools/category/{cat["slug"]}/index.html', page)
    print(f"  Built: tools/category/{cat['slug']}/index.html")


# ---------------------------------------------------------------------------
# Page: Tool Comparisons
# ---------------------------------------------------------------------------

def build_tool_comparison(comp, market_data):
    a = TOOL_DATABASE[comp["tool_a"]]
    b = TOOL_DATABASE[comp["tool_b"]]
    mc_a = get_mention_count(market_data, a["name"].split(" ")[0])
    mc_b = get_mention_count(market_data, b["name"].split(" ")[0])

    title = comp["title"]
    description = pad_description(
        f'{a["name"]} vs {b["name"]} for ABM. Features, pricing, ratings, and our verdict on which is better for your team.'
    )
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (comp["title"], None)]
    bc_schema = get_breadcrumb_schema([
        ("Home", "/"), ("Tools", "/tools/"),
        (comp["title"], f'/tools/compare/{comp["slug"]}/')
    ])

    header = f'''<section class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <div class="salary-eyebrow">Tool Comparison</div>
        <h1>{comp["title"]}</h1>
        <p>{comp["summary"]}</p>
    </div>
</section>'''

    table = f'''<table class="data-table">
    <thead><tr><th></th><th>{a["name"]}</th><th>{b["name"]}</th></tr></thead>
    <tbody>
        <tr><td><strong>Rating</strong></td><td>{a["rating"]["value"]}/5 ({a["rating"]["count"]} reviews)</td><td>{b["rating"]["value"]}/5 ({b["rating"]["count"]} reviews)</td></tr>
        <tr><td><strong>Founded</strong></td><td>{a["founded"]}</td><td>{b["founded"]}</td></tr>
        <tr><td><strong>HQ</strong></td><td>{a["hq"]}</td><td>{b["hq"]}</td></tr>
        <tr><td><strong>Pricing</strong></td><td>{a["pricing"]}</td><td>{b["pricing"]}</td></tr>
        <tr><td><strong>Best For</strong></td><td>{a["best_for"]}</td><td>{b["best_for"]}</td></tr>
        <tr><td><strong>Job Mentions</strong></td><td>{mc_a if mc_a > 0 else "N/A"}</td><td>{mc_b if mc_b > 0 else "N/A"}</td></tr>
    </tbody>
</table>'''

    a_strengths = "\n".join(f"<li>{s}</li>" for s in a["strengths"][:4])
    b_strengths = "\n".join(f"<li>{s}</li>" for s in b["strengths"][:4])
    a_weaknesses = "\n".join(f"<li>{w}</li>" for w in a["weaknesses"][:3])
    b_weaknesses = "\n".join(f"<li>{w}</li>" for w in b["weaknesses"][:3])

    faq_pairs = [
        (f'Is {a["name"]} or {b["name"]} better for ABM?',
         comp["verdict"]),
        (f'Which is more affordable, {a["name"]} or {b["name"]}?',
         f'{a["name"]}: {a["pricing"]}. {b["name"]}: {b["pricing"]}.'),
    ]

    body = f'''{header}
<div class="salary-content">
    <h2>Side-by-Side Comparison</h2>
    {table}

    <h2>{a["name"]} Strengths</h2>
    <ul>{a_strengths}</ul>

    <h2>{b["name"]} Strengths</h2>
    <ul>{b_strengths}</ul>

    <h2>{a["name"]} Weaknesses</h2>
    <ul>{a_weaknesses}</ul>

    <h2>{b["name"]} Weaknesses</h2>
    <ul>{b_weaknesses}</ul>

    <h2>Our Verdict</h2>
    <p>{comp["verdict"]}</p>

    <div class="related-links-grid" style="margin-top: var(--abm-space-8);">
        <a href="/tools/{a["slug"]}/" class="related-link-card">Read {a["name"]} Review</a>
        <a href="/tools/{b["slug"]}/" class="related-link-card">Read {b["name"]} Review</a>
    </div>

    {faq_html(faq_pairs)}
    {newsletter_cta_html("Get weekly tool comparisons.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path=f'/tools/compare/{comp["slug"]}/',
        body_content=body, active_path="/tools/",
        extra_head=bc_schema + get_faq_schema(faq_pairs),
    )
    write_page(f'tools/compare/{comp["slug"]}/index.html', page)
    print(f"  Built: tools/compare/{comp['slug']}/index.html")


# ---------------------------------------------------------------------------
# Page: Roundups
# ---------------------------------------------------------------------------

def build_roundup(roundup, market_data):
    title = roundup["title"]
    description = pad_description(roundup["description"])
    slug = roundup["slug"]
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (roundup["title"].replace("Best ", ""), None)]
    bc_schema = get_breadcrumb_schema([
        ("Home", "/"), ("Tools", "/tools/"),
        (roundup["title"], f'/tools/{slug}/')
    ])

    header = f'''<section class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <div class="salary-eyebrow">Roundup</div>
        <h1>{roundup["title"]}</h1>
        <p>{roundup["intro"]}</p>
    </div>
</section>'''

    # Tool entries
    entries = ""
    for i, tool_key in enumerate(roundup["tools"], 1):
        tool = TOOL_DATABASE[tool_key]
        mc = get_mention_count(market_data, tool["name"].split(" ")[0])
        mc_text = f" | {mc} job mentions" if mc > 0 else ""
        strengths_top = ", ".join(tool["strengths"][:3])
        weaknesses_top = ", ".join(tool["weaknesses"][:2])
        entries += f'''
    <div style="margin-bottom: var(--abm-space-8); padding-bottom: var(--abm-space-8); border-bottom: 1px solid var(--abm-border-subtle);">
        <h2>#{i} {tool["name"]}</h2>
        <p style="font-size: var(--abm-text-sm);">{star_rating_html(tool["rating"]["value"])} ({tool["rating"]["count"]} reviews){mc_text}</p>
        <p>{tool["tagline"]}</p>
        <p><strong>Pricing:</strong> {tool["pricing"]}</p>
        <p><strong>Best for:</strong> {tool["best_for"]}</p>
        <p><strong>Top strengths:</strong> {strengths_top}</p>
        <p><strong>Watch out for:</strong> {weaknesses_top}</p>
        <a href="/tools/{tool["slug"]}/" class="btn btn--ghost" style="margin-top: var(--abm-space-3);">Read Full Review &rarr;</a>
    </div>
'''

    # Quick comparison table
    rows = []
    for tool_key in roundup["tools"]:
        tool = TOOL_DATABASE[tool_key]
        rows.append([
            f'<a href="/tools/{tool["slug"]}/"><strong>{tool["name"]}</strong></a>',
            f'{tool["rating"]["value"]}/5',
            tool["pricing"].split(",")[0],
        ])

    table = f'''<table class="data-table">
    <thead><tr><th>Tool</th><th>Rating</th><th>Starting Price</th></tr></thead>
    <tbody>{"".join(f"<tr>{''.join(f'<td>{c}</td>' for c in row)}</tr>" for row in rows)}</tbody>
</table>'''

    body = f'''{header}
<div class="salary-content">
    <h2>Quick Comparison</h2>
    {table}

    {entries}

    {newsletter_cta_html("Get weekly tool roundups.")}
</div>'''

    page = get_page_wrapper(
        title=title, description=description,
        canonical_path=f'/tools/{slug}/',
        body_content=body, active_path="/tools/", extra_head=bc_schema,
    )
    write_page(f'tools/{slug}/index.html', page)
    print(f"  Built: tools/{slug}/index.html")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def build_all_tool_pages(project_dir):
    """Called from build.py to generate all tool pages."""
    market_data = load_market_data(project_dir)
    print("\n  Building tool pages...")

    build_tools_index(market_data)

    # Individual tool reviews
    for tool_key, tool in TOOL_DATABASE.items():
        build_tool_review(tool_key, tool, market_data, TOOL_COMPARISONS)
    print(f"  Built: {len(TOOL_DATABASE)} tool review pages")

    # Category pages
    for cat_key, cat in CATEGORIES.items():
        build_category_page(cat_key, cat, market_data)

    # Comparison pages
    for comp in TOOL_COMPARISONS:
        build_tool_comparison(comp, market_data)

    # Roundup pages
    for roundup in ROUNDUPS:
        build_roundup(roundup, market_data)
