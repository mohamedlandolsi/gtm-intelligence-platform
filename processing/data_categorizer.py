"""
Data Categorizer for GTM Intelligence
Advanced categorization and aggregation of intelligence data
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime
from collections import defaultdict, Counter
import pandas as pd


class DataCategorizer:
    """Categorizes and aggregates intelligence data for GTM insights"""
    
    def __init__(self):
        self.gtm_signals = {
            'market_expansion': {
                'weight': 0.9,
                'indicators': ['expansion', 'new market', 'international', 'launches in']
            },
            'product_innovation': {
                'weight': 0.85,
                'indicators': ['product launch', 'new feature', 'innovation', 'release']
            },
            'partnership_strategy': {
                'weight': 0.8,
                'indicators': ['partnership', 'integration', 'collaboration']
            },
            'talent_acquisition': {
                'weight': 0.7,
                'indicators': ['hiring', 'talent', 'join our team', 'positions']
            },
            'funding_growth': {
                'weight': 0.95,
                'indicators': ['funding', 'raises', 'investment', 'valuation']
            },
            'customer_traction': {
                'weight': 0.85,
                'indicators': ['customer', 'case study', 'powers', 'enables']
            }
        }
    
    def categorize_all_data(self, data_dir: str = 'outputs/classified') -> Dict:
        """
        Categorize all classified data and create unified intelligence view
        
        Args:
            data_dir: Directory containing classified data files
            
        Returns:
            Dictionary with categorized intelligence
        """
        intelligence = {
            'company_overview': {},
            'gtm_signals': {},
            'competitive_intelligence': {},
            'developer_ecosystem': {},
            'growth_indicators': {},
            'strategic_initiatives': [],
            'recommendations': [],
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'data_sources': []
            }
        }
        
        # Load all classified data
        classified_files = self._get_classified_files(data_dir)
        
        for file_path in classified_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                source = os.path.basename(file_path)
                intelligence['metadata']['data_sources'].append(source)
                
                # Process different data types
                if 'news' in source:
                    self._process_news_data(data, intelligence)
                elif 'linkedin' in source:
                    self._process_linkedin_data(data, intelligence)
                elif 'github' in source:
                    self._process_github_data(data, intelligence)
                elif 'announcements' in source:
                    self._process_announcements_data(data, intelligence)
                elif 'crunchbase' in source:
                    self._process_crunchbase_data(data, intelligence)
        
        # Generate aggregated insights
        intelligence['gtm_signals'] = self._aggregate_gtm_signals(intelligence)
        intelligence['recommendations'] = self._generate_recommendations(intelligence)
        
        return intelligence
    
    def create_gtm_summary(self, intelligence: Dict) -> Dict:
        """
        Create executive summary of GTM intelligence
        
        Args:
            intelligence: Full intelligence dictionary
            
        Returns:
            Executive summary
        """
        summary = {
            'executive_summary': {},
            'key_findings': [],
            'priority_signals': [],
            'action_items': [],
            'generated_at': datetime.now().isoformat()
        }
        
        # Extract key findings
        gtm_signals = intelligence.get('gtm_signals', {})
        for signal_type, signal_data in gtm_signals.items():
            if signal_data.get('strength', 0) > 0.7:
                summary['key_findings'].append({
                    'type': signal_type,
                    'strength': signal_data.get('strength'),
                    'description': signal_data.get('summary'),
                    'evidence_count': len(signal_data.get('evidence', []))
                })
        
        # Sort findings by strength
        summary['key_findings'].sort(key=lambda x: x['strength'], reverse=True)
        
        # Extract priority signals
        strategic_initiatives = intelligence.get('strategic_initiatives', [])
        summary['priority_signals'] = strategic_initiatives[:5]
        
        # Generate action items
        summary['action_items'] = intelligence.get('recommendations', [])[:10]
        
        # Create executive summary text
        summary['executive_summary'] = self._create_executive_text(intelligence, summary)
        
        return summary
    
    def create_category_report(self, intelligence: Dict, category: str) -> Dict:
        """
        Create detailed report for specific category
        
        Args:
            intelligence: Full intelligence dictionary
            category: Category to report on (e.g., 'product_innovation')
            
        Returns:
            Category-specific report
        """
        report = {
            'category': category,
            'overview': {},
            'detailed_findings': [],
            'timeline': [],
            'recommendations': [],
            'generated_at': datetime.now().isoformat()
        }
        
        # Extract category-specific data
        gtm_signals = intelligence.get('gtm_signals', {})
        if category in gtm_signals:
            signal_data = gtm_signals[category]
            
            report['overview'] = {
                'strength': signal_data.get('strength'),
                'total_signals': len(signal_data.get('evidence', [])),
                'summary': signal_data.get('summary')
            }
            
            report['detailed_findings'] = signal_data.get('evidence', [])
            report['timeline'] = self._create_timeline(signal_data.get('evidence', []))
        
        # Category-specific recommendations
        all_recommendations = intelligence.get('recommendations', [])
        report['recommendations'] = [
            rec for rec in all_recommendations 
            if category in rec.get('related_categories', [])
        ]
        
        return report
    
    def _get_classified_files(self, data_dir: str) -> List[str]:
        """Get all classified data files"""
        files = []
        if os.path.exists(data_dir):
            for filename in os.listdir(data_dir):
                if filename.endswith('.json'):
                    files.append(os.path.join(data_dir, filename))
        return files
    
    def _process_news_data(self, data: List[Dict], intelligence: Dict):
        """Process classified news data"""
        for article in data:
            categories = article.get('gtm_categories', [])
            relevance = article.get('relevance_score', 0)
            
            if relevance > 0.5:
                initiative = {
                    'type': 'news',
                    'title': article.get('title'),
                    'categories': categories,
                    'date': article.get('published_at'),
                    'source': article.get('source'),
                    'url': article.get('url'),
                    'relevance': relevance,
                    'sentiment': article.get('sentiment')
                }
                intelligence['strategic_initiatives'].append(initiative)
    
    def _process_linkedin_data(self, data: Dict, intelligence: Dict):
        """Process classified LinkedIn data"""
        # Process job postings for hiring trends
        gtm_roles = [job for job in data.get('job_postings', []) if job.get('is_gtm_role')]
        
        intelligence['growth_indicators']['hiring_velocity'] = {
            'total_postings': len(data.get('job_postings', [])),
            'gtm_roles': len(gtm_roles),
            'departments_hiring': list(set(job.get('department') for job in data.get('job_postings', []))),
            'seniority_mix': Counter(job.get('seniority_level') for job in gtm_roles)
        }
        
        # Process employee insights
        employee_insights = data.get('employee_insights', {})
        intelligence['growth_indicators']['team_growth'] = {
            'total_employees': employee_insights.get('total_employees'),
            'growth_6m': employee_insights.get('employee_growth_6m'),
            'growth_1y': employee_insights.get('employee_growth_1y'),
            'department_distribution': employee_insights.get('department_distribution', {})
        }
    
    def _process_github_data(self, data: Dict, intelligence: Dict):
        """Process classified GitHub data"""
        repos = data.get('repositories', [])
        
        # Developer ecosystem metrics
        sdks = [repo for repo in repos if repo.get('is_sdk')]
        
        intelligence['developer_ecosystem'] = {
            'total_repositories': len(repos),
            'sdk_count': len(sdks),
            'total_stars': sum(repo.get('stars', 0) for repo in repos),
            'languages': list(set(repo.get('language') for repo in repos if repo.get('language'))),
            'top_repos': sorted(repos, key=lambda x: x.get('traction_score', 0), reverse=True)[:5],
            'developer_traction': sum(repo.get('traction_score', 0) for repo in sdks) / len(sdks) if sdks else 0
        }
    
    def _process_announcements_data(self, data: Dict, intelligence: Dict):
        """Process classified announcements data"""
        for post in data.get('blog_posts', []):
            if 'product_launch' in post.get('gtm_categories', []):
                intelligence['strategic_initiatives'].append({
                    'type': 'product_announcement',
                    'title': post.get('title'),
                    'date': post.get('published_date'),
                    'url': post.get('url'),
                    'content_type': post.get('content_type')
                })
    
    def _process_crunchbase_data(self, data: Dict, intelligence: Dict):
        """Process Crunchbase data"""
        if 'entities' in data and data['entities']:
            entity = data['entities'][0]
            props = entity.get('properties', {})
            
            intelligence['company_overview'] = {
                'name': props.get('identifier', {}).get('value'),
                'description': props.get('short_description'),
                'categories': props.get('categories', []),
                'founded': props.get('founded_on'),
                'headquarters': props.get('headquarters_location'),
                'website': props.get('website_url'),
                'employees': props.get('employee_count'),
                'funding_total': props.get('funding_total'),
                'last_funding': props.get('last_funding_type')
            }
    
    def _aggregate_gtm_signals(self, intelligence: Dict) -> Dict:
        """Aggregate all data into GTM signals"""
        signals = {}
        
        for signal_type, config in self.gtm_signals.items():
            evidence = []
            
            # Search through strategic initiatives for matching signals
            for initiative in intelligence.get('strategic_initiatives', []):
                categories = initiative.get('categories', [])
                title = (initiative.get('title') or '').lower()
                
                # Check if initiative matches this signal
                if any(indicator in title for indicator in config['indicators']):
                    evidence.append(initiative)
            
            # Calculate signal strength
            strength = min(len(evidence) * 0.15 * config['weight'], 1.0)
            
            signals[signal_type] = {
                'strength': round(strength, 2),
                'evidence_count': len(evidence),
                'evidence': evidence[:10],  # Top 10 pieces of evidence
                'summary': self._create_signal_summary(signal_type, evidence)
            }
        
        return signals
    
    def _create_signal_summary(self, signal_type: str, evidence: List[Dict]) -> str:
        """Create summary text for a GTM signal"""
        if not evidence:
            return f"No strong signals detected for {signal_type.replace('_', ' ')}"
        
        count = len(evidence)
        signal_name = signal_type.replace('_', ' ').title()
        
        return f"Detected {count} indicators of {signal_name}. Recent activity suggests active focus in this area."
    
    def _generate_recommendations(self, intelligence: Dict) -> List[Dict]:
        """Generate GTM recommendations based on intelligence"""
        recommendations = []
        
        gtm_signals = intelligence.get('gtm_signals', {})
        
        # Recommendation 1: Product positioning
        if gtm_signals.get('product_innovation', {}).get('strength', 0) > 0.6:
            recommendations.append({
                'priority': 'high',
                'category': 'positioning',
                'title': 'Competitive differentiation opportunity',
                'description': 'Strong product innovation signals suggest new capabilities to highlight in sales conversations',
                'action': 'Update sales collateral to emphasize latest product launches',
                'related_categories': ['product_innovation']
            })
        
        # Recommendation 2: Market timing
        if gtm_signals.get('market_expansion', {}).get('strength', 0) > 0.7:
            recommendations.append({
                'priority': 'high',
                'category': 'timing',
                'title': 'Market expansion momentum',
                'description': 'Company is actively expanding into new markets - opportunity to engage before market saturation',
                'action': 'Prioritize outreach, emphasizing early partnership benefits',
                'related_categories': ['market_expansion', 'partnership_strategy']
            })
        
        # Recommendation 3: Developer engagement
        dev_traction = intelligence.get('developer_ecosystem', {}).get('developer_traction', 0)
        if dev_traction > 50:
            recommendations.append({
                'priority': 'medium',
                'category': 'engagement',
                'title': 'Strong developer ecosystem',
                'description': 'High GitHub activity indicates technical depth and developer adoption',
                'action': 'Leverage developer-focused messaging in technical sales conversations',
                'related_categories': ['product_innovation']
            })
        
        # Recommendation 4: Hiring velocity
        hiring = intelligence.get('growth_indicators', {}).get('hiring_velocity', {})
        if hiring.get('gtm_roles', 0) > 10:
            recommendations.append({
                'priority': 'high',
                'category': 'timing',
                'title': 'GTM team expansion',
                'description': f"Company is actively hiring {hiring.get('gtm_roles')} GTM roles - signals growth phase",
                'action': 'Engage now while team is ramping and establishing processes',
                'related_categories': ['talent_acquisition']
            })
        
        # Recommendation 5: Partnership opportunities
        if gtm_signals.get('partnership_strategy', {}).get('strength', 0) > 0.6:
            recommendations.append({
                'priority': 'medium',
                'category': 'partnerships',
                'title': 'Active partnership strategy',
                'description': 'Multiple partnership announcements indicate openness to collaborations',
                'action': 'Explore strategic partnership angles in sales approach',
                'related_categories': ['partnership_strategy']
            })
        
        return recommendations
    
    def _create_executive_text(self, intelligence: Dict, summary: Dict) -> str:
        """Create executive summary text"""
        company = intelligence.get('company_overview', {}).get('name', 'Target Company')
        
        text = f"GTM Intelligence Summary for {company}\n\n"
        
        # Key signals
        top_signals = summary['key_findings'][:3]
        if top_signals:
            text += "Top GTM Signals:\n"
            for signal in top_signals:
                text += f"- {signal['type'].replace('_', ' ').title()}: {signal['description']}\n"
        
        # Growth indicators
        hiring = intelligence.get('growth_indicators', {}).get('hiring_velocity', {})
        if hiring:
            text += f"\nGrowth Indicators:\n"
            text += f"- {hiring.get('total_postings', 0)} active job postings ({hiring.get('gtm_roles', 0)} GTM roles)\n"
        
        return text
    
    def _create_timeline(self, evidence: List[Dict]) -> List[Dict]:
        """Create timeline from evidence"""
        timeline = []
        for item in evidence:
            if 'date' in item:
                timeline.append({
                    'date': item['date'],
                    'event': item.get('title'),
                    'type': item.get('type')
                })
        
        timeline.sort(key=lambda x: x['date'], reverse=True)
        return timeline
    
    def save_categorized_data(self, data: Dict, filename: str):
        """Save categorized data to JSON file"""
        output_path = os.path.join('outputs', 'categorized', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved categorized data to {output_path}")


if __name__ == "__main__":
    categorizer = DataCategorizer()
    
    # Categorize all intelligence
    intelligence = categorizer.categorize_all_data()
    categorizer.save_categorized_data(intelligence, 'full_intelligence.json')
    
    # Create executive summary
    summary = categorizer.create_gtm_summary(intelligence)
    categorizer.save_categorized_data(summary, 'executive_summary.json')
    
    print("Data categorization complete")
