"""
Recommendations Generator for GTM Intelligence
Generates actionable recommendations for sales and GTM teams
"""

import json
import os
from typing import Dict, List
from datetime import datetime


class RecommendationsGenerator:
    """Generates GTM recommendations from intelligence data"""
    
    def __init__(self):
        self.recommendation_types = {
            'positioning': 'How to position in sales conversations',
            'timing': 'When to engage and optimal timing',
            'messaging': 'Key messages and value propositions',
            'competitive': 'Competitive differentiation points',
            'engagement': 'Engagement strategies and channels',
            'partnerships': 'Partnership opportunities'
        }
    
    def generate_all_recommendations(self, intelligence: Dict, company_name: str) -> Dict:
        """
        Generate comprehensive recommendations
        
        Args:
            intelligence: Full intelligence dictionary
            company_name: Target company name
            
        Returns:
            Dictionary with all recommendations
        """
        recommendations = {
            'company': company_name,
            'generated_at': datetime.now().isoformat(),
            'positioning_recommendations': [],
            'timing_recommendations': [],
            'messaging_recommendations': [],
            'competitive_recommendations': [],
            'engagement_recommendations': [],
            'partnership_recommendations': [],
            'priority_actions': [],
            'talking_points': []
        }
        
        # Generate recommendations by type
        recommendations['positioning_recommendations'] = self._generate_positioning_recs(intelligence)
        recommendations['timing_recommendations'] = self._generate_timing_recs(intelligence)
        recommendations['messaging_recommendations'] = self._generate_messaging_recs(intelligence)
        recommendations['competitive_recommendations'] = self._generate_competitive_recs(intelligence)
        recommendations['engagement_recommendations'] = self._generate_engagement_recs(intelligence)
        recommendations['partnership_recommendations'] = self._generate_partnership_recs(intelligence)
        
        # Generate priority actions
        recommendations['priority_actions'] = self._generate_priority_actions(intelligence)
        
        # Generate talking points
        recommendations['talking_points'] = self._generate_talking_points(intelligence)
        
        return recommendations
    
    def _generate_positioning_recs(self, intelligence: Dict) -> List[Dict]:
        """Generate positioning recommendations"""
        recs = []
        gtm_signals = intelligence.get('gtm_signals', {})
        
        # Product innovation positioning
        product_signal = gtm_signals.get('product_innovation', {})
        if product_signal.get('strength', 0) > 0.6:
            recs.append({
                'title': 'Emphasize Innovation Partnership',
                'priority': 'high',
                'rationale': f"Strong product innovation signals (strength: {product_signal.get('strength'):.2f})",
                'recommendation': 'Position your solution as enabling their continued innovation and supporting their product velocity',
                'talking_points': [
                    'Support their rapid product development cycle',
                    'Enable faster time-to-market for new features',
                    'Scale with their innovation roadmap'
                ]
            })
        
        # Market expansion positioning
        expansion_signal = gtm_signals.get('market_expansion', {})
        if expansion_signal.get('strength', 0) > 0.6:
            recs.append({
                'title': 'Support Global Expansion',
                'priority': 'high',
                'rationale': f"Active market expansion detected (strength: {expansion_signal.get('strength'):.2f})",
                'recommendation': 'Position as a partner for their global growth, highlighting international capabilities',
                'talking_points': [
                    'Support their multi-market strategy',
                    'Enable consistent experience across regions',
                    'Proven success with expanding companies'
                ]
            })
        
        # Developer ecosystem positioning
        dev_traction = intelligence.get('developer_ecosystem', {}).get('developer_traction', 0)
        if dev_traction > 50:
            recs.append({
                'title': 'Technical Depth Positioning',
                'priority': 'medium',
                'rationale': f"Strong developer ecosystem (traction score: {dev_traction:.1f})",
                'recommendation': 'Position with technical depth, emphasizing API quality and developer experience',
                'talking_points': [
                    'Built for developers, by developers',
                    'Comprehensive API documentation and SDKs',
                    'Active developer community support'
                ]
            })
        
        return recs
    
    def _generate_timing_recs(self, intelligence: Dict) -> List[Dict]:
        """Generate timing recommendations"""
        recs = []
        growth = intelligence.get('growth_indicators', {})
        
        # Hiring velocity timing
        hiring = growth.get('hiring_velocity', {})
        if hiring.get('gtm_roles', 0) > 10:
            recs.append({
                'title': 'Engage During GTM Team Build-Out',
                'priority': 'high',
                'urgency': 'immediate',
                'rationale': f"Actively hiring {hiring.get('gtm_roles')} GTM roles",
                'recommendation': 'Engage immediately while team is being built and processes are being established',
                'timing_window': '1-3 months',
                'key_insight': 'New GTM teams are more open to new tools and establishing best practices'
            })
        
        # Funding timing
        funding_signal = intelligence.get('gtm_signals', {}).get('funding_growth', {})
        if funding_signal.get('strength', 0) > 0.7:
            recent_funding = any(
                'funding' in init.get('title', '').lower()
                for init in intelligence.get('strategic_initiatives', [])[:10]
            )
            if recent_funding:
                recs.append({
                    'title': 'Post-Funding Growth Window',
                    'priority': 'high',
                    'urgency': 'immediate',
                    'rationale': 'Recent funding round detected',
                    'recommendation': 'Engage within 2-4 months of funding announcement when budgets are being allocated',
                    'timing_window': '2-4 months',
                    'key_insight': 'Companies typically make significant purchases within 6 months of funding'
                })
        
        # Product launch timing
        product_signal = intelligence.get('gtm_signals', {}).get('product_innovation', {})
        if product_signal.get('strength', 0) > 0.7:
            recs.append({
                'title': 'Product Launch Support Opportunity',
                'priority': 'medium',
                'urgency': 'near-term',
                'rationale': 'Multiple product launches detected',
                'recommendation': 'Position as supporting their product launches with complementary capabilities',
                'timing_window': '1-2 months',
                'key_insight': 'Engage before/during launch for maximum impact'
            })
        
        return recs
    
    def _generate_messaging_recs(self, intelligence: Dict) -> List[Dict]:
        """Generate messaging recommendations"""
        recs = []
        
        # Compile key themes
        gtm_signals = intelligence.get('gtm_signals', {})
        strong_signals = [
            name for name, data in gtm_signals.items()
            if data.get('strength', 0) > 0.6
        ]
        
        if strong_signals:
            themes = [signal.replace('_', ' ').title() for signal in strong_signals]
            
            recs.append({
                'title': 'Core Messaging Themes',
                'priority': 'high',
                'themes': themes,
                'recommendation': 'Focus messaging on these validated themes based on their recent activity',
                'message_framework': {
                    'primary': themes[0] if themes else 'Growth Support',
                    'secondary': themes[1:3] if len(themes) > 1 else []
                }
            })
        
        # Customer success messaging
        customer_signal = gtm_signals.get('customer_traction', {})
        if customer_signal.get('strength', 0) > 0.5:
            recs.append({
                'title': 'Customer Success Stories',
                'priority': 'medium',
                'recommendation': 'Leverage customer success stories from similar companies',
                'message_examples': [
                    'Join [similar company] in accelerating growth',
                    'Trusted by leading fintech companies like yours',
                    'Powering innovation at companies similar to yours'
                ]
            })
        
        return recs
    
    def _generate_competitive_recs(self, intelligence: Dict) -> List[Dict]:
        """Generate competitive recommendations"""
        recs = []
        
        # Check for competitive intelligence
        competitive_signal = intelligence.get('gtm_signals', {}).get('competitive', {})
        
        if competitive_signal.get('evidence'):
            recs.append({
                'title': 'Competitive Awareness',
                'priority': 'medium',
                'recommendation': 'Be prepared for competitive comparisons',
                'preparation_tips': [
                    'Research their current vendors and stack',
                    'Prepare differentiation talking points',
                    'Understand switching costs and migration paths'
                ]
            })
        
        # Developer ecosystem advantage
        dev_traction = intelligence.get('developer_ecosystem', {}).get('developer_traction', 0)
        if dev_traction > 60:
            recs.append({
                'title': 'Developer-First Competitive Angle',
                'priority': 'medium',
                'recommendation': 'They value developer experience - differentiate on this',
                'competitive_points': [
                    'Superior API design and documentation',
                    'Active developer community',
                    'Comprehensive SDK support'
                ]
            })
        
        return recs
    
    def _generate_engagement_recs(self, intelligence: Dict) -> List[Dict]:
        """Generate engagement strategy recommendations"""
        recs = []
        
        # LinkedIn engagement
        linkedin_data = intelligence.get('growth_indicators', {})
        if linkedin_data:
            recs.append({
                'title': 'LinkedIn Social Selling',
                'priority': 'medium',
                'channels': ['LinkedIn'],
                'recommendation': 'Engage with their LinkedIn content and thought leadership',
                'tactics': [
                    'Comment thoughtfully on company posts',
                    'Share their content with value-add commentary',
                    'Connect with GTM leaders at the company'
                ]
            })
        
        # Developer community engagement
        dev_eco = intelligence.get('developer_ecosystem', {})
        if dev_eco.get('total_repositories', 0) > 5:
            recs.append({
                'title': 'Developer Community Engagement',
                'priority': 'low',
                'channels': ['GitHub', 'Developer Forums'],
                'recommendation': 'Engage through their developer community',
                'tactics': [
                    'Contribute to their open source projects',
                    'Create integration examples',
                    'Participate in developer discussions'
                ]
            })
        
        # Event engagement
        event_signal = intelligence.get('gtm_signals', {}).get('event', {})
        if event_signal.get('evidence'):
            events = [ev.get('title') for ev in event_signal.get('evidence', [])[:3]]
            recs.append({
                'title': 'Event-Based Engagement',
                'priority': 'medium',
                'channels': ['Events', 'Conferences'],
                'recommendation': 'Connect at industry events where they\'re present',
                'upcoming_events': events
            })
        
        return recs
    
    def _generate_partnership_recs(self, intelligence: Dict) -> List[Dict]:
        """Generate partnership recommendations"""
        recs = []
        
        partnership_signal = intelligence.get('gtm_signals', {}).get('partnership_strategy', {})
        
        if partnership_signal.get('strength', 0) > 0.6:
            recs.append({
                'title': 'Strategic Partnership Opportunity',
                'priority': 'high',
                'rationale': f"Active partnership strategy (strength: {partnership_signal.get('strength'):.2f})",
                'recommendation': 'Explore formal partnership beyond vendor relationship',
                'partnership_angles': [
                    'Co-marketing opportunities',
                    'Joint customer success programs',
                    'Integration partnership',
                    'Reseller or referral partnership'
                ]
            })
            
            # Extract recent partnerships
            recent_partnerships = [
                ev.get('title') for ev in partnership_signal.get('evidence', [])
                if 'partner' in ev.get('title', '').lower()
            ][:3]
            
            if recent_partnerships:
                recs.append({
                    'title': 'Learn from Recent Partnerships',
                    'priority': 'medium',
                    'recommendation': 'Study their recent partnership announcements for patterns',
                    'recent_examples': recent_partnerships,
                    'analysis_points': [
                        'What value did each partnership provide?',
                        'What partner characteristics do they prefer?',
                        'How do they announce/promote partnerships?'
                    ]
                })
        
        return recs
    
    def _generate_priority_actions(self, intelligence: Dict) -> List[Dict]:
        """Generate priority action items"""
        actions = []
        
        # Analyze all signals for high-priority actions
        gtm_signals = intelligence.get('gtm_signals', {})
        growth = intelligence.get('growth_indicators', {})
        
        # Action 1: Immediate outreach if hiring
        if growth.get('hiring_velocity', {}).get('gtm_roles', 0) > 10:
            actions.append({
                'priority': 1,
                'urgency': 'immediate',
                'action': 'Initiate outreach to GTM leaders',
                'why': 'Company is rapidly building GTM team - optimal timing',
                'how': 'LinkedIn connection + personalized message about supporting team ramp',
                'timeline': 'This week'
            })
        
        # Action 2: Content engagement
        if any(signal.get('strength', 0) > 0.7 for signal in gtm_signals.values()):
            actions.append({
                'priority': 2,
                'urgency': 'near-term',
                'action': 'Engage with recent company content',
                'why': 'Build familiarity and demonstrate relevant interest',
                'how': 'Comment on LinkedIn posts, share blog articles with insights',
                'timeline': 'This week'
            })
        
        # Action 3: Research personalization
        actions.append({
            'priority': 3,
            'urgency': 'near-term',
            'action': 'Develop personalized value proposition',
            'why': 'Generic outreach won\'t resonate with innovative fintech',
            'how': 'Use intelligence insights to craft company-specific messaging',
            'timeline': 'Before first outreach'
        })
        
        # Action 4: Stakeholder mapping
        if growth.get('team_growth', {}).get('total_employees', 0) > 1000:
            actions.append({
                'priority': 4,
                'urgency': 'this-month',
                'action': 'Map key stakeholders and decision makers',
                'why': 'Larger organizations require multi-threading',
                'how': 'LinkedIn research + organizational chart building',
                'timeline': 'This month'
            })
        
        return actions
    
    def _generate_talking_points(self, intelligence: Dict) -> List[Dict]:
        """Generate sales talking points"""
        talking_points = []
        
        gtm_signals = intelligence.get('gtm_signals', {})
        growth = intelligence.get('growth_indicators', {})
        
        # Growth talking point
        team_growth = growth.get('team_growth', {})
        if team_growth.get('growth_1y'):
            talking_points.append({
                'category': 'growth',
                'point': f"Congrats on the growth - I saw you're now at {team_growth.get('total_employees')} employees",
                'follow_up': 'How is your team handling the scaling challenges?',
                'context': 'Use when discussing growth or team expansion'
            })
        
        # Product innovation talking point
        if gtm_signals.get('product_innovation', {}).get('strength', 0) > 0.6:
            evidence = gtm_signals['product_innovation'].get('evidence', [])
            if evidence:
                recent_launch = evidence[0].get('title', '')
                talking_points.append({
                    'category': 'product',
                    'point': f"I noticed your recent {recent_launch}",
                    'follow_up': 'How has the market response been? What\'s driving the product roadmap?',
                    'context': 'Use when discussing product strategy'
                })
        
        # Market expansion talking point
        if gtm_signals.get('market_expansion', {}).get('strength', 0) > 0.6:
            talking_points.append({
                'category': 'expansion',
                'point': 'I see you\'re expanding into new markets',
                'follow_up': 'What challenges are you facing with multi-market operations?',
                'context': 'Use when discussing international or market expansion'
            })
        
        # Hiring talking point
        if growth.get('hiring_velocity', {}).get('gtm_roles', 0) > 5:
            gtm_count = growth['hiring_velocity']['gtm_roles']
            talking_points.append({
                'category': 'hiring',
                'point': f"I noticed you're hiring for {gtm_count} GTM roles",
                'follow_up': 'How are you thinking about ramping the new team members?',
                'context': 'Use when discussing team building or onboarding'
            })
        
        return talking_points
    
    def save_recommendations(self, recommendations: Dict, filename: str):
        """Save recommendations to JSON file"""
        output_path = os.path.join('outputs', 'recommendations', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(recommendations, f, indent=2, ensure_ascii=False)
        
        print(f"Saved recommendations to {output_path}")
    
    def generate_recommendations_report(self, recommendations: Dict) -> str:
        """Generate text report of recommendations"""
        report = []
        company = recommendations.get('company', 'Target Company')
        
        report.append(f"GTM RECOMMENDATIONS: {company.upper()}")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("\n")
        
        # Priority Actions
        report.append("PRIORITY ACTIONS")
        report.append("-" * 80)
        for action in recommendations.get('priority_actions', []):
            report.append(f"\n{action['priority']}. {action['action']} [{action['urgency'].upper()}]")
            report.append(f"   Why: {action['why']}")
            report.append(f"   How: {action['how']}")
            report.append(f"   Timeline: {action['timeline']}")
        
        report.append("\n")
        
        # Talking Points
        report.append("KEY TALKING POINTS")
        report.append("-" * 80)
        for idx, tp in enumerate(recommendations.get('talking_points', []), 1):
            report.append(f"\n{idx}. [{tp['category'].upper()}] {tp['point']}")
            report.append(f"   Follow-up: {tp['follow_up']}")
            report.append(f"   Context: {tp['context']}")
        
        report.append("\n")
        
        # Positioning
        report.append("POSITIONING RECOMMENDATIONS")
        report.append("-" * 80)
        for rec in recommendations.get('positioning_recommendations', []):
            report.append(f"\n• {rec['title']} [{rec['priority'].upper()}]")
            report.append(f"  {rec['recommendation']}")
        
        report.append("\n")
        report.append("=" * 80)
        
        return "\n".join(report)


if __name__ == "__main__":
    # Load intelligence data
    with open('outputs/categorized/full_intelligence.json', 'r') as f:
        intelligence = json.load(f)
    
    generator = RecommendationsGenerator()
    company_name = "Stripe"
    
    # Generate recommendations
    recommendations = generator.generate_all_recommendations(intelligence, company_name)
    generator.save_recommendations(recommendations, f'{company_name.lower()}_recommendations.json')
    
    # Generate report
    report = generator.generate_recommendations_report(recommendations)
    output_path = os.path.join('outputs', 'recommendations', f'{company_name.lower()}_recommendations_report.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("Recommendations generation complete")
