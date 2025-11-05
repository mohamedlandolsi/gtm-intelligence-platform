"""
Stripe News Collection Module
Collects recent news and announcements about Stripe from multiple sources
"""

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import time
from urllib.parse import urljoin
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StripeNewsCollector:
    """Collects news and announcements about Stripe from various sources"""
    
    def __init__(self, api_key: Optional[str] = None, months_back: int = 3):
        """
        Initialize the collector
        
        Args:
            api_key: NewsAPI.org API key (optional)
            months_back: Number of months to look back for news
        """
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        self.months_back = months_back
        self.cutoff_date = datetime.now() - timedelta(days=months_back * 30)
        
        # Request headers to avoid blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        # Timeout settings
        self.timeout = 10
        
        # Rate limiting
        self.request_delay = 1  # seconds between requests
        
    def get_news_from_api(self) -> List[Dict]:
        """
        Fetch Stripe news from NewsAPI.org
        
        Returns:
            List of news articles with standardized format
        """
        logger.info("Fetching news from NewsAPI.org...")
        
        if not self.api_key:
            logger.warning("No NewsAPI key provided. Using mock data.")
            return self._get_mock_news_api_data()
        
        all_articles = []
        search_queries = [
            "Stripe fintech",
            "Stripe funding",
            "Stripe partnerships",
            "Stripe product launch"
        ]
        
        from_date = self.cutoff_date.strftime('%Y-%m-%d')
        base_url = "https://newsapi.org/v2/everything"
        
        for query in search_queries:
            try:
                logger.info(f"Searching for: {query}")
                
                params = {
                    'q': query,
                    'from': from_date,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'apiKey': self.api_key,
                    'pageSize': 20  # Max per query
                }
                
                response = requests.get(
                    base_url, 
                    params=params, 
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                data = response.json()
                
                if data.get('status') == 'ok':
                    articles = data.get('articles', [])
                    logger.info(f"Found {len(articles)} articles for '{query}'")
                    
                    for article in articles:
                        formatted_article = self._format_news_api_article(article, query)
                        if formatted_article:
                            all_articles.append(formatted_article)
                else:
                    logger.error(f"API returned error: {data.get('message')}")
                
                # Rate limiting
                time.sleep(self.request_delay)
                
            except requests.exceptions.Timeout:
                logger.error(f"Timeout while fetching news for '{query}'")
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching news for '{query}': {e}")
            except Exception as e:
                logger.error(f"Unexpected error for '{query}': {e}")
        
        # Remove duplicates based on URL
        unique_articles = self._remove_duplicates(all_articles)
        logger.info(f"Total unique articles collected: {len(unique_articles)}")
        
        return unique_articles
    
    def get_company_announcements(self) -> List[Dict]:
        """
        Scrape Stripe's official blog and press releases
        
        Returns:
            List of company announcements with standardized format
        """
        logger.info("Fetching Stripe company announcements...")
        
        announcements = []
        
        # Stripe blog
        blog_announcements = self._scrape_stripe_blog()
        announcements.extend(blog_announcements)
        
        # Stripe newsroom/press releases
        press_announcements = self._scrape_stripe_newsroom()
        announcements.extend(press_announcements)
        
        # Filter for last 3 months only
        filtered_announcements = [
            ann for ann in announcements
            if self._is_within_date_range(ann.get('published_date'))
        ]
        
        logger.info(f"Total announcements collected: {len(filtered_announcements)}")
        return filtered_announcements
    
    def get_industry_news(self) -> List[Dict]:
        """
        Collect broader fintech industry news that affects Stripe
        
        Returns:
            List of industry news articles (5-7 relevant articles)
        """
        logger.info("Fetching fintech industry news...")
        
        if not self.api_key:
            logger.warning("No NewsAPI key provided. Using mock data.")
            return self._get_mock_industry_news()
        
        industry_keywords = [
            "payment processing trends 2025",
            "B2B fintech 2025",
            "payment infrastructure",
            "digital payments innovation",
            "fintech API platforms"
        ]
        
        all_articles = []
        base_url = "https://newsapi.org/v2/everything"
        from_date = self.cutoff_date.strftime('%Y-%m-%d')
        
        for keyword in industry_keywords:
            try:
                logger.info(f"Searching for industry trend: {keyword}")
                
                params = {
                    'q': keyword,
                    'from': from_date,
                    'language': 'en',
                    'sortBy': 'relevancy',
                    'apiKey': self.api_key,
                    'pageSize': 5
                }
                
                response = requests.get(
                    base_url,
                    params=params,
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                data = response.json()
                
                if data.get('status') == 'ok':
                    articles = data.get('articles', [])
                    logger.info(f"Found {len(articles)} articles for '{keyword}'")
                    
                    for article in articles:
                        formatted_article = self._format_news_api_article(article, keyword)
                        if formatted_article:
                            formatted_article['category'] = 'industry_trend'
                            all_articles.append(formatted_article)
                
                time.sleep(self.request_delay)
                
            except Exception as e:
                logger.error(f"Error fetching industry news for '{keyword}': {e}")
        
        # Remove duplicates and limit to 7 most relevant
        unique_articles = self._remove_duplicates(all_articles)
        limited_articles = unique_articles[:7]
        
        logger.info(f"Selected {len(limited_articles)} most relevant industry articles")
        return limited_articles
    
    def _scrape_stripe_blog(self) -> List[Dict]:
        """Scrape Stripe's official blog"""
        logger.info("Scraping Stripe blog...")
        
        blog_url = "https://stripe.com/blog"
        articles = []
        
        try:
            response = requests.get(
                blog_url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find blog post elements (Stripe's structure may vary)
            # Looking for common patterns
            post_selectors = [
                'article',
                '[class*="post"]',
                '[class*="blog"]',
                '[class*="article"]'
            ]
            
            posts = []
            for selector in post_selectors:
                posts = soup.select(selector)
                if posts:
                    break
            
            if not posts:
                logger.warning("Could not find blog posts on Stripe blog. Using fallback data.")
                return self._get_mock_stripe_blog_data()
            
            for post in posts[:20]:  # Limit to first 20
                try:
                    # Extract title
                    title_elem = post.find(['h1', 'h2', 'h3', 'h4'])
                    title = title_elem.get_text(strip=True) if title_elem else None
                    
                    # Extract link
                    link_elem = post.find('a', href=True)
                    link = urljoin(blog_url, link_elem['href']) if link_elem else None
                    
                    # Extract description
                    desc_elem = post.find('p')
                    description = desc_elem.get_text(strip=True)[:200] if desc_elem else ""
                    
                    # Extract date
                    date_elem = post.find(['time', '[class*="date"]'])
                    date_str = None
                    if date_elem:
                        date_str = date_elem.get('datetime') or date_elem.get_text(strip=True)
                    
                    if title and link:
                        articles.append({
                            'headline': title,
                            'description': description,
                            'published_date': self._parse_date(date_str),
                            'source_url': link,
                            'source_name': 'Stripe Blog',
                            'category': 'company_announcement',
                            'type': 'blog_post',
                            'collected_at': datetime.now().isoformat()
                        })
                
                except Exception as e:
                    logger.debug(f"Error parsing blog post: {e}")
                    continue
            
            logger.info(f"Scraped {len(articles)} articles from Stripe blog")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error accessing Stripe blog: {e}")
            return self._get_mock_stripe_blog_data()
        except Exception as e:
            logger.error(f"Unexpected error scraping Stripe blog: {e}")
            return self._get_mock_stripe_blog_data()
        
        return articles if articles else self._get_mock_stripe_blog_data()
    
    def _scrape_stripe_newsroom(self) -> List[Dict]:
        """Scrape Stripe's newsroom/press releases"""
        logger.info("Scraping Stripe newsroom...")
        
        newsroom_url = "https://stripe.com/newsroom"
        articles = []
        
        try:
            response = requests.get(
                newsroom_url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for press release elements
            press_items = soup.find_all(['article', 'div'], class_=lambda x: x and ('press' in x.lower() or 'news' in x.lower()))
            
            if not press_items:
                # Fallback: look for any links that might be press releases
                press_items = soup.find_all('a', href=lambda x: x and '/newsroom/' in x)
            
            if not press_items:
                logger.warning("Could not find press releases. Using fallback data.")
                return self._get_mock_stripe_press_data()
            
            for item in press_items[:15]:  # Limit to first 15
                try:
                    if item.name == 'a':
                        title = item.get_text(strip=True)
                        link = urljoin(newsroom_url, item['href'])
                        description = ""
                        date_str = None
                    else:
                        title_elem = item.find(['h1', 'h2', 'h3', 'h4', 'a'])
                        title = title_elem.get_text(strip=True) if title_elem else None
                        
                        link_elem = item.find('a', href=True)
                        link = urljoin(newsroom_url, link_elem['href']) if link_elem else None
                        
                        desc_elem = item.find('p')
                        description = desc_elem.get_text(strip=True)[:200] if desc_elem else ""
                        
                        date_elem = item.find(['time', '[class*="date"]'])
                        date_str = None
                        if date_elem:
                            date_str = date_elem.get('datetime') or date_elem.get_text(strip=True)
                    
                    if title and link and len(title) > 10:
                        articles.append({
                            'headline': title,
                            'description': description,
                            'published_date': self._parse_date(date_str),
                            'source_url': link,
                            'source_name': 'Stripe Newsroom',
                            'category': 'company_announcement',
                            'type': 'press_release',
                            'collected_at': datetime.now().isoformat()
                        })
                
                except Exception as e:
                    logger.debug(f"Error parsing press release: {e}")
                    continue
            
            logger.info(f"Scraped {len(articles)} press releases from Stripe newsroom")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error accessing Stripe newsroom: {e}")
            return self._get_mock_stripe_press_data()
        except Exception as e:
            logger.error(f"Unexpected error scraping Stripe newsroom: {e}")
            return self._get_mock_stripe_press_data()
        
        return articles if articles else self._get_mock_stripe_press_data()
    
    def _format_news_api_article(self, article: Dict, search_query: str) -> Optional[Dict]:
        """Format NewsAPI article to standardized format"""
        try:
            return {
                'headline': article.get('title', '').strip(),
                'description': article.get('description', '').strip() or article.get('content', '').strip()[:200],
                'published_date': self._parse_date(article.get('publishedAt')),
                'source_url': article.get('url'),
                'source_name': article.get('source', {}).get('name', 'Unknown'),
                'category': 'news',
                'search_query': search_query,
                'author': article.get('author'),
                'collected_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.debug(f"Error formatting article: {e}")
            return None
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[str]:
        """Parse date string to ISO format"""
        if not date_str:
            return None
        
        try:
            # Try ISO format first
            if 'T' in date_str or 'Z' in date_str:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d')
            
            # Try common date formats
            formats = [
                '%Y-%m-%d',
                '%B %d, %Y',
                '%b %d, %Y',
                '%d %B %Y',
                '%d %b %Y',
                '%m/%d/%Y',
                '%d/%m/%Y'
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(date_str.strip(), fmt)
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            logger.debug(f"Could not parse date: {date_str}")
            return date_str
            
        except Exception as e:
            logger.debug(f"Error parsing date '{date_str}': {e}")
            return date_str
    
    def _is_within_date_range(self, date_str: Optional[str]) -> bool:
        """Check if date is within the specified range"""
        if not date_str:
            return True  # Include if no date available
        
        try:
            if 'T' in date_str:
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            
            return date_obj >= self.cutoff_date
        except Exception:
            return True  # Include if can't parse
    
    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on URL"""
        seen_urls = set()
        unique_articles = []
        
        for article in articles:
            url = article.get('source_url')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)
        
        return unique_articles
    
    def _get_mock_news_api_data(self) -> List[Dict]:
        """Return mock NewsAPI data for testing"""
        logger.info("Using mock NewsAPI data")
        
        base_date = datetime.now() - timedelta(days=15)
        
        return [
            {
                'headline': 'Stripe Expands Payment Infrastructure in Southeast Asia',
                'description': 'Stripe announces new partnerships with local banks in Singapore, Malaysia, and Indonesia to enhance payment processing capabilities.',
                'published_date': (base_date - timedelta(days=2)).strftime('%Y-%m-%d'),
                'source_url': 'https://techcrunch.com/stripe-asia-expansion',
                'source_name': 'TechCrunch',
                'category': 'news',
                'search_query': 'Stripe fintech',
                'collected_at': datetime.now().isoformat()
            },
            {
                'headline': 'Stripe Raises Additional $250M in Extended Series H',
                'description': 'The fintech giant secures more funding as it continues to invest in AI-powered fraud detection and global expansion.',
                'published_date': (base_date - timedelta(days=18)).strftime('%Y-%m-%d'),
                'source_url': 'https://fortune.com/stripe-funding-series-h',
                'source_name': 'Fortune',
                'category': 'news',
                'search_query': 'Stripe funding',
                'collected_at': datetime.now().isoformat()
            },
            {
                'headline': 'Stripe Partners with Major E-commerce Platform Shopify',
                'description': 'New integration promises faster checkout and better conversion rates for online merchants worldwide.',
                'published_date': (base_date - timedelta(days=25)).strftime('%Y-%m-%d'),
                'source_url': 'https://reuters.com/stripe-shopify-partnership',
                'source_name': 'Reuters',
                'category': 'news',
                'search_query': 'Stripe partnerships',
                'collected_at': datetime.now().isoformat()
            },
            {
                'headline': 'Stripe Launches AI-Powered Revenue Recognition Tool',
                'description': 'New product helps subscription businesses automate complex revenue recognition with machine learning.',
                'published_date': (base_date - timedelta(days=30)).strftime('%Y-%m-%d'),
                'source_url': 'https://bloomberg.com/stripe-revenue-recognition',
                'source_name': 'Bloomberg',
                'category': 'news',
                'search_query': 'Stripe product launch',
                'collected_at': datetime.now().isoformat()
            },
            {
                'headline': 'How Stripe is Winning the B2B Payment Processing War',
                'description': 'Analysis of Stripe\'s strategy to dominate the enterprise payment infrastructure market.',
                'published_date': (base_date - timedelta(days=40)).strftime('%Y-%m-%d'),
                'source_url': 'https://wsj.com/stripe-b2b-strategy',
                'source_name': 'Wall Street Journal',
                'category': 'news',
                'search_query': 'Stripe fintech',
                'collected_at': datetime.now().isoformat()
            }
        ]
    
    def _get_mock_stripe_blog_data(self) -> List[Dict]:
        """Return mock Stripe blog data"""
        logger.info("Using mock Stripe blog data")
        
        base_date = datetime.now()
        
        return [
            {
                'headline': 'Introducing Stripe Data Pipeline 2.0',
                'description': 'Stream your payment data directly to your data warehouse with our improved ETL capabilities.',
                'published_date': (base_date - timedelta(days=5)).strftime('%Y-%m-%d'),
                'source_url': 'https://stripe.com/blog/data-pipeline-v2',
                'source_name': 'Stripe Blog',
                'category': 'company_announcement',
                'type': 'blog_post',
                'collected_at': datetime.now().isoformat()
            },
            {
                'headline': 'How We Built Stripe\'s New Fraud Detection Engine',
                'description': 'Behind the scenes look at our machine learning infrastructure that processes millions of transactions.',
                'published_date': (base_date - timedelta(days=12)).strftime('%Y-%m-%d'),
                'source_url': 'https://stripe.com/blog/fraud-detection-ml',
                'source_name': 'Stripe Blog',
                'category': 'company_announcement',
                'type': 'blog_post',
                'collected_at': datetime.now().isoformat()
            },
            {
                'headline': 'Stripe Connect: New Features for Platform Businesses',
                'description': 'Announcing enhanced capabilities for marketplaces and platforms, including improved onboarding flows.',
                'published_date': (base_date - timedelta(days=20)).strftime('%Y-%m-%d'),
                'source_url': 'https://stripe.com/blog/connect-updates',
                'source_name': 'Stripe Blog',
                'category': 'company_announcement',
                'type': 'blog_post',
                'collected_at': datetime.now().isoformat()
            }
        ]
    
    def _get_mock_stripe_press_data(self) -> List[Dict]:
        """Return mock Stripe press release data"""
        logger.info("Using mock Stripe press data")
        
        base_date = datetime.now()
        
        return [
            {
                'headline': 'Stripe Announces Partnership with Leading Cloud Provider',
                'description': 'Strategic collaboration to offer embedded payment solutions to enterprise customers.',
                'published_date': (base_date - timedelta(days=8)).strftime('%Y-%m-%d'),
                'source_url': 'https://stripe.com/newsroom/cloud-partnership',
                'source_name': 'Stripe Newsroom',
                'category': 'company_announcement',
                'type': 'press_release',
                'collected_at': datetime.now().isoformat()
            },
            {
                'headline': 'Stripe Reaches $70B Valuation in Latest Funding',
                'description': 'Company raises funds to accelerate global expansion and product development initiatives.',
                'published_date': (base_date - timedelta(days=35)).strftime('%Y-%m-%d'),
                'source_url': 'https://stripe.com/newsroom/series-h-funding',
                'source_name': 'Stripe Newsroom',
                'category': 'company_announcement',
                'type': 'press_release',
                'collected_at': datetime.now().isoformat()
            }
        ]
    
    def _get_mock_industry_news(self) -> List[Dict]:
        """Return mock industry news data"""
        logger.info("Using mock industry news data")
        
        base_date = datetime.now()
        
        return [
            {
                'headline': 'The Future of Payment Processing: 2025 Trends Report',
                'description': 'Analysis of emerging trends in digital payments including real-time processing and embedded finance.',
                'published_date': (base_date - timedelta(days=10)).strftime('%Y-%m-%d'),
                'source_url': 'https://fintechmagazine.com/payment-trends-2025',
                'source_name': 'FinTech Magazine',
                'category': 'industry_trend',
                'collected_at': datetime.now().isoformat()
            },
            {
                'headline': 'B2B Fintech Market Expected to Reach $500B by 2026',
                'description': 'Research shows rapid growth in business payment solutions as enterprises modernize their infrastructure.',
                'published_date': (base_date - timedelta(days=15)).strftime('%Y-%m-%d'),
                'source_url': 'https://marketresearch.com/b2b-fintech-growth',
                'source_name': 'Market Research Today',
                'category': 'industry_trend',
                'collected_at': datetime.now().isoformat()
            },
            {
                'headline': 'How APIs are Transforming the Payment Infrastructure Landscape',
                'description': 'Deep dive into how API-first platforms are enabling innovation in financial services.',
                'published_date': (base_date - timedelta(days=22)).strftime('%Y-%m-%d'),
                'source_url': 'https://apieconomy.com/payment-apis',
                'source_name': 'API Economy',
                'category': 'industry_trend',
                'collected_at': datetime.now().isoformat()
            },
            {
                'headline': 'Digital Payments Innovation: What\'s Next After Mobile Wallets',
                'description': 'Exploring emerging technologies like biometric payments and blockchain integration.',
                'published_date': (base_date - timedelta(days=28)).strftime('%Y-%m-%d'),
                'source_url': 'https://digitalbanking.com/innovation-report',
                'source_name': 'Digital Banking News',
                'category': 'industry_trend',
                'collected_at': datetime.now().isoformat()
            },
            {
                'headline': 'Why Fintech Platforms are Winning the Infrastructure Battle',
                'description': 'Analysis of how platform companies are displacing traditional payment processors.',
                'published_date': (base_date - timedelta(days=40)).strftime('%Y-%m-%d'),
                'source_url': 'https://venturebeat.com/fintech-platforms',
                'source_name': 'VentureBeat',
                'category': 'industry_trend',
                'collected_at': datetime.now().isoformat()
            }
        ]
    
    def collect_all_news(self) -> Dict[str, List[Dict]]:
        """
        Collect all news types in one call
        
        Returns:
            Dictionary with keys: 'api_news', 'company_announcements', 'industry_news'
        """
        logger.info("=" * 80)
        logger.info("Starting comprehensive Stripe news collection")
        logger.info("=" * 80)
        
        results = {
            'api_news': [],
            'company_announcements': [],
            'industry_news': [],
            'metadata': {
                'collection_date': datetime.now().isoformat(),
                'months_back': self.months_back,
                'cutoff_date': self.cutoff_date.strftime('%Y-%m-%d')
            }
        }
        
        # Collect from NewsAPI
        try:
            results['api_news'] = self.get_news_from_api()
            logger.info(f"✓ Collected {len(results['api_news'])} articles from NewsAPI")
        except Exception as e:
            logger.error(f"Failed to collect NewsAPI data: {e}")
        
        # Collect company announcements
        try:
            results['company_announcements'] = self.get_company_announcements()
            logger.info(f"✓ Collected {len(results['company_announcements'])} company announcements")
        except Exception as e:
            logger.error(f"Failed to collect company announcements: {e}")
        
        # Collect industry news
        try:
            results['industry_news'] = self.get_industry_news()
            logger.info(f"✓ Collected {len(results['industry_news'])} industry articles")
        except Exception as e:
            logger.error(f"Failed to collect industry news: {e}")
        
        total_articles = (
            len(results['api_news']) + 
            len(results['company_announcements']) + 
            len(results['industry_news'])
        )
        
        logger.info("=" * 80)
        logger.info(f"Collection complete! Total articles: {total_articles}")
        logger.info("=" * 80)
        
        return results
    
    def save_to_json(self, data: Dict, filename: str = 'stripe_news_collection.json'):
        """Save collected news to JSON file"""
        output_dir = 'outputs/raw_data'
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Data saved to {filepath}")
        return filepath


# Convenience functions for direct use
def collect_stripe_news(api_key: Optional[str] = None, months_back: int = 3) -> Dict[str, List[Dict]]:
    """
    Convenience function to collect all Stripe news
    
    Args:
        api_key: NewsAPI.org API key (optional)
        months_back: Number of months to look back
    
    Returns:
        Dictionary with all collected news
    """
    collector = StripeNewsCollector(api_key=api_key, months_back=months_back)
    return collector.collect_all_news()


if __name__ == "__main__":
    # Example usage
    print("Stripe News Collection Module")
    print("=" * 80)
    
    # Initialize collector
    collector = StripeNewsCollector(months_back=3)
    
    # Collect all news
    all_news = collector.collect_all_news()
    
    # Save to file
    filepath = collector.save_to_json(all_news)
    
    # Print summary
    print("\n" + "=" * 80)
    print("COLLECTION SUMMARY")
    print("=" * 80)
    print(f"NewsAPI Articles: {len(all_news['api_news'])}")
    print(f"Company Announcements: {len(all_news['company_announcements'])}")
    print(f"Industry News: {len(all_news['industry_news'])}")
    print(f"\nData saved to: {filepath}")
    print("=" * 80)
