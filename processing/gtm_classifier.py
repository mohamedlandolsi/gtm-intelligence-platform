"""
GTM Signal Classifier
Categorizes market signals into GTM (Go-To-Market) dimensions
"""

import re
from typing import List, Dict, Set, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GTMSignalClassifier:
    """Classifies market signals into GTM dimensions"""
    
    def __init__(self):
        """Initialize the classifier with category patterns"""
        
        # Define GTM categories with descriptions
        self.categories = {
            'TIMING': {
                'description': 'Market readiness, seasonal trends, launch windows',
                'weight': 1.0
            },
            'MESSAGING': {
                'description': 'Company positioning, key narratives, brand story',
                'weight': 1.0
            },
            'ICP': {
                'description': 'Ideal Customer Profile, target segments, customer focus',
                'weight': 1.0
            },
            'COMPETITIVE': {
                'description': 'Competitive moves, market threats, differentiation',
                'weight': 1.0
            },
            'PRODUCT': {
                'description': 'Product updates, feature launches, technical expansion',
                'weight': 1.0
            },
            'MARKET': {
                'description': 'Broader market trends, industry dynamics, macro factors',
                'weight': 1.0
            },
            'TALENT': {
                'description': 'Hiring, executive moves, organizational signals',
                'weight': 1.0
            }
        }
        
        # Define patterns for each category
        self._initialize_patterns()
    
    def _initialize_patterns(self):
        """Initialize keyword patterns for each GTM category"""
        
        self.patterns = {
            'TIMING': {
                'keywords': [
                    'launch', 'release', 'announce', 'unveil', 'debut',
                    'q1', 'q2', 'q3', 'q4', 'quarter', 'quarterly',
                    'seasonal', 'holiday', 'year-end', 'fiscal',
                    'timing', 'schedule', 'roadmap', 'timeline',
                    'coming soon', 'upcoming', 'planned', 'slated',
                    'availability', 'rollout', 'phase', 'beta',
                    'early access', 'preview', 'waitlist'
                ],
                'signal_types': [
                    'product_launch', 'api_versioning', 'sdk_update'
                ],
                'patterns': [
                    r'\b(q[1-4]|quarter)\b',
                    r'\b(20\d{2})\b',  # Year mentions
                    r'\b(launch|release).*?(soon|date|schedule|timeline)\b',
                    r'\b(beta|preview|early access)\b'
                ]
            },
            
            'MESSAGING': {
                'keywords': [
                    'position', 'focus', 'mission', 'vision', 'value',
                    'announce', 'statement', 'message', 'brand',
                    'narrative', 'story', 'commitment', 'priority',
                    'emphasis', 'highlight', 'showcase', 'promote',
                    'champion', 'advocate', 'support', 'enable',
                    'empower', 'transform', 'revolutionize', 'redefine',
                    'leading', 'pioneer', 'innovate', 'breakthrough'
                ],
                'signal_types': [
                    'partnership', 'market_expansion', 'announcement'
                ],
                'patterns': [
                    r'\b(position|positioning).*?(as|for|to)\b',
                    r'\b(focus|focused|focusing).*?(on)\b',
                    r'\b(mission|vision|commitment).*?(to|is)\b',
                    r'\b(enable|empower|transform)\b'
                ]
            },
            
            'ICP': {
                'keywords': [
                    'enterprise', 'smb', 'small business', 'mid-market',
                    'startup', 'fortune 500', 'b2b', 'b2c',
                    'segment', 'target', 'customer', 'vertical',
                    'industry', 'sector', 'market segment',
                    'saas', 'e-commerce', 'retail', 'fintech',
                    'healthcare', 'education', 'government',
                    'developer', 'technical', 'non-technical',
                    'global', 'regional', 'local', 'international'
                ],
                'signal_types': [
                    'market_expansion', 'partnership', 'hiring'
                ],
                'patterns': [
                    r'\b(target|targeting|targets).*?(market|segment|customer)\b',
                    r'\b(enterprise|smb|mid-market|startup)\b',
                    r'\b(b2b|b2c)\b',
                    r'\b(vertical|industry|sector).*?(focus|expansion)\b'
                ]
            },
            
            'COMPETITIVE': {
                'keywords': [
                    'competitor', 'compete', 'competition', 'competitive',
                    'versus', 'vs', 'alternative', 'differentiation',
                    'advantage', 'edge', 'superior', 'better than',
                    'market share', 'leader', 'challenger', 'threat',
                    'disruption', 'disrupt', 'challenge', 'rivalry',
                    'plaid', 'adyen', 'square', 'paypal', 'braintree',
                    'unique', 'only', 'first', 'exclusive',
                    'benchmark', 'outperform', 'surpass'
                ],
                'signal_types': [
                    'competitive_move', 'acquisition', 'partnership'
                ],
                'patterns': [
                    r'\b(vs|versus|compared to|competing with)\b',
                    r'\b(competitor|competition|competitive)\b',
                    r'\b(plaid|adyen|square|paypal|braintree)\b',
                    r'\b(differentiate|differentiation|advantage)\b',
                    r'\b(market share|leader|leadership)\b'
                ]
            },
            
            'PRODUCT': {
                'keywords': [
                    'product', 'feature', 'api', 'sdk', 'release',
                    'version', 'update', 'enhancement', 'improvement',
                    'capability', 'functionality', 'integration',
                    'platform', 'service', 'tool', 'solution',
                    'technology', 'infrastructure', 'architecture',
                    'performance', 'scalability', 'reliability',
                    'security', 'compliance', 'certification',
                    'documentation', 'developer experience', 'dx'
                ],
                'signal_types': [
                    'sdk_update', 'new_api_endpoint', 'api_expansion',
                    'api_enhancement', 'product_launch', 'developer_tools',
                    'new_repository', 'commit_activity'
                ],
                'patterns': [
                    r'\b(api|sdk|product|feature).*?(new|release|launch|update)\b',
                    r'\b(version|v\d+\.\d+)\b',
                    r'\b(repository|repo|github)\b',
                    r'\b(developer|development|engineering)\b'
                ]
            },
            
            'MARKET': {
                'keywords': [
                    'market', 'industry', 'trend', 'growth', 'expansion',
                    'adoption', 'demand', 'opportunity', 'landscape',
                    'macroeconomic', 'economic', 'regulation', 'regulatory',
                    'compliance', 'policy', 'legislation', 'law',
                    'globalization', 'digital transformation', 'shift',
                    'consumer behavior', 'spending', 'investment',
                    'forecast', 'projection', 'estimate', 'report',
                    'research', 'analysis', 'study', 'survey'
                ],
                'signal_types': [
                    'market_expansion', 'regulatory', 'industry_trend'
                ],
                'patterns': [
                    r'\b(market|industry).*?(grow|growth|expanding|expansion)\b',
                    r'\b(trend|trending|shift|transformation)\b',
                    r'\b(regulation|regulatory|compliance|policy)\b',
                    r'\b(\d+%|percent).*?(growth|increase|rise)\b'
                ]
            },
            
            'TALENT': {
                'keywords': [
                    'hire', 'hiring', 'recruit', 'recruitment', 'join',
                    'employee', 'headcount', 'team', 'staff', 'workforce',
                    'executive', 'ceo', 'cto', 'cfo', 'vp', 'director',
                    'manager', 'lead', 'head of', 'chief',
                    'appointment', 'promotion', 'departure', 'exit',
                    'organizational', 'org chart', 'restructure',
                    'talent', 'skill', 'expertise', 'experience',
                    'opening', 'position', 'role', 'job'
                ],
                'signal_types': [
                    'hiring', 'growth', 'leadership_change', 'org_change'
                ],
                'patterns': [
                    r'\b(hire|hiring|hired|recruit)\b',
                    r'\b(ceo|cto|cfo|cmo|vp|director|executive)\b',
                    r'\b(join|joined|joining).*?(as|team)\b',
                    r'\b(position|role|opening|job)\b',
                    r'\b(\d+\+?).*?(employee|hire|position|opening)\b'
                ]
            }
        }
    
    def classify_gtm_signals(self, signals_list: List[Dict]) -> List[Dict]:
        """
        Classify market signals into GTM dimensions
        
        Args:
            signals_list: List of signal dictionaries with at least:
                - headline: str
                - description: str
                - signal_type: str
        
        Returns:
            List of signals with added GTM classifications:
                - primary_category: str (main GTM dimension)
                - secondary_categories: List[str] (additional relevant dimensions)
                - category_scores: Dict[str, float] (confidence scores)
                - gtm_insights: str (explanation of classification)
        """
        logger.info(f"Classifying {len(signals_list)} signals into GTM dimensions...")
        
        classified_signals = []
        
        for signal in signals_list:
            classified = self._classify_single_signal(signal)
            classified_signals.append(classified)
        
        # Generate summary
        self._log_classification_summary(classified_signals)
        
        return classified_signals
    
    def _classify_single_signal(self, signal: Dict) -> Dict:
        """Classify a single signal into GTM categories"""
        
        # Extract text to analyze
        headline = signal.get('headline', '').lower()
        description = signal.get('description', '').lower()
        signal_type = signal.get('signal_type', '').lower()
        
        combined_text = f"{headline} {description}"
        
        # Calculate scores for each category
        category_scores = {}
        
        for category, patterns in self.patterns.items():
            score = self._calculate_category_score(
                combined_text,
                signal_type,
                patterns
            )
            category_scores[category] = score
        
        # Determine primary and secondary categories
        primary_category, secondary_categories = self._determine_categories(
            category_scores
        )
        
        # Generate insights
        gtm_insights = self._generate_insights(
            signal,
            primary_category,
            secondary_categories,
            category_scores
        )
        
        # Add classifications to signal
        classified_signal = signal.copy()
        classified_signal['primary_category'] = primary_category
        classified_signal['secondary_categories'] = secondary_categories
        classified_signal['category_scores'] = category_scores
        classified_signal['gtm_insights'] = gtm_insights
        
        return classified_signal
    
    def _calculate_category_score(
        self,
        text: str,
        signal_type: str,
        patterns: Dict
    ) -> float:
        """Calculate relevance score for a category"""
        
        score = 0.0
        
        # Check keywords (0.4 weight)
        keyword_matches = sum(
            1 for keyword in patterns['keywords']
            if keyword.lower() in text
        )
        if keyword_matches > 0:
            # Normalize by number of keywords, cap at 0.4
            score += min(0.4, (keyword_matches / len(patterns['keywords'])) * 2)
        
        # Check signal type match (0.3 weight)
        if signal_type in patterns.get('signal_types', []):
            score += 0.3
        
        # Check regex patterns (0.3 weight)
        pattern_matches = sum(
            1 for pattern in patterns.get('patterns', [])
            if re.search(pattern, text, re.IGNORECASE)
        )
        if pattern_matches > 0:
            score += min(0.3, (pattern_matches / len(patterns.get('patterns', [1]))) * 0.5)
        
        return min(1.0, score)  # Cap at 1.0
    
    def _determine_categories(
        self,
        category_scores: Dict[str, float]
    ) -> Tuple[str, List[str]]:
        """Determine primary and secondary categories from scores"""
        
        # Sort categories by score
        sorted_categories = sorted(
            category_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Primary category: highest score (must be > 0.2)
        if sorted_categories[0][1] >= 0.2:
            primary_category = sorted_categories[0][0]
        else:
            primary_category = 'PRODUCT'  # Default fallback
        
        # Secondary categories: score >= 0.3 and not primary
        secondary_categories = [
            cat for cat, score in sorted_categories[1:]
            if score >= 0.3
        ]
        
        # Limit to top 2 secondary categories
        secondary_categories = secondary_categories[:2]
        
        return primary_category, secondary_categories
    
    def _generate_insights(
        self,
        signal: Dict,
        primary_category: str,
        secondary_categories: List[str],
        category_scores: Dict[str, float]
    ) -> str:
        """Generate human-readable insights about the classification"""
        
        insights = []
        
        # Primary category insight
        primary_score = category_scores[primary_category]
        confidence = 'high' if primary_score >= 0.6 else 'medium' if primary_score >= 0.4 else 'low'
        
        insights.append(
            f"Primary GTM dimension: {primary_category} (confidence: {confidence})"
        )
        
        # Explanation based on category
        explanations = {
            'TIMING': 'This signal indicates a specific timing opportunity or launch window.',
            'MESSAGING': 'This signal reveals how the company is positioning itself in the market.',
            'ICP': 'This signal provides clues about target customer segments and ideal customer profile.',
            'COMPETITIVE': 'This signal relates to competitive positioning and market dynamics.',
            'PRODUCT': 'This signal concerns product development, features, or technical capabilities.',
            'MARKET': 'This signal reflects broader market trends and industry dynamics.',
            'TALENT': 'This signal indicates organizational changes and strategic hiring.'
        }
        
        insights.append(explanations.get(primary_category, ''))
        
        # Secondary categories
        if secondary_categories:
            insights.append(
                f"Also relevant to: {', '.join(secondary_categories)}"
            )
        
        # GTM action implications
        actions = self._suggest_gtm_actions(
            signal,
            primary_category,
            secondary_categories
        )
        if actions:
            insights.append(f"GTM Action: {actions}")
        
        return ' '.join(insights)
    
    def _suggest_gtm_actions(
        self,
        signal: Dict,
        primary_category: str,
        secondary_categories: List[str]
    ) -> str:
        """Suggest GTM actions based on classification"""
        
        actions = {
            'TIMING': 'Monitor launch windows and adjust campaign timing accordingly.',
            'MESSAGING': 'Align competitive messaging and positioning materials.',
            'ICP': 'Refine targeting criteria and customer segmentation strategy.',
            'COMPETITIVE': 'Update competitive battlecards and differentiation talking points.',
            'PRODUCT': 'Prepare product marketing collateral and technical documentation.',
            'MARKET': 'Adjust market strategy and consider new opportunities.',
            'TALENT': 'Monitor organizational changes that signal strategic direction.'
        }
        
        return actions.get(primary_category, '')
    
    def _log_classification_summary(self, classified_signals: List[Dict]):
        """Log summary of classification results"""
        
        # Count by primary category
        primary_counts = {}
        for signal in classified_signals:
            cat = signal['primary_category']
            primary_counts[cat] = primary_counts.get(cat, 0) + 1
        
        logger.info("\nClassification Summary:")
        logger.info("-" * 60)
        for category in self.categories.keys():
            count = primary_counts.get(category, 0)
            percentage = (count / len(classified_signals) * 100) if classified_signals else 0
            logger.info(f"  {category:15s}: {count:3d} signals ({percentage:5.1f}%)")
        
        logger.info("-" * 60)
        logger.info(f"Total classified: {len(classified_signals)} signals")
    
    def generate_gtm_report(self, classified_signals: List[Dict]) -> Dict:
        """Generate comprehensive GTM analysis report"""
        
        report = {
            'total_signals': len(classified_signals),
            'by_primary_category': {},
            'by_secondary_category': {},
            'high_confidence_signals': [],
            'multi_dimensional_signals': [],
            'category_combinations': {},
            'gtm_recommendations': []
        }
        
        # Count by primary category
        for signal in classified_signals:
            primary = signal['primary_category']
            report['by_primary_category'][primary] = \
                report['by_primary_category'].get(primary, 0) + 1
            
            # Count secondary categories
            for secondary in signal.get('secondary_categories', []):
                report['by_secondary_category'][secondary] = \
                    report['by_secondary_category'].get(secondary, 0) + 1
            
            # High confidence signals (primary score >= 0.6)
            primary_score = signal.get('category_scores', {}).get(primary, 0)
            if primary_score >= 0.6:
                report['high_confidence_signals'].append({
                    'headline': signal.get('headline', ''),
                    'category': primary,
                    'score': primary_score
                })
            
            # Multi-dimensional signals (has secondary categories)
            if signal.get('secondary_categories'):
                report['multi_dimensional_signals'].append({
                    'headline': signal.get('headline', ''),
                    'primary': primary,
                    'secondary': signal['secondary_categories']
                })
            
            # Category combinations
            if signal.get('secondary_categories'):
                combo = f"{primary} + {', '.join(signal['secondary_categories'])}"
                report['category_combinations'][combo] = \
                    report['category_combinations'].get(combo, 0) + 1
        
        # Generate GTM recommendations
        report['gtm_recommendations'] = self._generate_gtm_recommendations(
            report
        )
        
        return report
    
    def _generate_gtm_recommendations(self, report: Dict) -> List[str]:
        """Generate actionable GTM recommendations from classified signals"""
        
        recommendations = []
        
        by_category = report['by_primary_category']
        total = report['total_signals']
        
        # Product-heavy signals
        if by_category.get('PRODUCT', 0) / total > 0.4:
            recommendations.append(
                "High product activity detected. Recommend preparing product marketing "
                "campaigns and technical content to support launches."
            )
        
        # Competitive signals
        if by_category.get('COMPETITIVE', 0) >= 3:
            recommendations.append(
                "Multiple competitive signals detected. Update competitive battlecards "
                "and brief sales team on positioning changes."
            )
        
        # ICP signals
        if by_category.get('ICP', 0) >= 2:
            recommendations.append(
                "Target customer signals present. Review and refine ICP definitions "
                "and segmentation strategy."
            )
        
        # Timing signals
        if by_category.get('TIMING', 0) >= 2:
            recommendations.append(
                "Launch timing opportunities identified. Coordinate marketing calendar "
                "and campaign planning."
            )
        
        # Talent signals
        if by_category.get('TALENT', 0) >= 3:
            recommendations.append(
                "Significant organizational changes detected. Monitor for strategic "
                "shifts and new market focuses."
            )
        
        # Multi-dimensional signals
        if len(report['multi_dimensional_signals']) / total > 0.3:
            recommendations.append(
                "Many signals span multiple GTM dimensions. Consider integrated "
                "campaigns that address multiple angles."
            )
        
        return recommendations


def classify_gtm_signals(signals_list: List[Dict]) -> List[Dict]:
    """
    Convenience function to classify signals into GTM dimensions
    
    Args:
        signals_list: List of market signal dictionaries
        
    Returns:
        List of signals with GTM classifications added
    """
    classifier = GTMSignalClassifier()
    return classifier.classify_gtm_signals(signals_list)


if __name__ == "__main__":
    # Example usage
    print("GTM Signal Classifier")
    print("=" * 80)
    
    # Sample signals for testing
    sample_signals = [
        {
            'headline': 'Stripe launches new API for cryptocurrency payments',
            'description': 'New API endpoint allows merchants to accept crypto payments with automatic conversion to fiat',
            'signal_type': 'new_api_endpoint',
            'date_detected': '2025-11-05'
        },
        {
            'headline': 'Stripe hires 150+ positions in enterprise sales',
            'description': 'Stripe is actively hiring for 150 open positions globally, with focus on enterprise B2B sales',
            'signal_type': 'hiring',
            'date_detected': '2025-11-05'
        },
        {
            'headline': 'PayPal launches competing real-time payment service',
            'description': 'PayPal announces new instant payment processing competing directly with Stripe',
            'signal_type': 'competitive_move',
            'date_detected': '2025-11-04'
        }
    ]
    
    # Classify signals
    classifier = GTMSignalClassifier()
    classified = classifier.classify_gtm_signals(sample_signals)
    
    # Display results
    print(f"\nClassified {len(classified)} signals:\n")
    
    for i, signal in enumerate(classified, 1):
        print(f"{i}. {signal['headline']}")
        print(f"   Primary: {signal['primary_category']}")
        if signal['secondary_categories']:
            print(f"   Secondary: {', '.join(signal['secondary_categories'])}")
        print(f"   Insights: {signal['gtm_insights']}")
        print()
    
    # Generate GTM report
    report = classifier.generate_gtm_report(classified)
    
    print("\n" + "=" * 80)
    print("GTM ANALYSIS REPORT")
    print("=" * 80)
    print(f"\nTotal Signals: {report['total_signals']}")
    print(f"\nBy Primary Category:")
    for cat, count in sorted(report['by_primary_category'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")
    
    if report['gtm_recommendations']:
        print(f"\nGTM Recommendations:")
        for i, rec in enumerate(report['gtm_recommendations'], 1):
            print(f"  {i}. {rec}")
