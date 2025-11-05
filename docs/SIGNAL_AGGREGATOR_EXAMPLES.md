# Signal Aggregator - Practical Examples

## Example 1: Basic Signal Aggregation

Simplest way to get aggregated market signals:

```python
from processing.signal_aggregator import aggregate_market_signals

# Get top 15 signals from last 90 days
signals = aggregate_market_signals()

# Display results
for i, signal in enumerate(signals, 1):
    print(f"{i}. [{signal['date_detected']}] {signal['signal_type']}")
    print(f"   {signal['headline']}")
    print(f"   Confidence: {signal['confidence_level']} | Source: {signal['source']}")
    print()
```

**Output:**
```
1. [2025-11-05] growth
   Stripe has approximately 12,538 employees
   Confidence: high | Source: LinkedIn

2. [2025-11-05] hiring
   Stripe is actively hiring for 150+ open positions globally
   Confidence: high | Source: LinkedIn

3. [2025-11-05] sdk_update
   stripe-android repository actively maintained
   Confidence: high | Source: GitHub
```

---

## Example 2: Custom Parameters

Control what signals you get with custom parameters:

```python
from processing.signal_aggregator import aggregate_market_signals

# High-confidence signals from last 30 days only
signals = aggregate_market_signals(
    max_signals=20,        # Get up to 20 signals
    min_confidence='high', # Only high-confidence
    days_lookback=30       # Last 30 days
)

print(f"Found {len(signals)} high-confidence signals")

# Group by source
from collections import defaultdict
by_source = defaultdict(list)
for signal in signals:
    by_source[signal['source']].append(signal)

for source, sigs in by_source.items():
    print(f"\n{source}: {len(sigs)} signals")
    for sig in sigs[:3]:  # Show first 3
        print(f"  - {sig['headline'][:60]}...")
```

**Output:**
```
Found 18 high-confidence signals

GitHub: 10 signals
  - stripe-android repository actively maintained...
  - stripe-python repository actively maintained...
  - stripe-php repository actively maintained...

LinkedIn: 4 signals
  - Stripe has approximately 12,538 employees...
  - Stripe is actively hiring for 150+ open positions...
  - Engineering department has 80+ open positions...

Stripe Official: 4 signals
  - Financial Connections API v2 launched...
  - API version 2024-11-01 released...
  - Climate API updates for carbon removal...
```

---

## Example 3: Advanced Usage with Full Control

Use the `MarketSignalsAggregator` class for advanced features:

```python
from processing.signal_aggregator import MarketSignalsAggregator

# Initialize aggregator
aggregator = MarketSignalsAggregator()

# Get signals
signals = aggregator.aggregate_market_signals(
    max_signals=25,
    min_confidence='medium',
    days_lookback=60
)

# Generate comprehensive report
summary = aggregator.generate_summary_report(signals)

print("="*80)
print("MARKET SIGNALS SUMMARY")
print("="*80)

print(f"\nTotal Signals: {summary['total_signals']}")
print(f"Date Range: {summary['date_range']['earliest']} to {summary['date_range']['latest']}")

print("\nSignal Distribution by Type:")
for sig_type, count in sorted(summary['by_type'].items(), key=lambda x: x[1], reverse=True):
    percentage = (count / summary['total_signals']) * 100
    bar = '█' * int(percentage / 5)  # Scale for display
    print(f"  {sig_type:20s} {bar} {count} ({percentage:.1f}%)")

print("\nSignal Distribution by Source:")
for source, count in sorted(summary['by_source'].items(), key=lambda x: x[1], reverse=True):
    percentage = (count / summary['total_signals']) * 100
    print(f"  {source:20s} {count} signals ({percentage:.1f}%)")

print("\nConfidence Breakdown:")
for conf in ['high', 'medium', 'low']:
    count = summary['by_confidence'].get(conf, 0)
    if count > 0:
        percentage = (count / summary['total_signals']) * 100
        print(f"  {conf.upper():10s} {count} ({percentage:.1f}%)")

# Save to file
filepath = aggregator.save_aggregated_signals(signals, filename='weekly_briefing.json')
print(f"\nSaved to: {filepath}")
```

**Output:**
```
================================================================================
MARKET SIGNALS SUMMARY
================================================================================

Total Signals: 25
Date Range: 2025-09-15 to 2025-11-05

Signal Distribution by Type:
  sdk_update           ████████████ 12 (48.0%)
  hiring               ████ 4 (16.0%)
  new_api_endpoint     ███ 3 (12.0%)
  growth               ██ 2 (8.0%)
  api_expansion        ██ 2 (8.0%)
  commit_activity      █ 1 (4.0%)
  developer_tools      █ 1 (4.0%)

Signal Distribution by Source:
  GitHub               15 signals (60.0%)
  LinkedIn             6 signals (24.0%)
  Stripe Official      4 signals (16.0%)

Confidence Breakdown:
  HIGH       25 (100.0%)

Saved to: outputs/aggregated/weekly_briefing.json
```

---

## Example 4: Handling Conflicting Information

Demonstrate conflict resolution when multiple sources report the same event:

```python
from processing.signal_aggregator import MarketSignalsAggregator

# Create test signals about the same funding round
test_signals = [
    {
        'signal_id': 'SIG-001',
        'signal_type': 'funding',
        'headline': 'Stripe raises $600M in Series H',
        'description': 'TechCrunch reports Stripe raised $600M at $95B valuation.',
        'date_detected': '2025-10-15',
        'source': 'News',
        'source_url': 'https://techcrunch.com/stripe',
        'confidence_level': 'medium',
        'raw_json': {'amount': '$600M', 'valuation': '$95B'}
    },
    {
        'signal_id': 'SIG-002',
        'signal_type': 'funding',
        'headline': 'Stripe secures $600M Series H funding',
        'description': 'Crunchbase confirms $600M round. Investors include Sequoia, Thrive. Company valued at $95B.',
        'date_detected': '2025-10-15',
        'source': 'Crunchbase',
        'source_url': 'https://crunchbase.com/stripe',
        'confidence_level': 'high',
        'raw_json': {'amount': '$600M', 'valuation': '$95B', 'investors': ['Sequoia', 'Thrive']}
    },
    {
        'signal_id': 'SIG-003',
        'signal_type': 'funding',
        'headline': 'Stripe closes $600M at $95B valuation',
        'description': 'Bloomberg: Stripe has completed a $600 million Series H at $95B valuation.',
        'date_detected': '2025-10-15',
        'source': 'News',
        'source_url': 'https://bloomberg.com/stripe',
        'confidence_level': 'high',
        'raw_json': {'amount': '$600M', 'valuation': '$95B'}
    }
]

# Initialize aggregator
aggregator = MarketSignalsAggregator()

print("BEFORE CONFLICT RESOLUTION:")
print("="*80)
for i, signal in enumerate(test_signals, 1):
    print(f"{i}. {signal['headline']}")
    print(f"   Source: {signal['source']} | Confidence: {signal['confidence_level']}")
    print(f"   Description: {signal['description'][:80]}...")
    print()

# Resolve conflicts
resolved = aggregator.handle_conflicting_information(test_signals)

print("\nAFTER CONFLICT RESOLUTION:")
print("="*80)
print(f"Reduced from {len(test_signals)} signals to {len(resolved)} signal(s)\n")

for signal in resolved:
    print(f"Headline: {signal['headline']}")
    print(f"Description: {signal['description']}")
    print(f"Primary Source: {signal['source']}")
    print(f"Confidence: {signal['confidence_level']}")
    if 'sources' in signal:
        print(f"All Sources: {', '.join(signal['sources'])}")
    if 'note' in signal:
        print(f"Note: {signal['note']}")
```

**Output:**
```
BEFORE CONFLICT RESOLUTION:
================================================================================
1. Stripe raises $600M in Series H
   Source: News | Confidence: medium
   Description: TechCrunch reports Stripe raised $600M at $95B valuation....

2. Stripe secures $600M Series H funding
   Source: Crunchbase | Confidence: high
   Description: Crunchbase confirms $600M round. Investors include Sequoia, Thrive. Company v...

3. Stripe closes $600M at $95B valuation
   Source: News | Confidence: high
   Description: Bloomberg: Stripe has completed a $600 million Series H at $95B valuation....


AFTER CONFLICT RESOLUTION:
================================================================================
Reduced from 3 signals to 1 signal(s)

Headline: Stripe secures $600M Series H funding
Description: Crunchbase confirms $600M round. Investors include Sequoia, Thrive. Company valued at $95B.
Primary Source: Crunchbase
Confidence: high
All Sources: News, Crunchbase
Note: Information aggregated from 3 sources: News, Crunchbase, News
```

---

## Example 5: Daily Intelligence Briefing

Create a daily briefing email/report:

```python
from processing.signal_aggregator import aggregate_market_signals
from datetime import datetime, timedelta

def generate_daily_briefing():
    """Generate daily intelligence briefing"""
    
    # Get signals from last 24 hours
    signals = aggregate_market_signals(
        max_signals=10,
        min_confidence='high',
        days_lookback=1
    )
    
    today = datetime.now().strftime('%B %d, %Y')
    
    print("="*80)
    print(f"STRIPE INTELLIGENCE BRIEFING")
    print(f"{today}")
    print("="*80)
    
    if not signals:
        print("\n📭 No new high-confidence signals in the last 24 hours.")
        return
    
    print(f"\n📊 {len(signals)} High-Priority Signals Detected\n")
    
    # Group by category
    technical = [s for s in signals if s['signal_type'] in ['sdk_update', 'new_api_endpoint', 'api_expansion']]
    business = [s for s in signals if s['signal_type'] in ['funding', 'hiring', 'growth', 'partnership']]
    market = [s for s in signals if s['signal_type'] in ['product_launch', 'market_expansion', 'competitive_move']]
    
    if technical:
        print("🔧 TECHNICAL SIGNALS")
        print("-"*80)
        for signal in technical:
            print(f"• {signal['headline']}")
            print(f"  Source: {signal['source']} | {signal['date_detected']}")
            print()
    
    if business:
        print("💼 BUSINESS SIGNALS")
        print("-"*80)
        for signal in business:
            print(f"• {signal['headline']}")
            print(f"  Source: {signal['source']} | {signal['date_detected']}")
            print()
    
    if market:
        print("🎯 MARKET SIGNALS")
        print("-"*80)
        for signal in market:
            print(f"• {signal['headline']}")
            print(f"  Source: {signal['source']} | {signal['date_detected']}")
            print()
    
    print("="*80)
    print("End of briefing")
    print("="*80)

# Run the briefing
generate_daily_briefing()
```

**Output:**
```
================================================================================
STRIPE INTELLIGENCE BRIEFING
November 05, 2025
================================================================================

📊 6 High-Priority Signals Detected

🔧 TECHNICAL SIGNALS
--------------------------------------------------------------------------------
• stripe-android repository actively maintained
  Source: GitHub | 2025-11-05

• stripe-python repository actively maintained
  Source: GitHub | 2025-11-04

• Financial Connections API v2 launched with real-time verification
  Source: Stripe Official | 2025-11-05


💼 BUSINESS SIGNALS
--------------------------------------------------------------------------------
• Stripe has approximately 12,538 employees
  Source: LinkedIn | 2025-11-05

• Stripe is actively hiring for 150+ open positions globally
  Source: LinkedIn | 2025-11-05

• Engineering department has 80+ open positions
  Source: LinkedIn | 2025-11-05

================================================================================
End of briefing
================================================================================
```

---

## Example 6: Competitive Intelligence Analysis

Track competitive moves and market positioning:

```python
from processing.signal_aggregator import aggregate_market_signals

# Get signals from last quarter
signals = aggregate_market_signals(
    max_signals=50,
    min_confidence='medium',
    days_lookback=90
)

print("="*80)
print("COMPETITIVE INTELLIGENCE ANALYSIS")
print("="*80)

# Extract competitive signals
competitive_keywords = [
    'competitor', 'competitive', 'versus', 'vs', 
    'plaid', 'adyen', 'square', 'paypal',
    'market share', 'positioning'
]

competitive_signals = []
for signal in signals:
    description = signal.get('description', '').lower()
    headline = signal.get('headline', '').lower()
    
    if any(keyword in description or keyword in headline for keyword in competitive_keywords):
        competitive_signals.append(signal)

print(f"\nIdentified {len(competitive_signals)} competitive signals:\n")

# Analyze by signal type
from collections import Counter
type_counter = Counter(s['signal_type'] for s in competitive_signals)

print("Competitive Activity by Type:")
for sig_type, count in type_counter.most_common():
    print(f"  • {sig_type}: {count}")

print("\nKey Competitive Signals:")
print("-"*80)

for i, signal in enumerate(competitive_signals[:5], 1):
    print(f"\n{i}. {signal['headline']}")
    print(f"   Type: {signal['signal_type']} | Date: {signal['date_detected']}")
    print(f"   {signal['description'][:150]}...")
    
    # Extract competitive context
    if 'strategic_implication' in signal.get('raw_json', {}):
        print(f"   💡 {signal['raw_json']['strategic_implication'][:100]}...")

print("\n" + "="*80)
```

**Output:**
```
================================================================================
COMPETITIVE INTELLIGENCE ANALYSIS
================================================================================

Identified 8 competitive signals:

Competitive Activity by Type:
  • new_api_endpoint: 3
  • api_expansion: 2
  • sdk_update: 2
  • partnership: 1

Key Competitive Signals:

1. Financial Connections API v2 launched with real-time bank verification
   Type: new_api_endpoint | Date: 2025-10-18
   Financial Connections API v2 launched with real-time bank verification

Strategic Implication: Direct competition with Plaid in bank data aggregation...
   💡 Direct competition with Plaid in bank data aggregation market...

2. Tax API enhancements for automated tax calculation
   Type: api_expansion | Date: 2025-10-12
   Tax API enhancements for automated tax calculation

Strategic Implication: Competing with Avalara and TaxJar in tax compliance...
   💡 Competing with Avalara and TaxJar in tax compliance automation...

3. Climate API updates for carbon removal marketplace
   Type: api_expansion | Date: 2025-10-08
   Climate API updates for carbon removal marketplace

Strategic Implication: ESG/sustainability positioning vs traditional payment processors...
   💡 ESG/sustainability positioning vs traditional payment processors...

================================================================================
```

---

## Example 7: Signal Filtering and Custom Analysis

Create custom filters and analysis:

```python
from processing.signal_aggregator import MarketSignalsAggregator
from datetime import datetime

aggregator = MarketSignalsAggregator()

# Get large set of signals
all_signals = aggregator.aggregate_market_signals(
    max_signals=100,
    min_confidence='low',  # Get all signals
    days_lookback=365
)

print("="*80)
print("CUSTOM SIGNAL ANALYSIS")
print("="*80)

# Filter 1: Developer-focused signals
developer_types = ['sdk_update', 'new_api_endpoint', 'developer_tools', 'api_expansion']
developer_signals = [s for s in all_signals if s['signal_type'] in developer_types]

print(f"\n📱 Developer-Focused Signals: {len(developer_signals)}")
for signal in developer_signals[:5]:
    print(f"  • {signal['headline'][:60]}...")

# Filter 2: Growth indicators
growth_types = ['funding', 'hiring', 'growth', 'partnership', 'acquisition']
growth_signals = [s for s in all_signals if s['signal_type'] in growth_types]

print(f"\n📈 Growth Indicator Signals: {len(growth_signals)}")
for signal in growth_signals[:5]:
    print(f"  • {signal['headline'][:60]}...")

# Filter 3: Recent activity (last 7 days)
from datetime import timedelta
cutoff_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
recent_signals = [s for s in all_signals if s['date_detected'] >= cutoff_date]

print(f"\n⚡ Recent Activity (last 7 days): {len(recent_signals)}")
for signal in recent_signals[:5]:
    print(f"  • [{signal['date_detected']}] {signal['headline'][:50]}...")

# Filter 4: High-impact signals (high confidence + recent)
high_impact = [
    s for s in all_signals 
    if s['confidence_level'] == 'high' 
    and s['date_detected'] >= cutoff_date
]

print(f"\n🎯 High-Impact Signals (high confidence + recent): {len(high_impact)}")
for signal in high_impact[:5]:
    print(f"  • {signal['signal_type'].upper()}: {signal['headline'][:50]}...")

# Custom scoring
def calculate_priority_score(signal):
    """Custom scoring function"""
    score = 0
    
    # Confidence weight
    conf_weights = {'high': 10, 'medium': 5, 'low': 2}
    score += conf_weights.get(signal['confidence_level'], 0)
    
    # Recency weight (more recent = higher score)
    days_old = (datetime.now() - datetime.fromisoformat(signal['date_detected'])).days
    recency_score = max(0, 10 - (days_old / 7))  # Decay over weeks
    score += recency_score
    
    # Type weight (prioritize certain types)
    priority_types = ['funding', 'new_api_endpoint', 'partnership']
    if signal['signal_type'] in priority_types:
        score += 5
    
    return score

# Sort by custom score
scored_signals = [(s, calculate_priority_score(s)) for s in all_signals]
scored_signals.sort(key=lambda x: x[1], reverse=True)

print(f"\n🏆 Top 5 by Custom Priority Score:")
for signal, score in scored_signals[:5]:
    print(f"  • Score {score:.1f}: {signal['headline'][:55]}...")
    print(f"    {signal['date_detected']} | {signal['signal_type']} | {signal['confidence_level']}")

print("\n" + "="*80)
```

**Output:**
```
================================================================================
CUSTOM SIGNAL ANALYSIS
================================================================================

📱 Developer-Focused Signals: 28
  • stripe-android repository actively maintained...
  • stripe-python repository actively maintained...
  • stripe-php repository actively maintained...
  • stripe-react-native repository actively maintained...
  • stripe-python v8.0.0 released with async support...

📈 Growth Indicator Signals: 12
  • Stripe has approximately 12,538 employees...
  • Stripe is actively hiring for 150+ open positions globally...
  • Engineering department has 80+ open positions...
  • Product Management department has 25+ open positions...
  • Series H funding of $600M at $95B valuation...

⚡ Recent Activity (last 7 days): 15
  • [2025-11-05] Stripe has approximately 12,538 employees...
  • [2025-11-05] Stripe is actively hiring for 150+ open positions...
  • [2025-11-05] stripe-android repository actively maintained...
  • [2025-11-04] stripe-python repository actively maintained...
  • [2025-11-03] stripe-php repository actively maintained...

🎯 High-Impact Signals (high confidence + recent): 15
  • GROWTH: Stripe has approximately 12,538 employees...
  • HIRING: Stripe is actively hiring for 150+ open positions...
  • SDK_UPDATE: stripe-android repository actively maintained...
  • SDK_UPDATE: stripe-python repository actively maintained...
  • SDK_UPDATE: stripe-php repository actively maintained...

🏆 Top 5 by Custom Priority Score:
  • Score 19.9: Stripe has approximately 12,538 employees...
    2025-11-05 | growth | high
  • Score 19.9: Stripe is actively hiring for 150+ open positions...
    2025-11-05 | hiring | high
  • Score 19.9: stripe-android repository actively maintained...
    2025-11-05 | sdk_update | high
  • Score 18.8: stripe-python repository actively maintained...
    2025-11-04 | sdk_update | high
  • Score 17.6: stripe-php repository actively maintained...
    2025-11-03 | sdk_update | high

================================================================================
```

---

## Example 8: Export and Integration

Save signals in different formats:

```python
from processing.signal_aggregator import MarketSignalsAggregator
import json
import csv
from datetime import datetime

aggregator = MarketSignalsAggregator()

# Get signals
signals = aggregator.aggregate_market_signals(max_signals=20)

# 1. Save as JSON
json_path = aggregator.save_aggregated_signals(signals, filename='signals.json')
print(f"✓ Saved JSON: {json_path}")

# 2. Export to CSV
csv_path = 'outputs/aggregated/signals.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'signal_id', 'date_detected', 'signal_type', 'source',
        'confidence_level', 'headline', 'description', 'source_url'
    ])
    writer.writeheader()
    for signal in signals:
        # Create CSV-friendly version (no nested dicts)
        csv_signal = {
            'signal_id': signal['signal_id'],
            'date_detected': signal['date_detected'],
            'signal_type': signal['signal_type'],
            'source': signal['source'],
            'confidence_level': signal['confidence_level'],
            'headline': signal['headline'],
            'description': signal['description'][:200],  # Truncate
            'source_url': signal.get('source_url', '')
        }
        writer.writerow(csv_signal)

print(f"✓ Saved CSV: {csv_path}")

# 3. Generate Markdown report
md_path = 'outputs/aggregated/signals_report.md'
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(f"# Market Signals Report\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"Total Signals: {len(signals)}\n\n")
    f.write("---\n\n")
    
    for i, signal in enumerate(signals, 1):
        f.write(f"## {i}. {signal['headline']}\n\n")
        f.write(f"**Date:** {signal['date_detected']}  \n")
        f.write(f"**Type:** {signal['signal_type']}  \n")
        f.write(f"**Source:** {signal['source']}  \n")
        f.write(f"**Confidence:** {signal['confidence_level']}  \n\n")
        f.write(f"{signal['description']}\n\n")
        if signal.get('source_url'):
            f.write(f"[Source]({signal['source_url']})\n\n")
        f.write("---\n\n")

print(f"✓ Saved Markdown: {md_path}")

# 4. Print summary
summary = aggregator.generate_summary_report(signals)
print(f"\n📊 Summary:")
print(f"   • Total: {summary['total_signals']}")
print(f"   • Types: {len(summary['by_type'])}")
print(f"   • Sources: {len(summary['by_source'])}")
print(f"   • Date range: {summary['date_range']['earliest']} to {summary['date_range']['latest']}")
```

**Output:**
```
✓ Saved JSON: outputs/aggregated/signals.json
✓ Saved CSV: outputs/aggregated/signals.csv
✓ Saved Markdown: outputs/aggregated/signals_report.md

📊 Summary:
   • Total: 20
   • Types: 8
   • Sources: 3
   • Date range: 2025-09-25 to 2025-11-05
```

---

## Best Practices Summary

1. **Choose the Right Timeframe**
   - Daily briefings: `days_lookback=1`
   - Weekly reviews: `days_lookback=7`
   - Monthly planning: `days_lookback=30`
   - Quarterly strategy: `days_lookback=90`

2. **Set Appropriate Confidence Levels**
   - Executive reports: `min_confidence='high'`
   - Team briefings: `min_confidence='medium'`
   - Research/monitoring: `min_confidence='low'`

3. **Filter by Relevance**
   - Use custom filters for your specific use case
   - Combine multiple signal types for comprehensive analysis
   - Create domain-specific scoring functions

4. **Automate Regular Reports**
   - Schedule daily/weekly aggregation
   - Save to standard locations
   - Export in multiple formats for different audiences

5. **Monitor Data Quality**
   - Check signal counts and sources
   - Review confidence distributions
   - Validate date ranges

---

## Troubleshooting

**No signals returned:**
- Increase `days_lookback` parameter
- Lower `min_confidence` to 'low'
- Check if data collector files exist

**Too many duplicates:**
- Signals are already deduplicated automatically
- If still seeing duplicates, adjust similarity threshold in code

**Missing expected signals:**
- Check if signals are filtered by confidence level
- Verify date range covers the expected period
- Ensure source data files are up to date

---

## Next Steps

1. Try the examples above with your data
2. Customize parameters for your use case
3. Create automated daily/weekly reports
4. Integrate with your workflow (email, Slack, dashboard)
5. Build custom filters and scoring functions
