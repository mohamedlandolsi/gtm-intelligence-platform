"""
Export Utilities
Functions to export GTM signals, insights, and analysis in structured formats
"""

import csv
import json
from typing import List, Dict, Any
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def export_signals_to_csv(signals: List[Dict[str, Any]], output_path: str = None) -> str:
    """
    Export signals to CSV format with human-readable formatting
    
    Args:
        signals: List of classified signals
        output_path: Optional custom output path. Defaults to data/gtm_signals.csv
        
    Returns:
        Path to created CSV file
    """
    
    if output_path is None:
        output_path = 'data/gtm_signals.csv'
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    logger.info(f"Exporting {len(signals)} signals to CSV: {output_path}")
    
    # Sort signals by date (newest first)
    sorted_signals = sorted(
        signals, 
        key=lambda x: x.get('date_detected', ''), 
        reverse=True
    )
    
    # Calculate summary statistics
    if sorted_signals:
        date_range = _calculate_date_range(sorted_signals)
        summary_stats = _calculate_signal_summary(sorted_signals)
    else:
        date_range = {'start': 'N/A', 'end': 'N/A'}
        summary_stats = {}
    
    # Define CSV columns
    columns = [
        'signal_id',
        'headline',
        'description',
        'signal_type',
        'gtm_category',
        'date',
        'source',
        'source_url',
        'confidence',
        'strategic_implication'
    ]
    
    # Write CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        
        # Write summary rows
        writer.writerow({
            'signal_id': '# GTM SIGNALS EXPORT',
            'headline': f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            'description': '',
            'signal_type': '',
            'gtm_category': '',
            'date': '',
            'source': '',
            'source_url': '',
            'confidence': '',
            'strategic_implication': ''
        })
        
        writer.writerow({
            'signal_id': f'# Total Signals: {len(sorted_signals)}',
            'headline': f'Date Range: {date_range["start"]} to {date_range["end"]}',
            'description': '',
            'signal_type': '',
            'gtm_category': '',
            'date': '',
            'source': '',
            'source_url': '',
            'confidence': '',
            'strategic_implication': ''
        })
        
        if summary_stats:
            writer.writerow({
                'signal_id': f'# High Confidence: {summary_stats.get("high_confidence", 0)}',
                'headline': f'Categories: {", ".join(summary_stats.get("categories", []))}',
                'description': '',
                'signal_type': '',
                'gtm_category': '',
                'date': '',
                'source': '',
                'source_url': '',
                'confidence': '',
                'strategic_implication': ''
            })
        
        # Blank row separator
        writer.writerow({col: '' for col in columns})
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        for signal in sorted_signals:
            # Validate and clean data
            row = _prepare_signal_row(signal, columns)
            writer.writerow(row)
    
    logger.info(f"Successfully exported {len(sorted_signals)} signals to {output_path}")
    return output_path


def export_insights_to_csv(insights: Dict[str, Any], output_path: str = None) -> str:
    """
    Export insights to CSV format sorted by urgency
    
    Args:
        insights: Generated insights dictionary from generate_gtm_insights()
        output_path: Optional custom output path. Defaults to data/gtm_insights.csv
        
    Returns:
        Path to created CSV file
    """
    
    if output_path is None:
        output_path = 'data/gtm_insights.csv'
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    logger.info(f"Exporting insights to CSV: {output_path}")
    
    # Extract all insights with metadata
    all_insights = []
    insight_counter = 1
    
    for category, cat_data in insights.get('insights_by_category', {}).items():
        for insight in cat_data.get('insights', []):
            all_insights.append({
                'insight_id': f'INS-{insight_counter:03d}',
                'category': category,
                'insight_text': insight.get('insight_text', ''),
                'supporting_signals_count': len(insight.get('supporting_signals', [])),
                'confidence': insight.get('confidence_level', 'unknown'),
                'recommended_action': insight.get('recommended_action', ''),
                'urgency_level': _determine_urgency(insight, category)
            })
            insight_counter += 1
    
    # Add cross-category insights
    for cross_insight in insights.get('cross_category_insights', []):
        all_insights.append({
            'insight_id': f'INS-{insight_counter:03d}',
            'category': 'CROSS_CATEGORY',
            'insight_text': cross_insight.get('insight_text', ''),
            'supporting_signals_count': len(cross_insight.get('supporting_signals', [])),
            'confidence': cross_insight.get('confidence_level', 'unknown'),
            'recommended_action': cross_insight.get('recommended_action', ''),
            'urgency_level': _determine_urgency(cross_insight, 'CROSS_CATEGORY')
        })
        insight_counter += 1
    
    # Sort by urgency (high -> medium -> low)
    urgency_order = {'high': 0, 'medium': 1, 'low': 2}
    sorted_insights = sorted(
        all_insights,
        key=lambda x: (urgency_order.get(x['urgency_level'], 3), x['confidence'] != 'high')
    )
    
    # Define CSV columns
    columns = [
        'insight_id',
        'category',
        'insight_text',
        'supporting_signals_count',
        'confidence',
        'recommended_action',
        'urgency_level'
    ]
    
    # Calculate summary
    total_insights = len(sorted_insights)
    high_urgency = sum(1 for i in sorted_insights if i['urgency_level'] == 'high')
    high_confidence = sum(1 for i in sorted_insights if i['confidence'] == 'high')
    
    # Write CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        
        # Write summary rows
        writer.writerow({
            'insight_id': '# GTM INSIGHTS EXPORT',
            'category': f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            'insight_text': '',
            'supporting_signals_count': '',
            'confidence': '',
            'recommended_action': '',
            'urgency_level': ''
        })
        
        writer.writerow({
            'insight_id': f'# Total Insights: {total_insights}',
            'category': f'High Urgency: {high_urgency}',
            'insight_text': f'High Confidence: {high_confidence}',
            'supporting_signals_count': '',
            'confidence': '',
            'recommended_action': '',
            'urgency_level': ''
        })
        
        # Blank row separator
        writer.writerow({col: '' for col in columns})
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        for insight in sorted_insights:
            # Validate data
            validated_insight = _validate_insight_row(insight, columns)
            writer.writerow(validated_insight)
    
    logger.info(f"Successfully exported {len(sorted_insights)} insights to {output_path}")
    return output_path


def export_to_json(signals: List[Dict[str, Any]], insights: Dict[str, Any], 
                   executive_summary: str = None, output_path: str = None) -> str:
    """
    Export complete GTM analysis to JSON format
    
    Args:
        signals: List of classified signals
        insights: Generated insights dictionary
        executive_summary: Optional executive summary text
        output_path: Optional custom output path. Defaults to data/gtm_analysis_full.json
        
    Returns:
        Path to created JSON file
    """
    
    if output_path is None:
        output_path = 'data/gtm_analysis_full.json'
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    logger.info(f"Exporting complete analysis to JSON: {output_path}")
    
    # Build comprehensive analysis structure
    analysis = {
        'metadata': {
            'export_date': datetime.now().isoformat(),
            'export_version': '1.0.0',
            'platform': 'GTM Intelligence Platform',
            'total_signals': len(signals),
            'total_insights': insights.get('executive_summary', {}).get('total_insights_generated', 0)
        },
        'summary': {
            'date_range': _calculate_date_range(signals),
            'signal_breakdown': _calculate_signal_summary(signals),
            'insight_breakdown': _calculate_insight_summary(insights),
            'strategic_summary': insights.get('executive_summary', {}).get('strategic_summary', '')
        },
        'signals': {
            'total': len(signals),
            'data': signals,
            'by_category': _group_signals_by_category(signals),
            'by_source': _group_signals_by_source(signals),
            'by_confidence': _group_signals_by_confidence(signals)
        },
        'insights': {
            'total': insights.get('executive_summary', {}).get('total_insights_generated', 0),
            'by_category': insights.get('insights_by_category', {}),
            'cross_category': insights.get('cross_category_insights', []),
            'executive_summary': insights.get('executive_summary', {})
        },
        'recommendations': {
            'key_recommendations': insights.get('executive_summary', {}).get('key_recommendations', []),
            'high_confidence_insights': insights.get('executive_summary', {}).get('high_confidence_insights', []),
            'priority_actions': _extract_priority_actions(insights)
        }
    }
    
    # Add executive summary if provided
    if executive_summary:
        analysis['executive_summary_report'] = {
            'text': executive_summary,
            'word_count': len(executive_summary.split()),
            'generated_date': datetime.now().isoformat()
        }
    
    # Write JSON with proper formatting
    with open(output_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(analysis, jsonfile, indent=2, ensure_ascii=False)
    
    logger.info(f"Successfully exported complete analysis to {output_path}")
    return output_path


def export_all_formats(signals: List[Dict[str, Any]], insights: Dict[str, Any], 
                       executive_summary: str = None, output_dir: str = 'data') -> Dict[str, str]:
    """
    Export all formats at once
    
    Args:
        signals: List of classified signals
        insights: Generated insights dictionary
        executive_summary: Optional executive summary text
        output_dir: Directory for output files
        
    Returns:
        Dictionary with paths to all created files
    """
    
    logger.info(f"Exporting all formats to directory: {output_dir}")
    
    paths = {
        'signals_csv': export_signals_to_csv(signals, f'{output_dir}/gtm_signals.csv'),
        'insights_csv': export_insights_to_csv(insights, f'{output_dir}/gtm_insights.csv'),
        'full_json': export_to_json(signals, insights, executive_summary, f'{output_dir}/gtm_analysis_full.json')
    }
    
    logger.info(f"Successfully exported all formats: {', '.join(paths.keys())}")
    return paths


# Helper Functions

def _calculate_date_range(signals: List[Dict[str, Any]]) -> Dict[str, str]:
    """Calculate date range from signals"""
    
    dates = [s.get('date_detected', '') for s in signals if s.get('date_detected')]
    
    if dates:
        dates.sort()
        return {'start': dates[0], 'end': dates[-1]}
    else:
        return {'start': 'N/A', 'end': 'N/A'}


def _calculate_signal_summary(signals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate signal summary statistics"""
    
    from collections import defaultdict
    
    summary = {
        'total': len(signals),
        'high_confidence': sum(1 for s in signals if s.get('confidence_level') == 'high'),
        'categories': list(set(s.get('primary_category', 'UNKNOWN') for s in signals)),
        'sources': defaultdict(int),
        'signal_types': defaultdict(int)
    }
    
    for signal in signals:
        source = signal.get('source', 'Unknown')
        signal_type = signal.get('signal_type', 'unknown')
        summary['sources'][source] += 1
        summary['signal_types'][signal_type] += 1
    
    summary['sources'] = dict(summary['sources'])
    summary['signal_types'] = dict(summary['signal_types'])
    
    return summary


def _calculate_insight_summary(insights: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate insight summary statistics"""
    
    summary = {
        'total': insights.get('executive_summary', {}).get('total_insights_generated', 0),
        'categories': insights.get('executive_summary', {}).get('categories_covered', []),
        'high_confidence': len(insights.get('executive_summary', {}).get('high_confidence_insights', [])),
        'cross_category': len(insights.get('cross_category_insights', []))
    }
    
    return summary


def _prepare_signal_row(signal: Dict[str, Any], columns: List[str]) -> Dict[str, str]:
    """Prepare and validate signal row for CSV export"""
    
    row = {}
    
    for col in columns:
        if col == 'signal_id':
            row[col] = signal.get('signal_id', 'N/A')
        elif col == 'headline':
            row[col] = signal.get('headline', 'N/A')
        elif col == 'description':
            # Truncate long descriptions and clean newlines
            desc = signal.get('description', 'N/A')
            desc = desc.replace('\n', ' ').replace('\r', ' ')
            row[col] = desc[:500] + '...' if len(desc) > 500 else desc
        elif col == 'signal_type':
            row[col] = signal.get('signal_type', 'unknown')
        elif col == 'gtm_category':
            row[col] = signal.get('primary_category', 'UNKNOWN')
        elif col == 'date':
            row[col] = signal.get('date_detected', 'N/A')
        elif col == 'source':
            row[col] = signal.get('source', 'Unknown')
        elif col == 'source_url':
            row[col] = signal.get('source_url', 'N/A')
        elif col == 'confidence':
            row[col] = signal.get('confidence_level', 'unknown')
        elif col == 'strategic_implication':
            # Extract from raw_json if available
            raw = signal.get('raw_json', {})
            implication = raw.get('strategic_implication', '')
            if not implication:
                # Generate from GTM insights if available
                implication = signal.get('gtm_insights', '')
            # Clean and truncate
            implication = implication.replace('\n', ' ').replace('\r', ' ')
            row[col] = implication[:300] + '...' if len(implication) > 300 else implication
        else:
            row[col] = 'N/A'
    
    # Validate no nulls in critical fields
    critical_fields = ['signal_id', 'headline', 'date', 'gtm_category']
    for field in critical_fields:
        if not row.get(field) or row[field] == '':
            row[field] = 'N/A'
    
    return row


def _validate_insight_row(insight: Dict[str, Any], columns: List[str]) -> Dict[str, str]:
    """Validate insight row for CSV export"""
    
    validated = {}
    
    for col in columns:
        value = insight.get(col, '')
        
        # Clean newlines and carriage returns
        if isinstance(value, str):
            value = value.replace('\n', ' ').replace('\r', ' ')
        
        # Truncate long text fields
        if col in ['insight_text', 'recommended_action']:
            if len(str(value)) > 500:
                value = str(value)[:500] + '...'
        
        # Ensure no nulls
        if not value or value == '':
            value = 'N/A' if col != 'supporting_signals_count' else '0'
        
        validated[col] = str(value)
    
    return validated


def _determine_urgency(insight: Dict[str, Any], category: str) -> str:
    """Determine urgency level based on confidence and category"""
    
    confidence = insight.get('confidence_level', 'low')
    insight_text = insight.get('insight_text', '').lower()
    action = insight.get('recommended_action', '').lower()
    
    # High urgency criteria
    if confidence == 'high' and category in ['COMPETITIVE', 'TIMING']:
        return 'high'
    
    if any(word in insight_text for word in ['urgent', 'immediate', 'critical', 'aggressive']):
        return 'high'
    
    if any(word in action for word in ['immediate', 'urgent', 'critical', 'now']):
        return 'high'
    
    # Medium urgency
    if confidence == 'high' or category in ['PRODUCT', 'TALENT']:
        return 'medium'
    
    if any(word in insight_text for word in ['upcoming', 'soon', 'launch', 'expansion']):
        return 'medium'
    
    # Low urgency
    return 'low'


def _group_signals_by_category(signals: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group signals by primary category"""
    
    from collections import defaultdict
    grouped = defaultdict(list)
    
    for signal in signals:
        category = signal.get('primary_category', 'UNKNOWN')
        grouped[category].append(signal)
    
    return dict(grouped)


def _group_signals_by_source(signals: List[Dict[str, Any]]) -> Dict[str, int]:
    """Count signals by source"""
    
    from collections import defaultdict
    counts = defaultdict(int)
    
    for signal in signals:
        source = signal.get('source', 'Unknown')
        counts[source] += 1
    
    return dict(counts)


def _group_signals_by_confidence(signals: List[Dict[str, Any]]) -> Dict[str, int]:
    """Count signals by confidence level"""
    
    from collections import defaultdict
    counts = defaultdict(int)
    
    for signal in signals:
        confidence = signal.get('confidence_level', 'unknown')
        counts[confidence] += 1
    
    return dict(counts)


def _extract_priority_actions(insights: Dict[str, Any]) -> List[Dict[str, str]]:
    """Extract priority actions from insights"""
    
    actions = []
    
    for category, cat_data in insights.get('insights_by_category', {}).items():
        for insight in cat_data.get('insights', []):
            if insight.get('confidence_level') == 'high':
                actions.append({
                    'category': category,
                    'action': insight.get('recommended_action', ''),
                    'urgency': _determine_urgency(insight, category),
                    'confidence': 'high'
                })
    
    # Sort by urgency
    urgency_order = {'high': 0, 'medium': 1, 'low': 2}
    actions.sort(key=lambda x: urgency_order.get(x['urgency'], 3))
    
    return actions[:10]  # Top 10 priority actions
