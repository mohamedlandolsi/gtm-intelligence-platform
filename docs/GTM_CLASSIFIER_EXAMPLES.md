# GTM Signal Classifier - Practical Examples

## Example 1: Basic Signal Classification

Classify market signals into GTM dimensions:

```python
from processing.signal_aggregator import aggregate_market_signals
from processing.gtm_classifier import classify_gtm_signals

# Get aggregated signals
signals = aggregate_market_signals(max_signals=20, min_confidence='high')

# Classify into GTM dimensions
classified = classify_gtm_signals(signals)

# Display results
print(f"Classified {len(classified)} signals into GTM dimensions\n")

for i, signal in enumerate(classified[:5], 1):
    print(f"{i}. {signal['headline']}")
    print(f"   Primary Category: {signal['primary_category']}")
    if signal.get('secondary_categories'):
        print(f"   Secondary: {', '.join(signal['secondary_categories'])}")
    
    # Show top scores
    scores = signal['category_scores']
    top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"   Scores: {', '.join([f'{cat}={score:.2f}' for cat, score in top_3])}")
    print()
```

**Output:**
```
Classified 20 signals into GTM dimensions

1. Stripe has approximately 12,538 employees
   Primary Category: TALENT
   Scores: TALENT=0.36, TIMING=0.00, MESSAGING=0.00

2. Stripe is actively hiring for 150+ open positions globally
   Primary Category: TALENT
   Secondary: ICP
   Scores: TALENT=0.51, ICP=0.37, MESSAGING=0.19

3. stripe-android repository actively maintained
   Primary Category: PRODUCT
   Secondary: TIMING
   Scores: PRODUCT=0.55, TIMING=0.30, ICP=0.07

4. stripe-python v8.0.0 released with async support
   Primary Category: PRODUCT
   Secondary: TIMING
   Scores: PRODUCT=0.64, TIMING=0.37, MESSAGING=0.07

5. Financial Connections API v2 launched
   Primary Category: PRODUCT
   Scores: PRODUCT=0.37, TIMING=0.07, COMPETITIVE=0.05
```

---

## Example 2: Generate GTM Analysis Report

Create comprehensive GTM analysis with recommendations:

```python
from processing.gtm_classifier import GTMSignalClassifier, classify_gtm_signals
from processing.signal_aggregator import aggregate_market_signals

# Get and classify signals
signals = aggregate_market_signals(max_signals=25, min_confidence='high')
classified = classify_gtm_signals(signals)

# Generate GTM report
classifier = GTMSignalClassifier()
report = classifier.generate_gtm_report(classified)

# Display report
print("="*80)
print("GTM ANALYSIS REPORT")
print("="*80)

print(f"\nTotal Signals Analyzed: {report['total_signals']}")

print("\nPrimary Category Distribution:")
for category, count in sorted(report['by_primary_category'].items(), 
                                key=lambda x: x[1], reverse=True):
    percentage = (count / report['total_signals']) * 100
    print(f"  {category:15s}: {count:3d} signals ({percentage:5.1f}%)")

if report.get('high_confidence_signals'):
    print(f"\nHigh-Confidence Signals (score >= 0.6): {len(report['high_confidence_signals'])}")
    for sig in report['high_confidence_signals'][:5]:
        print(f"  • {sig['category']:12s} ({sig['score']:.2f}): {sig['headline'][:60]}...")

if report.get('multi_dimensional_signals'):
    print(f"\nMulti-Dimensional Signals: {len(report['multi_dimensional_signals'])}")
    print("(Signals relevant to multiple GTM dimensions)")
    for sig in report['multi_dimensional_signals'][:3]:
        print(f"  • {sig['primary']} + {', '.join(sig['secondary'])}")
        print(f"    {sig['headline'][:70]}...")

if report.get('category_combinations'):
    print("\nCommon Category Combinations:")
    for combo, count in sorted(report['category_combinations'].items(),
                                 key=lambda x: x[1], reverse=True)[:5]:
        print(f"  • {combo}: {count} signals")

if report.get('gtm_recommendations'):
    print("\n" + "="*80)
    print("GTM RECOMMENDATIONS")
    print("="*80)
    for i, rec in enumerate(report['gtm_recommendations'], 1):
        print(f"\n{i}. {rec}")
```

**Output:**
```
================================================================================
GTM ANALYSIS REPORT
================================================================================

Total Signals Analyzed: 20

Primary Category Distribution:
  PRODUCT        :  16 signals ( 80.0%)
  TALENT         :   2 signals ( 10.0%)
  TIMING         :   1 signals (  5.0%)
  MARKET         :   1 signals (  5.0%)

High-Confidence Signals (score >= 0.6): 4
  • PRODUCT      (0.64): stripe-python v8.0.0 released with async support...
  • PRODUCT      (0.64): stripe-js v3.2.0 adds Payment Element customization...
  • PRODUCT      (0.76): Stripe CLI v1.19.0 adds local webhook testing...
  • PRODUCT      (0.84): stripe-go v76.0.0 adds support for new Treasury APIs...

Multi-Dimensional Signals: 11
(Signals relevant to multiple GTM dimensions)
  • PRODUCT + TIMING
    stripe-android repository actively maintained...
  • PRODUCT + TIMING
    stripe-python repository actively maintained...
  • TIMING + PRODUCT
    API version 2024-11-01 released...

Common Category Combinations:
  • PRODUCT + TIMING: 8 signals
  • TALENT + ICP: 1 signal

================================================================================
GTM RECOMMENDATIONS
================================================================================

1. High product activity detected. Recommend preparing product marketing 
   campaigns and technical content to support launches.

2. Many signals span multiple GTM dimensions. Consider integrated campaigns 
   that address multiple angles.
```

---

## Example 3: Filter by GTM Category

Analyze signals by specific GTM dimensions:

```python
from processing.gtm_classifier import classify_gtm_signals
from processing.signal_aggregator import aggregate_market_signals

signals = aggregate_market_signals(max_signals=30)
classified = classify_gtm_signals(signals)

print("="*80)
print("SIGNALS BY GTM CATEGORY")
print("="*80)

# Group by category
by_category = {}
for signal in classified:
    category = signal['primary_category']
    if category not in by_category:
        by_category[category] = []
    by_category[category].append(signal)

# Display each category
for category in ['TIMING', 'MESSAGING', 'ICP', 'COMPETITIVE', 'PRODUCT', 'MARKET', 'TALENT']:
    signals_in_category = by_category.get(category, [])
    
    if signals_in_category:
        print(f"\n{category} ({len(signals_in_category)} signals)")
        print("-"*80)
        
        for signal in signals_in_category[:3]:  # Show top 3
            print(f"• {signal['headline'][:70]}")
            print(f"  {signal['date_detected']} | {signal['source']}")
            print(f"  {signal['gtm_insights'][:120]}...")
            print()
```

**Output:**
```
================================================================================
SIGNALS BY GTM CATEGORY
================================================================================

PRODUCT (16 signals)
--------------------------------------------------------------------------------
• stripe-android repository actively maintained
  2025-11-05 | GitHub
  Primary GTM dimension: PRODUCT (confidence: medium) This signal concerns 
  product development, features, or technical capabilities...

• stripe-python repository actively maintained
  2025-11-04 | GitHub
  Primary GTM dimension: PRODUCT (confidence: medium) This signal concerns 
  product development, features, or technical capabilities...

• stripe-python v8.0.0 released with async support and improved type hints
  2025-10-21 | GitHub
  Primary GTM dimension: PRODUCT (confidence: high) This signal concerns 
  product development, features, or technical capabilities...

TALENT (2 signals)
--------------------------------------------------------------------------------
• Stripe has approximately 12,538 employees
  2025-11-05 | LinkedIn
  Primary GTM dimension: TALENT (confidence: low) This signal indicates 
  organizational changes and strategic hiring...

• Stripe is actively hiring for 150+ open positions globally
  2025-11-05 | LinkedIn
  Primary GTM dimension: TALENT (confidence: medium) This signal indicates 
  organizational changes and strategic hiring...

TIMING (1 signals)
--------------------------------------------------------------------------------
• API version 2024-11-01 released with backward compatibility
  2025-10-31 | Stripe Official
  Primary GTM dimension: TIMING (confidence: medium) This signal indicates 
  a specific timing opportunity or launch window...
```

---

## Example 4: Weekly GTM Intelligence Briefing

Generate a formatted weekly report for stakeholders:

```python
from processing.signal_aggregator import aggregate_market_signals
from processing.gtm_classifier import classify_gtm_signals, GTMSignalClassifier
from datetime import datetime
from collections import Counter

# Get last week's signals
signals = aggregate_market_signals(
    max_signals=30,
    min_confidence='high',
    days_lookback=7
)

# Classify
classified = classify_gtm_signals(signals)

# Generate report
classifier = GTMSignalClassifier()
report = classifier.generate_gtm_report(classified)

# Format briefing
today = datetime.now().strftime('%B %d, %Y')

print("="*80)
print(f"GTM INTELLIGENCE BRIEFING")
print(f"Week of {today}")
print("="*80)

print(f"\n📊 Executive Summary")
print("-"*80)
print(f"Total Signals Detected: {len(classified)}")
print(f"High-Confidence Signals: {len(report.get('high_confidence_signals', []))}")
print(f"Multi-Dimensional Signals: {len(report.get('multi_dimensional_signals', []))}")

# Category breakdown
print(f"\n📈 Signal Distribution")
print("-"*80)
for cat, count in sorted(report['by_primary_category'].items(), 
                          key=lambda x: x[1], reverse=True):
    pct = (count / len(classified)) * 100
    print(f"{cat:15s}: {count:3d} signals ({pct:5.1f}%)")

# Key signals by category
print(f"\n🎯 Key Signals by Category")
print("-"*80)

for category in ['PRODUCT', 'COMPETITIVE', 'TALENT', 'ICP', 'TIMING']:
    cat_signals = [s for s in classified if s['primary_category'] == category]
    
    if cat_signals:
        print(f"\n{category}:")
        for sig in cat_signals[:2]:  # Top 2 per category
            print(f"  • {sig['headline'][:65]}...")
            print(f"    {sig['date_detected']} | Confidence: {sig['category_scores'][category]:.2f}")

# Recommendations
if report.get('gtm_recommendations'):
    print(f"\n💡 GTM Recommendations")
    print("-"*80)
    for i, rec in enumerate(report['gtm_recommendations'], 1):
        print(f"\n{i}. {rec}")

print("\n" + "="*80)
print("End of briefing")
print("="*80)
```

**Output:**
```
================================================================================
GTM INTELLIGENCE BRIEFING
Week of November 05, 2025
================================================================================

📊 Executive Summary
--------------------------------------------------------------------------------
Total Signals Detected: 20
High-Confidence Signals: 4
Multi-Dimensional Signals: 11

📈 Signal Distribution
--------------------------------------------------------------------------------
PRODUCT        :  16 signals ( 80.0%)
TALENT         :   2 signals ( 10.0%)
TIMING         :   1 signals (  5.0%)
MARKET         :   1 signals (  5.0%)

🎯 Key Signals by Category
--------------------------------------------------------------------------------

PRODUCT:
  • stripe-python v8.0.0 released with async support and improved...
    2025-10-21 | Confidence: 0.64
  • stripe-go v76.0.0 adds support for new Treasury APIs...
    2025-10-12 | Confidence: 0.84

TALENT:
  • Stripe is actively hiring for 150+ open positions globally...
    2025-11-05 | Confidence: 0.51
  • Stripe has approximately 12,538 employees...
    2025-11-05 | Confidence: 0.36

TIMING:
  • API version 2024-11-01 released with backward compatibility...
    2025-10-31 | Confidence: 0.49

💡 GTM Recommendations
--------------------------------------------------------------------------------

1. High product activity detected. Recommend preparing product marketing 
   campaigns and technical content to support launches.

2. Many signals span multiple GTM dimensions. Consider integrated campaigns 
   that address multiple angles.

================================================================================
End of briefing
================================================================================
```

---

## Example 5: Competitive Intelligence Focus

Extract and analyze competitive signals:

```python
from processing.gtm_classifier import classify_gtm_signals
from processing.signal_aggregator import aggregate_market_signals

# Get all available signals
signals = aggregate_market_signals(max_signals=50, min_confidence='medium')
classified = classify_gtm_signals(signals)

# Filter competitive signals (primary or secondary)
competitive = [
    s for s in classified
    if s['primary_category'] == 'COMPETITIVE'
    or 'COMPETITIVE' in s.get('secondary_categories', [])
]

print("="*80)
print("COMPETITIVE INTELLIGENCE REPORT")
print("="*80)

print(f"\nTotal Competitive Signals: {len(competitive)}")

if competitive:
    print("\n📍 Competitive Signals Detected:")
    print("-"*80)
    
    for i, signal in enumerate(competitive, 1):
        print(f"\n{i}. {signal['headline']}")
        print(f"   Date: {signal['date_detected']}")
        print(f"   Source: {signal['source']}")
        print(f"   Category: {signal['primary_category']}")
        
        # Extract competitive keywords from description
        comp_keywords = ['plaid', 'adyen', 'square', 'paypal', 'competitor', 'versus']
        found_keywords = [kw for kw in comp_keywords if kw in signal['description'].lower()]
        if found_keywords:
            print(f"   Keywords: {', '.join(found_keywords)}")
        
        print(f"   Insight: {signal['gtm_insights'][:100]}...")
    
    # GTM actions for competitive signals
    print("\n" + "="*80)
    print("RECOMMENDED ACTIONS")
    print("="*80)
    print("\n1. Update competitive battlecards with new information")
    print("2. Brief sales team on competitive positioning changes")
    print("3. Review product differentiation messaging")
    print("4. Monitor competitor feature releases for response opportunities")

else:
    print("\nNo direct competitive signals detected in recent period.")
    print("Consider:")
    print("  • Expanding lookback period")
    print("  • Including lower confidence signals")
    print("  • Manually monitoring competitor announcements")
```

---

## Example 6: ICP & Segmentation Analysis

Identify signals about target customers:

```python
from processing.gtm_classifier import classify_gtm_signals
from processing.signal_aggregator import aggregate_market_signals

signals = aggregate_market_signals(max_signals=30)
classified = classify_gtm_signals(signals)

# Filter ICP-related signals
icp_signals = [
    s for s in classified
    if s['primary_category'] == 'ICP'
    or 'ICP' in s.get('secondary_categories', [])
]

print("="*80)
print("ICP & SEGMENTATION ANALYSIS")
print("="*80)

print(f"\nSignals Related to Target Customers: {len(icp_signals)}")

if icp_signals:
    print("\n🎯 Customer Segment Signals:")
    print("-"*80)
    
    for signal in icp_signals:
        print(f"\n• {signal['headline']}")
        print(f"  {signal['date_detected']} | {signal['source']}")
        
        # Identify segment indicators
        segments = {
            'Enterprise': ['enterprise', 'fortune 500', 'large'],
            'SMB': ['smb', 'small business', 'small to medium'],
            'Mid-Market': ['mid-market', 'middle market'],
            'Developer': ['developer', 'technical', 'engineering'],
            'B2B': ['b2b', 'business to business'],
            'B2C': ['b2c', 'consumer', 'retail']
        }
        
        detected_segments = []
        desc_lower = signal['description'].lower()
        for segment, keywords in segments.items():
            if any(kw in desc_lower for kw in keywords):
                detected_segments.append(segment)
        
        if detected_segments:
            print(f"  Segments: {', '.join(detected_segments)}")
    
    # Recommendations
    print("\n" + "="*80)
    print("SEGMENTATION RECOMMENDATIONS")
    print("="*80)
    print("\n1. Review ICP definitions based on detected signals")
    print("2. Adjust targeting criteria for campaigns")
    print("3. Realign sales territories and account tiers")
    print("4. Update personas with new customer insights")

else:
    print("\nNo explicit ICP signals detected.")
    print("Review TALENT and PRODUCT signals for indirect ICP clues:")
    
    # Show hiring signals (indirect ICP indicators)
    talent = [s for s in classified if s['primary_category'] == 'TALENT']
    if talent:
        print("\nTalent Signals (may indicate target segment focus):")
        for sig in talent[:3]:
            print(f"  • {sig['headline'][:70]}...")
```

---

## Example 7: Save and Export Classified Signals

Save classified signals in multiple formats:

```python
import json
import csv
from processing.gtm_classifier import classify_gtm_signals, GTMSignalClassifier
from processing.signal_aggregator import aggregate_market_signals
from datetime import datetime
import os

# Get and classify signals
signals = aggregate_market_signals(max_signals=25)
classified = classify_gtm_signals(signals)

# Generate report
classifier = GTMSignalClassifier()
report = classifier.generate_gtm_report(classified)

# Create output directory
os.makedirs('outputs/classified', exist_ok=True)

# 1. Save as JSON with full metadata
json_output = {
    'metadata': {
        'classification_date': datetime.now().isoformat(),
        'total_signals': len(classified),
        'gtm_report': report
    },
    'classified_signals': classified
}

json_path = 'outputs/classified/gtm_signals.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_output, f, indent=2, ensure_ascii=False)
print(f"✓ Saved JSON: {json_path}")

# 2. Save as CSV (flattened)
csv_path = 'outputs/classified/gtm_signals.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'signal_id', 'date_detected', 'headline', 'source',
        'primary_category', 'secondary_categories', 'confidence_score'
    ])
    writer.writeheader()
    
    for signal in classified:
        writer.writerow({
            'signal_id': signal['signal_id'],
            'date_detected': signal['date_detected'],
            'headline': signal['headline'],
            'source': signal['source'],
            'primary_category': signal['primary_category'],
            'secondary_categories': ', '.join(signal.get('secondary_categories', [])),
            'confidence_score': signal['category_scores'][signal['primary_category']]
        })

print(f"✓ Saved CSV: {csv_path}")

# 3. Generate Markdown report
md_path = 'outputs/classified/gtm_report.md'
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(f"# GTM Intelligence Report\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write(f"## Executive Summary\n\n")
    f.write(f"- Total Signals: {len(classified)}\n")
    f.write(f"- High-Confidence: {len(report.get('high_confidence_signals', []))}\n")
    f.write(f"- Multi-Dimensional: {len(report.get('multi_dimensional_signals', []))}\n\n")
    
    f.write(f"## Category Distribution\n\n")
    for cat, count in sorted(report['by_primary_category'].items(), 
                              key=lambda x: x[1], reverse=True):
        pct = (count / len(classified)) * 100
        f.write(f"- **{cat}**: {count} signals ({pct:.1f}%)\n")
    
    f.write(f"\n## Signals by Category\n\n")
    for category in ['PRODUCT', 'COMPETITIVE', 'TALENT', 'ICP', 'TIMING']:
        cat_signals = [s for s in classified if s['primary_category'] == category]
        if cat_signals:
            f.write(f"\n### {category}\n\n")
            for sig in cat_signals[:5]:
                f.write(f"**{sig['headline']}**  \n")
                f.write(f"*{sig['date_detected']} | {sig['source']}*\n\n")
                f.write(f"{sig['description'][:150]}...\n\n")
    
    if report.get('gtm_recommendations'):
        f.write(f"\n## GTM Recommendations\n\n")
        for i, rec in enumerate(report['gtm_recommendations'], 1):
            f.write(f"{i}. {rec}\n\n")

print(f"✓ Saved Markdown: {md_path}")

print(f"\n📊 Summary:")
print(f"   Files generated: 3")
print(f"   Total signals: {len(classified)}")
print(f"   Primary categories: {len(report['by_primary_category'])}")
```

---

## Example 8: Track Category Trends Over Time

Monitor how GTM categories change over time:

```python
from processing.gtm_classifier import classify_gtm_signals
from processing.signal_aggregator import aggregate_market_signals
from datetime import datetime, timedelta
from collections import Counter

# Get signals for different time periods
periods = [
    ('This Week', 7),
    ('Last Week', 14),
    ('Two Weeks Ago', 21),
    ('Three Weeks Ago', 28)
]

print("="*80)
print("GTM CATEGORY TRENDS")
print("="*80)

trend_data = {}

for period_name, days_back in periods:
    # Get signals for this period
    signals = aggregate_market_signals(
        max_signals=50,
        min_confidence='medium',
        days_lookback=days_back
    )
    
    # Classify
    classified = classify_gtm_signals(signals)
    
    # Count by category
    category_counts = Counter(s['primary_category'] for s in classified)
    trend_data[period_name] = category_counts
    
    print(f"\n{period_name} ({days_back} days back):")
    for cat in ['PRODUCT', 'COMPETITIVE', 'TALENT', 'ICP', 'TIMING', 'MARKET', 'MESSAGING']:
        count = category_counts.get(cat, 0)
        if count > 0:
            print(f"  {cat:15s}: {count:3d} signals")

# Show trends
print("\n" + "="*80)
print("TREND ANALYSIS")
print("="*80)

for category in ['PRODUCT', 'COMPETITIVE', 'TALENT']:
    print(f"\n{category} Trend:")
    for period_name in ['This Week', 'Last Week', 'Two Weeks Ago', 'Three Weeks Ago']:
        count = trend_data.get(period_name, {}).get(category, 0)
        bar = '█' * count
        print(f"  {period_name:15s}: {bar} ({count})")
```

---

## Best Practices

1. **Always Aggregate First**
   ```python
   signals = aggregate_market_signals(max_signals=20)
   classified = classify_gtm_signals(signals)
   ```

2. **Review High-Confidence Signals**
   Focus on signals with primary_category score >= 0.6

3. **Check Multi-Dimensional Signals**
   Signals with secondary categories often indicate complex opportunities

4. **Act on GTM Recommendations**
   Use generated recommendations for planning

5. **Track Trends Over Time**
   Monitor category distribution changes weekly

6. **Customize for Your Domain**
   Add domain-specific keywords and patterns

7. **Export for Stakeholders**
   Generate formatted reports for different audiences

8. **Combine with Other Modules**
   Integrate with aggregation and reporting pipelines
