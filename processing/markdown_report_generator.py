"""
Markdown Report Generator for GTM Intelligence Platform

This module generates professional markdown reports from GTM signals, insights, and analysis.
Creates comprehensive reports suitable for executive review and strategic planning.
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_markdown_report(
    signals: List[Dict[str, Any]],
    insights: Dict[str, Any],
    executive_summary: Optional[str] = None,
    output_path: str = 'outputs/reports/GTM_ANALYSIS_STRIPE.md',
    company_name: str = 'Stripe'
) -> str:
    """
    Generate a comprehensive markdown report from GTM signals and insights.
    
    Creates a professional report with:
    - Executive summary
    - Market signals overview
    - Key findings with evidence and recommendations
    - Signals organized by GTM category
    - GTM recommendations
    - Competitive positioning analysis
    - Data sources and methodology
    
    Args:
        signals: List of classified GTM signals
        insights: Dictionary containing insights by category and cross-category patterns
        executive_summary: Optional executive summary text
        output_path: Path where the markdown file will be saved
        company_name: Name of the company being analyzed (default: Stripe)
    
    Returns:
        Path to the generated markdown file
    
    Example:
        >>> report_path = generate_markdown_report(
        ...     signals=classified_signals,
        ...     insights=gtm_insights,
        ...     executive_summary=exec_summary,
        ...     company_name='Stripe'
        ... )
    """
    logger.info(f"Generating markdown report for {company_name}")
    
    # Build report sections
    report_content = []
    
    # Header
    report_content.append(f"# GTM Intelligence Report: {company_name}\n")
    report_content.append(f"*Generated: {datetime.now().strftime('%B %d, %Y')}*\n")
    report_content.append("---\n")
    
    # Executive Summary
    report_content.append(_generate_executive_summary_section(
        executive_summary, signals, insights
    ))
    
    # Market Signals Overview
    report_content.append(_generate_signals_overview_section(signals))
    
    # Key Findings
    report_content.append(_generate_key_findings_section(signals, insights))
    
    # Signals by Category
    report_content.append(_generate_signals_by_category_section(signals))
    
    # GTM Recommendations
    report_content.append(_generate_recommendations_section(insights, signals))
    
    # Competitive Positioning
    report_content.append(_generate_competitive_positioning_section(signals, insights))
    
    # Data Sources & Methodology
    report_content.append(_generate_methodology_section(signals))
    
    # Combine all sections
    full_report = '\n'.join(report_content)
    
    # Write to file
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_report)
    
    logger.info(f"Successfully generated markdown report: {output_path}")
    logger.info(f"Report length: {len(full_report.split())} words")
    
    return output_path


def _generate_executive_summary_section(
    executive_summary: Optional[str],
    signals: List[Dict[str, Any]],
    insights: Dict[str, Any]
) -> str:
    """Generate the executive summary section."""
    content = ["## Executive Summary\n"]
    
    if executive_summary:
        # Extract just the executive summary paragraph (first section)
        lines = executive_summary.strip().split('\n')
        summary_text = []
        for line in lines:
            if line.strip().startswith('===') or line.strip().startswith('EXECUTIVE SUMMARY'):
                continue
            if line.strip().startswith('MARKET INTELLIGENCE OVERVIEW'):
                break
            if line.strip():
                summary_text.append(line.strip())
        
        if summary_text:
            content.append(' '.join(summary_text) + '\n')
    else:
        # Generate a brief summary from insights
        total_signals = len(signals)
        high_confidence = len([s for s in signals if s.get('confidence') == 'high'])
        categories = len(set(s.get('primary_category', 'UNKNOWN') for s in signals))
        
        content.append(
            f"Analysis of {total_signals} market signals reveals strategic insights across "
            f"{categories} GTM dimensions. This report synthesizes competitive intelligence, "
            f"product developments, and market positioning to inform go-to-market strategy. "
            f"Key findings indicate significant activity in product development, talent acquisition, "
            f"and strategic partnerships. High-confidence signals ({high_confidence} total) provide "
            f"actionable intelligence for competitive positioning and strategic response.\n"
        )
    
    return ''.join(content)


def _generate_signals_overview_section(signals: List[Dict[str, Any]]) -> str:
    """Generate the market signals overview section."""
    content = ["## Market Signals Overview\n"]
    
    # Calculate statistics
    total_signals = len(signals)
    date_range = _calculate_date_range(signals)
    source_counts = _calculate_source_counts(signals)
    
    # Count high confidence signals (checking multiple fields)
    high_confidence = 0
    for s in signals:
        conf = s.get('confidence') or s.get('confidence_level') or s.get('raw_json', {}).get('confidence_level')
        if conf == 'high':
            high_confidence += 1
    
    # Overview statistics
    content.append(f"**Total signals collected:** {total_signals}\n\n")
    content.append(f"**Analysis period:** {date_range}\n\n")
    content.append(f"**High-confidence signals:** {high_confidence} ({(high_confidence/total_signals*100):.0f}%)\n\n")
    
    # Data sources breakdown
    content.append("**Data sources:**\n\n")
    for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_signals * 100)
        content.append(f"- **{source}:** {count} signals ({percentage:.0f}%)\n")
    
    content.append("\n")
    return ''.join(content)


def _generate_key_findings_section(
    signals: List[Dict[str, Any]],
    insights: Dict[str, Any]
) -> str:
    """Generate key findings section with evidence and recommendations."""
    content = ["## Key Findings\n"]
    
    # Extract high-priority insights
    priority_insights = _extract_priority_insights(insights, signals)
    
    for i, finding in enumerate(priority_insights[:5], 1):
        content.append(f"### Finding {i}: {finding['headline']}\n")
        
        # Evidence
        content.append("**Evidence:**\n\n")
        for evidence in finding['evidence'][:3]:  # Top 3 pieces of evidence
            content.append(f"- {evidence}\n")
        content.append("\n")
        
        # GTM Impact
        content.append(f"**GTM Impact:** {finding['gtm_impact']}\n\n")
        
        # Recommendation
        content.append(f"**Recommendation:** {finding['recommendation']}\n\n")
    
    return ''.join(content)


def _generate_signals_by_category_section(signals: List[Dict[str, Any]]) -> str:
    """Generate signals organized by GTM category."""
    content = ["## Signals by Category\n"]
    
    # Group signals by category
    by_category = defaultdict(list)
    for signal in signals:
        category = signal.get('primary_category', 'UNKNOWN')
        by_category[category].append(signal)
    
    # GTM categories in order
    categories = ['TIMING', 'MESSAGING', 'ICP', 'COMPETITIVE', 'PRODUCT', 'MARKET', 'TALENT']
    
    for category in categories:
        category_signals = by_category.get(category, [])
        if not category_signals:
            continue
        
        content.append(f"### {category}\n")
        content.append(f"*{len(category_signals)} signals*\n\n")
        
        # Sort by date (newest first)
        sorted_signals = sorted(
            category_signals,
            key=lambda x: x.get('date', ''),
            reverse=True
        )
        
        for signal in sorted_signals[:10]:  # Show top 10 per category
            headline = signal.get('headline', 'Unknown signal')
            
            # Try multiple date fields
            date = signal.get('date') or signal.get('date_detected') or signal.get('raw_json', {}).get('date')
            if date:
                try:
                    date_formatted = datetime.strptime(date, '%Y-%m-%d').strftime('%b %d, %Y')
                except:
                    date_formatted = date
            else:
                date_formatted = 'Unknown date'
            
            # Try multiple confidence fields
            confidence = signal.get('confidence') or signal.get('confidence_level') or signal.get('raw_json', {}).get('confidence_level') or 'unknown'
            
            # Get strategic implication from gtm_insights or strategic_implication
            implication = signal.get('strategic_implication') or signal.get('gtm_insights', '')
            
            # Format signal entry
            content.append(f"**{headline}**  \n")
            content.append(f"*{date_formatted} • {confidence.title()} confidence*\n\n")
            
            if implication:
                # Clean and truncate implication
                clean_implication = implication.replace('\n', ' ').strip()
                if len(clean_implication) > 200:
                    clean_implication = clean_implication[:197] + '...'
                content.append(f"> {clean_implication}\n\n")
        
        if len(category_signals) > 10:
            content.append(f"*... and {len(category_signals) - 10} more signals*\n\n")
    
    return ''.join(content)


def _generate_recommendations_section(
    insights: Dict[str, Any],
    signals: List[Dict[str, Any]]
) -> str:
    """Generate GTM recommendations section."""
    content = ["## GTM Recommendations\n"]
    
    # Extract recommendations from insights
    recommendations = []
    
    # Category-specific recommendations
    for category, category_insights in insights.get('by_category', {}).items():
        for insight in category_insights:
            if 'recommended_actions' in insight:
                for action in insight['recommended_actions']:
                    recommendations.append({
                        'category': category,
                        'action': action,
                        'confidence': insight.get('confidence', 'medium'),
                        'supporting_count': insight.get('supporting_signals_count', 0)
                    })
    
    # Cross-category recommendations
    for insight in insights.get('cross_category_insights', []):
        if 'recommended_actions' in insight:
            for action in insight['recommended_actions']:
                recommendations.append({
                    'category': 'CROSS-CATEGORY',
                    'action': action,
                    'confidence': insight.get('confidence', 'medium'),
                    'supporting_count': insight.get('pattern_strength', 0)
                })
    
    # Sort by confidence and supporting signals
    recommendations.sort(
        key=lambda x: (
            1 if x['confidence'] == 'high' else 0,
            x['supporting_count']
        ),
        reverse=True
    )
    
    # Format top recommendations
    for i, rec in enumerate(recommendations[:7], 1):
        category_badge = f"*[{rec['category']}]*" if rec['category'] != 'CROSS-CATEGORY' else "*[Strategic]*"
        content.append(f"### {i}. {rec['action'].split('.')[0]}\n")
        content.append(f"{category_badge}\n\n")
        
        # Full recommendation text
        content.append(f"{rec['action']}\n\n")
        
        # Supporting evidence indicator
        if rec['supporting_count'] > 0:
            content.append(f"*Based on {rec['supporting_count']} supporting signals*\n\n")
    
    return ''.join(content)


def _generate_competitive_positioning_section(
    signals: List[Dict[str, Any]],
    insights: Dict[str, Any]
) -> str:
    """Generate competitive positioning analysis."""
    content = ["## Competitive Positioning\n"]
    
    # Analyze strengths
    content.append("### Stripe's Strengths\n")
    content.append("*Based on signal analysis*\n\n")
    
    strengths = _extract_strengths(signals, insights)
    for strength in strengths:
        content.append(f"- **{strength['title']}:** {strength['description']}\n")
    content.append("\n")
    
    # Analyze gaps/vulnerabilities
    content.append("### Stripe's Gaps & Vulnerabilities\n")
    content.append("*Potential areas of weakness*\n\n")
    
    gaps = _extract_gaps(signals, insights)
    for gap in gaps:
        content.append(f"- **{gap['title']}:** {gap['description']}\n")
    content.append("\n")
    
    # Differentiation opportunities
    content.append("### Differentiation Opportunities\n")
    content.append("*Strategic positioning for competitors*\n\n")
    
    opportunities = _extract_opportunities(signals, insights)
    for opp in opportunities:
        content.append(f"- **{opp['title']}:** {opp['description']}\n")
    content.append("\n")
    
    return ''.join(content)


def _generate_methodology_section(signals: List[Dict[str, Any]]) -> str:
    """Generate data sources and methodology section."""
    content = ["## Data Sources & Methodology\n"]
    
    content.append("### Collection Methods\n\n")
    
    # Group by source
    by_source = defaultdict(list)
    for signal in signals:
        source = signal.get('source', 'Unknown')
        by_source[source].append(signal)
    
    # Document each source
    source_descriptions = {
        'LinkedIn': 'Company profile monitoring for organizational changes, hiring patterns, and growth metrics.',
        'GitHub': 'Repository analysis for product development velocity, technology stack evolution, and open-source strategy.',
        'Stripe Official': 'Official communications, product announcements, and documentation updates.',
        'News': 'Media coverage and press releases for market positioning and strategic initiatives.',
        'Business Intelligence': 'Industry reports, analyst coverage, and competitive intelligence.'
    }
    
    for source in sorted(by_source.keys()):
        signal_count = len(by_source[source])
        description = source_descriptions.get(source, 'Market intelligence and competitive signals.')
        
        content.append(f"**{source}** ({signal_count} signals)\n\n")
        content.append(f"{description}\n\n")
    
    # Confidence methodology
    content.append("### Confidence Assessment\n\n")
    content.append(
        "Signals are assigned confidence levels based on:\n\n"
        "- **High:** Direct, verifiable data from authoritative sources (APIs, official sites)\n"
        "- **Medium:** Credible secondary sources with consistent patterns\n"
        "- **Low:** Indirect indicators requiring additional validation\n\n"
    )
    
    # Date range and currency
    date_range = _calculate_date_range(signals)
    content.append(f"**Analysis Period:** {date_range}\n\n")
    content.append(f"**Report Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n")
    
    # Overall confidence
    high_conf_count = 0
    for s in signals:
        conf = s.get('confidence') or s.get('confidence_level') or s.get('raw_json', {}).get('confidence_level')
        if conf == 'high':
            high_conf_count += 1
    
    high_conf_pct = (high_conf_count / len(signals) * 100) if signals else 0
    if high_conf_pct >= 70:
        overall = "High"
    elif high_conf_pct >= 40:
        overall = "Medium-High"
    else:
        overall = "Medium"
    
    content.append(f"**Overall Confidence Level:** {overall} (based on source diversity and signal verification)\n\n")
    
    content.append("---\n")
    content.append("*This report is generated automatically from the GTM Intelligence Platform.*\n")
    
    return ''.join(content)


# Helper functions

def _calculate_date_range(signals: List[Dict[str, Any]]) -> str:
    """Calculate the date range of signals."""
    if not signals:
        return "Unknown"
    
    # Try both 'date' and 'date_detected' fields
    dates = []
    for s in signals:
        date = s.get('date') or s.get('date_detected') or s.get('raw_json', {}).get('date')
        if date:
            dates.append(date)
    
    if not dates:
        return "Unknown"
    
    dates.sort()
    start_date = datetime.strptime(dates[0], '%Y-%m-%d').strftime('%b %Y')
    end_date = datetime.strptime(dates[-1], '%Y-%m-%d').strftime('%b %Y')
    
    if start_date == end_date:
        return start_date
    return f"{start_date} - {end_date}"


def _calculate_source_counts(signals: List[Dict[str, Any]]) -> Dict[str, int]:
    """Count signals by source."""
    counts = defaultdict(int)
    for signal in signals:
        source = signal.get('source', 'Unknown')
        counts[source] += 1
    return dict(counts)


def _extract_priority_insights(
    insights: Dict[str, Any],
    signals: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Extract priority insights as findings with evidence."""
    findings = []
    
    # Process category insights
    for category, category_insights in insights.get('by_category', {}).items():
        for insight in category_insights:
            # Build finding
            finding = {
                'headline': _extract_headline_from_insight(insight),
                'evidence': _extract_evidence(insight, signals, category),
                'gtm_impact': _extract_gtm_impact(insight, category),
                'recommendation': _extract_primary_recommendation(insight),
                'confidence': insight.get('confidence', 'medium'),
                'supporting_count': insight.get('supporting_signals_count', 0)
            }
            findings.append(finding)
    
    # Process cross-category insights
    for insight in insights.get('cross_category_insights', []):
        finding = {
            'headline': _extract_headline_from_insight(insight),
            'evidence': _extract_cross_category_evidence(insight, signals),
            'gtm_impact': _extract_gtm_impact(insight, 'STRATEGIC'),
            'recommendation': _extract_primary_recommendation(insight),
            'confidence': insight.get('confidence', 'medium'),
            'supporting_count': insight.get('pattern_strength', 0)
        }
        findings.append(finding)
    
    # Sort by confidence and supporting signals
    findings.sort(
        key=lambda x: (
            1 if x['confidence'] == 'high' else 0,
            x['supporting_count']
        ),
        reverse=True
    )
    
    return findings


def _extract_headline_from_insight(insight: Dict[str, Any]) -> str:
    """Extract a headline from an insight."""
    insight_text = insight.get('insight', '')
    
    # Extract first sentence or up to first period
    if '.' in insight_text:
        headline = insight_text.split('.')[0] + '.'
    else:
        headline = insight_text
    
    # Truncate if too long
    if len(headline) > 120:
        headline = headline[:117] + '...'
    
    return headline


def _extract_evidence(
    insight: Dict[str, Any],
    signals: List[Dict[str, Any]],
    category: str
) -> List[str]:
    """Extract evidence bullets from signals."""
    evidence = []
    
    # Filter signals by category
    category_signals = [s for s in signals if s.get('primary_category') == category]
    
    # Sort by date and confidence
    category_signals.sort(
        key=lambda x: (
            x.get('date') or x.get('date_detected') or x.get('raw_json', {}).get('date', ''),
            1 if (x.get('confidence') or x.get('confidence_level') or x.get('raw_json', {}).get('confidence_level')) == 'high' else 0
        ),
        reverse=True
    )
    
    # Extract top signals as evidence
    for signal in category_signals[:3]:
        headline = signal.get('headline', 'Unknown')
        date = signal.get('date') or signal.get('date_detected') or signal.get('raw_json', {}).get('date', '')
        if date:
            try:
                date_formatted = datetime.strptime(date, '%Y-%m-%d').strftime('%b %d, %Y')
                evidence.append(f"{headline} ({date_formatted})")
            except:
                evidence.append(headline)
        else:
            evidence.append(headline)
    
    return evidence


def _extract_cross_category_evidence(
    insight: Dict[str, Any],
    signals: List[Dict[str, Any]]
) -> List[str]:
    """Extract evidence from cross-category patterns."""
    evidence = []
    
    # Get categories involved
    categories = insight.get('categories', [])
    
    for category in categories[:3]:
        category_signals = [s for s in signals if s.get('primary_category') == category]
        if category_signals:
            top_signal = max(category_signals, key=lambda x: (
                x.get('date') or x.get('date_detected') or x.get('raw_json', {}).get('date', ''),
                1 if (x.get('confidence') or x.get('confidence_level') or x.get('raw_json', {}).get('confidence_level')) == 'high' else 0
            ))
            headline = top_signal.get('headline', 'Unknown')
            date = top_signal.get('date') or top_signal.get('date_detected') or top_signal.get('raw_json', {}).get('date', '')
            if date:
                try:
                    date_formatted = datetime.strptime(date, '%Y-%m-%d').strftime('%b %d, %Y')
                    evidence.append(f"[{category}] {headline} ({date_formatted})")
                except:
                    evidence.append(f"[{category}] {headline}")
            else:
                evidence.append(f"[{category}] {headline}")
    
    return evidence


def _extract_gtm_impact(insight: Dict[str, Any], category: str) -> str:
    """Extract GTM impact statement."""
    insight_text = insight.get('insight', '')
    
    # Look for impact indicators in the insight text
    impact_keywords = [
        'indicates', 'suggests', 'signals', 'means', 'implies',
        'opportunity', 'threat', 'advantage', 'risk', 'strategic'
    ]
    
    sentences = insight_text.split('.')
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in impact_keywords):
            clean_sentence = sentence.strip()
            if len(clean_sentence) > 20:
                return clean_sentence + '.'
    
    # Default impact based on category
    category_impacts = {
        'PRODUCT': 'Signals product strategy evolution that competitors must address.',
        'TIMING': 'Indicates market timing and launch windows for competitive response.',
        'TALENT': 'Reveals organizational priorities and strategic direction.',
        'COMPETITIVE': 'Directly impacts competitive positioning and market dynamics.',
        'MARKET': 'Affects market perception and positioning strategy.',
        'ICP': 'Influences target customer segment and messaging strategy.',
        'MESSAGING': 'Shapes market narrative and brand positioning.',
        'STRATEGIC': 'Cross-functional impact requiring coordinated strategic response.'
    }
    
    return category_impacts.get(category, 'Requires strategic assessment and potential response.')


def _extract_primary_recommendation(insight: Dict[str, Any]) -> str:
    """Extract primary recommendation from insight."""
    actions = insight.get('recommended_actions', [])
    
    if actions:
        # Return first action (usually most important)
        return actions[0]
    
    # Generate generic recommendation
    return "Monitor developments and assess strategic response options."


def _extract_strengths(
    signals: List[Dict[str, Any]],
    insights: Dict[str, Any]
) -> List[Dict[str, str]]:
    """Extract competitive strengths from signals."""
    strengths = []
    
    # Analyze product signals
    product_signals = [s for s in signals if s.get('primary_category') == 'PRODUCT']
    if len(product_signals) >= 5:
        strengths.append({
            'title': 'High Product Development Velocity',
            'description': f'Active development across {len(product_signals)} product signals indicates strong engineering capacity and innovation momentum.'
        })
    
    # Analyze talent signals
    talent_signals = [s for s in signals if s.get('primary_category') == 'TALENT']
    hiring_signals = [s for s in talent_signals if 'hiring' in s.get('signal_type', '').lower()]
    if hiring_signals:
        strengths.append({
            'title': 'Aggressive Growth Investment',
            'description': f'Active hiring across multiple departments suggests strong financial position and confidence in growth trajectory.'
        })
    
    # Analyze market signals
    market_signals = [s for s in signals if s.get('primary_category') == 'MARKET']
    if market_signals:
        strengths.append({
            'title': 'Strong Market Position',
            'description': 'Established brand presence and market recognition provides advantages in customer acquisition.'
        })
    
    return strengths[:4]  # Top 4 strengths


def _extract_gaps(
    signals: List[Dict[str, Any]],
    insights: Dict[str, Any]
) -> List[Dict[str, str]]:
    """Extract potential gaps and vulnerabilities."""
    gaps = []
    
    # Look for missing categories
    categories_present = set(s.get('primary_category') for s in signals)
    
    if 'COMPETITIVE' not in categories_present or len([s for s in signals if s.get('primary_category') == 'COMPETITIVE']) < 2:
        gaps.append({
            'title': 'Limited Competitive Intelligence Visibility',
            'description': 'Few competitive positioning signals may indicate reactive rather than proactive competitive strategy.'
        })
    
    if 'MESSAGING' not in categories_present or len([s for s in signals if s.get('primary_category') == 'MESSAGING']) < 2:
        gaps.append({
            'title': 'Messaging Strategy Opportunities',
            'description': 'Limited public messaging signals create opportunities for competitors to shape market narrative.'
        })
    
    # Large organization challenges
    talent_signals = [s for s in signals if s.get('primary_category') == 'TALENT']
    employee_counts = [s for s in talent_signals if 'employees' in s.get('headline', '').lower()]
    if employee_counts:
        gaps.append({
            'title': 'Organizational Complexity',
            'description': 'Large organizational scale may create slower decision-making and reduced agility compared to smaller competitors.'
        })
    
    return gaps[:4]  # Top 4 gaps


def _extract_opportunities(
    signals: List[Dict[str, Any]],
    insights: Dict[str, Any]
) -> List[Dict[str, str]]:
    """Extract differentiation opportunities for competitors."""
    opportunities = []
    
    # Speed and agility
    opportunities.append({
        'title': 'Speed & Agility',
        'description': 'Position as nimble alternative that can move faster on feature development and customer-specific customizations.'
    })
    
    # Specialized focus
    product_signals = [s for s in signals if s.get('primary_category') == 'PRODUCT']
    if len(product_signals) > 10:
        opportunities.append({
            'title': 'Vertical Specialization',
            'description': 'Deep specialization in specific industries or use cases vs. horizontal platform approach.'
        })
    
    # Customer service
    opportunities.append({
        'title': 'Premium Support & Service',
        'description': 'Differentiate on personalized support and customer success vs. scaled, automated support model.'
    })
    
    # Pricing flexibility
    opportunities.append({
        'title': 'Flexible Pricing Models',
        'description': 'Alternative pricing structures that better align with specific customer segments or use cases.'
    })
    
    return opportunities[:4]  # Top 4 opportunities


# Convenience function for easy usage
def create_gtm_report(
    signals_path: str,
    insights_path: str,
    executive_summary_path: Optional[str] = None,
    output_path: str = 'outputs/reports/GTM_ANALYSIS_STRIPE.md',
    company_name: str = 'Stripe'
) -> str:
    """
    Convenience function to generate report from file paths.
    
    Args:
        signals_path: Path to classified signals JSON file
        insights_path: Path to insights JSON file
        executive_summary_path: Optional path to executive summary text file
        output_path: Path for output markdown file
        company_name: Company being analyzed
    
    Returns:
        Path to generated markdown report
    """
    import json
    
    # Load signals
    with open(signals_path, 'r') as f:
        signals_data = json.load(f)
        signals = signals_data.get('classified_signals', signals_data.get('signals', []))
    
    # Load insights
    with open(insights_path, 'r') as f:
        insights = json.load(f)
    
    # Load executive summary if provided
    executive_summary = None
    if executive_summary_path:
        with open(executive_summary_path, 'r') as f:
            executive_summary = f.read()
    
    # Generate report
    return generate_markdown_report(
        signals=signals,
        insights=insights,
        executive_summary=executive_summary,
        output_path=output_path,
        company_name=company_name
    )


if __name__ == '__main__':
    # Example usage
    print("GTM Markdown Report Generator")
    print("=" * 80)
    print("\nUsage:")
    print("  from processing.markdown_report_generator import generate_markdown_report")
    print("  report_path = generate_markdown_report(signals, insights, executive_summary)")
    print("\nOr use convenience function:")
    print("  from processing.markdown_report_generator import create_gtm_report")
    print("  report_path = create_gtm_report(")
    print("      signals_path='outputs/classified/gtm_classified_signals.json',")
    print("      insights_path='outputs/insights/gtm_insights_report.json',")
    print("      executive_summary_path='outputs/reports/executive_summary.txt'")
    print("  )")
