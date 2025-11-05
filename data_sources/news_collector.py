"""
News API Collector for GTM Intelligence
Collects news articles about fintech companies from various news APIs
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json


class NewsCollector:
    """Collects news articles from multiple news APIs"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2/everything"
        
    def collect_company_news(
        self, 
        company_name: str, 
        days_back: int = 30,
        language: str = "en"
    ) -> List[Dict]:
        """
        Collect news articles about a specific company
        
        Args:
            company_name: Name of the company (e.g., "Stripe")
            days_back: Number of days to look back
            language: Language of articles
            
        Returns:
            List of news articles with metadata
        """
        if not self.api_key:
            print("Warning: No API key provided. Using mock data.")
            return self._get_mock_data(company_name)
        
        from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        params = {
            'q': f'"{company_name}" AND (fintech OR payments OR finance)',
            'from': from_date,
            'language': language,
            'sortBy': 'publishedAt',
            'apiKey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'source': article.get('source', {}).get('name'),
                    'title': article.get('title'),
                    'description': article.get('description'),
                    'url': article.get('url'),
                    'published_at': article.get('publishedAt'),
                    'content': article.get('content'),
                    'category': 'news',
                    'collected_at': datetime.now().isoformat()
                })
            
            return articles
        except requests.exceptions.RequestException as e:
            print(f"Error collecting news: {e}")
            return []
    
    def _get_mock_data(self, company_name: str) -> List[Dict]:
        """Return mock data for testing without API key"""
        return [
            {
                'source': 'TechCrunch',
                'title': f'{company_name} announces new payment feature',
                'description': f'{company_name} expands its fintech capabilities',
                'url': 'https://example.com/article1',
                'published_at': datetime.now().isoformat(),
                'content': 'Mock article content',
                'category': 'news',
                'collected_at': datetime.now().isoformat()
            }
        ]
    
    def save_to_json(self, articles: List[Dict], filename: str):
        """Save collected articles to JSON file"""
        output_path = os.path.join('outputs', 'raw_data', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(articles)} articles to {output_path}")


if __name__ == "__main__":
    collector = NewsCollector()
    articles = collector.collect_company_news("Stripe", days_back=30)
    collector.save_to_json(articles, 'stripe_news.json')
    print(f"Collected {len(articles)} news articles")
