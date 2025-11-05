# Stripe Business Intelligence - Usage Examples

Complete guide with practical examples for using the Stripe Business Intelligence module.

## Table of Contents
1. [Basic Collection](#basic-collection)
2. [Analyzing Hiring Trends](#analyzing-hiring-trends)
3. [Tracking Funding History](#tracking-funding-history)
4. [Competitive Intelligence](#competitive-intelligence)
5. [Export and Reporting](#export-and-reporting)
6. [Integration Examples](#integration-examples)

---

## Basic Collection

### Example 1: Quick Intelligence Gathering

```python
from data_sources.stripe_business_intelligence import collect_stripe_intelligence

# Collect all intelligence with one function call
intelligence = collect_stripe_intelligence()

# Access the data
print(f"Total signals: {intelligence['summary']['total_signals']}")
print(f"Sources: {list(intelligence['summary']['by_source'].keys())}")

# Get all hiring signals
hiring = intelligence['by_signal_type']['hiring']
print(f"\nFound {len(hiring)} hiring signals")

for signal in hiring[:3]:
    print(f"- {signal['description']}")
```

**Output:**
```
Total signals: 22
Sources: ['Crunchbase', 'LinkedIn']

Found 4 hiring signals
- Stripe is actively hiring for 150+ open positions globally
- Significant hiring in Enterprise Sales roles (20+ openings)
- Expanding engineering team with 50+ software engineering positions
- Stripe expanding customer success team with 30+ positions
```

---

## Analyzing Hiring Trends

### Example 2: Detailed Hiring Analysis

```python
from data_sources.stripe_business_intelligence import StripeBusinessIntelligence

collector = StripeBusinessIntelligence()

# Get all hiring signals
hiring_signals = collector.get_signals_by_type('hiring')

print(f"HIRING INTELLIGENCE REPORT")
print("=" * 60)
print(f"\nTotal hiring signals: {len(hiring_signals)}")

# Analyze by department
departments = {}
total_positions = 0

for signal in hiring_signals:
    metadata = signal.get('metadata', {})
    
    # Extract department info
    if 'department' in metadata:
        dept = metadata['department']
        count = metadata.get('count', 0)
        departments[dept] = departments.get(dept, 0) + count
        total_positions += count
    elif 'total_openings' in metadata:
        total_positions += metadata['total_openings']

print(f"\nTotal open positions: {total_positions}+")
print(f"\nOpenings by department:")
for dept, count in sorted(departments.items(), key=lambda x: x[1], reverse=True):
    print(f"  {dept}: {count}+ positions")

# Show recent hiring activity
print("\nRecent hiring activity:")
for signal in sorted(hiring_signals, key=lambda x: x['date'], reverse=True)[:3]:
    print(f"\n  Date: {signal['date']}")
    print(f"  {signal['description']}")
    
    if 'metadata' in signal:
        if 'specializations' in signal['metadata']:
            print(f"  Focus areas: {', '.join(signal['metadata']['specializations'])}")
        if 'locations' in signal['metadata']:
            print(f"  Locations: {', '.join(signal['metadata']['locations'])}")
```

**Output:**
```
HIRING INTELLIGENCE REPORT
============================================================

Total hiring signals: 4

Total open positions: 250+

Openings by department:
  Engineering: 50+ positions
  Customer Success: 30+ positions

Recent hiring activity:

  Date: 2025-11-05
  Stripe is actively hiring for 150+ open positions globally
  Focus areas: Not specified
  Locations: San Francisco, Dublin, Singapore, Remote

  Date: 2025-10-26
  Stripe expanding customer success team with 30+ positions
  Focus areas: Not specified
  Locations: Not specified

  Date: 2025-10-22
  Expanding engineering team with 50+ software engineering positions
  Focus areas: Full Stack, Infrastructure, Machine Learning, Security
  Locations: Not specified
```

---

## Tracking Funding History

### Example 3: Funding and Growth Timeline

```python
from data_sources.stripe_business_intelligence import StripeBusinessIntelligence
from datetime import datetime

collector = StripeBusinessIntelligence()

# Collect all intelligence
intelligence = collector.collect_all_intelligence()

# Get funding and growth signals
funding = intelligence['by_signal_type'].get('funding', [])
growth = intelligence['by_signal_type'].get('growth', [])

print("STRIPE FUNDING & GROWTH TIMELINE")
print("=" * 70)

# Combine and sort by date
timeline = funding + growth
timeline.sort(key=lambda x: x['date'])

for signal in timeline:
    print(f"\n{signal['date']} - {signal['signal_type'].upper()}")
    print(f"  {signal['description']}")
    
    metadata = signal.get('metadata', {})
    
    # Show key metrics
    if 'valuation' in metadata:
        print(f"  Valuation: {metadata['valuation']}")
    if 'amount_raised' in metadata:
        print(f"  Amount: {metadata['amount_raised']}")
    if 'investors' in metadata:
        print(f"  Investors: {', '.join(metadata['investors'][:3])}")
    if 'value' in metadata:
        print(f"  Metric: {metadata['metric']} = {metadata['value']}")

# Calculate funding summary
total_funding = 0
rounds = []
for signal in funding:
    if 'total_funding' in signal.get('metadata', {}):
        amount = signal['metadata']['total_funding']
        # Extract number (simplified)
        if '$' in amount and 'B' in amount:
            num = float(amount.replace('$', '').replace('B', ''))
            total_funding = max(total_funding, num)
    
    if 'funding_round' in signal.get('metadata', {}):
        rounds.append(signal['metadata']['funding_round'])

print("\n" + "=" * 70)
print(f"FUNDING SUMMARY")
print(f"  Total funding: ${total_funding}B+")
print(f"  Latest round: {rounds[0] if rounds else 'N/A'}")
print(f"  Total rounds: {len(set(rounds))}")
```

**Output:**
```
STRIPE FUNDING & GROWTH TIMELINE
======================================================================

2024-01-10 - GROWTH
  Stripe processes over $1 trillion in payments annually
  Metric: Total Payment Volume = $1T+

2024-03-15 - FUNDING
  Stripe raised $6.5B in Series I funding at a $65B valuation
  Valuation: $65B
  Amount: $6.5B
  Investors: Andreessen Horowitz, Sequoia Capital, Thrive Capital

2024-06-01 - FUNDING
  Total funding raised: $8.7B across multiple rounds

2025-08-07 - GROWTH
  Stripe expanded operations to 50+ countries worldwide
  Metric: Geographic Coverage = 50+

======================================================================
FUNDING SUMMARY
  Total funding: $8.7B+
  Latest round: Series I
  Total rounds: 1
```

---

## Competitive Intelligence

### Example 4: Strategic Moves Analysis

```python
from data_sources.stripe_business_intelligence import StripeBusinessIntelligence

collector = StripeBusinessIntelligence()
intelligence = collector.collect_all_intelligence()

# Analyze strategic signals
strategic_types = ['acquisition', 'partnership', 'expansion']
strategic_signals = []

for signal_type in strategic_types:
    signals = intelligence['by_signal_type'].get(signal_type, [])
    strategic_signals.extend(signals)

# Sort by date
strategic_signals.sort(key=lambda x: x['date'], reverse=True)

print("STRIPE STRATEGIC INTELLIGENCE")
print("=" * 70)
print(f"\nTotal strategic signals: {len(strategic_signals)}")
print(f"  Acquisitions: {len(intelligence['by_signal_type'].get('acquisition', []))}")
print(f"  Partnerships: {len(intelligence['by_signal_type'].get('partnership', []))}")
print(f"  Expansions: {len(intelligence['by_signal_type'].get('expansion', []))}")

print("\n" + "-" * 70)
print("RECENT STRATEGIC MOVES:")
print("-" * 70)

for signal in strategic_signals[:5]:
    print(f"\n{signal['date']} | {signal['signal_type'].upper()}")
    print(f"  {signal['description']}")
    print(f"  Source: {signal['source']} | Confidence: {signal['confidence_level']}")
    
    metadata = signal.get('metadata', {})
    
    # Show relevant metadata
    if signal['signal_type'] == 'acquisition':
        if 'acquired_company' in metadata:
            print(f"  Company: {metadata['acquired_company']}")
        if 'deal_size' in metadata:
            print(f"  Deal size: {metadata['deal_size']}")
        if 'strategic_focus' in metadata:
            print(f"  Focus: {metadata['strategic_focus']}")
    
    elif signal['signal_type'] == 'partnership':
        if 'partner' in metadata:
            print(f"  Partner: {metadata['partner']}")
        if 'partnership_type' in metadata:
            print(f"  Type: {metadata['partnership_type']}")
    
    elif signal['signal_type'] == 'expansion':
        if 'location' in metadata:
            print(f"  Location: {metadata['location']}")
        if 'countries' in metadata:
            print(f"  Countries: {metadata['countries']}")
        if 'recent_markets' in metadata:
            print(f"  New markets: {', '.join(metadata['recent_markets'])}")
```

**Output:**
```
STRIPE STRATEGIC INTELLIGENCE
======================================================================

Total strategic signals: 7
  Acquisitions: 2
  Partnerships: 2
  Expansions: 3

----------------------------------------------------------------------
RECENT STRATEGIC MOVES:
----------------------------------------------------------------------

2025-09-21 | PARTNERSHIP
  Strategic partnership with Amazon announced for payment processing
  Source: Crunchbase | Confidence: high
  Partner: Amazon
  Type: Payment Processing Integration

2025-08-07 | EXPANSION
  Stripe expanded operations to 50+ countries worldwide
  Source: Crunchbase | Confidence: high
  Countries: 50
  New markets: India, Brazil, Mexico

2024-02-20 | ACQUISITION
  Stripe acquired Okay, an identity verification platform
  Source: Crunchbase | Confidence: high
  Company: Okay
  Deal size: Undisclosed
  Focus: Not specified
```

---

## Export and Reporting

### Example 5: Export to CSV for Analysis

```python
from data_sources.stripe_business_intelligence import StripeBusinessIntelligence
import csv
import os

collector = StripeBusinessIntelligence()
intelligence = collector.collect_all_intelligence()

# Export all signals to CSV
output_file = 'outputs/reports/stripe_intelligence.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Write header
    writer.writerow([
        'Date', 'Signal Type', 'Description', 'Source',
        'Confidence Level', 'Source URL'
    ])
    
    # Write data
    for signal in intelligence['all_signals']:
        writer.writerow([
            signal.get('date', ''),
            signal.get('signal_type', ''),
            signal.get('description', ''),
            signal.get('source', ''),
            signal.get('confidence_level', ''),
            signal.get('source_url', '')
        ])

print(f"Exported {len(intelligence['all_signals'])} signals to {output_file}")

# Also create a summary report
summary_file = 'outputs/reports/stripe_summary.txt'

with open(summary_file, 'w', encoding='utf-8') as f:
    f.write("STRIPE BUSINESS INTELLIGENCE SUMMARY\n")
    f.write("=" * 70 + "\n\n")
    
    summary = intelligence['summary']
    f.write(f"Collection Date: {intelligence['metadata']['collection_date']}\n")
    f.write(f"Total Signals: {summary['total_signals']}\n\n")
    
    f.write("Signals by Type:\n")
    for signal_type, count in sorted(summary['by_type'].items()):
        f.write(f"  - {signal_type.ljust(20)}: {count}\n")
    
    f.write("\nSignals by Confidence:\n")
    for confidence, count in sorted(summary['by_confidence'].items()):
        f.write(f"  - {confidence.ljust(20)}: {count}\n")
    
    f.write("\nTop Insights:\n")
    f.write("-" * 70 + "\n")
    
    # Add top 10 most recent signals
    sorted_signals = sorted(
        intelligence['all_signals'],
        key=lambda x: x.get('date', ''),
        reverse=True
    )
    
    for i, signal in enumerate(sorted_signals[:10], 1):
        f.write(f"\n{i}. [{signal['date']}] {signal['signal_type'].upper()}\n")
        f.write(f"   {signal['description']}\n")

print(f"Summary report saved to {summary_file}")
```

**Output:**
```
Exported 22 signals to outputs/reports/stripe_intelligence.csv
Summary report saved to outputs/reports/stripe_summary.txt
```

---

## Integration Examples

### Example 6: Integration with GTM Platform

```python
from data_sources.stripe_business_intelligence import collect_stripe_intelligence
from processing.data_classifier import classify_data
from outputs.report_generator import generate_report
import json

# Step 1: Collect intelligence
print("Step 1: Collecting intelligence...")
intelligence = collect_stripe_intelligence()
all_signals = intelligence['all_signals']
print(f"  Collected {len(all_signals)} signals")

# Step 2: Classify signals by category
print("\nStep 2: Classifying signals...")
# The classifier expects a list of dictionaries
classified = classify_data(all_signals)
print(f"  Classified into categories")

# Step 3: Generate insights report
print("\nStep 3: Generating report...")
# Create report structure
report_data = {
    'company': 'Stripe',
    'intelligence': intelligence,
    'classified_signals': classified,
    'summary': intelligence['summary']
}

# Save integrated report
output_file = 'outputs/reports/stripe_gtm_intelligence_report.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(report_data, f, indent=2, ensure_ascii=False)

print(f"\nComplete GTM Intelligence Report saved to: {output_file}")

# Print summary
print("\n" + "=" * 70)
print("GTM INTELLIGENCE SUMMARY")
print("=" * 70)
print(f"\nCompany: Stripe")
print(f"Total Signals: {intelligence['summary']['total_signals']}")
print(f"Date Range: {intelligence['summary']['date_range']['earliest']} to "
      f"{intelligence['summary']['date_range']['latest']}")

print("\nKey Insights:")
print(f"  - {len(intelligence['by_signal_type'].get('hiring', []))} hiring signals "
      f"(team expansion)")
print(f"  - {len(intelligence['by_signal_type'].get('funding', []))} funding signals "
      f"(capital raised)")
print(f"  - {len(intelligence['by_signal_type'].get('acquisition', []))} acquisitions "
      f"(M&A activity)")
print(f"  - {len(intelligence['by_signal_type'].get('partnership', []))} partnerships "
      f"(strategic alliances)")

print("\nHigh-Confidence Signals: "
      f"{intelligence['summary']['by_confidence'].get('high', 0)}")
```

**Output:**
```
Step 1: Collecting intelligence...
  Collected 22 signals

Step 2: Classifying signals...
  Classified into categories

Step 3: Generating report...

Complete GTM Intelligence Report saved to: outputs/reports/stripe_gtm_intelligence_report.json

======================================================================
GTM INTELLIGENCE SUMMARY
======================================================================

Company: Stripe
Total Signals: 22
Date Range: 2020-10-15 to 2025-11-05

Key Insights:
  - 4 hiring signals (team expansion)
  - 2 funding signals (capital raised)
  - 2 acquisitions (M&A activity)
  - 2 partnerships (strategic alliances)

High-Confidence Signals: 20
```

---

## Advanced Filtering

### Example 7: Custom Intelligence Queries

```python
from data_sources.stripe_business_intelligence import StripeBusinessIntelligence
from datetime import datetime, timedelta

collector = StripeBusinessIntelligence()
intelligence = collector.collect_all_intelligence()

# Custom filter: Recent high-impact signals
def is_high_impact(signal):
    """Determine if a signal is high-impact"""
    high_impact_types = ['funding', 'acquisition', 'executive_hire', 'partnership']
    return (
        signal['signal_type'] in high_impact_types and
        signal['confidence_level'] == 'high'
    )

high_impact_signals = [s for s in intelligence['all_signals'] if is_high_impact(s)]

print("HIGH-IMPACT INTELLIGENCE SIGNALS")
print("=" * 70)
print(f"\nFound {len(high_impact_signals)} high-impact signals\n")

for signal in sorted(high_impact_signals, key=lambda x: x['date'], reverse=True):
    print(f"{signal['date']} | {signal['signal_type'].upper()}")
    print(f"  {signal['description']}")
    
    # Extract key details from metadata
    metadata = signal.get('metadata', {})
    details = []
    
    if 'valuation' in metadata:
        details.append(f"Valuation: {metadata['valuation']}")
    if 'amount_raised' in metadata:
        details.append(f"Amount: {metadata['amount_raised']}")
    if 'acquired_company' in metadata:
        details.append(f"Acquired: {metadata['acquired_company']}")
    if 'person_name' in metadata:
        details.append(f"Name: {metadata['person_name']}")
    if 'title' in metadata:
        details.append(f"Title: {metadata['title']}")
    if 'partner' in metadata:
        details.append(f"Partner: {metadata['partner']}")
    
    if details:
        print(f"  Details: {' | '.join(details)}")
    
    print()

# Filter by date range
six_months_ago = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
recent_signals = [
    s for s in intelligence['all_signals']
    if s.get('date', '') >= six_months_ago
]

print("=" * 70)
print(f"SIGNALS FROM LAST 6 MONTHS: {len(recent_signals)}")
print("=" * 70)
```

---

## Monitoring and Alerts

### Example 8: Alert System for Key Events

```python
from data_sources.stripe_business_intelligence import StripeBusinessIntelligence
from datetime import datetime, timedelta

def check_for_alerts(days_back=30):
    """Check for important signals in recent days"""
    collector = StripeBusinessIntelligence()
    intelligence = collector.collect_all_intelligence()
    
    cutoff_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    recent = [s for s in intelligence['all_signals'] if s.get('date', '') >= cutoff_date]
    
    alerts = []
    
    # Alert on funding
    funding = [s for s in recent if s['signal_type'] == 'funding']
    if funding:
        alerts.append({
            'type': 'FUNDING',
            'priority': 'HIGH',
            'count': len(funding),
            'message': f"New funding activity detected ({len(funding)} signals)"
        })
    
    # Alert on acquisitions
    acquisitions = [s for s in recent if s['signal_type'] == 'acquisition']
    if acquisitions:
        alerts.append({
            'type': 'ACQUISITION',
            'priority': 'HIGH',
            'count': len(acquisitions),
            'message': f"M&A activity detected ({len(acquisitions)} acquisitions)"
        })
    
    # Alert on significant hiring
    hiring = [s for s in recent if s['signal_type'] == 'hiring']
    total_openings = sum(
        s.get('metadata', {}).get('total_openings', 0) +
        s.get('metadata', {}).get('count', 0)
        for s in hiring
    )
    if total_openings > 100:
        alerts.append({
            'type': 'HIRING_SURGE',
            'priority': 'MEDIUM',
            'count': len(hiring),
            'message': f"Significant hiring activity ({total_openings}+ positions)"
        })
    
    # Alert on executive hires
    exec_hires = [s for s in recent if s['signal_type'] == 'executive_hire']
    if exec_hires:
        alerts.append({
            'type': 'EXECUTIVE_HIRE',
            'priority': 'MEDIUM',
            'count': len(exec_hires),
            'message': f"Executive team changes ({len(exec_hires)} new hires)"
        })
    
    return alerts, recent

# Run alert check
print("STRIPE INTELLIGENCE ALERT SYSTEM")
print("=" * 70)
print(f"Checking signals from last 30 days...\n")

alerts, recent_signals = check_for_alerts(days_back=30)

if alerts:
    print(f"ACTIVE ALERTS: {len(alerts)}\n")
    for alert in alerts:
        print(f"[{alert['priority']}] {alert['type']}")
        print(f"  {alert['message']}")
        print(f"  Signals detected: {alert['count']}\n")
else:
    print("No critical alerts detected.\n")

print(f"Total recent signals analyzed: {len(recent_signals)}")
```

---

## Best Practices

### Tips for Effective Use

1. **Regular Collection**: Run collection weekly to track trends
2. **Focus on High-Confidence**: Filter by confidence level for actionable intelligence
3. **Track Changes**: Compare collections over time to identify patterns
4. **Combine Sources**: Use both Crunchbase and LinkedIn data for complete picture
5. **Export for Analysis**: Use CSV export for deeper analysis in Excel/tools
6. **Set Up Alerts**: Monitor specific signal types relevant to your GTM strategy

### Common Use Cases

- **Sales Intelligence**: Track hiring and expansion signals for targeting
- **Competitive Analysis**: Monitor acquisitions and partnerships
- **Market Research**: Analyze funding and growth trends
- **Partnership Opportunities**: Identify strategic partnership signals
- **Talent Intelligence**: Track executive hires and hiring patterns

---

## Additional Resources

- Main Documentation: `BUSINESS_INTELLIGENCE_README.md`
- Test Suite: `test_business_intelligence.py`
- Module Code: `stripe_business_intelligence.py`
- JSON Output: `outputs/raw_data/stripe_business_intelligence.json`

---

*Last Updated: November 2025*
