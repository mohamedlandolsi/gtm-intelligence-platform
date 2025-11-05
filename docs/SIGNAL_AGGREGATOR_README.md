# Market Signals Aggregator

## Overview

The Signal Aggregator module combines data from all intelligence sources (news, business intelligence, technical signals) into a unified, deduplicated, high-value signal feed. It intelligently handles conflicting information and produces actionable market insights.

## Key Features

### 1. **Unified Signal Format**
All signals are standardized into a common schema:
```python
{
    'signal_id': 'SIG-20251105-A1B2C3D4',  # Unique identifier
    'signal_type': 'funding',              # Category
    'headline': 'Brief summary',           # Short title
    'description': 'Detailed explanation', # Full context
    'date_detected': '2025-11-05',        # YYYY-MM-DD format
    'source': 'Crunchbase',               # Origin
    'source_url': 'https://...',          # Reference link
    'confidence_level': 'high',           # high/medium/low
    'raw_json': {...}                     # Original data
}
```

### 2. **Intelligent Deduplication**
Removes duplicate signals using three methods:
- **Exact ID matching**: Same signal_id = duplicate
- **URL matching**: Same source_url = duplicate  
- **Fuzzy content matching**: 85%+ headline similarity on same date = duplicate

### 3. **Conflict Resolution**
When multiple sources report the same event:
1. **Group similar signals** by date and content similarity (>70%)
2. **Rank by confidence**: Prefer Crunchbase, LinkedIn, GitHub over general news
3. **Merge information**: Use most detailed description, combine all sources
4. **Flag conflicts**: Add notes when sources significantly disagree

### 4. **Smart Filtering**
- **Confidence threshold**: Filter by high/medium/low confidence
- **Date filtering**: Only include signals from last N days
- **Type filtering**: Focus on specific signal categories

### 5. **Quality Scoring**
Signals are prioritized by:
- **Date** (most recent first)
- **Confidence level** (high > medium > low)
- **Source reliability** (Crunchbase/LinkedIn/GitHub > News)

## Usage

### Basic Usage

```python
from processing.signal_aggregator import aggregate_market_signals

# Get top 15 high-confidence signals from last 90 days
signals = aggregate_market_signals(
    max_signals=15,
    min_confidence='medium',
    days_lookback=90
)

for signal in signals:
    print(f"[{signal['date_detected']}] {signal['signal_type']}")
    print(f"  {signal['headline']}")
    print(f"  Source: {signal['source']} | Confidence: {signal['confidence_level']}")
```

### Advanced Usage

```python
from processing.signal_aggregator import MarketSignalsAggregator

aggregator = MarketSignalsAggregator()

# Get signals with custom parameters
signals = aggregator.aggregate_market_signals(
    max_signals=20,
    min_confidence='high',  # Only high-confidence signals
    days_lookback=30        # Last 30 days only
)

# Handle conflicts manually
resolved_signals = aggregator.handle_conflicting_information(signals)

# Generate summary report
summary = aggregator.generate_summary_report(signals)
print(f"Total signals: {summary['total_signals']}")
print(f"By type: {summary['by_type']}")
print(f"By source: {summary['by_source']}")

# Save to file
filepath = aggregator.save_aggregated_signals(
    signals,
    filename='my_signals.json'
)
```

## Data Sources

The aggregator pulls from three main collectors:

### 1. News Collector
- **File**: `outputs/raw_data/stripe_news_collection.json`
- **Sources**: NewsAPI, Stripe blog, industry newsrooms
- **Signal types**: `product_launch`, `partnership`, `market_expansion`
- **Confidence**: Medium (news) to High (official announcements)

### 2. Business Intelligence Collector
- **File**: `outputs/raw_data/stripe_business_intelligence.json`
- **Sources**: Crunchbase, LinkedIn
- **Signal types**: `funding`, `valuation`, `hiring`, `growth`
- **Confidence**: High (verified business data)

### 3. Technical Signals Collector
- **File**: `outputs/raw_data/stripe_technical_signals.json`
- **Sources**: GitHub API, Stripe API changelog
- **Signal types**: `sdk_update`, `new_api_endpoint`, `api_expansion`, `commit_activity`
- **Confidence**: High (official technical data)

## Signal Types

### Business Signals
- `funding`: Funding rounds, investments
- `valuation`: Company valuation changes
- `growth`: Employee count, market metrics
- `hiring`: Job openings, talent acquisition
- `partnership`: Business partnerships
- `acquisition`: M&A activity

### Technical Signals
- `sdk_update`: SDK releases and updates
- `new_api_endpoint`: New API capabilities
- `api_expansion`: API feature additions
- `api_enhancement`: Performance improvements
- `commit_activity`: Development velocity
- `new_repository`: New open source projects
- `developer_tools`: New tools for developers

### Market Signals
- `product_launch`: New product announcements
- `market_expansion`: Geographic/vertical expansion
- `competitive_move`: Strategic positioning
- `regulatory`: Compliance and regulation news

## Confidence Levels

### High Confidence
- **Sources**: Crunchbase, LinkedIn, GitHub API, Stripe Official
- **Characteristics**: 
  - Verified business data
  - Official technical releases
  - First-party announcements
- **Use case**: Strategic decision-making

### Medium Confidence
- **Sources**: Reputable news outlets, industry analysts
- **Characteristics**:
  - Third-party reporting
  - Unverified claims
  - Analyst estimates
- **Use case**: Market awareness, further investigation

### Low Confidence
- **Sources**: Social media, rumors, unverified reports
- **Characteristics**:
  - Unconfirmed information
  - Secondary sources
  - Speculative content
- **Use case**: Early signals, monitoring only

## Deduplication Strategy

### Example: Same Event, Multiple Sources

**Input (3 signals):**
1. TechCrunch: "Stripe raises $600M at $95B valuation" (Medium confidence)
2. Crunchbase: "Stripe secures $600M funding" (High confidence)
3. Bloomberg: "Stripe closes $600M Series H" (High confidence)

**Output (1 signal):**
- **Headline**: Most accurate from high-confidence source
- **Description**: Most detailed (Bloomberg's full context)
- **Sources**: ["TechCrunch", "Crunchbase", "Bloomberg"]
- **Confidence**: High (highest available)
- **Note**: "Information aggregated from 3 sources: TechCrunch, Crunchbase, Bloomberg"

### Deduplication Rules

1. **Exact Match**: Same `signal_id` → Remove duplicate
2. **URL Match**: Same `source_url` → Remove duplicate
3. **Content Match**: 85%+ headline similarity + same date → Merge into one signal

## Conflict Resolution

### Resolution Strategy

When multiple sources report different details about the same event:

1. **Identify Related Signals**
   - Same date + similar headline (>70% similarity)
   - Same topic/entity
   - Same event type

2. **Rank Sources**
   ```
   Tier 1 (High): Crunchbase, LinkedIn, GitHub, Stripe Official
   Tier 2 (Medium): TechCrunch, Bloomberg, Reuters, WSJ
   Tier 3 (Low): General news, blogs, social media
   ```

3. **Merge Strategy**
   - Primary signal: Highest confidence source
   - Description: Longest/most detailed
   - Sources: All contributing sources listed
   - Metadata: Combine unique attributes

4. **Flag Unresolved Conflicts**
   - Add `note` field with conflict details
   - Preserve all `raw_json` for manual review
   - Flag for human verification if critical

### Example Conflict Resolution

**Conflict**: Different valuations reported
- Source A: "$95B valuation"
- Source B: "$92B valuation"  
- Source C: "$95B valuation"

**Resolution**:
- Use most common value: $95B
- Add note: "Valuation reported as $92B by Source B, $95B by Sources A and C"
- Confidence: Medium (conflicting reports)
- Flag for verification

## Output Format

### Aggregated JSON Structure

```json
{
  "metadata": {
    "aggregation_date": "2025-11-05T19:45:00",
    "total_signals": 15,
    "summary": {
      "total_signals": 15,
      "by_type": {
        "sdk_update": 5,
        "hiring": 3,
        "funding": 2,
        ...
      },
      "by_source": {
        "GitHub": 7,
        "LinkedIn": 4,
        "Crunchbase": 2,
        ...
      },
      "by_confidence": {
        "high": 12,
        "medium": 3
      },
      "date_range": {
        "earliest": "2025-10-06",
        "latest": "2025-11-05"
      }
    }
  },
  "signals": [
    {
      "signal_id": "SIG-20251105-A1B2C3D4",
      "signal_type": "funding",
      "headline": "Stripe raises $600M Series H",
      "description": "Detailed description...",
      "date_detected": "2025-11-05",
      "source": "Crunchbase",
      "source_url": "https://...",
      "confidence_level": "high",
      "raw_json": {...}
    },
    ...
  ]
}
```

## Performance

### Processing Metrics

From real test run:
- **Input**: 76 raw signals from all sources
- **After standardization**: 76 signals
- **After deduplication**: 44 unique signals (32 duplicates removed = 42% reduction)
- **After confidence filter**: 44 signals (all medium+ confidence)
- **After date filter**: 23 recent signals
- **Final output**: 15 top signals

### Processing Time
- Load all sources: ~15ms
- Standardize signals: ~1ms
- Remove duplicates: ~40ms (fuzzy matching)
- Filter & sort: ~1ms
- **Total**: ~60ms for 76 signals

## Best Practices

### 1. Choose Appropriate Timeframe
```python
# For tactical decisions (weekly reviews)
signals = aggregate_market_signals(days_lookback=7)

# For strategic planning (quarterly)
signals = aggregate_market_signals(days_lookback=90)

# For historical analysis
signals = aggregate_market_signals(days_lookback=365)
```

### 2. Set Confidence Thresholds
```python
# For executive briefings (only verified data)
signals = aggregate_market_signals(min_confidence='high')

# For market monitoring (broader coverage)
signals = aggregate_market_signals(min_confidence='medium')

# For early warning (everything)
signals = aggregate_market_signals(min_confidence='low')
```

### 3. Focus on Relevant Signal Types
```python
# After aggregation, filter by type
technical_signals = [s for s in signals if s['signal_type'] in [
    'sdk_update', 'new_api_endpoint', 'commit_activity'
]]

business_signals = [s for s in signals if s['signal_type'] in [
    'funding', 'hiring', 'partnership'
]]
```

### 4. Monitor Data Freshness
```python
summary = aggregator.generate_summary_report(signals)
date_range = summary['date_range']

# Alert if no recent signals
from datetime import datetime, timedelta
latest = datetime.fromisoformat(date_range['latest'])
if datetime.now() - latest > timedelta(days=7):
    print("⚠️ No signals in last 7 days - check data collectors")
```

## Troubleshooting

### No Signals Returned

**Problem**: `aggregate_market_signals()` returns empty list

**Solutions**:
1. Check data files exist:
   ```python
   import os
   print(os.path.exists('outputs/raw_data/stripe_news_collection.json'))
   print(os.path.exists('outputs/raw_data/stripe_business_intelligence.json'))
   print(os.path.exists('outputs/raw_data/stripe_technical_signals.json'))
   ```

2. Increase lookback period:
   ```python
   signals = aggregate_market_signals(days_lookback=365)  # 1 year
   ```

3. Lower confidence threshold:
   ```python
   signals = aggregate_market_signals(min_confidence='low')
   ```

### Too Many Duplicates

**Problem**: Many signals look similar after aggregation

**Solutions**:
1. Adjust similarity threshold in `_calculate_similarity()` (current: 85%)
2. Improve headline normalization
3. Add custom deduplication rules for specific signal types

### Conflicts Not Resolved

**Problem**: Related signals not being merged

**Solutions**:
1. Lower similarity threshold in `_are_signals_related()` (current: 70%)
2. Add additional grouping criteria (same company, same event type)
3. Use `handle_conflicting_information()` manually with custom logic

### Wrong Confidence Levels

**Problem**: Signals have incorrect confidence assignments

**Solutions**:
1. Review `_determine_confidence()` logic
2. Add your domain-specific confidence rules
3. Override confidence in post-processing:
   ```python
   for signal in signals:
       if signal['source'] == 'MyTrustedSource':
           signal['confidence_level'] = 'high'
   ```

## API Reference

### Functions

#### `aggregate_market_signals()`
```python
def aggregate_market_signals(
    max_signals: int = 15,
    min_confidence: str = 'medium',
    days_lookback: int = 90
) -> List[Dict]
```

Convenience function to aggregate signals with default settings.

**Parameters**:
- `max_signals`: Maximum signals to return (default: 15)
- `min_confidence`: Minimum confidence level - 'low', 'medium', 'high' (default: 'medium')
- `days_lookback`: Include signals from last N days (default: 90)

**Returns**: List of standardized signal dictionaries

### Classes

#### `MarketSignalsAggregator`

Main class for signal aggregation.

**Methods**:

##### `aggregate_market_signals()`
Full aggregation pipeline with filtering and sorting.

##### `handle_conflicting_information()`
```python
def handle_conflicting_information(
    signals: List[Dict],
    conflict_field: str = 'description'
) -> List[Dict]
```

Resolve conflicts between related signals.

##### `generate_summary_report()`
```python
def generate_summary_report(signals: List[Dict]) -> Dict
```

Generate statistical summary of signals.

##### `save_aggregated_signals()`
```python
def save_aggregated_signals(
    signals: List[Dict],
    filename: str = 'aggregated_market_signals.json'
) -> str
```

Save signals to JSON file in `outputs/aggregated/` directory.

## Integration Examples

### Daily Intelligence Briefing

```python
from processing.signal_aggregator import aggregate_market_signals
from datetime import datetime

# Get yesterday's signals
signals = aggregate_market_signals(
    max_signals=10,
    min_confidence='high',
    days_lookback=1
)

# Format as daily briefing
print(f"Intelligence Briefing - {datetime.now().strftime('%Y-%m-%d')}")
print("="*60)

for i, signal in enumerate(signals, 1):
    print(f"\n{i}. [{signal['signal_type'].upper()}] {signal['headline']}")
    print(f"   Source: {signal['source']}")
    print(f"   {signal['description'][:200]}...")
```

### Competitive Monitoring

```python
# Track competitive moves
signals = aggregate_market_signals(max_signals=50, days_lookback=30)

competitive_signals = [
    s for s in signals 
    if 'competitive' in s.get('signal_type', '').lower()
    or 'competitor' in s.get('description', '').lower()
]

print(f"Detected {len(competitive_signals)} competitive signals:")
for signal in competitive_signals:
    print(f"- {signal['headline']}")
```

### Trend Analysis

```python
from collections import Counter

# Analyze signal patterns
signals = aggregate_market_signals(max_signals=100, days_lookback=90)

# Count by type
type_counts = Counter(s['signal_type'] for s in signals)
print("Top signal types:")
for sig_type, count in type_counts.most_common(5):
    print(f"  {sig_type}: {count}")

# Count by source
source_counts = Counter(s['source'] for s in signals)
print("\nMost active sources:")
for source, count in source_counts.most_common(5):
    print(f"  {source}: {count}")
```

## Future Enhancements

### Planned Features

1. **ML-Based Deduplication**: Use embeddings for semantic similarity
2. **Signal Scoring**: ML model to predict signal importance
3. **Real-time Streaming**: Process signals as they arrive
4. **Custom Filters**: User-defined signal filtering rules
5. **Signal Relationships**: Link related signals (cause/effect)
6. **Historical Tracking**: Track signal evolution over time
7. **Alert System**: Notify on high-priority signals
8. **Export Formats**: CSV, PDF, Slack integration

### Extensibility

The aggregator is designed for easy extension:

```python
class CustomAggregator(MarketSignalsAggregator):
    def _load_custom_source(self):
        """Add your own data source"""
        pass
    
    def _custom_confidence_rules(self, signal):
        """Add domain-specific confidence logic"""
        pass
    
    def _custom_deduplication(self, signals):
        """Add specialized deduplication"""
        pass
```

## License

Part of the GTM Intelligence Platform.
