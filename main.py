"""
Main Orchestrator for GTM Intelligence Platform
Coordinates data collection, processing, and report generation
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional

# Import collectors
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_sources.news_collector import NewsCollector
from data_sources.crunchbase_collector import CrunchbaseCollector
from data_sources.linkedin_collector import LinkedInCollector
from data_sources.company_announcements_collector import CompanyAnnouncementsCollector
from data_sources.github_collector import GitHubCollector

# Import processors
from processing.data_classifier import DataClassifier
from processing.data_categorizer import DataCategorizer

# Import outputs
from outputs.report_generator import ReportGenerator
from outputs.recommendations_generator import RecommendationsGenerator


class GTMIntelligencePlatform:
    """Main orchestrator for GTM intelligence gathering"""
    
    def __init__(self, config_path: str = 'config/config.json'):
        """Initialize the platform with configuration"""
        self.config = self._load_config(config_path)
        self.company_name = None
        
        # Initialize collectors
        self.news_collector = NewsCollector()
        self.crunchbase_collector = CrunchbaseCollector()
        self.linkedin_collector = LinkedInCollector()
        self.announcements_collector = CompanyAnnouncementsCollector()
        self.github_collector = GitHubCollector()
        
        # Initialize processors
        self.classifier = DataClassifier()
        self.categorizer = DataCategorizer()
        
        # Initialize output generators
        self.report_generator = ReportGenerator()
        self.recommendations_generator = RecommendationsGenerator()
        
        # Create output directories
        self._create_directories()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'data_collection': {
                'news_days_back': 30,
                'github_search_limit': 30,
                'enable_mock_data': True
            },
            'processing': {
                'min_relevance_score': 0.3,
                'high_priority_threshold': 0.7
            },
            'output': {
                'generate_csv': True,
                'generate_reports': True,
                'generate_recommendations': True
            }
        }
    
    def _create_directories(self):
        """Create necessary output directories"""
        dirs = [
            'outputs/raw_data',
            'outputs/classified',
            'outputs/categorized',
            'outputs/reports',
            'outputs/recommendations'
        ]
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
    
    def run_full_intelligence_gathering(self, company_name: str, company_config: Dict):
        """
        Run complete intelligence gathering pipeline
        
        Args:
            company_name: Name of the target company
            company_config: Company-specific configuration (URLs, IDs, etc.)
        """
        self.company_name = company_name
        print(f"\n{'='*80}")
        print(f"GTM Intelligence Platform - {company_name}")
        print(f"{'='*80}\n")
        
        # Phase 1: Data Collection
        print("Phase 1: Data Collection")
        print("-" * 80)
        raw_data = self._collect_all_data(company_config)
        
        # Phase 2: Data Classification
        print("\nPhase 2: Data Classification")
        print("-" * 80)
        classified_data = self._classify_all_data(raw_data)
        
        # Phase 3: Data Categorization
        print("\nPhase 3: Data Categorization")
        print("-" * 80)
        intelligence = self._categorize_data()
        
        # Phase 4: Report Generation
        print("\nPhase 4: Report Generation")
        print("-" * 80)
        self._generate_reports(intelligence)
        
        # Phase 5: Recommendations
        print("\nPhase 5: Recommendations Generation")
        print("-" * 80)
        self._generate_recommendations(intelligence)
        
        print(f"\n{'='*80}")
        print("Intelligence gathering complete!")
        print(f"{'='*80}\n")
        print(f"Check the 'outputs/' directory for all generated files.")
    
    def _collect_all_data(self, company_config: Dict) -> Dict:
        """Collect data from all sources"""
        raw_data = {}
        
        # Collect news
        print("  → Collecting news articles...")
        news_articles = self.news_collector.collect_company_news(
            self.company_name,
            days_back=self.config['data_collection']['news_days_back']
        )
        self.news_collector.save_to_json(news_articles, f'{self.company_name.lower()}_news.json')
        raw_data['news'] = news_articles
        print(f"    ✓ Collected {len(news_articles)} articles")
        
        # Collect Crunchbase data
        print("  → Collecting Crunchbase data...")
        crunchbase_data = self.crunchbase_collector.get_organization_data(self.company_name)
        self.crunchbase_collector.save_to_json(crunchbase_data, f'{self.company_name.lower()}_crunchbase.json')
        raw_data['crunchbase'] = crunchbase_data
        print("    ✓ Collected company data")
        
        # Collect LinkedIn data
        print("  → Collecting LinkedIn data...")
        linkedin_updates = self.linkedin_collector.collect_company_updates(
            company_config.get('linkedin_id', self.company_name.lower())
        )
        linkedin_jobs = self.linkedin_collector.collect_job_postings(self.company_name)
        linkedin_insights = self.linkedin_collector.collect_employee_insights(self.company_name)
        
        linkedin_data = {
            'updates': linkedin_updates,
            'job_postings': linkedin_jobs,
            'employee_insights': linkedin_insights
        }
        self.linkedin_collector.save_to_json(linkedin_data, f'{self.company_name.lower()}_linkedin.json')
        raw_data['linkedin'] = linkedin_data
        print(f"    ✓ Collected {len(linkedin_updates)} updates, {len(linkedin_jobs)} jobs")
        
        # Collect company announcements
        print("  → Collecting company announcements...")
        blog_posts = self.announcements_collector.collect_blog_posts(
            company_config.get('blog_url', f'https://{self.company_name.lower()}.com/blog')
        )
        press_releases = self.announcements_collector.collect_press_releases(
            company_config.get('press_url', f'https://{self.company_name.lower()}.com/newsroom')
        )
        product_updates = self.announcements_collector.collect_product_updates(
            company_config.get('changelog_url', f'https://{self.company_name.lower()}.com/changelog')
        )
        
        announcements_data = {
            'blog_posts': blog_posts,
            'press_releases': press_releases,
            'product_updates': product_updates
        }
        self.announcements_collector.save_to_json(announcements_data, f'{self.company_name.lower()}_announcements.json')
        raw_data['announcements'] = announcements_data
        print(f"    ✓ Collected {len(blog_posts)} posts, {len(press_releases)} releases")
        
        # Collect GitHub data
        print("  → Collecting GitHub data...")
        github_repos = self.github_collector.search_company_repositories(
            self.company_name,
            org_name=company_config.get('github_org')
        )
        
        github_data = {
            'repositories': github_repos,
            'recent_activity': []
        }
        self.github_collector.save_to_json(github_data, f'{self.company_name.lower()}_github.json')
        raw_data['github'] = github_data
        print(f"    ✓ Collected {len(github_repos)} repositories")
        
        return raw_data
    
    def _classify_all_data(self, raw_data: Dict) -> Dict:
        """Classify all collected data"""
        classified_data = {}
        
        # Classify news
        print("  → Classifying news articles...")
        classified_news = self.classifier.classify_news_articles(raw_data.get('news', []))
        self.classifier.save_classified_data(classified_news, f'{self.company_name.lower()}_news_classified.json')
        classified_data['news'] = classified_news
        print(f"    ✓ Classified {len(classified_news)} articles")
        
        # Classify LinkedIn data
        print("  → Classifying LinkedIn data...")
        classified_linkedin = self.classifier.classify_linkedin_data(raw_data.get('linkedin', {}))
        self.classifier.save_classified_data(classified_linkedin, f'{self.company_name.lower()}_linkedin_classified.json')
        classified_data['linkedin'] = classified_linkedin
        print("    ✓ Classified LinkedIn data")
        
        # Classify GitHub data
        print("  → Classifying GitHub data...")
        classified_github = self.classifier.classify_github_data(raw_data.get('github', {}))
        self.classifier.save_classified_data(classified_github, f'{self.company_name.lower()}_github_classified.json')
        classified_data['github'] = classified_github
        print("    ✓ Classified GitHub data")
        
        # Classify announcements
        print("  → Classifying company announcements...")
        classified_announcements = self.classifier.classify_company_announcements(raw_data.get('announcements', {}))
        self.classifier.save_classified_data(classified_announcements, f'{self.company_name.lower()}_announcements_classified.json')
        classified_data['announcements'] = classified_announcements
        print("    ✓ Classified announcements")
        
        # Save Crunchbase data (already structured)
        if 'crunchbase' in raw_data:
            self.classifier.save_classified_data(raw_data['crunchbase'], f'{self.company_name.lower()}_crunchbase_classified.json')
        
        return classified_data
    
    def _categorize_data(self) -> Dict:
        """Categorize and aggregate all data"""
        print("  → Aggregating intelligence signals...")
        intelligence = self.categorizer.categorize_all_data('outputs/classified')
        self.categorizer.save_categorized_data(intelligence, 'full_intelligence.json')
        print("    ✓ Created unified intelligence view")
        
        print("  → Generating executive summary...")
        summary = self.categorizer.create_gtm_summary(intelligence)
        self.categorizer.save_categorized_data(summary, 'executive_summary.json')
        print("    ✓ Generated executive summary")
        
        return intelligence
    
    def _generate_reports(self, intelligence: Dict):
        """Generate all reports"""
        print("  → Generating executive report...")
        exec_report = self.report_generator.generate_executive_report(intelligence, self.company_name)
        self.report_generator.save_report(exec_report, f'{self.company_name.lower()}_executive_report.txt')
        print("    ✓ Executive report generated")
        
        print("  → Generating detailed analysis...")
        detailed_report = self.report_generator.generate_detailed_report(intelligence, self.company_name)
        self.report_generator.save_report(detailed_report, f'{self.company_name.lower()}_detailed_report.txt')
        print("    ✓ Detailed analysis generated")
        
        if self.config['output']['generate_csv']:
            print("  → Generating CSV export...")
            df = self.report_generator.generate_csv_export(intelligence, self.company_name)
            self.report_generator.save_csv(df, f'{self.company_name.lower()}_data_export.csv')
            print("    ✓ CSV export generated")
    
    def _generate_recommendations(self, intelligence: Dict):
        """Generate GTM recommendations"""
        print("  → Generating GTM recommendations...")
        recommendations = self.recommendations_generator.generate_all_recommendations(intelligence, self.company_name)
        self.recommendations_generator.save_recommendations(recommendations, f'{self.company_name.lower()}_recommendations.json')
        print("    ✓ Recommendations JSON generated")
        
        print("  → Generating recommendations report...")
        rec_report = self.recommendations_generator.generate_recommendations_report(recommendations)
        output_path = os.path.join('outputs', 'recommendations', f'{self.company_name.lower()}_recommendations_report.txt')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rec_report)
        print("    ✓ Recommendations report generated")


def main():
    """Main entry point"""
    # Initialize platform
    platform = GTMIntelligencePlatform()
    
    # Example: Stripe fintech case study
    stripe_config = {
        'linkedin_id': 'stripe',
        'github_org': 'stripe',
        'blog_url': 'https://stripe.com/blog',
        'press_url': 'https://stripe.com/newsroom',
        'changelog_url': 'https://stripe.com/docs/upgrades'
    }
    
    # Run intelligence gathering
    platform.run_full_intelligence_gathering("Stripe", stripe_config)
    
    # You can add more companies here
    # platform.run_full_intelligence_gathering("Plaid", plaid_config)
    # platform.run_full_intelligence_gathering("Brex", brex_config)


if __name__ == "__main__":
    main()
