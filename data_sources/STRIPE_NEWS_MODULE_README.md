# Stripe News Collection Module

A comprehensive Python module for collecting recent news and announcements about Stripe from multiple sources.

## Features

### 1. **NewsAPI Integration** (`get_news_from_api()`)
- Searches NewsAPI.org for Stripe-related news
- Multiple search queries:
  - "Stripe fintech"
  - "Stripe funding"
  - "Stripe partnerships"
  - "Stripe product launch"
- Configurable time range (default: 3 months)
- Automatic deduplication
- Rate limiting and error handling

### 2. **Company Announcements** (`get_company_announcements()`)
- Scrapes Stripe's official blog
- Scrapes Stripe's newsroom/press releases
- Filters for last 3 months
- Extracts: title, date, description, link
- Fallback to mock data if scraping fails

### 3. **Industry News** (`get_industry_news()`)
- Collects broader fintech trends
- Keywords:
  - "payment processing trends 2025"
  - "B2B fintech 2025"
  - "payment infrastructure"
  - "digital payments innovation"
  - "fintech API platforms"
- Returns 5-7 most relevant articles

## Installation

```bash
pip install requests beautifulsoup4 lxml
```

Optional (for NewsAPI access):
```bash
pip install newsapi-python
```

## Usage

### Quick Start

```python
from data_sources.stripe_news_module import collect_stripe_news

# Collect all news types at once
all_news = collect_stripe_news(api_key='your_api_key', months_back=3)

print(f"API News: {len(all_news['api_news'])}")
print(f"Announcements: {len(all_news['company_announcements'])}")
print(f"Industry: {len(all_news['industry_news'])}")
```

### Individual Functions

```python
from data_sources.stripe_news_module import StripeNewsCollector

# Initialize
collector = StripeNewsCollector(api_key='your_api_key', months_back=3)

# Get news from NewsAPI
api_news = collector.get_news_from_api()

# Get company announcements
announcements = collector.get_company_announcements()

# Get industry news
industry_news = collector.get_industry_news()

# Collect everything
all_news = collector.collect_all_news()

# Save to file
collector.save_to_json(all_news, 'stripe_news.json')
```

### Using Environment Variables

```python
import os
os.environ['NEWS_API_KEY'] = 'your_api_key'

from data_sources.stripe_news_module import StripeNewsCollector

# Will automatically use NEWS_API_KEY from environment
collector = StripeNewsCollector()
news = collector.collect_all_news()
```

## Data Format

All functions return data in a standardized format:

```python
{
    'headline': 'Article title',
    'description': 'Brief description or excerpt',
    'published_date': '2024-11-05',  # ISO format
    'source_url': 'https://example.com/article',
    'source_name': 'TechCrunch',
    'category': 'news',  # or 'company_announcement', 'industry_trend'
    'collected_at': '2024-11-05T10:30:00'
}
```

### Complete Collection Structure

```python
{
    'api_news': [
        {
            'headline': '...',
            'description': '...',
            'published_date': '...',
            'source_url': '...',
            'source_name': '...',
            'category': 'news',
            'search_query': 'Stripe funding',
            'author': '...',
            'collected_at': '...'
        }
    ],
    'company_announcements': [
        {
            'headline': '...',
            'description': '...',
            'published_date': '...',
            'source_url': '...',
            'source_name': 'Stripe Blog',
            'category': 'company_announcement',
            'type': 'blog_post',  # or 'press_release'
            'collected_at': '...'
        }
    ],
    'industry_news': [
        {
            'headline': '...',
            'description': '...',
            'published_date': '...',
            'source_url': '...',
            'source_name': '...',
            'category': 'industry_trend',
            'collected_at': '...'
        }
    ],
    'metadata': {
        'collection_date': '2024-11-05T10:30:00',
        'months_back': 3,
        'cutoff_date': '2024-08-05'
    }
}
```

## Error Handling

The module includes comprehensive error handling:

- **Timeouts**: 10-second timeout on all HTTP requests
- **Rate Limiting**: 1-second delay between API calls
- **Fallback Data**: Returns mock data if APIs fail
- **Logging**: Detailed logging of all operations
- **Duplicate Removal**: Automatic deduplication by URL

## Testing

Run the test script to verify functionality:

```bash
python test_stripe_news.py
```

This will:
- Test each function individually
- Validate data format
- Check error handling
- Display categorized results
- Save test data to JSON

## API Key Setup

### NewsAPI.org (Free Tier)

1. Sign up at https://newsapi.org/
2. Get your API key
3. Set environment variable:
   ```bash
   # Windows PowerShell
   $env:NEWS_API_KEY = "your_key_here"
   
   # Linux/Mac
   export NEWS_API_KEY="your_key_here"
   ```

Or add to `.env` file:
```
NEWS_API_KEY=your_key_here
```

### Without API Key

The module works without an API key by using mock data:

```python
# No API key needed - will use mock data
collector = StripeNewsCollector()
news = collector.collect_all_news()
```

## Logging

The module uses Python's logging module:

```python
import logging

# Set logging level
logging.basicConfig(level=logging.DEBUG)  # Verbose
logging.basicConfig(level=logging.INFO)   # Normal (default)
logging.basicConfig(level=logging.WARNING) # Quiet
```

## Configuration

Customize collection parameters:

```python
collector = StripeNewsCollector(
    api_key='your_key',
    months_back=6  # Look back 6 months instead of 3
)

# Custom timeout
collector.timeout = 15  # 15 seconds

# Custom rate limiting
collector.request_delay = 2  # 2 seconds between requests
```

## Output Files

Save collected data:

```python
collector = StripeNewsCollector()
all_news = collector.collect_all_news()

# Save to JSON
filepath = collector.save_to_json(all_news, 'stripe_news.json')
# Saves to: outputs/raw_data/stripe_news.json
```

## Integration with Main Platform

This module integrates seamlessly with the GTM Intelligence Platform:

```python
# In main.py or other scripts
from data_sources.stripe_news_module import StripeNewsCollector

collector = StripeNewsCollector()
stripe_news = collector.collect_all_news()

# Process with existing classifiers
from processing.data_classifier import DataClassifier

classifier = DataClassifier()
classified_news = classifier.classify_news_articles(
    stripe_news['api_news'] + 
    stripe_news['company_announcements'] + 
    stripe_news['industry_news']
)
```

## Examples

### Example 1: Get Recent Funding News

```python
collector = StripeNewsCollector(months_back=1)
news = collector.get_news_from_api()

funding_news = [
    article for article in news 
    if 'funding' in article.get('search_query', '').lower()
]

for article in funding_news:
    print(f"{article['headline']}")
    print(f"  {article['source_name']} - {article['published_date']}")
```

### Example 2: Monitor Product Launches

```python
collector = StripeNewsCollector()
announcements = collector.get_company_announcements()

blog_posts = [
    ann for ann in announcements 
    if ann['type'] == 'blog_post'
]

for post in blog_posts:
    print(f"{post['headline']}")
    print(f"  {post['source_url']}")
```

### Example 3: Track Industry Trends

```python
collector = StripeNewsCollector()
industry = collector.get_industry_news()

for article in industry:
    print(f"{article['headline']}")
    print(f"  {article['description'][:100]}...")
```

## Troubleshooting

### Issue: No articles returned

**Solution**: Check if API key is valid or use mock data:
```python
collector = StripeNewsCollector()  # Will use mock data
```

### Issue: Timeout errors

**Solution**: Increase timeout:
```python
collector = StripeNewsCollector()
collector.timeout = 20  # 20 seconds
```

### Issue: Rate limiting

**Solution**: Increase delay:
```python
collector = StripeNewsCollector()
collector.request_delay = 3  # 3 seconds between requests
```

## Requirements

- Python 3.8+
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0

## License

Part of the GTM Intelligence Platform project.
