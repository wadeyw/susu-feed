# Kolect.ai Deep Dive: The 100M Creator Database -- Mechanics Analysis

Date: 2026-06-11

## The Core Question

How does a 2025-founded, unfunded, likely <10-person startup claim a 100M+ creator database? Is it possible? Is it real? How?

## Short Answer

**It is almost certainly a combination of: (1) open network scraping, (2) on-demand enrichment (not pre-stored), and (3) self-registration.** The database is likely NOT 100M fully-enriched profiles stored in their own servers. It is more likely a search index of public profiles with on-demand API calls for enrichment when a brand queries.

---

## 1. The Open Network Model (Used by Modash)

This is the industry-standard approach. Modash publicly explains their process:

> "Data is collected about every public creator profile **several times a month** from places like about sections, captions & descriptions of posts, images, videos, and other public info."
> -- Modash "Our Data" page

Key details:
- They collect **basic profile data** (bio, follower count, post URLs) from public sources
- They do NOT pre-enrich every profile with full demographics, engagement rates, fake follower analysis
- When you search, the basic index is fast (pre-indexed)
- When you view a profile, they run **on-demand enrichment** (ML models analyze the profile's actual posts, audience data, etc.)
- They call this an "Open Network Creator Database"

**This is the model Kolect almost certainly uses.** They call themselves "100M+ creators" but that's an index of public profiles -- the rich data (engagement rate, audience demographics, fake follower %) is computed on-demand.

### Cost Reality

Scraping basic profile data is cheap. Full enrichment is expensive.

From a Modash engineer quote: "Platforms will keep restricting access, AI will make discovery more valuable, and the **maintenance cost of scraping will only compound**."

The real cost is not in the initial scrape but in:
1. Keeping the data fresh (profiles change constantly)
2. Running ML models for enrichment (fake followers, demographics, engagement quality)
3. Maintaining the anti-scraping arms race

---

## 2. On-Demand Enrichment (The Key Insight)

Here's the critical architectural insight: **Kolect likely doesn't store 100M enriched profiles. They store 100M basic profile records and enrich on-demand.**

### Two-Tier Architecture

```
Tier 1: Index (stored)
  - Profile URL, username, bio, follower count, post count
  - Updated every 1-4 weeks
  - Cost: ~$0.01-0.03 per profile per refresh
  - Storage: ~100MB for 100M profiles

Tier 2: Enrichment (on-demand)
  - Engagement rate, audience demographics, fake follower %
  - Run ML models when brand queries a specific creator
  - Cost: ~$0.50-2.00 per enrichment call
  - Cached for days/weeks if profile is popular
```

This means:
- 100M basic profiles = cheap storage, cheap to maintain
- Only the profiles brands actually look at get enriched
- The "100M" claim is technically accurate (they have the index)
- But only a fraction have real-time enriched data

### Evidence from Kolect's Own UI

Looking at Kolect's creator cards in the UI:
- They show: follower count, engagement rate, view duration, content category, match score, price
- Match score and engagement rate require enrichment
- If they stored ALL of this for 100M profiles, the storage and compute cost would be enormous
- More likely: they enrich when a brand views a creator's profile

---

## 3. Cost Analysis: How Much Does This Actually Cost?

### Scenario A: Build In-House (from Dev.to TCO analysis)

| Cost Item | Annual | 3-Year TCO |
|-----------|--------|-----------|
| Engineers (5 FTE) | $480,000 | $1,440,000 |
| DevOps | $110,000 | $330,000 |
| Infrastructure (servers, proxy IPs) | $54,000 | $162,000 |
| Anti-scraping updates (18/year) | $35,000 | $105,000 |
| Technical debt/refactoring | $80,000 | $240,000 |
| Recruitment (15-20% turnover) | $60,000 | $180,000 |
| **Total** | **$819,000** | **$1,987,000** |

### Scenario B: Buy from API Providers

| Cost Item | Annual | 3-Year TCO |
|-----------|--------|-----------|
| API service (500K pages/month) | $8,172 | $24,516 |
| Data engineer (integration) | $90,000 | $270,000 |
| **Total** | **$98,172** | **$294,516** |

**Savings: 83% by buying vs building.**

### Scenario C: On-Demand Hybrid (Most Likely for Kolect)

| Component | Annual Cost |
|-----------|------------|
| Basic scraping (100M profiles, monthly refresh) | $50,000-200,000 |
| API enrichment (paid per call) | $20,000-100,000 |
| Engineers (2-3 to maintain scrapers) | $300,000-400,000 |
| **Total** | **$370,000-700,000** |

Even this lean approach requires $370K-700K/year. For an unfunded 2025 startup, this is a significant portion of any revenue.

### Real-World Pricing Data

From Reddit and industry sources:
- Some agencies charge **$60,000 for enrichment of 100,000 profiles** (with 5+ data points)
- Deep scrape via Apify: **~$2 per batch** (but limited data points)
- Official API data from Modash: enterprise pricing (not public, but likely $5K-50K+/month)
- Hir Infotech: custom scraping services, priced per project

---

## 4. Data Freshness and Maintenance

### How Often Data Gets Updated

From Flinque community and industry sources:
- **High-activity creators**: updated weekly or bi-weekly
- **Campaign-adjacent creators**: updated monthly
- **Long-tail creators**: updated quarterly or only when searched

This means Kolect's "100M creators" is a **moving target**:
- At any given moment, only a fraction have fresh data
- The rest are stale snapshots
- When a brand searches and finds a match, Kolect probably does a live enrichment call

### Platform Countermeasures

The anti-scraping arms race is relentless. From the Dev.to analysis:

| Month | Anti-Scraping Updates | Engineer-Days Lost |
|-------|----------------------|-------------------|
| Jan | 2 | 6 |
| Feb | 1 | 3 |
| Mar | 3 | 9 |
| Apr | 2 | 7 |
| **Total** | **18/year** | **54 days** |

This is for a team with dedicated scraping engineers. For a <10-person startup like Kolect, this is a massive ongoing drain.

### Platform Legal Actions

- **Meta v. Bright Data (2024)**: Meta pursued legal action against scrapers of its properties
- **hiQ Labs v. LinkedIn (2022)**: Established that scraping publicly accessible data does NOT violate CFAA
- **LinkedIn API**: approval rates under 5%, wait times 3-6 months
- **TikTok API**: constantly tightening access
- **Instagram**: actively detects and blocks automated access

---

## 5. Creator Self-Registration (The Growth Loop)

The other half of Kolect's 100M claim is likely **creator self-registration**. Here's how it works:

1. Kolect publishes a "join our creator network" page
2. Creators sign up to receive brand campaigns
3. When they sign up, Kolect pulls their public social profile data
4. The creator now has a profile in Kolect's database
5. Kolect can show this creator to brands

This is how Aspire, Grin, and most marketplace-style platforms started. The difference is:
- **Marketplace platforms** (Aspire, Grin): creators MUST sign up to be found
- **Open network platforms** (Modash, Kolect): they scrape public profiles regardless

Kolect likely uses **both**:
- Scraped public profiles for the "100M" number
- Self-registered creators for the "active marketplace" part

---

## 6. Team Discovery: Who Is Actually Running This?

From LinkedIn and public sources:

| Person | Role | Connection |
|--------|------|-----------|
| **Steven Huang** | Founder & CEO at Panoverse & Kolect.AI | Singapore-based |
| **Lin Shao** | Northwestern University, M.S. | Ex-Panoverse Inc. |
| **Yifan Lei** | Head of Innovative Marketing @ K2 LAB | Ex-Alibaba, Kolect AI, Columbia University |
| **Yining Zou** | Co-Founder (May 2024) | York Region, Canada |

**Key insights:**
- Co-founder Yining Zou started in May 2024 (before the 2025 founding date)
- CEO Steven Huang is based in Singapore
- Marketing lead Yifan Lei has Alibaba + Columbia background
- The team spans Singapore, Boston (Brighton MA), and Canada
- Northwestern University connection (Lin Shao) suggests US education network
- Strong Chinese diaspora network: Alibaba, Columbia, Singapore, Canada

This team structure supports the hypothesis that they started with Chinese D2C brands (Baseus, Taobao case studies) and expanded to Western markets.

---

## 7. The Verdict: What "100M Creators" Actually Means

### Most Likely Reality

| Metric | What They Claim | What It Probably Is |
|--------|---------------|-------------------|
| Database size | 100M+ creators | 100M+ basic profile records (index only) |
| Enriched profiles | Implied: all of them | Maybe 10-20M have basic enrichment; rest computed on-demand |
| Active creators | Implied: all of them | Likely 50K-200K have self-registered or been recently enriched |
| Fresh data | Implied: real-time | Updated weekly/monthly for active profiles; quarterly for long-tail |

### How They Probably Built It

1. **Phase 1 (mid-2024)**: Built basic scrapers for Instagram/TikTok/YouTube public profiles. Collected ~10M profiles.
2. **Phase 2 (late 2024)**: Launched creator self-registration. Creators sign up, Kolect enriches their profile.
3. **Phase 3 (early 2025)**: Scaled scraping to 100M+ profiles. On-demand enrichment for queries.
4. **Phase 4 (2025)**: Added AI matching, performance tracking, and campaign management layer on top.

### What This Means for Competition

**The "100M" number is marketing, not a moat.** Modash has 350M, GRIN has 300M, Influencity has 200M. The number itself is not special. What matters is:
- How many are **actively working with brands** (Kolect likely <1%)
- How fresh the data is
- How accurate the AI matching is
- Whether brands get real results (not just inflated numbers)

For a new entrant, the barrier is NOT building a 100M database. The barrier is:
1. Getting brands to trust your results
2. Getting creators to actually work through your platform (not just have their data in your DB)
3. Maintaining the scraping infrastructure against increasingly hostile platforms

---

## 8. Recommendations

### If You Want to Build a Similar Database

**Don't build from scratch.** The data shows:
- In-house scraping TCO: $2M over 3 years
- API + integration TCO: $330K over 3 years (83% savings)
- For a startup, **buy the base data, build the value-add on top**

**Recommended approach:**
1. Use an API provider for base data (EnsembleData, Modash API, or similar)
2. Build your own enrichment models for the data points that matter to your niche
3. Add creator self-registration for active marketplace dynamics
4. Focus engineering time on your unique value proposition, not scraping infrastructure

### If You Want to Compete Against Kolect

**Their weakest points:**
1. 100M is not special (modest by industry standards)
2. Unfunded 2025 startup -- no track record
3. Anonymous team -- hard for enterprise brands to trust
4. Performance-based pricing with no recurring revenue
5. Chinese diaspora focus -- may limit Western enterprise adoption
6. No independent verification of ROI claims

**Your advantages:**
1. Your experience at Creatorial gives you domain expertise
2. You can build a more transparent, verifiable platform
3. You can focus on niches Kolect ignores (B2B, enterprise)
4. You have access to better data sources if you build properly from day 1

---

## Data Sources

- Modash "Our Data" page (modash.io/data) -- open network methodology
- Modash Discovery API page (modash.io/influencer-marketing-api/discovery) -- API capabilities
- Dev.to "Hidden Cost of Building Your Own Web Scraping Team" -- TCO analysis with real numbers
- Hir Infotech "Creator Data API vs Custom Influencer Scraping" -- build vs buy comparison
- Zyte "Should AI Companies Build Their Own Web Scraping Pipelines" -- infrastructure maintenance analysis
- Hir Infotech "Influencer Data Scraping Company" -- legal/compliance context
- Bright Data "Best Social Media Data Providers" -- provider landscape
- Influencer Hero "Best Influencer Marketing API Providers" -- API provider landscape
- Reddit r/influencermarketing -- community cost discussions
- LinkedIn: Steven Huang (CEO), Yifan Lei (Marketing), Lin Shao, Yining Zou (Co-Founder)
- Kolect.ai: Privacy Policy, Terms of Service, About, How It Works, Pricing, Case Studies
- Tracxn, PitchBook -- company profile data
- Influencer Marketing Hub -- industry statistics
