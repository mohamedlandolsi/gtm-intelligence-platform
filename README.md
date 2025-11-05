# GTM Intelligence Platform

A comprehensive intelligence gathering tool focused on fintech companies, designed to collect, process, and analyze data for Go-To-Market (GTM) strategy development.

## 🎯 Purpose

This platform helps sales and GTM teams gather competitive intelligence about fintech companies by:
- Collecting data from multiple sources (news, social media, GitHub, company announcements)
- Classifying and categorizing intelligence signals
- Generating actionable recommendations for sales outreach
- Creating comprehensive reports for GTM strategy

## 📁 Project Structure

```
gtm-intelligence-platform/
│
├── data_sources/              # Data collection scripts
│   ├── news_collector.py      # News API integration
│   ├── crunchbase_collector.py # Crunchbase data
│   ├── linkedin_collector.py   # LinkedIn insights
│   ├── company_announcements_collector.py # Blog/press releases
│   └── github_collector.py     # GitHub repositories & activity
│
├── processing/                # Data processing & classification
│   ├── data_classifier.py     # Classify raw data into categories
│   └── data_categorizer.py    # Aggregate and categorize intelligence
│
├── outputs/                   # Report generation
│   ├── report_generator.py    # Generate formatted reports
│   ├── recommendations_generator.py # GTM recommendations
│   ├── raw_data/              # Raw collected data (JSON)
│   ├── classified/            # Classified data
│   ├── categorized/           # Aggregated intelligence
│   ├── reports/               # Generated reports (TXT, CSV)
│   └── recommendations/       # GTM recommendations
│
├── config/                    # Configuration files
│   ├── config.json           # Main configuration
│   └── .env.example          # Environment variables template
│
├── main.py                   # Main orchestrator script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
# Copy the example file
copy config\.env.example config\.env

# Edit config\.env and add your API keys
```

4. **Configure targets:**
   - Edit `config/config.json` to add your target companies
   - Customize collection parameters

### Quick Start

Run the complete intelligence gathering pipeline for Stripe:

```bash
python main.py
```

This will:
1. Collect data from all sources
2. Classify and categorize the data
3. Generate reports in `outputs/reports/`
4. Generate recommendations in `outputs/recommendations/`

## 📊 Data Sources

### 1. News API
- Collects recent news articles about target companies
- Tracks press mentions and industry coverage
- **API Key Required:** Get one at [newsapi.org](https://newsapi.org/)

### 2. Crunchbase
- Company information, funding rounds, acquisitions
- Employee count, categories, headquarters
- **API Key Required:** Get access at [Crunchbase API](https://www.crunchbase.com/products/crunchbase-api)

### 3. LinkedIn
- Company updates and posts
- Job postings and hiring trends
- Employee growth metrics
- **Note:** Uses mock data by default due to API restrictions

### 4. Company Announcements
- Blog posts and articles
- Press releases
- Product updates and changelogs
- **No API Key Required:** Web scraping

### 5. GitHub
- Repository activity and metrics
- SDK/library ecosystem
- Developer engagement
- **Optional API Token:** Increases rate limits

## 🔄 Processing Pipeline

### 1. Data Collection (`data_sources/`)
Raw data is collected from all sources and saved to `outputs/raw_data/`

### 2. Classification (`processing/data_classifier.py`)
Data is classified into GTM-relevant categories:
- Product launches
- Partnerships
- Funding rounds
- Market expansion
- Hiring trends
- Customer wins

### 3. Categorization (`processing/data_categorizer.py`)
Classified data is aggregated into intelligence signals:
- Market expansion momentum
- Product innovation activity
- Partnership strategy
- Talent acquisition velocity
- Funding & growth indicators
- Customer traction

### 4. Report Generation (`outputs/report_generator.py`)
Multiple report formats are generated:
- **Executive Report:** High-level overview
- **Detailed Analysis:** Comprehensive findings
- **CSV Export:** Raw data for further analysis

### 5. Recommendations (`outputs/recommendations_generator.py`)
Actionable GTM recommendations:
- Positioning strategies
- Timing recommendations
- Key talking points
- Engagement tactics
- Partnership opportunities

## 📈 Output Files

After running the platform, you'll find:

```
outputs/
├── raw_data/
│   ├── stripe_news.json
│   ├── stripe_crunchbase.json
│   ├── stripe_linkedin.json
│   ├── stripe_announcements.json
│   └── stripe_github.json
│
├── classified/
│   ├── stripe_news_classified.json
│   ├── stripe_linkedin_classified.json
│   └── ...
│
├── categorized/
│   ├── full_intelligence.json
│   └── executive_summary.json
│
├── reports/
│   ├── stripe_executive_report.txt
│   ├── stripe_detailed_report.txt
│   └── stripe_data_export.csv
│
└── recommendations/
    ├── stripe_recommendations.json
    └── stripe_recommendations_report.txt
```

## 🎯 Use Cases

### For Sales Teams
- Research prospects before outreach
- Identify optimal timing for engagement
- Develop personalized messaging
- Find conversation starters (recent news, hiring, etc.)

### For GTM Strategy
- Understand competitive landscape
- Track market expansion patterns
- Monitor product innovation cycles
- Identify partnership opportunities

### For Business Development
- Find companies in growth phases
- Track funding announcements
- Monitor hiring velocity
- Identify decision-maker changes

## 🔧 Customization

### Adding a New Company

Edit `config/config.json`:

```json
{
  "name": "YourCompany",
  "linkedin_id": "your-company",
  "github_org": "yourcompany",
  "blog_url": "https://yourcompany.com/blog",
  "press_url": "https://yourcompany.com/news"
}
```

Then run:
```python
from main import GTMIntelligencePlatform

platform = GTMIntelligencePlatform()
your_config = {...}
platform.run_full_intelligence_gathering("YourCompany", your_config)
```

### Adjusting Collection Parameters

Edit `config/config.json`:

```json
{
  "data_collection": {
    "news_days_back": 60,  // Collect 60 days of news
    "github_search_limit": 50,  // Get top 50 repos
    "enable_mock_data": false  // Use real APIs only
  }
}
```

## 🔑 API Keys & Rate Limits

### News API
- **Free Tier:** 100 requests/day
- **Paid Tier:** Higher limits available

### Crunchbase
- **Basic:** Limited requests/month
- **Pro:** Higher limits

### GitHub
- **No Auth:** 60 requests/hour
- **With Token:** 5,000 requests/hour

### LinkedIn
- **Restricted:** Official API requires partnership
- **Alternative:** Platform uses mock data by default

## 📝 Example: Stripe Case Study

The platform comes pre-configured with Stripe as an example fintech company. Running `main.py` will:

1. Collect Stripe's latest news, announcements, and GitHub activity
2. Analyze their hiring trends and growth signals
3. Generate insights about their GTM strategy
4. Provide actionable recommendations for engaging with Stripe

## 🛠️ Troubleshooting

### No API Keys
The platform works with mock data if API keys aren't provided. Set `"enable_mock_data": true` in config.

### Rate Limiting
If you hit rate limits, the platform will use cached data or mock data.

### Web Scraping Issues
Some websites block scrapers. The platform includes fallback mock data.

## 📚 Dependencies

Key Python packages:
- `requests` & `httpx` - HTTP clients for API calls
- `beautifulsoup4` - Web scraping
- `pandas` - Data processing
- `python-dotenv` - Environment variable management

See `requirements.txt` for the complete list.

## 🤝 Contributing

This is a template project. Feel free to:
- Add new data sources
- Improve classification algorithms
- Add visualization features
- Enhance reporting formats

## 📄 License

This project is provided as-is for educational and business purposes.

## ⚠️ Disclaimer

- Always respect website Terms of Service and robots.txt
- Use API keys responsibly and within rate limits
- Some data sources may require commercial licenses
- Mock data is provided for testing purposes only

## 🎓 Case Study: Using with Stripe

After running the intelligence gathering:

1. **Review Executive Report** (`outputs/reports/stripe_executive_report.txt`)
   - Get high-level overview of Stripe's GTM signals

2. **Check Recommendations** (`outputs/recommendations/stripe_recommendations_report.txt`)
   - Find specific actions to take
   - Get talking points for conversations

3. **Analyze Data Export** (`outputs/reports/stripe_data_export.csv`)
   - Import into your CRM
   - Track signals over time

4. **Act on Insights**
   - Use timing recommendations for outreach
   - Leverage talking points in conversations
   - Position based on intelligence gathered

---

**Built for GTM teams to make data-driven sales decisions** 🚀
