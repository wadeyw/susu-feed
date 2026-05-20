# AppLovin Axon 2.0 analysis for campaign ROI systems

Date: 2026-05-20

## Executive summary

AppLovin's Axon 2.0 is best understood not as a single magical model, but as a large-scale prediction-and-optimization system for ad delivery. Public information suggests four things matter most:

1. It is trained on enormous proprietary outcome data.
2. It sits directly inside a real-time auction / delivery loop.
3. It optimizes for measurable advertiser outcomes, not just broad relevance.
4. It improves because better performance attracts more spend, more inventory, and more feedback data, which further improves the system.

For your use case, the most transferable lesson is not "build an Axon." It is: build a closed-loop prediction system around your own transaction data, where each recommendation is scored against expected business outcome and every campaign result flows back into retraining.

## Important caveat

Axon 2.0 is proprietary. Public sources reveal business behavior and some high-level design patterns, but not the detailed model architecture, feature definitions, training pipeline, or serving code. So this report separates:

- Verified public facts
- Reasonable inferences
- Practical takeaways for your own system

## What public sources say

### 1) What Axon is

Verified public facts:

- AppLovin describes Axon Ads Manager as the cornerstone of its advertising solutions.
- In its 2025 10-K, AppLovin says Axon Ads Manager is powered by its Axon AI advertising recommendation engine and "matches advertiser demand with publisher supply through auctions at vast scale and at microsecond-level speeds."
- The same filing says more distribution gives AppLovin better insights for Axon AI, which then enhances the efficiency and effectiveness of Axon Ads Manager.

Interpretation:

This strongly suggests Axon is a production prediction engine embedded in ad auctions, not an offline reporting model.

### 2) What Axon 2.0 changed

Verified public facts:

- AdExchanger reported that Axon 2.0 was released in 2023 as an updated version of AppLovin's AI-powered ad tech software.
- AdExchanger also reported that Axon uses predictive machine learning to target app-install ads to users most likely to download those apps.
- In AppLovin's Q2 2023 shareholder letter, the company said outperformance was driven primarily by the successful rollout of "its latest AI-based advertising engine, AXON 2.0."
- In AdExchanger's coverage of AppLovin's Q2 2023 earnings call, CEO Adam Foroughi said Axon 2.0 was "dramatically better than the technologies that we were using" and that its impact on campaign performance was "immediate."
- In AdExchanger's coverage of AppLovin's Q4 2023 earnings call, Foroughi said, "there's a whole bunch of predictions along the way, and Axon 2.0 makes them better than the prior version."
- In AppLovin's 4Q23 shareholder letter, the company said the Axon engine "continues to learn and scale" and that advertisers spent more due to improved performance from its AI-enhanced advertising engine.

Interpretation:

The key phrase is "a whole bunch of predictions along the way." That suggests Axon 2.0 is likely an ensemble / multi-stage optimization system rather than one monolithic predictor. In other words, it probably improves multiple decisions in the serving path, such as:

- whether this user is a good target
- whether this ad / creative is a good fit
- expected value of showing this ad now
- bid level / auction aggressiveness
- pacing / budget allocation
- maybe post-click or downstream quality estimation

Public sources do not confirm the exact components, but the design pattern is clear: many small predictive decisions stacked into one real-time optimizer.

### 3) Why Axon 2.0 appears better than Axon 1.0

Verified public facts:

- AppLovin has publicly said Axon 2.0 improved performance enough to drive software-platform revenue acceleration.
- Foroughi said it was built to support more scale and be more efficient and effective.
- AppLovin's 4Q23 shareholder letter said AppDiscovery growth was driven by continued Axon performance as the engine learned and scaled.

Reasonable inference:

Axon 2.0 seems better than 1.0 not because of one algorithmic trick, but because it likely improved multiple layers together:

1. Better prediction quality
   - More accurate estimates of downstream user behavior.

2. Better use of scale
   - Better handling of more auction volume, more advertisers, more inventory, and more feedback.

3. Better optimization target
   - Closer alignment to advertiser economics, especially return on ad spend.

4. Better feedback loop
   - Improved campaign performance causes advertisers to spend more, which creates denser auctions and more training data.

5. Better system-level efficiency
   - Faster and more effective decisions at serving time.

In short: Axon 2.0 seems like a system upgrade, not just a model refresh.

### 4) How AppLovin thinks about the flywheel

Verified public facts:

- AppLovin's filings say that as more advertisers use its advertising solutions, it gains access to more data regarding users and user engagement.
- Its filings also say that as distribution grows, Axon gets better insights, which then further enhances efficiency and effectiveness.
- AppLovin's 4Q23 shareholder letter says improved performance caused advertisers to spend more.

Interpretation:

This implies a strong data flywheel:

better predictions -> better advertiser results -> more advertiser spend -> more auctions / impressions / outcomes -> more training data -> better predictions

That flywheel is probably the real moat, more than any single ML architecture choice.

### 5) How Axon is evolving beyond mobile gaming

Verified public facts:

- AdExchanger reported Axon was originally used to target app-install ads.
- In AppLovin's 2024 shareholder letter, the company said early adopters in gaming and direct-to-consumer commerce had already seen the impact of its technology.
- The same letter says AppLovin plans to broaden advertiser reach, personalize ad experiences with AI-generated creative variations, launch a self-service dashboard powered by AI agents, and explore applying its targeting technology to connected TV.
- In AppLovin's 2025 10-K, the company says one of its long-term objectives is to provide critical tools across multiple verticals, including web-based e-commerce and social media, and that early customers in these markets had experienced positive results.

Interpretation:

This is important. AppLovin is not only scaling model size; it is expanding the same prediction-and-optimization system into adjacent environments where the core problem is similar:

- lots of candidates
- large traffic volume
- measurable outcomes
- rapid feedback
- strong economic objective

That is exactly the pattern relevant to your campaign ROI system.

## Inferred design of Axon 2.0

Again, this section is inference, not public confirmation.

The most plausible design is something like this:

### A. Multi-stage prediction system

Not one score, but many scores:

- probability of click
- probability of install / conversion
- expected value after install / post-conversion quality
- expected revenue / ROAS
- bid optimization or auction win value
- creative-user compatibility
- maybe fraud / low-quality suppression

### B. Real-time serving loop

For each ad opportunity:

1. gather context
   - user, app, placement, device, time, geo, historical behaviors, campaign constraints
2. score candidates very fast
3. estimate business value
4. decide bid / rank / delivery
5. observe actual outcomes
6. feed outcomes back into training data

### C. Data flywheel as architecture, not just a side effect

A major reason it compounds is likely that the system was designed so every auction and downstream outcome becomes future training data.

### D. Outcome-first optimization

AppLovin's public messaging consistently focuses on profitable customer acquisition and measurable advertiser performance. That suggests the optimization target is not just surface engagement but some weighted business-value proxy.

### E. System co-design, not model-only design

Axon 2.0 likely improved because the model, auction logic, creative logic, feedback logging, and serving infrastructure were improved together. This matters because many teams over-focus on the model and underinvest in the loop around it.

## What you should borrow for your own system

You should not copy the ad-tech form factor literally. But you should borrow these principles.

### 1) Optimize for business outcome, not proxy vanity metrics

For your influencer recommendation system, do not rank mainly by semantic match, followers, or average views.

Rank by expected business value for this specific campaign, such as:

- expected conversions
- expected cost per conversion
- expected ROI / ROAS proxy
- expected probability of campaign success

Semantic matching should help retrieval and features, not be the final decision rule.

### 2) Use many small predictions, not one giant magic score

This is probably the most important Axon lesson.

For your case, instead of one opaque "best influencer" model, predict several things:

- expected reach / views
- expected engagement
- expected clicks
- expected conversions
- expected cost
- expected ROI
- uncertainty / confidence

Then combine them into a ranking policy.

That is easier to debug, easier to explain, and usually much safer.

### 3) Build the feedback loop first-class

Your real moat is not embeddings or LLM prompts. It is the closed loop between:

- recommendations shown
- influencers shortlisted
- influencers booked
- final price negotiated
- actual delivery metrics
- actual conversion / ROI outcomes
- retraining

Without this loop, the model never compounds.

### 4) Separate retrieval from ranking

This mirrors what sophisticated ad systems do.

Stage 1: candidate generation
- hard filters
- semantic retrieval
- lookalikes
- prior successful creators for similar campaigns

Stage 2: ranking
- supervised prediction models for outcomes
- business constraints
- budget fit
- uncertainty penalty

This is much more realistic than asking an LLM to choose directly from all influencers.

### 5) Treat scale as a product feature

Axon 2.0 seems better partly because scale improved the system. For you, scale means:

- more campaign-influencer rows logged cleanly
- more consistent feature definitions
- more downstream outcome capture
- faster retraining cadence
- denser comparison sets within each campaign

In recommendation systems, data plumbing is often more important than model cleverness.

## What not to copy from AppLovin

### 1) Do not start with a black box

AppLovin can afford black-box behavior because it has huge scale, dense feedback, and performance buyers.

You should start with transparent models and explicit business logic.

### 2) Do not optimize for bid-time microseconds before your labels are clean

Your bottleneck is unlikely to be serving latency. It is more likely to be:

- poor historical tables
- inconsistent conversion tracking
- selection bias
- weak labels
- small sample size per niche / country / campaign type

### 3) Do not jump straight to online self-learning

Axon's live flywheel is powerful, but you should first build:

- offline supervised models
- periodic retraining
- model-vs-baseline evaluation
- clear logging

Then later add exploration.

## Recommended system design for your campaign ROI platform

## Phase 0: instrumentation

Before serious ML, ensure each campaign-influencer opportunity can be logged as a row with:

- campaign_id
- client_id
- influencer_id
- recommendation timestamp
- recommended rank
- shortlisted / rejected / booked
- quoted price
- negotiated price
- deliverables
- expected campaign goal
- final views
- final engagement
- final clicks
- final conversions
- final attributed revenue if available
- computed ROI / ROAS / CPA metrics

If this table is weak, nothing downstream will be reliable.

## Phase 1: retrieval + rules baseline

Build a baseline with:

- hard filters
- semantic match
- audience / geo / category fit
- price-band fit
- recent performance stability
- simple price-efficiency metrics

This gives you a non-ML benchmark.

## Phase 2: first supervised models

Start with point prediction, not ranking models.

Train separate models for:

- predicted views
- predicted engagement
- predicted conversions
- predicted ROI proxy

Model choice:

- start with CatBoost or LightGBM
- CatBoost is especially practical if you have many categorical fields like niche, objective, country, platform, industry

Use only pre-decision features, such as:

- influencer profile and audience stats
- recent public performance
- price card / negotiated price band
- campaign objective and category
- target geo / language
- client industry
- historical performance on similar campaigns
- semantic similarity features
- LLM-derived structured features if helpful

## Phase 3: business-value ranking policy

After prediction, rank using a policy such as:

final_score =
  w1 * expected_roi
+ w2 * expected_conversions
+ w3 * relevance_fit
- w4 * uncertainty
- w5 * price_inefficiency
- w6 * risk

Different campaign types can use different weights.

This is the equivalent of learning "a whole bunch of predictions along the way" instead of depending on one score.

## Phase 4: retraining loop

Retrain weekly or monthly:

1. ingest new outcomes
2. rebuild training rows
3. retrain models
4. compare against current production model and baseline heuristic
5. deploy only if better

This is your version of the Axon learning loop.

## Phase 5: controlled exploration

Once the system is stable, add measured exploration so you do not only recommend historically popular creators.

Examples:

- reserve 1-2 shortlist slots for high-upside uncertain creators
- use uncertainty-aware ranking
- later add contextual bandits if volume supports it

## Why this is the right abstraction for you

AppLovin's actual domain is ad auctions, not influencer marketplaces. But the underlying pattern is very similar:

- many possible candidates
- noisy public signals
- proprietary transaction outcomes
- strong economic objective
- repeated decision loop
- opportunity for compounding from feedback

So the right lesson is not ad-tech imitation. It is system design discipline.

## Concrete build order for your team

### Step 1: define the target

Choose one main optimization target first:

- expected conversions
- or expected ROI proxy

Do not start with 5 objectives at once.

### Step 2: build the gold interaction table

One row = one historical campaign-influencer result.

This is your most valuable data asset.

### Step 3: ship a baseline scorer

Use heuristics + semantic retrieval first.

This gives you something to beat.

### Step 4: train first supervised models

Start with CatBoost point-prediction models.

Do not start with pairwise/listwise ranking yet.

### Step 5: add explanations

For each recommendation, return reasons like:

- strong audience-country overlap
- historically efficient in similar campaigns
- price is within expected ROI range
- recent performance is stable
- high confidence due to relevant prior outcomes

### Step 6: add retraining and monitoring

Track:

- prediction error
- ranking quality
- campaign ROI
- shortlist acceptance rate
- repeat client spend
- coverage across influencer segments

### Step 7: add exploration only after the basics work

This prevents the system from getting stuck recommending only well-known creators.

## Bottom line

The best way to think about Axon 2.0 is:

- not a single AI model
- not just a recommendation engine
- not just a better targeting algorithm

It is a tightly integrated outcome-optimization loop built on proprietary data, real-time decisioning, and continuous feedback.

For your business, the most valuable things to copy are:

1. optimize for measurable business outcome
2. use multiple predictions instead of one magic score
3. log every decision and outcome
4. retrain regularly
5. let better performance create a data flywheel

If you do those five things well, you do not need AppLovin-scale infrastructure to get real advantage.

## Source notes

Primary / near-primary sources used:

1. AppLovin 2025 10-K (SEC)
   - Axon Ads Manager description
   - microsecond-level auction language
   - distribution -> better insights -> better Axon efficiency
   - expansion into web-based e-commerce, social media, and CTV

2. AppLovin 4Q23 shareholder letter (SEC exhibit)
   - 2023 release of advanced Axon 2.0
   - continued learning and scaling
   - advertisers spent more due to improved performance

3. AppLovin Q2 2023 shareholder letter (SEC exhibit)
   - rollout of latest AI-based advertising engine AXON 2.0 driving outperformance

4. AppLovin 2024 shareholder letter (public PDF)
   - advancing models
   - personalized ad experiences with AI-created iterations
   - broader advertiser reach
   - direct-to-consumer commerce and CTV expansion
   - self-service dashboard powered by AI agents

5. AdExchanger coverage of AppLovin Q2 2023 and Q4 2023 earnings discussions
   - predictive ML targeting app-install ads
   - trained on first-party data from AppLovin's game portfolio and trillions of daily in-app events
   - Foroughi quote that Axon 2.0 was dramatically better and improved multiple predictions along the way

Note on infrastructure claims:

I did not independently verify the Google Cloud L4 GPU detail from the sources retrieved for this report, so I have not treated it as a confirmed design fact here.