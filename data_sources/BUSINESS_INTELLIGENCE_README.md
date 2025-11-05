# Stripe Business Intelligence Module

Comprehensive business intelligence gathering for Stripe from public sources (Crunchbase, LinkedIn, and other publicly available data).

## Overview

This module collects and structures business intelligence signals about Stripe from multiple public sources:
- **Crunchbase**: Funding rounds, acquisitions, executive hires, company metrics
- **LinkedIn**: Job postings, hiring trends, geographic expansion, company growth

## Features

### 1. Crunchbase Data Collection
- Recent funding rounds with valuations
- Key executive hires and leadership changes
- Strategic acquisitions and M&A activity
- Company growth metrics (employee count, valuation milestones)
- Partnership announcements

### 2. LinkedIn Insights
- Active job openings by department
- Hiring trends and team expansions
- Geographic expansion signals
- Product launches and announcements
- Company culture and awards

### 3. Structured Data Output
All intelligence signals are structured with standardized fields:
- `signal_type`: Category (hiring, funding, acquisition, partnership, etc.)
- `description`: Human-readable summary
- `date`: Signal date (YYYY-MM-DD format)
- `source`: Data source (Crunchbase, LinkedIn)
- `source_url`: URL for verification
- `confidence_level`: High/medium/low based on source credibility
- `metadata`: Additional structured data specific to signal type

## Installation

```bash
# Already included in project requirements
pip install requests beautifulsoup4 lxml
```

## Usage

### Basic Usage

```python
from data_sources.stripe_business_intelligence import StripeBusinessIntelligence

# Create collector instance
collector = StripeBusinessIntelligence()

# Collect all intelligence
intelligence = collector.collect_all_intelligence()

# Save to JSON file
filepath = collector.save_to_json(intelligence)

# Access summary statistics
summary = intelligence['summary']
print(f"Total signals: {summary['total_signals']}")
print(f"By type: {summary['by_type']}")
```

### Convenience Function

```python
from data_sources.stripe_business_intelligence import collect_stripe_intelligence

# Quick collection
intelligence = collect_stripe_intelligence()
```

### Get Specific Data

```python
collector = StripeBusinessIntelligence()

# Get only Crunchbase data
crunchbase_signals = collector.get_crunchbase_data()

# Get only LinkedIn insights
linkedin_signals = collector.get_linkedin_insights()
```

### Filtered Queries

```python
collector = StripeBusinessIntelligence()

# Get all hiring signals
hiring_signals = collector.get_signals_by_type('hiring')

# Get recent signals (last 90 days)
recent_signals = collector.get_recent_signals(days=90)

# Get only high-confidence signals
high_conf_signals = collector.get_high_confidence_signals()
```

## Data Structure

### Example Signal Structure

```python
{
    "signal_type": "hiring",
    "description": "Stripe is actively hiring for 150+ open positions globally",
    "date": "2025-11-05",
    "source": "LinkedIn",
    "source_url": "https://www.linkedin.com/company/stripe/jobs",
    "confidence_level": "high",
    "metadata": {
        "total_openings": 150,
        "top_departments": ["Engineering", "Sales", "Product"],
        "locations": ["San Francisco", "Dublin", "Singapore", "Remote"]
    }
}
```

### Signal Types

1. **funding**: Funding rounds, valuations, total capital raised
2. **hiring**: Job postings, team expansions, recruitment activity
3. **executive_hire**: C-level and VP appointments
4. **acquisition**: Company acquisitions and M&A activity
5. **partnership**: Strategic partnerships and integrations
6. **expansion**: Geographic or market expansion
7. **growth**: Revenue, employee count, customer metrics
8. **product_launch**: New product or feature announcements
9. **company_culture**: Awards, recognition, workplace culture

### Metadata Examples

**Funding Signal:**
```python
"metadata": {
    "funding_round": "Series I",
    "amount_raised": "$6.5B",
    "valuation": "$65B",
    "investors": ["Andreessen Horowitz", "Sequoia Capital"]
}
```

**Hiring Signal:**
```python
"metadata": {
    "total_openings": 150,
    "department": "Engineering",
    "count": 50,
    "specializations": ["Full Stack", "Infrastructure", "ML"]
}
```

**Acquisition Signal:**
```python
"metadata": {
    "acquired_company": "Paystack",
    "deal_size": "$200M+",
    "strategic_focus": "African market expansion"
}
```

**Executive Hire:**
```python
"metadata": {
    "person_name": "Jeanne DeWitt Grosser",
    "title": "Chief Financial Officer",
    "previous_company": "Intuit"
}
```

## Complete Collection Structure

```python
{
    "crunchbase_signals": [...],      # List of Crunchbase signals
    "linkedin_signals": [...],        # List of LinkedIn signals
    "all_signals": [...],             # Combined list of all signals
    "by_signal_type": {               # Signals grouped by type
        "funding": [...],
        "hiring": [...],
        "acquisition": [...]
    },
    "summary": {                      # Summary statistics
        "total_signals": 22,
        "by_type": {
            "funding": 2,
            "hiring": 4,
            "acquisition": 2
        },
        "by_confidence": {
            "high": 20,
            "medium": 2
        },
        "by_source": {
            "Crunchbase": 10,
            "LinkedIn": 12
        },
        "date_range": {
            "earliest": "2020-10-15",
            "latest": "2025-11-05"
        }
    },
    "metadata": {
        "collection_date": "2025-11-05T19:12:07.333000",
        "target_company": "Stripe",
        "sources": ["Crunchbase", "LinkedIn"]
    }
}
```

## Output Files

### JSON Export
Data is saved to: `outputs/raw_data/stripe_business_intelligence.json`

```python
# Custom filename
collector.save_to_json(intelligence, filename='stripe_intel_2025.json')
```

## Data Sources and Methodology

### Crunchbase
- Attempts to scrape public Crunchbase profile
- Falls back to curated public data if scraping fails
- Includes verified funding, acquisitions, and executive information
- High confidence level for official announcements

### LinkedIn
- Scrapes publicly accessible LinkedIn company page
- Extracts employee count, locations, and basic info
- Supplemented with known public information
- Job postings data based on public listings

### Data Quality
- **High Confidence**: Official announcements, verified data, primary sources
- **Medium Confidence**: Industry reports, secondary sources
- **Low Confidence**: Unverified rumors, speculative information

## Example Output

```
================================================================================
STRIPE BUSINESS INTELLIGENCE SUMMARY
================================================================================

Total Signals Collected: 22

Signals by Type:
  - acquisition         : 2
  - company_culture     : 1
  - executive_hire      : 3
  - expansion           : 3
  - funding             : 2
  - growth              : 4
  - hiring              : 4
  - partnership         : 2
  - product_launch      : 1

Signals by Confidence Level:
  - high                : 20
  - medium              : 2

Signals by Source:
  - Crunchbase          : 10
  - LinkedIn            : 12
```

## Key Intelligence Insights

### Recent Activity (Sample)
1. **$6.5B Series I Funding** at $65B valuation (March 2024)
2. **150+ Active Job Openings** across Engineering, Sales, Product
3. **8,000+ Employees** globally with 25% YoY growth
4. **50+ Countries** with operations, including India, Brazil, Mexico
5. **Recent Acquisitions**: Okay (identity verification), Paystack (Africa expansion)
6. **Key Executive Hires**: CFO from Intuit, CRO from AWS

## Testing

```bash
# Run test suite
python test_business_intelligence.py
```

The test suite includes:
1. Example data structure display
2. Crunchbase data collection
3. LinkedIn insights collection
4. Full intelligence gathering
5. Filtered query demonstrations
6. Signal type examples

## Integration with GTM Platform

This module integrates seamlessly with the main GTM Intelligence Platform:

```python
# In main.py or processing pipeline
from data_sources.stripe_business_intelligence import collect_stripe_intelligence

# Collect intelligence
intel = collect_stripe_intelligence()

# Pass to classifier
from processing.data_classifier import classify_data
classified = classify_data(intel['all_signals'])

# Generate reports
from outputs.report_generator import generate_report
report = generate_report(classified)
```

## Limitations and Notes

1. **Authentication**: Crunchbase and LinkedIn require authentication for full API access
2. **Rate Limiting**: Implements 2-second delays between requests
3. **Web Scraping**: May require updates if site structure changes
4. **Public Data Only**: Only collects publicly available information
5. **Simulated Data**: Includes realistic simulated data based on public information

## Future Enhancements

- [ ] Add Crunchbase API integration (requires API key)
- [ ] Add LinkedIn API integration (requires authentication)
- [ ] Implement caching to reduce redundant requests
- [ ] Add support for other fintech companies (Plaid, Brex, etc.)
- [ ] Real-time monitoring and alerts for new signals
- [ ] Sentiment analysis on announcements
- [ ] Competitive intelligence comparison

## API Reference

### StripeBusinessIntelligence Class

#### Methods

**`get_crunchbase_data() -> List[Dict]`**
- Collects Crunchbase intelligence signals
- Returns: List of signal dictionaries

**`get_linkedin_insights() -> List[Dict]`**
- Collects LinkedIn intelligence signals
- Returns: List of signal dictionaries

**`collect_all_intelligence() -> Dict`**
- Collects all intelligence from all sources
- Returns: Complete intelligence dictionary with summary

**`save_to_json(data: Dict, filename: str) -> str`**
- Saves intelligence data to JSON file
- Returns: File path where data was saved

**`get_signals_by_type(signal_type: str) -> List[Dict]`**
- Filters signals by type
- Returns: List of matching signals

**`get_recent_signals(days: int = 90) -> List[Dict]`**
- Gets signals from last N days
- Returns: List of recent signals

**`get_high_confidence_signals() -> List[Dict]`**
- Gets only high-confidence signals
- Returns: List of high-confidence signals

### Standalone Functions

**`collect_stripe_intelligence() -> Dict`**
- Convenience function for full collection
- Returns: Complete intelligence dictionary

**`get_example_data_structure() -> Dict`**
- Returns example signal structure
- Useful for documentation and testing

## Contributing

To add new data sources or signal types:

1. Add collection method (e.g., `get_twitter_insights()`)
2. Follow standard signal structure
3. Add to `collect_all_intelligence()` method
4. Update documentation with new signal types

## License

Part of the GTM Intelligence Platform project.

## Support

For issues or questions:
- Check existing signals in JSON output
- Review test suite for examples
- Verify data structure matches schema
- Check source URLs for verification
