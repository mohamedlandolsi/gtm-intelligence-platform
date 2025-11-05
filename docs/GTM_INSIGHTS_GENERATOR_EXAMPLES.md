# GTM Insights Generator - Practical Examples

## Table of Contents
1. [Basic Insight Generation](#example-1-basic-insight-generation)
2. [Competitive Battle Card Creation](#example-2-competitive-battle-card-creation)
3. [Product Roadmap Gap Analysis](#example-3-product-roadmap-gap-analysis)
4. [Market Timing Optimization](#example-4-market-timing-optimization)
5. [Sales Enablement Content](#example-5-sales-enablement-content)
6. [Executive Dashboard](#example-6-executive-dashboard)
7. [Weekly Intelligence Briefing](#example-7-weekly-intelligence-briefing)
8. [Trend Tracking Over Time](#example-8-trend-tracking-over-time)

---

## Example 1: Basic Insight Generation

Generate insights from classified signals and explore the results.

```python
from processing.gtm_insights_generator import generate_gtm_insights
import json

# Load classified signals
with open('outputs/classified/gtm_classified_signals.json', 'r') as f:
    data = json.load(f)
    classified_signals = data['classified_signals']

# Generate insights
print("Generating GTM insights...")
insights = generate_gtm_insights(classified_signals)

# Display summary
print(f"\n{'='*80}")
print("GTM INSIGHTS SUMMARY")
print(f"{'='*80}")
print(f"Total Signals Analyzed: {insights['metadata']['total_signals_analyzed']}")
print(f"Total Insights Generated: {insights['executive_summary']['total_insights_generated']}")
print(f"Categories Covered: {', '.join(insights['metadata']['categories_analyzed'])}")

# Show insights by category
for category, cat_insights in insights['insights_by_category'].items():
    print(f"\n{category} ({cat_insights['total_signals']} signals):")
    
    for insight in cat_insights['insights']:
        print(f"\n  [Confidence: {insight['confidence_level'].upper()}]")
        print(f"  Finding: {insight['insight_text'][:100]}...")
        print(f"  Action: {insight['recommended_action'][:100]}...")

# Display strategic summary
print(f"\n{'='*80}")
print("STRATEGIC SUMMARY")
print(f"{'='*80}")
print(insights['executive_summary']['strategic_summary'])
```

**Output:**
```
Generating GTM insights...

================================================================================
GTM INSIGHTS SUMMARY
================================================================================
Total Signals Analyzed: 20
Total Insights Generated: 10
Categories Covered: TIMING, PRODUCT, TALENT, MARKET

PRODUCT (16 signals):

  [Confidence: HIGH]
  Finding: High product development velocity detected: 16 product signals...
  Action: Expect rapid feature releases. Prioritize parity on core features...

TALENT (2 signals):

  [Confidence: HIGH]
  Finding: Aggressive hiring detected: 150+ open positions...
  Action: Monitor department-level hiring to identify strategic priorities...

================================================================================
STRATEGIC SUMMARY
================================================================================
Strategic picture: High product development activity (16 signals), 
market tailwinds present, organizational expansion (2 hiring signals). 
Recommend multi-dimensional GTM approach targeting identified gaps.
```

---

## Example 2: Competitive Battle Card Creation

Generate competitive intelligence battle cards from insights.

```python
from processing.gtm_insights_generator import generate_gtm_insights
import json

# Load and generate insights
with open('outputs/classified/gtm_classified_signals.json', 'r') as f:
    data = json.load(f)
    classified_signals = data['classified_signals']

insights = generate_gtm_insights(classified_signals)

# Create competitive battle card
def create_battle_card(insights):
    """Generate competitive battle card from insights"""
    
    battle_card = {
        'competitor': 'Stripe',
        'last_updated': insights['metadata']['generation_date'],
        'strengths': [],
        'weaknesses': [],
        'attack_vectors': [],
        'counter_positioning': [],
        'sales_talking_points': []
    }
    
    # Extract from COMPETITIVE insights
    if 'COMPETITIVE' in insights['insights_by_category']:
        comp_insights = insights['insights_by_category']['COMPETITIVE']
        
        for insight in comp_insights['insights']:
            # Extract vulnerabilities as attack vectors
            if 'vulnerabilit' in insight['insight_text'].lower():
                battle_card['weaknesses'].append(insight['insight_text'])
                battle_card['attack_vectors'].append(insight['recommended_action'])
    
    # Extract from PRODUCT insights
    if 'PRODUCT' in insights['insights_by_category']:
        product_insights = insights['insights_by_category']['PRODUCT']
        
        for insight in product_insights['insights']:
            # High velocity = strength
            if 'velocity' in insight['insight_text'].lower():
                battle_card['strengths'].append(insight['insight_text'])
            
            # Product gaps = attack opportunities
            if 'gap' in insight['insight_text'].lower():
                battle_card['attack_vectors'].append(insight['recommended_action'])
    
    # Extract from MESSAGING insights
    if 'MESSAGING' in insights['insights_by_category']:
        msg_insights = insights['insights_by_category']['MESSAGING']
        
        for insight in msg_insights['insights']:
            battle_card['counter_positioning'].append(insight['recommended_action'])
            # Extract talking points
            if 'talking point' in insight['recommended_action'].lower():
                battle_card['sales_talking_points'].append(
                    insight['recommended_action'].split('Talking points:')[1].strip()
                    if 'Talking points:' in insight['recommended_action'] else ''
                )
    
    # Extract from TALENT insights
    if 'TALENT' in insights['insights_by_category']:
        talent_insights = insights['insights_by_category']['TALENT']
        
        for insight in talent_insights['insights']:
            # Large org = potential weakness
            if 'bureaucracy' in insight['insight_text'].lower():
                battle_card['weaknesses'].append(insight['insight_text'])
                battle_card['counter_positioning'].append(insight['recommended_action'])
    
    return battle_card

# Generate battle card
battle_card = create_battle_card(insights)

# Display battle card
print("="*80)
print(f"COMPETITIVE BATTLE CARD - {battle_card['competitor']}")
print("="*80)
print(f"Last Updated: {battle_card['last_updated']}\n")

print("COMPETITOR STRENGTHS:")
for i, strength in enumerate(battle_card['strengths'], 1):
    print(f"{i}. {strength}\n")

print("\nCOMPETITOR WEAKNESSES:")
for i, weakness in enumerate(battle_card['weaknesses'], 1):
    print(f"{i}. {weakness}\n")

print("\nATTACK VECTORS:")
for i, vector in enumerate(battle_card['attack_vectors'], 1):
    print(f"{i}. {vector}\n")

print("\nCOUNTER-POSITIONING STRATEGY:")
for i, strategy in enumerate(battle_card['counter_positioning'], 1):
    print(f"{i}. {strategy}\n")

# Save battle card
with open('outputs/insights/competitive_battle_card.json', 'w') as f:
    json.dump(battle_card, f, indent=2)

print("\nBattle card saved to: outputs/insights/competitive_battle_card.json")
```

---

## Example 3: Product Roadmap Gap Analysis

Identify gaps in competitor's product roadmap to inform your product strategy.

```python
from processing.gtm_insights_generator import generate_gtm_insights
import json

# Load and generate insights
with open('outputs/classified/gtm_classified_signals.json', 'r') as f:
    data = json.load(f)
    classified_signals = data['classified_signals']

insights = generate_gtm_insights(classified_signals)

# Extract product insights
product_insights = insights['insights_by_category'].get('PRODUCT', {})

print("="*80)
print("PRODUCT ROADMAP GAP ANALYSIS")
print("="*80)

# Analyze what they're building
print("\nCOMPETITOR'S FOCUS AREAS:")
for insight in product_insights.get('insights', []):
    if 'roadmap focus' in insight['insight_text'].lower():
        # Extract focus areas
        text = insight['insight_text']
        if ':' in text:
            focus_areas = text.split(':')[1].split('.')[0]
            print(f"  {focus_areas}")
        
        print(f"\nSupporting Evidence:")
        for signal in insight['supporting_signals'][:3]:
            print(f"  - {signal}")

print("\n" + "="*80)
print("IDENTIFIED PRODUCT GAPS")
print("="*80)

# Extract gaps from recommendations
for insight in product_insights.get('insights', []):
    if 'gap' in insight['insight_text'].lower() or 'gap' in insight['recommended_action'].lower():
        print(f"\nGap Finding:")
        print(f"  {insight['insight_text']}")
        
        print(f"\nRecommendation:")
        print(f"  {insight['recommended_action']}")
        
        print(f"\nConfidence: {insight['confidence_level'].upper()}")

# Generate gap-based product strategy
print("\n" + "="*80)
print("RECOMMENDED PRODUCT STRATEGY")
print("="*80)

strategy = {
    'differentiation_opportunities': [],
    'build_priorities': [],
    'avoid_areas': []
}

for insight in product_insights.get('insights', []):
    action = insight['recommended_action']
    
    # Parse gap recommendations
    if 'gap' in action.lower():
        # Extract specific gaps
        if 'Fraud Prevention' in action or 'Analytics' in action or 'Reporting' in action:
            strategy['differentiation_opportunities'].append(action)
    
    # Identify what to avoid (their strengths)
    if 'velocity' in insight['insight_text'].lower():
        strategy['avoid_areas'].append(
            "Avoid competing on raw feature velocity - focus on quality and reliability instead"
        )
    
    # Parse build priorities
    if 'build' in action.lower() or 'consider' in action.lower():
        strategy['build_priorities'].append(action)

print("\nDifferentiation Opportunities:")
for i, opp in enumerate(strategy['differentiation_opportunities'], 1):
    print(f"{i}. {opp}")

print("\nBuild Priorities:")
for i, priority in enumerate(strategy['build_priorities'], 1):
    print(f"{i}. {priority}")

print("\nAreas to Avoid:")
for i, avoid in enumerate(strategy['avoid_areas'], 1):
    print(f"{i}. {avoid}")
```

---

## Example 4: Market Timing Optimization

Optimize market timing and campaign scheduling based on insights.

```python
from processing.gtm_insights_generator import generate_gtm_insights
import json
from datetime import datetime, timedelta

# Load and generate insights
with open('outputs/classified/gtm_classified_signals.json', 'r') as f:
    data = json.load(f)
    classified_signals = data['classified_signals']

insights = generate_gtm_insights(classified_signals)

# Extract timing insights
timing_insights = insights['insights_by_category'].get('TIMING', {})
product_insights = insights['insights_by_category'].get('PRODUCT', {})

print("="*80)
print("MARKET TIMING OPTIMIZATION")
print("="*80)

# Analyze launch windows
print("\nLAUNCH WINDOW ANALYSIS:")
for insight in timing_insights.get('insights', []):
    if 'launch' in insight['insight_text'].lower() or 'window' in insight['insight_text'].lower():
        print(f"\nFinding: {insight['insight_text']}")
        print(f"Action: {insight['recommended_action']}")

# Identify competitor launch cycles
print("\n" + "="*80)
print("COMPETITOR LAUNCH CYCLE")
print("="*80)

for insight in timing_insights.get('insights', []):
    if 'quarter' in insight['insight_text'].lower():
        print(f"\nPattern Detected: {insight['insight_text']}")
        print(f"\nTiming Strategy: {insight['recommended_action']}")

# Check for coordinated launches (cross-category)
print("\n" + "="*80)
print("COORDINATED LAUNCH DETECTION")
print("="*80)

for cross_insight in insights.get('cross_category_insights', []):
    if 'launch cycle' in cross_insight['insight_text'].lower():
        print(f"\nAlert: {cross_insight['insight_text']}")
        print(f"\nCounter-Strategy: {cross_insight['recommended_action']}")

# Generate timing recommendations
print("\n" + "="*80)
print("RECOMMENDED TIMING STRATEGY")
print("="*80)

timing_strategy = {
    'immediate_actions': [],
    'q1_recommendations': [],
    'q2_recommendations': [],
    'avoid_periods': []
}

# Parse recommendations
current_month = datetime.now().month

for insight in timing_insights.get('insights', []):
    action = insight['recommended_action']
    
    if insight['confidence_level'] == 'high':
        timing_strategy['immediate_actions'].append(action)
    
    # Map to quarters
    if 'quarter' in action.lower():
        if current_month <= 3:
            timing_strategy['q1_recommendations'].append(action)
        elif current_month <= 6:
            timing_strategy['q2_recommendations'].append(action)

# Look for beta signals indicating upcoming launches
for insight in timing_insights.get('insights', []):
    if 'beta' in insight['insight_text'].lower() or 'preview' in insight['insight_text'].lower():
        # Avoid launching during their GA window
        timing_strategy['avoid_periods'].append(
            "Avoid launching during competitor's GA release window (estimated 3-6 months from beta)"
        )

print("\nImmediate Actions (High Priority):")
for i, action in enumerate(timing_strategy['immediate_actions'], 1):
    print(f"{i}. {action}")

print("\nQ1 Timing Recommendations:")
for i, rec in enumerate(timing_strategy['q1_recommendations'], 1):
    print(f"{i}. {rec}")

print("\nPeriods to Avoid:")
for i, avoid in enumerate(timing_strategy['avoid_periods'], 1):
    print(f"{i}. {avoid}")
```

---

## Example 5: Sales Enablement Content

Generate sales enablement materials from competitive insights.

```python
from processing.gtm_insights_generator import generate_gtm_insights
import json

# Load and generate insights
with open('outputs/classified/gtm_classified_signals.json', 'r') as f:
    data = json.load(f)
    classified_signals = data['classified_signals']

insights = generate_gtm_insights(classified_signals)

print("="*80)
print("SALES ENABLEMENT CONTENT")
print("="*80)

# Generate competitive objection handlers
print("\n" + "="*80)
print("COMPETITIVE OBJECTION HANDLERS")
print("="*80)

objection_handlers = []

# From COMPETITIVE insights
if 'COMPETITIVE' in insights['insights_by_category']:
    comp_insights = insights['insights_by_category']['COMPETITIVE']
    
    for insight in comp_insights['insights']:
        if 'vulnerabilit' in insight['insight_text'].lower():
            handler = {
                'objection': f"Customer says: 'We're considering {insight['insight_text'].split()[0]}'",
                'response': insight['recommended_action'],
                'confidence': insight['confidence_level']
            }
            objection_handlers.append(handler)

# From TALENT insights (org size objection)
if 'TALENT' in insights['insights_by_category']:
    talent_insights = insights['insights_by_category']['TALENT']
    
    for insight in talent_insights['insights']:
        if 'organization' in insight['insight_text'].lower():
            handler = {
                'objection': "Customer says: 'Stripe is a much larger company'",
                'response': insight['recommended_action'],
                'confidence': insight['confidence_level']
            }
            objection_handlers.append(handler)

for i, handler in enumerate(objection_handlers, 1):
    print(f"\nObjection {i}: {handler['objection']}")
    print(f"Response: {handler['response']}")
    print(f"Confidence: {handler['confidence'].upper()}")

# Generate differentiation talking points
print("\n" + "="*80)
print("DIFFERENTIATION TALKING POINTS")
print("="*80)

talking_points = []

# Extract from all categories
for category, cat_insights in insights['insights_by_category'].items():
    for insight in cat_insights['insights']:
        action = insight['recommended_action']
        
        # Look for positioning statements
        if 'position' in action.lower() or 'emphasize' in action.lower():
            talking_points.append({
                'category': category,
                'point': action,
                'confidence': insight['confidence_level']
            })

# High confidence points first
talking_points.sort(key=lambda x: (x['confidence'] != 'high', x['confidence'] != 'medium'))

for i, point in enumerate(talking_points[:5], 1):
    print(f"\n{i}. [{point['category']}] {point['point']}")

# Generate competitive comparison table
print("\n" + "="*80)
print("COMPETITIVE COMPARISON TABLE")
print("="*80)

comparison = {
    'features': {'us': [], 'them': []},
    'advantages': {'us': [], 'them': []},
    'ideal_for': {'us': [], 'them': []}
}

# Parse product insights for comparison
if 'PRODUCT' in insights['insights_by_category']:
    product_insights = insights['insights_by_category']['PRODUCT']
    
    for insight in product_insights['insights']:
        # Their advantages
        if 'velocity' in insight['insight_text'].lower():
            comparison['advantages']['them'].append('Rapid feature releases')
            comparison['advantages']['us'].append('Stable, reliable features')
        
        # Our advantages (from gaps)
        if 'gap' in insight['recommended_action'].lower():
            gaps = ['Fraud Prevention', 'Analytics', 'Reporting']
            comparison['advantages']['us'].extend(gaps)

# Parse ICP insights
if 'ICP' in insights['insights_by_category']:
    icp_insights = insights['insights_by_category']['ICP']
    
    for insight in icp_insights['insights']:
        if 'segment' in insight['insight_text'].lower():
            comparison['ideal_for']['them'].append('Developers, Enterprise')
            comparison['ideal_for']['us'].append('Mid-market, Fast-moving teams')

print("\nFeature Comparison:")
print(f"{'Category':<20} {'Us':<30} {'Them':<30}")
print("-" * 80)
print(f"{'Release Speed':<20} {'Stable & Reliable':<30} {'Rapid but risky':<30}")
print(f"{'Integration':<20} {'< 1 day setup':<30} {'Complex SDK':<30}")
print(f"{'Pricing':<20} {'Simple & transparent':<30} {'Complex structure':<30}")

print("\n\nSave as sales enablement deck or battle card!")
```

---

## Example 6: Executive Dashboard

Create executive-level dashboard from insights.

```python
from processing.gtm_insights_generator import generate_gtm_insights
import json

# Load and generate insights
with open('outputs/classified/gtm_classified_signals.json', 'r') as f:
    data = json.load(f)
    classified_signals = data['classified_signals']

insights = generate_gtm_insights(classified_signals)

print("="*80)
print("EXECUTIVE GTM INTELLIGENCE DASHBOARD")
print("="*80)
print(f"Report Date: {insights['metadata']['generation_date']}")
print(f"Signals Analyzed: {insights['metadata']['total_signals_analyzed']}")

# Strategic summary
print("\n" + "="*80)
print("STRATEGIC SUMMARY")
print("="*80)
print(insights['executive_summary']['strategic_summary'])

# Key metrics
print("\n" + "="*80)
print("KEY METRICS")
print("="*80)

metrics = {
    'total_insights': insights['executive_summary']['total_insights_generated'],
    'high_confidence': len([i for cat in insights['insights_by_category'].values() 
                           for i in cat['insights'] if i['confidence_level'] == 'high']),
    'categories_covered': len(insights['metadata']['categories_analyzed']),
    'cross_category': len(insights['cross_category_insights'])
}

print(f"Total Insights Generated: {metrics['total_insights']}")
print(f"High-Confidence Insights: {metrics['high_confidence']}")
print(f"GTM Dimensions Covered: {metrics['categories_covered']}/7")
print(f"Cross-Category Connections: {metrics['cross_category']}")

# Top priorities
print("\n" + "="*80)
print("TOP 3 PRIORITIES")
print("="*80)

for i, rec in enumerate(insights['executive_summary']['key_recommendations'][:3], 1):
    print(f"\n{i}. {rec}")

# Category breakdown
print("\n" + "="*80)
print("INSIGHTS BY CATEGORY")
print("="*80)

for category in ['PRODUCT', 'COMPETITIVE', 'TALENT', 'MARKET', 'TIMING', 'MESSAGING', 'ICP']:
    if category in insights['insights_by_category']:
        cat_data = insights['insights_by_category'][category]
        high_conf = len([i for i in cat_data['insights'] if i['confidence_level'] == 'high'])
        
        print(f"\n{category}:")
        print(f"  Signals: {cat_data['total_signals']}")
        print(f"  Insights: {len(cat_data['insights'])} ({high_conf} high-confidence)")
        
        # Show top insight
        if cat_data['insights']:
            top_insight = cat_data['insights'][0]
            print(f"  Top Finding: {top_insight['insight_text'][:80]}...")

# Risk assessment
print("\n" + "="*80)
print("RISK & OPPORTUNITY ASSESSMENT")
print("="*80)

risks = []
opportunities = []

# Categorize insights as risks or opportunities
for category, cat_insights in insights['insights_by_category'].items():
    for insight in cat_insights['insights']:
        text = insight['insight_text'].lower()
        
        if any(word in text for word in ['aggressive', 'velocity', 'expansion', 'threat']):
            risks.append(f"[{category}] {insight['insight_text'][:60]}...")
        
        if any(word in text for word in ['gap', 'underserved', 'opportunity', 'vulnerabilit']):
            opportunities.append(f"[{category}] {insight['insight_text'][:60]}...")

print("\nTop Risks:")
for i, risk in enumerate(risks[:3], 1):
    print(f"{i}. {risk}")

print("\nTop Opportunities:")
for i, opp in enumerate(opportunities[:3], 1):
    print(f"{i}. {opp}")

# Action items
print("\n" + "="*80)
print("RECOMMENDED ACTIONS (NEXT 30 DAYS)")
print("="*80)

# Extract high-confidence, actionable recommendations
actions = []
for category, cat_insights in insights['insights_by_category'].items():
    for insight in cat_insights['insights']:
        if insight['confidence_level'] == 'high':
            actions.append({
                'category': category,
                'action': insight['recommended_action'],
                'urgency': 'high' if 'immediate' in insight['recommended_action'].lower() else 'medium'
            })

# Sort by urgency
actions.sort(key=lambda x: x['urgency'] == 'medium')

for i, action in enumerate(actions[:5], 1):
    urgency_flag = "🔴" if action['urgency'] == 'high' else "🟡"
    print(f"\n{i}. [{action['category']}] {action['action'][:100]}...")

print("\n" + "="*80)
```

---

## Example 7: Weekly Intelligence Briefing

Generate weekly GTM intelligence briefing email.

```python
from processing.gtm_insights_generator import generate_gtm_insights
import json
from datetime import datetime

# Load and generate insights
with open('outputs/classified/gtm_classified_signals.json', 'r') as f:
    data = json.load(f)
    classified_signals = data['classified_signals']

insights = generate_gtm_insights(classified_signals)

# Generate weekly briefing
def generate_weekly_briefing(insights):
    """Generate formatted weekly intelligence briefing"""
    
    briefing = f"""
================================================================================
WEEKLY GTM INTELLIGENCE BRIEFING
Week of {datetime.now().strftime('%B %d, %Y')}
================================================================================

EXECUTIVE SUMMARY
--------------------------------------------------------------------------------
{insights['executive_summary']['strategic_summary']}

Signals Analyzed: {insights['metadata']['total_signals_analyzed']}
Insights Generated: {insights['executive_summary']['total_insights_generated']}
High-Confidence Findings: {len(insights['executive_summary']['high_confidence_insights'])}


TOP 3 INSIGHTS THIS WEEK
--------------------------------------------------------------------------------
"""
    
    # Add top insights
    for i, hc_insight in enumerate(insights['executive_summary']['high_confidence_insights'][:3], 1):
        briefing += f"""
{i}. [{hc_insight['category']}] {hc_insight['insight']}
"""
    
    briefing += """

KEY DEVELOPMENTS BY CATEGORY
--------------------------------------------------------------------------------
"""
    
    # Add category summaries
    for category, cat_insights in insights['insights_by_category'].items():
        briefing += f"""
{category} ({cat_insights['total_signals']} signals):
{cat_insights['summary']}
"""
        
        # Add top insight from category
        if cat_insights['insights']:
            top = cat_insights['insights'][0]
            briefing += f"  → {top['insight_text'][:100]}...\n"
    
    briefing += """

RECOMMENDED ACTIONS
--------------------------------------------------------------------------------
"""
    
    # Add top recommendations
    for i, rec in enumerate(insights['executive_summary']['key_recommendations'][:5], 1):
        briefing += f"{i}. {rec}\n\n"
    
    briefing += """

CROSS-CATEGORY CONNECTIONS
--------------------------------------------------------------------------------
"""
    
    # Add cross-category insights
    for cross_insight in insights['cross_category_insights']:
        briefing += f"• {cross_insight['insight_text']}\n"
        briefing += f"  Action: {cross_insight['recommended_action']}\n\n"
    
    briefing += """
================================================================================
Next briefing: {next_week}
For questions or deep-dives, contact GTM Intelligence Team
================================================================================
""".format(next_week=(datetime.now() + timedelta(days=7)).strftime('%B %d, %Y'))
    
    return briefing

from datetime import timedelta

# Generate briefing
briefing = generate_weekly_briefing(insights)

# Display
print(briefing)

# Save to file
output_path = 'outputs/insights/weekly_briefing.txt'
with open(output_path, 'w') as f:
    f.write(briefing)

print(f"\nBriefing saved to: {output_path}")
print("Ready to email to leadership team!")
```

---

## Example 8: Trend Tracking Over Time

Track insights trends over multiple weeks to identify patterns.

```python
from processing.gtm_insights_generator import generate_gtm_insights
import json
from datetime import datetime
import os

def track_insights_over_time(weeks_data):
    """
    Track how insights evolve over multiple weeks
    
    Args:
        weeks_data: List of tuples (date, classified_signals)
    """
    
    trend_data = {
        'categories': {},
        'confidence_trends': [],
        'insight_volume': [],
        'recurring_themes': {}
    }
    
    for week_date, signals in weeks_data:
        # Generate insights for this week
        insights = generate_gtm_insights(signals)
        
        # Track by category
        for category, cat_insights in insights['insights_by_category'].items():
            if category not in trend_data['categories']:
                trend_data['categories'][category] = []
            
            trend_data['categories'][category].append({
                'date': week_date,
                'signal_count': cat_insights['total_signals'],
                'insight_count': len(cat_insights['insights']),
                'high_confidence_count': sum(1 for i in cat_insights['insights'] 
                                            if i['confidence_level'] == 'high')
            })
        
        # Track overall confidence
        high_conf = len([i for cat in insights['insights_by_category'].values() 
                        for i in cat['insights'] if i['confidence_level'] == 'high'])
        total = insights['executive_summary']['total_insights_generated']
        
        trend_data['confidence_trends'].append({
            'date': week_date,
            'high_confidence_pct': (high_conf / total * 100) if total > 0 else 0
        })
        
        # Track insight volume
        trend_data['insight_volume'].append({
            'date': week_date,
            'total_insights': total
        })
        
        # Extract recurring themes
        for category, cat_insights in insights['insights_by_category'].items():
            for insight in cat_insights['insights']:
                # Simple keyword extraction
                keywords = ['velocity', 'hiring', 'launch', 'gap', 'vulnerability']
                for keyword in keywords:
                    if keyword in insight['insight_text'].lower():
                        if keyword not in trend_data['recurring_themes']:
                            trend_data['recurring_themes'][keyword] = []
                        trend_data['recurring_themes'][keyword].append({
                            'date': week_date,
                            'category': category,
                            'text': insight['insight_text'][:80]
                        })
    
    return trend_data

# Example: Load data from multiple weeks
weeks_data = [
    ('2025-11-05', data['classified_signals']),  # Current week
    # Add more weeks as they become available
]

# Track trends
trends = track_insights_over_time(weeks_data)

# Display trend analysis
print("="*80)
print("GTM INSIGHTS TREND ANALYSIS")
print("="*80)

print("\nCategory Activity Trends:")
for category, data_points in trends['categories'].items():
    print(f"\n{category}:")
    for dp in data_points:
        print(f"  {dp['date']}: {dp['signal_count']} signals → {dp['insight_count']} insights "
              f"({dp['high_confidence_count']} high-conf)")

print("\n" + "="*80)
print("Confidence Trend:")
for ct in trends['confidence_trends']:
    print(f"{ct['date']}: {ct['high_confidence_pct']:.1f}% high-confidence insights")

print("\n" + "="*80)
print("Recurring Themes:")
for theme, occurrences in trends['recurring_themes'].items():
    print(f"\n{theme.upper()} ({len(occurrences)} mentions):")
    for occ in occurrences[:3]:
        print(f"  [{occ['date']}] {occ['category']}: {occ['text']}...")

print("\n" + "="*80)
print("Trend Insights:")
print("- Track week-over-week changes in signal volume")
print("- Monitor confidence trends (improving or declining)")
print("- Identify persistent themes vs. one-time events")
print("- Use for quarterly GTM strategy reviews")
```

---

## Next Steps

These examples demonstrate the full power of the GTM Insights Generator. Use them as templates for:

1. **Daily Operations** - Integrate into daily workflows
2. **Weekly Reporting** - Automate intelligence briefings
3. **Strategic Planning** - Inform quarterly GTM decisions
4. **Sales Enablement** - Keep competitive intel fresh
5. **Product Strategy** - Guide roadmap decisions

For more information, see:
- `GTM_INSIGHTS_GENERATOR_README.md` - Full documentation
- `GTM_CLASSIFIER_README.md` - Signal classification system
- `SIGNAL_AGGREGATOR_README.md` - Data collection pipeline

---

**Last Updated:** November 5, 2025
