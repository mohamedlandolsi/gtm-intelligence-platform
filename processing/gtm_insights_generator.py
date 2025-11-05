"""
GTM Insights Generator
Transforms classified market signals into actionable GTM insights
"""

from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GTMInsightsGenerator:
    """Generates actionable GTM insights from classified signals"""
    
    def __init__(self):
        """Initialize the insights generator"""
        self.category_templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize insight templates for each GTM category"""
        
        return {
            'TIMING': {
                'description': 'Launch windows and market timing opportunities',
                'insight_types': [
                    'launch_windows',
                    'seasonal_patterns',
                    'market_readiness',
                    'competitive_timing'
                ],
                'keywords': {
                    'launch_signals': ['launch', 'release', 'announce', 'debut', 'rollout'],
                    'timing_indicators': ['q1', 'q2', 'q3', 'q4', 'quarter', 'upcoming', 'planned'],
                    'readiness': ['beta', 'preview', 'early access', 'availability']
                }
            },
            
            'MESSAGING': {
                'description': 'Brand positioning and narrative strategies',
                'insight_types': [
                    'narrative_analysis',
                    'positioning_strategy',
                    'counter_positioning',
                    'talking_points'
                ],
                'keywords': {
                    'positioning': ['position', 'focus', 'mission', 'vision', 'value'],
                    'narrative': ['message', 'story', 'commitment', 'priority'],
                    'action': ['enable', 'empower', 'transform', 'revolutionize']
                }
            },
            
            'ICP': {
                'description': 'Target customer segments and profiles',
                'insight_types': [
                    'target_segments',
                    'emerging_profiles',
                    'underserved_markets',
                    'segment_shifts'
                ],
                'keywords': {
                    'segments': ['enterprise', 'smb', 'mid-market', 'startup'],
                    'verticals': ['fintech', 'saas', 'ecommerce', 'marketplace', 'platform'],
                    'geography': ['global', 'regional', 'domestic', 'international']
                }
            },
            
            'COMPETITIVE': {
                'description': 'Competitive landscape and differentiation',
                'insight_types': [
                    'main_competitors',
                    'vulnerabilities',
                    'differentiation_opportunities',
                    'competitive_moves'
                ],
                'keywords': {
                    'competitors': ['plaid', 'adyen', 'square', 'paypal', 'braintree'],
                    'comparison': ['versus', 'compared to', 'alternative to', 'competitor'],
                    'differentiation': ['unique', 'better', 'advantage', 'edge']
                }
            },
            
            'PRODUCT': {
                'description': 'Product development and roadmap signals',
                'insight_types': [
                    'product_roadmap',
                    'feature_gaps',
                    'development_velocity',
                    'innovation_areas'
                ],
                'keywords': {
                    'development': ['build', 'develop', 'create', 'ship', 'release'],
                    'features': ['api', 'sdk', 'feature', 'capability', 'functionality'],
                    'technology': ['infrastructure', 'platform', 'integration', 'ecosystem']
                }
            },
            
            'MARKET': {
                'description': 'Market trends and industry dynamics',
                'insight_types': [
                    'tailwinds',
                    'headwinds',
                    'growth_opportunities',
                    'market_shifts'
                ],
                'keywords': {
                    'trends': ['trend', 'shift', 'movement', 'change', 'evolution'],
                    'growth': ['growth', 'expansion', 'opportunity', 'potential'],
                    'challenges': ['challenge', 'risk', 'threat', 'obstacle']
                }
            },
            
            'TALENT': {
                'description': 'Organizational and talent signals',
                'insight_types': [
                    'strategic_direction',
                    'organizational_strength',
                    'capability_gaps',
                    'expansion_signals'
                ],
                'keywords': {
                    'hiring': ['hire', 'hiring', 'recruit', 'talent', 'position'],
                    'leadership': ['ceo', 'cto', 'cfo', 'vp', 'executive', 'leader'],
                    'growth': ['expansion', 'scale', 'grow', 'team building']
                }
            }
        }
    
    def generate_gtm_insights(self, classified_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive GTM insights from classified signals
        
        Args:
            classified_signals: List of signals with GTM classifications
            
        Returns:
            Dictionary containing insights by category, with supporting signals and actions
        """
        logger.info(f"Generating GTM insights from {len(classified_signals)} signals")
        
        # Group signals by primary category
        signals_by_category = self._group_signals_by_category(classified_signals)
        
        # Generate insights for each category
        insights = {
            'metadata': {
                'total_signals_analyzed': len(classified_signals),
                'generation_date': datetime.now().strftime('%Y-%m-%d'),
                'categories_analyzed': list(signals_by_category.keys())
            },
            'insights_by_category': {}
        }
        
        for category, signals in signals_by_category.items():
            if signals:
                category_insights = self._generate_category_insights(category, signals)
                insights['insights_by_category'][category] = category_insights
        
        # Generate executive summary
        insights['executive_summary'] = self._generate_executive_summary(insights)
        
        # Generate cross-category insights
        insights['cross_category_insights'] = self._generate_cross_category_insights(classified_signals)
        
        logger.info(f"Generated insights for {len(insights['insights_by_category'])} categories")
        return insights
    
    def _group_signals_by_category(self, signals: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group signals by their primary GTM category"""
        
        grouped = defaultdict(list)
        for signal in signals:
            primary = signal.get('primary_category', 'UNKNOWN')
            grouped[primary].append(signal)
        
        return dict(grouped)
    
    def _generate_category_insights(self, category: str, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights for a specific GTM category"""
        
        if category == 'TIMING':
            return self._generate_timing_insights(signals)
        elif category == 'MESSAGING':
            return self._generate_messaging_insights(signals)
        elif category == 'ICP':
            return self._generate_icp_insights(signals)
        elif category == 'COMPETITIVE':
            return self._generate_competitive_insights(signals)
        elif category == 'PRODUCT':
            return self._generate_product_insights(signals)
        elif category == 'MARKET':
            return self._generate_market_insights(signals)
        elif category == 'TALENT':
            return self._generate_talent_insights(signals)
        else:
            return self._generate_generic_insights(category, signals)
    
    def _generate_timing_insights(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate TIMING-specific insights"""
        
        insights = []
        
        # Analyze launch windows
        launch_signals = [s for s in signals if any(
            keyword in s.get('headline', '').lower() + s.get('description', '').lower()
            for keyword in ['launch', 'release', 'announce', 'rollout']
        )]
        
        if launch_signals:
            insight = {
                'insight_text': f"Detected {len(launch_signals)} launch-related signals indicating active release cycles. "
                               f"Market window is currently OPEN for competitive announcements.",
                'supporting_signals': [s['headline'] for s in launch_signals[:3]],
                'confidence_level': self._calculate_confidence(launch_signals),
                'recommended_action': "Monitor launch windows closely. Consider timing competitive releases to "
                                     "capitalize on market attention or to counter-program Stripe announcements."
            }
            insights.append(insight)
        
        # Analyze seasonal patterns
        quarter_mentions = sum(1 for s in signals if any(
            q in s.get('description', '').lower() for q in ['q1', 'q2', 'q3', 'q4', 'quarter']
        ))
        
        if quarter_mentions > 0:
            insight = {
                'insight_text': f"Identified {quarter_mentions} signals with quarterly timing indicators. "
                               f"Stripe appears to follow quarterly release cadence.",
                'supporting_signals': [s['headline'] for s in signals if 'q' in s.get('description', '').lower()][:2],
                'confidence_level': 'medium' if quarter_mentions >= 2 else 'low',
                'recommended_action': "Align product launches and marketing campaigns with quarterly cycles. "
                                     "Expect major announcements at quarter boundaries (Jan, Apr, Jul, Oct)."
            }
            insights.append(insight)
        
        # Beta/Preview signals
        beta_signals = [s for s in signals if any(
            keyword in s.get('headline', '').lower() + s.get('description', '').lower()
            for keyword in ['beta', 'preview', 'early access']
        )]
        
        if beta_signals:
            insight = {
                'insight_text': f"Found {len(beta_signals)} beta/preview signals suggesting upcoming GA releases. "
                               f"Market readiness window opening in 3-6 months.",
                'supporting_signals': [s['headline'] for s in beta_signals],
                'confidence_level': 'high',
                'recommended_action': "Prepare competitive responses for expected GA launches. Consider pre-emptive "
                                     "announcements or positioning to capture early adopters."
            }
            insights.append(insight)
        
        return {
            'category': 'TIMING',
            'total_signals': len(signals),
            'insights': insights,
            'summary': f"Analysis of {len(signals)} timing signals reveals launch windows and seasonal patterns."
        }
    
    def _generate_messaging_insights(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate MESSAGING-specific insights"""
        
        insights = []
        
        # Analyze positioning keywords
        positioning_words = ['enable', 'empower', 'transform', 'revolutionize', 'pioneer', 'leading']
        positioning_signals = [s for s in signals if any(
            word in s.get('headline', '').lower() + s.get('description', '').lower()
            for word in positioning_words
        )]
        
        if positioning_signals:
            insight = {
                'insight_text': f"Stripe's messaging emphasizes enablement and transformation themes. "
                               f"Detected {len(positioning_signals)} signals with strong positioning language.",
                'supporting_signals': [s['headline'] for s in positioning_signals[:3]],
                'confidence_level': 'high',
                'recommended_action': "Counter-positioning strategy: Emphasize simplicity, reliability, and proven results "
                                     "vs. transformative promises. Talking points: 'Built for today's needs, not tomorrow's unknowns.'"
            }
            insights.append(insight)
        
        # Analyze focus areas
        focus_areas = self._extract_focus_areas(signals)
        if focus_areas:
            insight = {
                'insight_text': f"Key messaging focus areas: {', '.join(focus_areas[:3])}. "
                               f"Narrative centers on {focus_areas[0]} as primary value proposition.",
                'supporting_signals': [s['headline'] for s in signals[:2]],
                'confidence_level': 'medium',
                'recommended_action': f"Sales talking points: Address {focus_areas[0]} directly. "
                                     f"Position as alternative approach that delivers faster value."
            }
            insights.append(insight)
        
        return {
            'category': 'MESSAGING',
            'total_signals': len(signals),
            'insights': insights,
            'summary': f"Messaging analysis reveals positioning strategy and key narratives from {len(signals)} signals."
        }
    
    def _generate_icp_insights(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate ICP-specific insights"""
        
        insights = []
        
        # Extract target segments
        segments = self._extract_customer_segments(signals)
        
        if segments:
            insight = {
                'insight_text': f"Target customer segments identified: {', '.join(segments)}. "
                               f"Primary focus on {segments[0]} segment.",
                'supporting_signals': [s['headline'] for s in signals[:3]],
                'confidence_level': 'high' if len(segments) >= 3 else 'medium',
                'recommended_action': f"Target underserved segments: Look for customers outside the {segments[0]} "
                                     f"category who are underserved by Stripe's current positioning."
            }
            insights.append(insight)
        
        # Identify emerging profiles
        hiring_signals = [s for s in signals if 'secondary_categories' in s and 'TALENT' in s.get('secondary_categories', [])]
        
        if hiring_signals:
            insight = {
                'insight_text': f"Hiring patterns suggest expansion into new customer segments. "
                               f"{len(hiring_signals)} signals indicate organizational shifts.",
                'supporting_signals': [s['headline'] for s in hiring_signals],
                'confidence_level': 'medium',
                'recommended_action': "Monitor hiring announcements for clues about new target segments. "
                                     "Sales teams recruiting suggests enterprise push; more engineers suggests developer-first approach."
            }
            insights.append(insight)
        
        return {
            'category': 'ICP',
            'total_signals': len(signals),
            'insights': insights,
            'summary': f"ICP analysis identifies target segments and emerging customer profiles from {len(signals)} signals."
        }
    
    def _generate_competitive_insights(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate COMPETITIVE-specific insights"""
        
        insights = []
        
        # Identify main competitors mentioned
        competitors = self._extract_competitors(signals)
        
        if competitors:
            insight = {
                'insight_text': f"Main competitive threats identified: {', '.join(competitors)}. "
                               f"Signals indicate active competition in shared markets.",
                'supporting_signals': [s['headline'] for s in signals],
                'confidence_level': 'high',
                'recommended_action': f"Differentiation strategy: Position against {competitors[0]} by emphasizing "
                                     f"areas where Stripe shows vulnerability (e.g., pricing complexity, integration difficulty)."
            }
            insights.append(insight)
        
        # Analyze competitive vulnerabilities
        insight = {
            'insight_text': "Potential Stripe vulnerabilities: Complex pricing structure, enterprise-focused positioning "
                           "may leave mid-market underserved, SDK complexity creates integration friction.",
            'supporting_signals': [s['headline'] for s in signals[:2]],
            'confidence_level': 'medium',
            'recommended_action': "Attack vectors: Simple transparent pricing, white-glove mid-market support, "
                                 "faster integration (< 1 day setup). Win where Stripe is overbuilt."
        }
        insights.append(insight)
        
        return {
            'category': 'COMPETITIVE',
            'total_signals': len(signals),
            'insights': insights,
            'summary': f"Competitive analysis reveals threats, vulnerabilities, and differentiation opportunities from {len(signals)} signals."
        }
    
    def _generate_product_insights(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate PRODUCT-specific insights"""
        
        insights = []
        
        # Analyze product development velocity
        high_confidence_signals = [s for s in signals if s.get('confidence_level') == 'high']
        
        insight = {
            'insight_text': f"High product development velocity detected: {len(signals)} product signals, "
                           f"{len(high_confidence_signals)} high-confidence. Stripe is in aggressive build mode.",
            'supporting_signals': [s['headline'] for s in high_confidence_signals[:3]],
            'confidence_level': 'high',
            'recommended_action': "Expect rapid feature releases. Prioritize parity on core features while identifying "
                                 "areas where Stripe is over-investing (potential gaps to exploit)."
        }
        insights.append(insight)
        
        # Identify product categories
        product_areas = self._extract_product_areas(signals)
        
        if product_areas:
            insight = {
                'insight_text': f"Product roadmap focus areas: {', '.join(product_areas[:5])}. "
                               f"Primary investment in {product_areas[0]}.",
                'supporting_signals': [s['headline'] for s in signals[:4]],
                'confidence_level': 'high',
                'recommended_action': f"Product gaps to exploit: Areas NOT in their roadmap - {self._identify_gaps(product_areas)}. "
                                     f"Consider building differentiated capabilities in these gaps."
            }
            insights.append(insight)
        
        # Analyze release patterns
        version_signals = [s for s in signals if any(
            indicator in s.get('headline', '').lower()
            for indicator in ['v', 'version', 'release', 'update']
        )]
        
        if len(version_signals) >= 3:
            insight = {
                'insight_text': f"Rapid release cadence: {len(version_signals)} version updates detected. "
                               f"Suggests strong engineering velocity and continuous deployment.",
                'supporting_signals': [s['headline'] for s in version_signals[:3]],
                'confidence_level': 'high',
                'recommended_action': "Match release velocity with quality. Emphasize stability and reliability "
                                     "as counter to Stripe's rapid iteration (which may introduce bugs)."
            }
            insights.append(insight)
        
        return {
            'category': 'PRODUCT',
            'total_signals': len(signals),
            'insights': insights,
            'summary': f"Product analysis reveals roadmap direction and development velocity from {len(signals)} signals."
        }
    
    def _generate_market_insights(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate MARKET-specific insights"""
        
        insights = []
        
        # Identify market trends
        trend_keywords = ['trend', 'growth', 'adoption', 'shift', 'evolution', 'expansion']
        trend_signals = [s for s in signals if any(
            keyword in s.get('description', '').lower()
            for keyword in trend_keywords
        )]
        
        if trend_signals:
            # Tailwinds
            positive_keywords = ['growth', 'opportunity', 'adoption', 'expansion', 'increase']
            tailwinds = [s for s in trend_signals if any(
                kw in s.get('description', '').lower() for kw in positive_keywords
            )]
            
            if tailwinds:
                insight = {
                    'insight_text': f"Market tailwinds identified: {len(tailwinds)} positive market signals. "
                                   f"Strong market momentum supporting growth.",
                    'supporting_signals': [s['headline'] for s in tailwinds],
                    'confidence_level': 'high',
                    'recommended_action': "Capitalize on market tailwinds with aggressive marketing. "
                                         "Market conditions favor expansion and customer acquisition."
                }
                insights.append(insight)
            
            # Headwinds
            negative_keywords = ['challenge', 'risk', 'decline', 'threat', 'concern', 'regulation']
            headwinds = [s for s in trend_signals if any(
                kw in s.get('description', '').lower() for kw in negative_keywords
            )]
            
            if headwinds:
                insight = {
                    'insight_text': f"Market headwinds detected: {len(headwinds)} signals indicate challenges. "
                                   f"Market conditions may create obstacles.",
                    'supporting_signals': [s['headline'] for s in headwinds],
                    'confidence_level': 'medium',
                    'recommended_action': "Position solutions that address market headwinds directly. "
                                         "Use challenges as differentiation opportunities."
                }
                insights.append(insight)
        
        # Growth opportunities
        opportunity_signals = [s for s in signals if 'opportunity' in s.get('description', '').lower()]
        
        if opportunity_signals:
            insight = {
                'insight_text': f"Growth opportunities identified: {len(opportunity_signals)} signals point to "
                               f"expansion potential in new markets or segments.",
                'supporting_signals': [s['headline'] for s in opportunity_signals],
                'confidence_level': 'medium',
                'recommended_action': "Evaluate expansion opportunities. Consider entering markets where Stripe "
                                     "signals interest but has not yet achieved dominance."
            }
            insights.append(insight)
        
        return {
            'category': 'MARKET',
            'total_signals': len(signals),
            'insights': insights,
            'summary': f"Market analysis identifies tailwinds, headwinds, and growth opportunities from {len(signals)} signals."
        }
    
    def _generate_talent_insights(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate TALENT-specific insights"""
        
        insights = []
        
        # Analyze hiring signals
        hiring_signals = [s for s in signals if 'hiring' in s.get('signal_type', '').lower() 
                         or 'hire' in s.get('headline', '').lower()]
        
        if hiring_signals:
            # Extract hiring numbers
            total_positions = self._extract_hiring_numbers(hiring_signals)
            
            insight = {
                'insight_text': f"Aggressive hiring detected: {total_positions}+ open positions across {len(hiring_signals)} signals. "
                               f"Indicates strong growth trajectory and strategic expansion.",
                'supporting_signals': [s['headline'] for s in hiring_signals],
                'confidence_level': 'high',
                'recommended_action': "Strategic direction: Large-scale hiring suggests preparation for major initiatives. "
                                     "Monitor department-level hiring to identify strategic priorities (eng = product, sales = market expansion)."
            }
            insights.append(insight)
        
        # Employee count signals
        employee_signals = [s for s in signals if 'employee' in s.get('headline', '').lower()]
        
        if employee_signals:
            employee_count = self._extract_employee_count(employee_signals)
            
            insight = {
                'insight_text': f"Organizational strength: ~{employee_count:,} employees. "
                               f"Large organization with strong resources but potential for bureaucracy.",
                'supporting_signals': [s['headline'] for s in employee_signals],
                'confidence_level': 'high',
                'recommended_action': "Competitive advantage: Emphasize agility and speed vs. Stripe's large organization. "
                                     "Position as nimble alternative that can move faster and customize solutions."
            }
            insights.append(insight)
        
        # Leadership signals
        leadership_keywords = ['ceo', 'cto', 'cfo', 'vp', 'executive', 'chief', 'head of']
        leadership_signals = [s for s in signals if any(
            keyword in s.get('description', '').lower()
            for keyword in leadership_keywords
        )]
        
        if leadership_signals:
            insight = {
                'insight_text': f"Leadership changes detected: {len(leadership_signals)} executive-level signals. "
                               f"May indicate strategic pivots or new priorities.",
                'supporting_signals': [s['headline'] for s in leadership_signals],
                'confidence_level': 'medium',
                'recommended_action': "Monitor executive hires for strategic direction signals. "
                                     "New CTO = product focus, new CRO = sales push, new CFO = IPO/profitability focus."
            }
            insights.append(insight)
        
        return {
            'category': 'TALENT',
            'total_signals': len(signals),
            'insights': insights,
            'summary': f"Talent analysis reveals organizational strength and strategic direction from {len(signals)} signals."
        }
    
    def _generate_generic_insights(self, category: str, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate generic insights for unknown categories"""
        
        insights = [{
            'insight_text': f"Detected {len(signals)} signals in {category} category requiring further analysis.",
            'supporting_signals': [s['headline'] for s in signals[:3]],
            'confidence_level': 'low',
            'recommended_action': "Review signals manually for strategic implications."
        }]
        
        return {
            'category': category,
            'total_signals': len(signals),
            'insights': insights,
            'summary': f"Generic analysis of {len(signals)} {category} signals."
        }
    
    def _generate_executive_summary(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of all insights"""
        
        total_insights = sum(
            len(cat_insights.get('insights', []))
            for cat_insights in insights.get('insights_by_category', {}).values()
        )
        
        categories_analyzed = list(insights.get('insights_by_category', {}).keys())
        
        # Identify top priorities
        high_confidence_insights = []
        for category, cat_insights in insights.get('insights_by_category', {}).items():
            for insight in cat_insights.get('insights', []):
                if insight.get('confidence_level') == 'high':
                    high_confidence_insights.append({
                        'category': category,
                        'insight': insight['insight_text'][:200] + '...'
                    })
        
        return {
            'total_insights_generated': total_insights,
            'categories_covered': categories_analyzed,
            'high_confidence_insights': high_confidence_insights[:5],
            'key_recommendations': self._extract_top_recommendations(insights),
            'strategic_summary': self._generate_strategic_summary(insights)
        }
    
    def _generate_cross_category_insights(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate insights that span multiple GTM categories"""
        
        cross_insights = []
        
        # Find multi-dimensional signals
        multi_dim_signals = [s for s in signals if len(s.get('secondary_categories', [])) > 0]
        
        if len(multi_dim_signals) > len(signals) * 0.3:  # More than 30% are multi-dimensional
            insight = {
                'insight_text': f"High interconnection: {len(multi_dim_signals)} of {len(signals)} signals ({len(multi_dim_signals)*100//len(signals)}%) "
                               f"span multiple GTM dimensions. Indicates complex strategic initiatives.",
                'supporting_signals': [s['headline'] for s in multi_dim_signals[:3]],
                'confidence_level': 'high',
                'recommended_action': "Integrated GTM approach required. Single-dimension strategies will miss key connections. "
                                     "Coordinate across product, marketing, and sales for holistic response."
            }
            cross_insights.append(insight)
        
        # Product + Timing combinations
        product_timing_signals = [s for s in signals 
                                 if s.get('primary_category') == 'PRODUCT' 
                                 and 'TIMING' in s.get('secondary_categories', [])]
        
        if len(product_timing_signals) >= 3:
            insight = {
                'insight_text': f"Product launch cycle detected: {len(product_timing_signals)} signals combine PRODUCT + TIMING. "
                               f"Stripe is in active launch mode with coordinated releases.",
                'supporting_signals': [s['headline'] for s in product_timing_signals[:3]],
                'confidence_level': 'high',
                'recommended_action': "Prepare for coordinated product announcements. Consider counter-programming with "
                                     "own product launches or strategic partnerships to dilute their message."
            }
            cross_insights.append(insight)
        
        # Talent + ICP combinations
        talent_icp_signals = [s for s in signals 
                             if (s.get('primary_category') == 'TALENT' and 'ICP' in s.get('secondary_categories', []))
                             or (s.get('primary_category') == 'ICP' and 'TALENT' in s.get('secondary_categories', []))]
        
        if talent_icp_signals:
            insight = {
                'insight_text': f"Strategic expansion signaled: {len(talent_icp_signals)} signals link hiring to customer segments. "
                               f"Indicates planned expansion into new markets or segments.",
                'supporting_signals': [s['headline'] for s in talent_icp_signals],
                'confidence_level': 'medium',
                'recommended_action': "Anticipate market expansion. Identify target segments being staffed up and "
                                     "prepare competitive defenses or first-mover advantages in adjacent segments."
            }
            cross_insights.append(insight)
        
        return cross_insights
    
    def _calculate_confidence(self, signals: List[Dict[str, Any]]) -> str:
        """Calculate confidence level based on signal quality and quantity"""
        
        high_conf_signals = sum(1 for s in signals if s.get('confidence_level') == 'high')
        
        if len(signals) >= 5 and high_conf_signals >= 3:
            return 'high'
        elif len(signals) >= 2 and high_conf_signals >= 1:
            return 'medium'
        else:
            return 'low'
    
    def _extract_focus_areas(self, signals: List[Dict[str, Any]]) -> List[str]:
        """Extract key focus areas from signals"""
        
        focus_keywords = {
            'developer_experience': ['developer', 'dx', 'api', 'sdk', 'integration'],
            'enterprise': ['enterprise', 'large', 'scale', 'global'],
            'innovation': ['innovation', 'new', 'cutting-edge', 'advanced'],
            'reliability': ['reliable', 'stability', 'uptime', 'resilience'],
            'growth': ['growth', 'expansion', 'scale', 'accelerate']
        }
        
        focus_scores = defaultdict(int)
        for signal in signals:
            text = (signal.get('headline', '') + ' ' + signal.get('description', '')).lower()
            for area, keywords in focus_keywords.items():
                if any(kw in text for kw in keywords):
                    focus_scores[area] += 1
        
        # Sort by frequency
        sorted_areas = sorted(focus_scores.items(), key=lambda x: x[1], reverse=True)
        return [area for area, score in sorted_areas if score > 0]
    
    def _extract_customer_segments(self, signals: List[Dict[str, Any]]) -> List[str]:
        """Extract customer segments from signals"""
        
        segment_keywords = {
            'developers': ['developer', 'engineer', 'api', 'sdk', 'code'],
            'enterprise': ['enterprise', 'large business', 'fortune', 'global'],
            'smb': ['smb', 'small business', 'startup', 'small to medium'],
            'fintech': ['fintech', 'financial', 'banking', 'payment'],
            'saas': ['saas', 'software', 'platform', 'application'],
            'ecommerce': ['ecommerce', 'retail', 'online store', 'shopping'],
            'marketplaces': ['marketplace', 'platform', 'multi-sided']
        }
        
        segment_scores = defaultdict(int)
        for signal in signals:
            text = (signal.get('headline', '') + ' ' + signal.get('description', '')).lower()
            for segment, keywords in segment_keywords.items():
                if any(kw in text for kw in keywords):
                    segment_scores[segment] += 1
        
        sorted_segments = sorted(segment_scores.items(), key=lambda x: x[1], reverse=True)
        return [seg for seg, score in sorted_segments if score > 0]
    
    def _extract_competitors(self, signals: List[Dict[str, Any]]) -> List[str]:
        """Extract competitor mentions from signals"""
        
        competitors = ['Plaid', 'Adyen', 'Square', 'PayPal', 'Braintree', 'Checkout.com', 'Mollie']
        
        found_competitors = []
        for signal in signals:
            text = (signal.get('headline', '') + ' ' + signal.get('description', '')).lower()
            for comp in competitors:
                if comp.lower() in text and comp not in found_competitors:
                    found_competitors.append(comp)
        
        return found_competitors
    
    def _extract_product_areas(self, signals: List[Dict[str, Any]]) -> List[str]:
        """Extract product areas from signals"""
        
        product_areas = defaultdict(int)
        
        # Keywords for different product categories
        categories = {
            'SDKs': ['sdk', 'library', 'package', 'python', 'javascript', 'go', 'php', 'ruby'],
            'APIs': ['api', 'endpoint', 'rest', 'graphql', 'webhook'],
            'Payment Processing': ['payment', 'checkout', 'transaction', 'processing'],
            'Developer Tools': ['cli', 'tool', 'debug', 'test', 'developer'],
            'Financial Products': ['treasury', 'issuing', 'capital', 'banking'],
            'Billing': ['billing', 'subscription', 'invoice', 'recurring'],
            'Terminal': ['terminal', 'pos', 'in-person', 'retail']
        }
        
        for signal in signals:
            text = (signal.get('headline', '') + ' ' + signal.get('description', '')).lower()
            for area, keywords in categories.items():
                if any(kw in text for kw in keywords):
                    product_areas[area] += 1
        
        sorted_areas = sorted(product_areas.items(), key=lambda x: x[1], reverse=True)
        return [area for area, count in sorted_areas if count > 0]
    
    def _identify_gaps(self, covered_areas: List[str]) -> str:
        """Identify product gaps based on what's NOT being built"""
        
        all_areas = [
            'Fraud Prevention', 'Analytics', 'Reporting', 'Tax Automation',
            'Compliance Tools', 'Customer Portal', 'White-labeling', 'Custom Branding'
        ]
        
        gaps = [area for area in all_areas if area not in covered_areas]
        
        if gaps:
            return ', '.join(gaps[:3])
        else:
            return 'Adjacent verticals not yet addressed'
    
    def _extract_hiring_numbers(self, signals: List[Dict[str, Any]]) -> int:
        """Extract hiring numbers from signals"""
        
        import re
        total = 0
        
        for signal in signals:
            text = signal.get('headline', '') + ' ' + signal.get('description', '')
            # Look for patterns like "150+ positions" or "hiring 200"
            matches = re.findall(r'(\d+)\+?\s*(?:positions|openings|roles|jobs)', text, re.IGNORECASE)
            if matches:
                total += int(matches[0])
        
        return total if total > 0 else 100  # Default estimate if not found
    
    def _extract_employee_count(self, signals: List[Dict[str, Any]]) -> int:
        """Extract employee count from signals"""
        
        import re
        
        for signal in signals:
            text = signal.get('headline', '') + ' ' + signal.get('description', '')
            # Look for patterns like "12,538 employees"
            matches = re.findall(r'([\d,]+)\s*employees', text, re.IGNORECASE)
            if matches:
                return int(matches[0].replace(',', ''))
        
        return 10000  # Default estimate
    
    def _extract_top_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Extract top recommended actions across all categories"""
        
        recommendations = []
        
        for cat_insights in insights.get('insights_by_category', {}).values():
            for insight in cat_insights.get('insights', []):
                if insight.get('confidence_level') == 'high':
                    action = insight.get('recommended_action', '')
                    if action and action not in recommendations:
                        recommendations.append(action)
        
        return recommendations[:5]
    
    def _generate_strategic_summary(self, insights: Dict[str, Any]) -> str:
        """Generate high-level strategic summary"""
        
        categories = insights.get('insights_by_category', {})
        
        summary_parts = []
        
        # Product velocity
        if 'PRODUCT' in categories:
            product_count = categories['PRODUCT']['total_signals']
            summary_parts.append(f"High product development activity ({product_count} signals)")
        
        # Market dynamics
        if 'MARKET' in categories:
            summary_parts.append("market tailwinds present")
        
        # Competitive landscape
        if 'COMPETITIVE' in categories:
            summary_parts.append("competitive vulnerabilities identified")
        
        # Talent signals
        if 'TALENT' in categories:
            talent_count = categories['TALENT']['total_signals']
            summary_parts.append(f"organizational expansion ({talent_count} hiring signals)")
        
        if summary_parts:
            return "Strategic picture: " + ", ".join(summary_parts) + ". " + \
                   "Recommend multi-dimensional GTM approach targeting identified gaps and vulnerabilities."
        else:
            return "Limited strategic signals detected. Recommend continued monitoring for trend development."


# Convenience function
def generate_gtm_insights(classified_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate GTM insights from classified signals
    
    Args:
        classified_signals: List of signals with GTM classifications
        
    Returns:
        Dictionary containing insights by category with supporting signals and actions
    """
    generator = GTMInsightsGenerator()
    return generator.generate_gtm_insights(classified_signals)


def generate_executive_summary(insights: Dict[str, Any], signals: List[Dict[str, Any]]) -> str:
    """
    Generate professional executive summary report from insights and signals
    
    Args:
        insights: Generated GTM insights from generate_gtm_insights()
        signals: Original list of all signals (classified and unclassified)
        
    Returns:
        Formatted executive summary report (250-400 words)
    """
    
    # Extract metadata
    total_signals = len(signals)
    date_range = _extract_date_range(signals)
    source_breakdown = _extract_source_breakdown(signals)
    
    # Build report sections
    report_sections = []
    
    # 1. Executive Summary (150 words)
    exec_summary = _build_executive_summary_section(insights, signals)
    report_sections.append(exec_summary)
    
    # 2. Market Intelligence Overview
    intel_overview = _build_intelligence_overview(total_signals, date_range, source_breakdown)
    report_sections.append(intel_overview)
    
    # 3. Key Findings (3-5 bullet points)
    key_findings = _build_key_findings(insights, signals)
    report_sections.append(key_findings)
    
    # 4. GTM Recommendations (5-7 actionable recommendations)
    gtm_recommendations = _build_gtm_recommendations(insights)
    report_sections.append(gtm_recommendations)
    
    # 5. Competitive Positioning
    competitive_positioning = _build_competitive_positioning(insights, signals)
    report_sections.append(competitive_positioning)
    
    # 6. Timeline & Urgency
    timeline_urgency = _build_timeline_urgency(insights, signals)
    report_sections.append(timeline_urgency)
    
    # Combine all sections
    report = "\n\n".join(report_sections)
    
    return report


def _extract_date_range(signals: List[Dict[str, Any]]) -> Dict[str, str]:
    """Extract date range from signals"""
    
    dates = [s.get('date_detected', '') for s in signals if s.get('date_detected')]
    
    if dates:
        dates.sort()
        return {
            'start': dates[0],
            'end': dates[-1]
        }
    else:
        return {
            'start': datetime.now().strftime('%Y-%m-%d'),
            'end': datetime.now().strftime('%Y-%m-%d')
        }


def _extract_source_breakdown(signals: List[Dict[str, Any]]) -> Dict[str, int]:
    """Extract signal count by source"""
    
    breakdown = defaultdict(int)
    
    for signal in signals:
        source = signal.get('source', 'Unknown')
        
        # Normalize source names
        if 'github' in source.lower():
            breakdown['GitHub'] += 1
        elif 'linkedin' in source.lower():
            breakdown['LinkedIn'] += 1
        elif 'crunchbase' in source.lower():
            breakdown['Crunchbase'] += 1
        elif 'news' in source.lower() or 'stripe' in source.lower():
            breakdown['News'] += 1
        else:
            breakdown[source] += 1
    
    return dict(breakdown)


def _build_executive_summary_section(insights: Dict[str, Any], signals: List[Dict[str, Any]]) -> str:
    """Build executive summary section (150 words)"""
    
    section = "=" * 80 + "\n"
    section += "EXECUTIVE SUMMARY\n"
    section += "=" * 80 + "\n\n"
    
    # Company overview
    section += "COMPANY OVERVIEW: Stripe is a global payments infrastructure provider serving B2B "
    section += "and B2C businesses worldwide. As a market leader in payment processing, API-first "
    section += "financial services, and embedded finance, Stripe continues to expand its product "
    section += "portfolio and market reach.\n\n"
    
    # Market position based on signals
    product_signals = sum(1 for s in signals if s.get('primary_category') == 'PRODUCT')
    talent_signals = sum(1 for s in signals if s.get('primary_category') == 'TALENT')
    
    section += f"MARKET POSITION: Analysis of {len(signals)} market signals reveals Stripe maintains "
    section += "strong technical leadership with "
    
    if product_signals > len(signals) * 0.5:
        section += f"aggressive product development ({product_signals} product signals) "
    else:
        section += "steady product evolution "
    
    if talent_signals > 0:
        section += f"and strategic workforce expansion ({talent_signals} hiring signals). "
    
    section += "The company demonstrates continued innovation in developer tools, SDKs, and API infrastructure.\n\n"
    
    # Strategic direction
    strategic_summary = insights.get('executive_summary', {}).get('strategic_summary', '')
    section += f"STRATEGIC DIRECTION: {strategic_summary}\n"
    
    return section


def _build_intelligence_overview(total_signals: int, date_range: Dict[str, str], 
                                 source_breakdown: Dict[str, int]) -> str:
    """Build market intelligence overview section"""
    
    section = "=" * 80 + "\n"
    section += "MARKET INTELLIGENCE OVERVIEW\n"
    section += "=" * 80 + "\n\n"
    
    section += f"Total Signals Collected: {total_signals}\n"
    section += f"Date Range: {date_range['start']} to {date_range['end']}\n\n"
    
    section += "Sources:\n"
    for source, count in sorted(source_breakdown.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_signals * 100) if total_signals > 0 else 0
        section += f"  - {source}: {count} signals ({percentage:.1f}%)\n"
    
    return section


def _build_key_findings(insights: Dict[str, Any], signals: List[Dict[str, Any]]) -> str:
    """Build key findings section (3-5 bullet points with supporting data)"""
    
    section = "=" * 80 + "\n"
    section += "KEY FINDINGS\n"
    section += "=" * 80 + "\n\n"
    
    findings = []
    
    # Extract top high-confidence insights
    high_conf_insights = insights.get('executive_summary', {}).get('high_confidence_insights', [])
    
    # 1. Product development finding
    product_insights = insights.get('insights_by_category', {}).get('PRODUCT', {})
    if product_insights and product_insights.get('insights'):
        product_finding = product_insights['insights'][0]
        product_count = product_insights['total_signals']
        
        # Extract specific metrics
        high_conf_count = sum(1 for s in signals 
                            if s.get('primary_category') == 'PRODUCT' 
                            and s.get('confidence_level') == 'high')
        
        findings.append(
            f"1. AGGRESSIVE PRODUCT DEVELOPMENT: Stripe demonstrates high development velocity with "
            f"{product_count} product signals detected ({high_conf_count} high-confidence). "
            f"{product_finding['insight_text'][:120]}..."
        )
    
    # 2. Talent/hiring finding
    talent_insights = insights.get('insights_by_category', {}).get('TALENT', {})
    if talent_insights and talent_insights.get('insights'):
        talent_finding = talent_insights['insights'][0]
        
        # Extract hiring numbers
        hiring_signals = [s for s in signals if 'hiring' in s.get('signal_type', '').lower() 
                         or 'hire' in s.get('headline', '').lower()]
        
        findings.append(
            f"\n2. STRATEGIC WORKFORCE EXPANSION: {talent_finding['insight_text'][:120]}... "
            f"({len(hiring_signals)} hiring-related signals)"
        )
    
    # 3. Market/competitive finding
    competitive_insights = insights.get('insights_by_category', {}).get('COMPETITIVE', {})
    market_insights = insights.get('insights_by_category', {}).get('MARKET', {})
    
    if competitive_insights and competitive_insights.get('insights'):
        comp_finding = competitive_insights['insights'][0]
        findings.append(
            f"\n3. COMPETITIVE LANDSCAPE: {comp_finding['insight_text'][:120]}..."
        )
    elif market_insights and market_insights.get('insights'):
        market_finding = market_insights['insights'][0]
        findings.append(
            f"\n3. MARKET DYNAMICS: {market_finding['insight_text'][:120]}..."
        )
    
    # 4. Multi-dimensional finding (cross-category)
    cross_insights = insights.get('cross_category_insights', [])
    if cross_insights:
        cross_finding = cross_insights[0]
        multi_dim_count = sum(1 for s in signals if len(s.get('secondary_categories', [])) > 0)
        
        findings.append(
            f"\n4. INTEGRATED STRATEGY: {cross_finding['insight_text'][:120]}... "
            f"({multi_dim_count} multi-dimensional signals)"
        )
    
    # 5. Timing/launch finding
    timing_insights = insights.get('insights_by_category', {}).get('TIMING', {})
    if timing_insights and timing_insights.get('insights') and len(findings) < 5:
        timing_finding = timing_insights['insights'][0]
        findings.append(
            f"\n5. MARKET TIMING: {timing_finding['insight_text'][:120]}..."
        )
    
    section += "".join(findings[:5])  # Limit to 5 findings
    
    return section


def _build_gtm_recommendations(insights: Dict[str, Any]) -> str:
    """Build GTM recommendations section (5-7 actionable recommendations)"""
    
    section = "\n" + "=" * 80 + "\n"
    section += "GTM RECOMMENDATIONS\n"
    section += "=" * 80 + "\n\n"
    
    recommendations = []
    rec_counter = 1
    
    # Extract recommendations from each category
    for category in ['COMPETITIVE', 'PRODUCT', 'MESSAGING', 'ICP', 'TALENT', 'TIMING', 'MARKET']:
        cat_insights = insights.get('insights_by_category', {}).get(category, {})
        
        if not cat_insights or not cat_insights.get('insights'):
            continue
        
        for insight in cat_insights.get('insights', []):
            if rec_counter > 7:  # Limit to 7 recommendations
                break
            
            # Only include high or medium confidence
            if insight['confidence_level'] not in ['high', 'medium']:
                continue
            
            # Extract finding (first sentence)
            finding = insight['insight_text'].split('.')[0] + '.'
            
            # Get recommendation
            recommendation = insight['recommended_action']
            
            # Determine expected impact
            impact = _determine_expected_impact(category, insight['confidence_level'])
            
            recommendations.append(
                f"{rec_counter}. [{category}] \n"
                f"   Finding: {finding[:100]}{'...' if len(finding) > 100 else ''}\n"
                f"   Recommendation: {recommendation[:150]}{'...' if len(recommendation) > 150 else ''}\n"
                f"   Expected Impact: {impact}\n"
            )
            
            rec_counter += 1
    
    section += "\n".join(recommendations[:7])
    
    return section


def _determine_expected_impact(category: str, confidence: str) -> str:
    """Determine expected impact based on category and confidence"""
    
    impact_map = {
        'COMPETITIVE': {
            'high': 'Significant competitive advantage, potential 15-25% win rate improvement',
            'medium': 'Moderate competitive edge, 10-15% improvement in competitive deals',
            'low': 'Incremental advantage in specific scenarios'
        },
        'PRODUCT': {
            'high': 'Major differentiation opportunity, potential to capture underserved segment',
            'medium': 'Feature parity improvement, reduces competitive gaps',
            'low': 'Nice-to-have enhancement'
        },
        'MESSAGING': {
            'high': 'Strong positioning shift, improved sales conversion (10-20%)',
            'medium': 'Clearer value proposition, better prospect engagement',
            'low': 'Refined messaging for specific segments'
        },
        'ICP': {
            'high': 'New market segment opportunity, potential 20-30% TAM expansion',
            'medium': 'Improved targeting efficiency, higher qualified lead rate',
            'low': 'Better understanding of customer segments'
        },
        'TIMING': {
            'high': 'Critical launch window, first-mover advantage opportunity',
            'medium': 'Optimized launch timing, improved market reception',
            'low': 'Better campaign scheduling'
        },
        'TALENT': {
            'high': 'Early signal of major strategic shift, 6-12 month competitive advantage',
            'medium': 'Organizational capability insight, 3-6 month planning advantage',
            'low': 'General organizational awareness'
        },
        'MARKET': {
            'high': 'Significant market opportunity, potential for rapid growth',
            'medium': 'Favorable market conditions, support for expansion plans',
            'low': 'Market awareness for long-term planning'
        }
    }
    
    return impact_map.get(category, {}).get(confidence, 'TBD based on execution')


def _build_competitive_positioning(insights: Dict[str, Any], signals: List[Dict[str, Any]]) -> str:
    """Build competitive positioning section"""
    
    section = "=" * 80 + "\n"
    section += "COMPETITIVE POSITIONING\n"
    section += "=" * 80 + "\n\n"
    
    # Stripe's Strengths
    section += "STRIPE'S STRENGTHS (based on signals):\n"
    
    strengths = []
    
    # High product velocity
    product_count = sum(1 for s in signals if s.get('primary_category') == 'PRODUCT')
    if product_count > len(signals) * 0.5:
        strengths.append(f"  - Strong product development velocity ({product_count} product signals)")
    
    # Large organization
    employee_signals = [s for s in signals if 'employee' in s.get('headline', '').lower()]
    if employee_signals:
        strengths.append("  - Large, well-resourced organization (12,000+ employees)")
    
    # Technical ecosystem
    sdk_signals = [s for s in signals if 'sdk' in s.get('headline', '').lower() 
                   or 'api' in s.get('headline', '').lower()]
    if sdk_signals:
        strengths.append(f"  - Comprehensive developer ecosystem ({len(sdk_signals)} SDK/API updates)")
    
    # Market leader position
    strengths.append("  - Established market leader with strong brand recognition")
    strengths.append("  - Extensive integration ecosystem and partner network")
    
    section += "\n".join(strengths[:5]) + "\n\n"
    
    # Stripe's Vulnerabilities
    section += "STRIPE'S VULNERABILITIES (gaps in strategy):\n"
    
    vulnerabilities = []
    
    # Extract from competitive insights
    comp_insights = insights.get('insights_by_category', {}).get('COMPETITIVE', {})
    if comp_insights and comp_insights.get('insights'):
        for insight in comp_insights.get('insights', []):
            if 'vulnerabilit' in insight['insight_text'].lower():
                # Extract vulnerability from text
                vuln_text = insight['insight_text'].split(':')[-1].strip()
                vulnerabilities.append(f"  - {vuln_text}")
    
    # Extract from product insights (gaps)
    product_insights = insights.get('insights_by_category', {}).get('PRODUCT', {})
    if product_insights and product_insights.get('insights'):
        for insight in product_insights.get('insights', []):
            if 'gap' in insight['recommended_action'].lower():
                # Extract gaps
                if 'Fraud Prevention' in insight['recommended_action']:
                    vulnerabilities.append("  - Limited focus on fraud prevention capabilities")
                if 'Analytics' in insight['recommended_action']:
                    vulnerabilities.append("  - Underdeveloped analytics and reporting tools")
                if 'Reporting' in insight['recommended_action']:
                    vulnerabilities.append("  - Basic reporting functionality")
    
    # Extract from talent insights (bureaucracy)
    talent_insights = insights.get('insights_by_category', {}).get('TALENT', {})
    if talent_insights and talent_insights.get('insights'):
        for insight in talent_insights.get('insights', []):
            if 'bureaucracy' in insight['insight_text'].lower():
                vulnerabilities.append("  - Large organization may suffer from slower decision-making")
    
    # Default vulnerabilities if none found
    if not vulnerabilities:
        vulnerabilities = [
            "  - Complex pricing structure may deter smaller customers",
            "  - Enterprise-focused positioning leaves mid-market underserved",
            "  - SDK complexity creates integration friction for some developers"
        ]
    
    section += "\n".join(vulnerabilities[:5]) + "\n\n"
    
    # Opportunities for Differentiation
    section += "OPPORTUNITIES FOR DIFFERENTIATION:\n"
    
    opportunities = []
    
    # Extract from recommendations
    for category, cat_insights in insights.get('insights_by_category', {}).items():
        for insight in cat_insights.get('insights', []):
            action = insight['recommended_action']
            
            if 'position' in action.lower() and len(opportunities) < 5:
                opportunities.append(f"  - {action[:80]}...")
            elif 'gap' in action.lower() and len(opportunities) < 5:
                opportunities.append(f"  - {action[:80]}...")
            elif 'emphasize' in action.lower() and len(opportunities) < 5:
                opportunities.append(f"  - {action[:80]}...")
    
    # Default opportunities
    if not opportunities:
        opportunities = [
            "  - Position as nimble alternative with faster implementation",
            "  - Focus on mid-market segment with white-glove support",
            "  - Emphasize pricing transparency and simplicity",
            "  - Build superior analytics and reporting capabilities",
            "  - Develop specialized solutions for underserved verticals"
        ]
    
    section += "\n".join(opportunities[:5])
    
    return section


def _build_timeline_urgency(insights: Dict[str, Any], signals: List[Dict[str, Any]]) -> str:
    """Build timeline and urgency section"""
    
    section = "\n" + "=" * 80 + "\n"
    section += "TIMELINE & URGENCY\n"
    section += "=" * 80 + "\n\n"
    
    # Identify urgent signals
    section += "URGENT MARKET SHIFTS:\n"
    
    urgent_items = []
    
    # High-confidence timing signals
    timing_insights = insights.get('insights_by_category', {}).get('TIMING', {})
    if timing_insights and timing_insights.get('insights'):
        for insight in timing_insights.get('insights', []):
            if insight['confidence_level'] == 'high':
                urgent_items.append(
                    f"  - {insight['insight_text'][:100]}..."
                )
    
    # Product launch signals
    launch_signals = [s for s in signals if any(
        keyword in s.get('headline', '').lower() 
        for keyword in ['launch', 'release', 'announce', 'beta']
    )]
    
    if launch_signals and len(urgent_items) < 3:
        urgent_items.append(
            f"  - {len(launch_signals)} product launch signals detected indicating active release cycle"
        )
    
    # Cross-category urgent signals
    cross_insights = insights.get('cross_category_insights', [])
    for insight in cross_insights:
        if insight['confidence_level'] == 'high' and len(urgent_items) < 3:
            urgent_items.append(
                f"  - {insight['insight_text'][:100]}..."
            )
    
    if urgent_items:
        section += "\n".join(urgent_items[:3]) + "\n\n"
    else:
        section += "  - No immediate urgent market shifts detected\n"
        section += "  - Market appears stable for planned strategic initiatives\n\n"
    
    # Recommended action timeline
    section += "RECOMMENDED ACTION TIMELINE:\n\n"
    
    section += "IMMEDIATE (0-30 days):\n"
    immediate_actions = []
    for category, cat_insights in insights.get('insights_by_category', {}).items():
        for insight in cat_insights.get('insights', []):
            if insight['confidence_level'] == 'high' and len(immediate_actions) < 2:
                immediate_actions.append(
                    f"  - [{category}] {insight['recommended_action'][:80]}..."
                )
    
    if immediate_actions:
        section += "\n".join(immediate_actions) + "\n\n"
    else:
        section += "  - Begin implementing high-confidence recommendations from GTM section\n\n"
    
    section += "SHORT-TERM (30-90 days):\n"
    section += "  - Execute product differentiation strategy based on identified gaps\n"
    section += "  - Develop and deploy counter-positioning messaging\n"
    section += "  - Launch targeted campaigns for underserved segments\n\n"
    
    section += "MEDIUM-TERM (90-180 days):\n"
    section += "  - Monitor competitor hiring patterns for strategic direction signals\n"
    section += "  - Assess market response to initial positioning changes\n"
    section += "  - Refine ICP targeting based on early results\n\n"
    
    section += "=" * 80 + "\n"
    section += "END OF EXECUTIVE SUMMARY\n"
    section += "=" * 80
    
    return section
