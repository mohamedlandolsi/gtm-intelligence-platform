"""
Data Classifier for GTM Intelligence
Classifies collected data into categories relevant for GTM strategy
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime
import re


class DataClassifier:
    """Classifies data into GTM-relevant categories"""
    
    def __init__(self):
        self.gtm_categories = {
            'product_launch': [
                'launch', 'announcing', 'introduce', 'new product', 'release',
                'available now', 'introducing'
            ],
            'partnership': [
                'partner', 'partnership', 'collaboration', 'integration',
                'announces partnership', 'teams up', 'joins forces'
            ],
            'funding': [
                'funding', 'raises', 'series', 'investment', 'valuation',
                'round', 'capital', 'investors'
            ],
            'expansion': [
                'expands', 'expansion', 'entering', 'new market', 'launches in',
                'available in', 'global', 'international'
            ],
            'hiring': [
                'hiring', 'join our team', 'we\'re looking for', 'career',
                'job opening', 'positions', 'talent'
            ],
            'customer_win': [
                'customer', 'case study', 'success story', 'client',
                'powers', 'helps', 'enables'
            ],
            'competitive': [
                'vs', 'versus', 'alternative', 'comparison', 'better than',
                'replaces', 'migration'
            ],
            'thought_leadership': [
                'guide', 'how to', 'best practices', 'trends', 'future of',
                'insights', 'report'
            ],
            'event': [
                'conference', 'summit', 'webinar', 'event', 'speaking',
                'presenting', 'join us'
            ]
        }
        
        self.sentiment_positive = [
            'excited', 'proud', 'delighted', 'thrilled', 'happy',
            'success', 'growth', 'milestone', 'achievement'
        ]
        
        self.sentiment_negative = [
            'issue', 'problem', 'outage', 'incident', 'apologize',
            'sorry', 'delayed', 'concern'
        ]
    
    def classify_news_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Classify news articles by GTM relevance and category
        
        Args:
            articles: List of news articles
            
        Returns:
            List of classified articles with added metadata
        """
        classified = []
        
        for article in articles:
            text = f"{article.get('title', '')} {article.get('description', '')}".lower()
            
            # Determine categories
            categories = self._categorize_text(text)
            
            # Determine sentiment
            sentiment = self._analyze_sentiment(text)
            
            # Calculate GTM relevance score
            relevance_score = self._calculate_relevance_score(text, categories)
            
            classified_article = article.copy()
            classified_article.update({
                'gtm_categories': categories,
                'sentiment': sentiment,
                'relevance_score': relevance_score,
                'classified_at': datetime.now().isoformat()
            })
            
            classified.append(classified_article)
        
        # Sort by relevance score
        classified.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return classified
    
    def classify_linkedin_data(self, linkedin_data: Dict) -> Dict:
        """
        Classify LinkedIn data (posts, jobs, insights)
        
        Args:
            linkedin_data: Dictionary with LinkedIn data
            
        Returns:
            Classified LinkedIn data
        """
        classified = {
            'updates': [],
            'job_postings': [],
            'employee_insights': linkedin_data.get('employee_insights', {}),
            'classified_at': datetime.now().isoformat()
        }
        
        # Classify updates
        for update in linkedin_data.get('updates', []):
            text = update.get('content', '').lower()
            categories = self._categorize_text(text)
            sentiment = self._analyze_sentiment(text)
            
            classified_update = update.copy()
            classified_update.update({
                'gtm_categories': categories,
                'sentiment': sentiment,
                'engagement_score': self._calculate_engagement_score(update)
            })
            classified['updates'].append(classified_update)
        
        # Classify job postings
        for job in linkedin_data.get('job_postings', []):
            classified_job = job.copy()
            classified_job['is_gtm_role'] = self._is_gtm_role(job)
            classified_job['seniority_level'] = self._extract_seniority(job)
            classified['job_postings'].append(classified_job)
        
        return classified
    
    def classify_github_data(self, github_data: Dict) -> Dict:
        """
        Classify GitHub repositories and activity
        
        Args:
            github_data: Dictionary with GitHub data
            
        Returns:
            Classified GitHub data
        """
        classified = {
            'repositories': [],
            'recent_activity': github_data.get('recent_activity', []),
            'classified_at': datetime.now().isoformat()
        }
        
        for repo in github_data.get('repositories', []):
            classified_repo = repo.copy()
            
            # Determine repository type
            classified_repo['repo_type'] = self._classify_repository_type(repo)
            
            # Calculate developer traction score
            classified_repo['traction_score'] = self._calculate_traction_score(repo)
            
            # Determine if it's a customer-facing SDK
            classified_repo['is_sdk'] = self._is_sdk(repo)
            
            classified['repositories'].append(classified_repo)
        
        return classified
    
    def classify_company_announcements(self, announcements: Dict) -> Dict:
        """
        Classify company announcements (blog posts, press releases, updates)
        
        Args:
            announcements: Dictionary with company announcements
            
        Returns:
            Classified announcements
        """
        classified = {
            'blog_posts': [],
            'press_releases': [],
            'product_updates': [],
            'classified_at': datetime.now().isoformat()
        }
        
        # Classify blog posts
        for post in announcements.get('blog_posts', []):
            text = f"{post.get('title', '')} {post.get('description', '')}".lower()
            categories = self._categorize_text(text)
            
            classified_post = post.copy()
            classified_post['gtm_categories'] = categories
            classified_post['content_type'] = self._determine_content_type(text)
            classified['blog_posts'].append(classified_post)
        
        # Classify press releases
        for release in announcements.get('press_releases', []):
            text = f"{release.get('title', '')} {release.get('description', '')}".lower()
            categories = self._categorize_text(text)
            
            classified_release = release.copy()
            classified_release['gtm_categories'] = categories
            classified_release['priority'] = 'high' if any(cat in ['funding', 'product_launch', 'partnership'] for cat in categories) else 'medium'
            classified['press_releases'].append(classified_release)
        
        # Classify product updates
        for update in announcements.get('product_updates', []):
            classified_update = update.copy()
            classified_update['impact'] = self._assess_product_update_impact(update)
            classified['product_updates'].append(classified_update)
        
        return classified
    
    def _categorize_text(self, text: str) -> List[str]:
        """Categorize text based on keyword matching"""
        categories = []
        
        for category, keywords in self.gtm_categories.items():
            if any(keyword in text for keyword in keywords):
                categories.append(category)
        
        return categories if categories else ['general']
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_count = sum(1 for word in self.sentiment_positive if word in text)
        negative_count = sum(1 for word in self.sentiment_negative if word in text)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _calculate_relevance_score(self, text: str, categories: List[str]) -> float:
        """Calculate GTM relevance score (0-1)"""
        high_priority_categories = ['product_launch', 'partnership', 'funding', 'expansion', 'customer_win']
        
        score = 0.0
        
        # Base score from categories
        if any(cat in high_priority_categories for cat in categories):
            score += 0.6
        elif categories and categories != ['general']:
            score += 0.3
        
        # Boost for multiple categories
        score += min(len(categories) * 0.1, 0.3)
        
        # Boost for GTM keywords
        gtm_keywords = ['sales', 'revenue', 'market', 'customer', 'growth']
        score += sum(0.02 for keyword in gtm_keywords if keyword in text)
        
        return min(score, 1.0)
    
    def _calculate_engagement_score(self, update: Dict) -> float:
        """Calculate engagement score for LinkedIn updates"""
        likes = update.get('likes', 0)
        comments = update.get('comments', 0)
        shares = update.get('shares', 0)
        
        # Weighted engagement score
        score = (likes * 1) + (comments * 3) + (shares * 5)
        
        # Normalize to 0-100
        return min(score / 50, 100)
    
    def _is_gtm_role(self, job: Dict) -> bool:
        """Determine if job posting is for a GTM role"""
        gtm_keywords = [
            'sales', 'account executive', 'business development', 'gtm',
            'go-to-market', 'revenue', 'partnership', 'marketing',
            'customer success', 'account manager'
        ]
        
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        
        return any(keyword in title or keyword in description for keyword in gtm_keywords)
    
    def _extract_seniority(self, job: Dict) -> str:
        """Extract seniority level from job posting"""
        title = job.get('title', '').lower()
        seniority = job.get('seniority', '').lower()
        
        if 'senior' in title or 'senior' in seniority or 'lead' in title:
            return 'senior'
        elif 'junior' in title or 'entry' in seniority:
            return 'junior'
        elif 'director' in title or 'vp' in title or 'head of' in title:
            return 'leadership'
        else:
            return 'mid-level'
    
    def _classify_repository_type(self, repo: Dict) -> str:
        """Classify type of GitHub repository"""
        name = repo.get('name', '').lower()
        description = (repo.get('description') or '').lower()
        topics = [t.lower() for t in repo.get('topics', [])]
        
        if any(term in name or term in description for term in ['sdk', 'client', 'library', 'api']):
            return 'sdk'
        elif any(term in topics for term in ['documentation', 'docs']):
            return 'documentation'
        elif 'sample' in name or 'example' in name or 'demo' in name:
            return 'sample'
        else:
            return 'tool'
    
    def _calculate_traction_score(self, repo: Dict) -> float:
        """Calculate developer traction score for repository"""
        stars = repo.get('stars', 0)
        forks = repo.get('forks', 0)
        watchers = repo.get('watchers', 0)
        
        # Weighted traction score
        score = (stars * 1) + (forks * 2) + (watchers * 0.5)
        
        # Normalize to 0-100
        return min(score / 100, 100)
    
    def _is_sdk(self, repo: Dict) -> bool:
        """Determine if repository is an SDK"""
        sdk_indicators = ['sdk', 'client', 'library', '-node', '-python', '-java', '-ruby', '-php']
        name = repo.get('name', '').lower()
        return any(indicator in name for indicator in sdk_indicators)
    
    def _determine_content_type(self, text: str) -> str:
        """Determine type of blog content"""
        if any(term in text for term in ['how to', 'guide', 'tutorial']):
            return 'educational'
        elif any(term in text for term in ['case study', 'customer', 'success story']):
            return 'case_study'
        elif any(term in text for term in ['announce', 'launch', 'introducing']):
            return 'announcement'
        elif any(term in text for term in ['trend', 'future', 'report', 'insights']):
            return 'thought_leadership'
        else:
            return 'general'
    
    def _assess_product_update_impact(self, update: Dict) -> str:
        """Assess impact level of product update"""
        title = update.get('title', '').lower()
        description = update.get('description', '').lower()
        category = update.get('category', '').lower()
        
        high_impact_terms = ['major', 'new', 'launch', 'breaking', 'security', 'critical']
        
        if any(term in title or term in description for term in high_impact_terms):
            return 'high'
        elif category in ['security', 'breaking_change']:
            return 'high'
        else:
            return 'medium'
    
    def save_classified_data(self, classified_data: Dict, filename: str):
        """Save classified data to JSON file"""
        output_path = os.path.join('outputs', 'classified', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(classified_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved classified data to {output_path}")


if __name__ == "__main__":
    classifier = DataClassifier()
    
    # Example: Classify news articles
    with open('outputs/raw_data/stripe_news.json', 'r') as f:
        news_data = json.load(f)
    
    classified_news = classifier.classify_news_articles(news_data)
    classifier.save_classified_data(classified_news, 'stripe_news_classified.json')
    
    print("Data classification complete")
