"""
Market Signals Aggregator
Combines signals from all data sources into a unified format
"""

import os
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Set
import logging
from difflib import SequenceMatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MarketSignalsAggregator:
    """Aggregates and standardizes signals from all data sources"""
    
    def __init__(self):
        """Initialize the aggregator"""
        self.signal_id_counter = 1000
        self.seen_signals: Set[str] = set()
        
    def aggregate_market_signals(
        self,
        max_signals: int = 15,
        min_confidence: str = 'medium',
        days_lookback: int = 90
    ) -> List[Dict]:
        """
        Aggregate signals from all data sources into unified format
        
        Args:
            max_signals: Maximum number of signals to return
            min_confidence: Minimum confidence level (low/medium/high)
            days_lookback: Only include signals from last N days
            
        Returns:
            List of standardized, deduplicated signals sorted by date
        """
        logger.info("="*80)
        logger.info("Starting market signals aggregation")
        logger.info("="*80)
        
        all_signals = []
        
        # 1. Load data from all sources
        logger.info("\n1. Loading data from all sources...")
        
        news_signals = self._load_news_signals()
        logger.info(f"   Loaded {len(news_signals)} news signals")
        all_signals.extend(news_signals)
        
        business_signals = self._load_business_intelligence()
        logger.info(f"   Loaded {len(business_signals)} business intelligence signals")
        all_signals.extend(business_signals)
        
        technical_signals = self._load_technical_signals()
        logger.info(f"   Loaded {len(technical_signals)} technical signals")
        all_signals.extend(technical_signals)
        
        logger.info(f"\n   Total raw signals loaded: {len(all_signals)}")
        
        # 2. Standardize all signals into unified format
        logger.info("\n2. Standardizing signals into unified format...")
        standardized_signals = []
        for signal in all_signals:
            try:
                standardized = self._standardize_signal(signal)
                if standardized:
                    standardized_signals.append(standardized)
            except Exception as e:
                logger.warning(f"   Failed to standardize signal: {e}")
        
        logger.info(f"   Standardized {len(standardized_signals)} signals")
        
        # 3. Remove duplicates
        logger.info("\n3. Removing duplicate signals...")
        unique_signals = self._remove_duplicates(standardized_signals)
        logger.info(f"   Removed {len(standardized_signals) - len(unique_signals)} duplicates")
        logger.info(f"   Unique signals: {len(unique_signals)}")
        
        # 4. Filter by confidence level
        logger.info(f"\n4. Filtering by confidence level (>= {min_confidence})...")
        confidence_levels = {'low': 1, 'medium': 2, 'high': 3}
        min_level = confidence_levels.get(min_confidence, 2)
        
        filtered_signals = [
            s for s in unique_signals
            if confidence_levels.get(s.get('confidence_level', 'low'), 0) >= min_level
        ]
        logger.info(f"   Retained {len(filtered_signals)} signals after confidence filter")
        
        # 5. Filter by date
        logger.info(f"\n5. Filtering by date (last {days_lookback} days)...")
        cutoff_date = self._get_cutoff_date(days_lookback)
        recent_signals = [
            s for s in filtered_signals
            if s.get('date_detected', '0000-00-00') >= cutoff_date
        ]
        logger.info(f"   Retained {len(recent_signals)} recent signals")
        
        # 6. Sort by date (most recent first) and confidence
        logger.info("\n6. Sorting by date and confidence...")
        sorted_signals = sorted(
            recent_signals,
            key=lambda x: (
                x.get('date_detected', '0000-00-00'),
                confidence_levels.get(x.get('confidence_level', 'low'), 0)
            ),
            reverse=True
        )
        
        # 7. Return top N signals
        final_signals = sorted_signals[:max_signals]
        
        logger.info("\n" + "="*80)
        logger.info(f"Aggregation complete!")
        logger.info(f"Returning {len(final_signals)} high-value signals")
        logger.info("="*80 + "\n")
        
        return final_signals
    
    def _load_news_signals(self) -> List[Dict]:
        """Load signals from news collector"""
        try:
            filepath = 'outputs/raw_data/stripe_news_collection.json'
            if not os.path.exists(filepath):
                # Try alternative location
                filepath = 'outputs/raw_data/test_stripe_news_collection.json'
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Handle different data structures
                    if isinstance(data, dict):
                        # Combine all news types
                        signals = []
                        signals.extend(data.get('api_news', []))
                        signals.extend(data.get('company_announcements', []))
                        signals.extend(data.get('industry_news', []))
                        return signals
                    elif isinstance(data, list):
                        return data
            
            logger.warning("News data file not found, using empty list")
            return []
        
        except Exception as e:
            logger.warning(f"Failed to load news signals: {e}")
            return []
    
    def _load_business_intelligence(self) -> List[Dict]:
        """Load signals from business intelligence collector"""
        try:
            filepath = 'outputs/raw_data/stripe_business_intelligence.json'
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Get all signals from business intelligence
                    if isinstance(data, dict):
                        signals = data.get('all_signals', [])
                        if not signals:
                            # Try alternative structure
                            signals = []
                            signals.extend(data.get('crunchbase_signals', []))
                            signals.extend(data.get('linkedin_signals', []))
                        return signals
                    elif isinstance(data, list):
                        return data
            
            logger.warning("Business intelligence data file not found, using empty list")
            return []
        
        except Exception as e:
            logger.warning(f"Failed to load business intelligence: {e}")
            return []
    
    def _load_technical_signals(self) -> List[Dict]:
        """Load signals from technical signals collector"""
        try:
            filepath = 'outputs/raw_data/stripe_technical_signals.json'
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Get all technical signals
                    if isinstance(data, dict):
                        signals = data.get('all_signals', [])
                        if not signals:
                            # Try alternative structure
                            signals = []
                            signals.extend(data.get('github_signals', []))
                            signals.extend(data.get('api_signals', []))
                        return signals
                    elif isinstance(data, list):
                        return data
            
            logger.warning("Technical signals data file not found, using empty list")
            return []
        
        except Exception as e:
            logger.warning(f"Failed to load technical signals: {e}")
            return []
    
    def _standardize_signal(self, raw_signal: Dict) -> Optional[Dict]:
        """
        Convert raw signal to standardized format
        
        Standardized format:
        {
            'signal_id': str,
            'signal_type': str,
            'headline': str,
            'description': str,
            'date_detected': str (YYYY-MM-DD),
            'source': str,
            'source_url': str,
            'confidence_level': str,
            'raw_json': dict
        }
        """
        # Determine source type
        source = self._determine_source(raw_signal)
        
        # Extract common fields
        signal_type = raw_signal.get('signal_type', 'unknown')
        date_detected = raw_signal.get('date', raw_signal.get('publishedAt', ''))
        
        # Parse date if needed
        if 'T' in date_detected:
            date_detected = date_detected.split('T')[0]
        
        # Generate headline and description based on source
        headline, description = self._generate_headline_description(raw_signal, source)
        
        # Get confidence level
        confidence = self._determine_confidence(raw_signal, source)
        
        # Get source URL
        source_url = raw_signal.get('source_url', raw_signal.get('url', ''))
        
        # Generate unique signal ID
        signal_id = self._generate_signal_id(headline, date_detected, source)
        
        standardized = {
            'signal_id': signal_id,
            'signal_type': signal_type,
            'headline': headline,
            'description': description,
            'date_detected': date_detected,
            'source': source,
            'source_url': source_url,
            'confidence_level': confidence,
            'raw_json': raw_signal
        }
        
        return standardized
    
    def _determine_source(self, signal: Dict) -> str:
        """Determine the source of a signal"""
        # Check for explicit source field
        if 'source' in signal:
            source = signal['source']
            if 'GitHub' in source:
                return 'GitHub'
            elif 'Crunchbase' in source:
                return 'Crunchbase'
            elif 'LinkedIn' in source:
                return 'LinkedIn'
            elif 'NewsAPI' in source or 'News' in source:
                return 'News'
            elif 'Stripe' in source:
                return 'Stripe Official'
        
        # Check for signal characteristics
        if 'repository' in signal.get('metadata', {}):
            return 'GitHub'
        
        if 'api_name' in signal.get('metadata', {}):
            return 'Stripe API Changelog'
        
        if 'funding_round' in signal.get('metadata', {}):
            return 'Crunchbase'
        
        if 'total_openings' in signal.get('metadata', {}) or 'department' in signal.get('metadata', {}):
            return 'LinkedIn'
        
        if 'title' in signal and 'url' in signal:
            return 'News'
        
        return 'Unknown'
    
    def _generate_headline_description(self, signal: Dict, source: str) -> tuple:
        """Generate headline and description for signal"""
        
        # For news articles
        if source == 'News':
            headline = signal.get('title', '')[:100]
            description = signal.get('description', signal.get('content', ''))[:500]
            return headline, description
        
        # For business intelligence signals
        if source in ['Crunchbase', 'LinkedIn']:
            headline = signal.get('description', '')[:100]
            description = signal.get('description', '')
            
            # Add metadata context
            metadata = signal.get('metadata', {})
            if metadata:
                if 'amount_raised' in metadata:
                    description += f"\nAmount: {metadata['amount_raised']}"
                if 'valuation' in metadata:
                    description += f"\nValuation: {metadata['valuation']}"
                if 'total_openings' in metadata:
                    description += f"\nOpen positions: {metadata['total_openings']}"
            
            return headline, description
        
        # For technical signals
        if source in ['GitHub', 'Stripe API Changelog']:
            headline = signal.get('technical_detail', '')[:100]
            description = signal.get('technical_detail', '')
            
            # Add strategic implication
            if 'strategic_implication' in signal:
                description += f"\n\nStrategic Implication: {signal['strategic_implication']}"
            
            # Add metadata context
            metadata = signal.get('metadata', {})
            if metadata:
                if 'version' in metadata:
                    description += f"\nVersion: {metadata['version']}"
                if 'api_name' in metadata:
                    description += f"\nAPI: {metadata['api_name']}"
            
            return headline, description
        
        # Fallback
        headline = signal.get('description', signal.get('title', 'Signal'))[:100]
        description = signal.get('description', signal.get('technical_detail', ''))
        return headline, description
    
    def _determine_confidence(self, signal: Dict, source: str) -> str:
        """Determine confidence level of signal"""
        
        # Check explicit confidence field
        if 'confidence_level' in signal:
            return signal['confidence_level']
        
        # Source-based confidence
        if source in ['Crunchbase', 'Stripe Official', 'Stripe API Changelog']:
            return 'high'
        
        if source == 'GitHub':
            # High confidence for official GitHub data
            return 'high'
        
        if source == 'LinkedIn':
            # LinkedIn data is generally reliable
            return 'high'
        
        if source == 'News':
            # News requires source validation
            source_name = signal.get('source', {})
            if isinstance(source_name, dict):
                source_name = source_name.get('name', '')
            
            # Tier 1 news sources
            tier1 = ['TechCrunch', 'Bloomberg', 'Reuters', 'Wall Street Journal', 'Financial Times']
            if any(t in str(source_name) for t in tier1):
                return 'high'
            
            return 'medium'
        
        return 'medium'
    
    def _generate_signal_id(self, headline: str, date: str, source: str) -> str:
        """Generate unique signal ID based on content"""
        # Create hash of key fields
        content = f"{headline}|{date}|{source}".encode('utf-8')
        hash_obj = hashlib.md5(content)
        hash_hex = hash_obj.hexdigest()[:8]
        
        # Format: SIG-YYYYMMDD-HASH
        date_str = date.replace('-', '')
        return f"SIG-{date_str}-{hash_hex.upper()}"
    
    def _remove_duplicates(self, signals: List[Dict]) -> List[Dict]:
        """
        Remove duplicate signals using intelligent matching
        
        Signals are considered duplicates if:
        1. Same signal_id (exact match)
        2. Similar headline + same date (fuzzy match)
        3. Same source_url
        """
        unique_signals = []
        seen_ids = set()
        seen_urls = set()
        seen_content = []
        
        for signal in signals:
            signal_id = signal.get('signal_id', '')
            source_url = signal.get('source_url', '')
            headline = signal.get('headline', '')
            date = signal.get('date_detected', '')
            
            # Check exact ID match
            if signal_id in seen_ids:
                logger.debug(f"Duplicate ID: {signal_id}")
                continue
            
            # Check URL match
            if source_url and source_url in seen_urls:
                logger.debug(f"Duplicate URL: {source_url}")
                continue
            
            # Check fuzzy headline match on same date
            is_duplicate = False
            for seen_headline, seen_date in seen_content:
                if date == seen_date:
                    similarity = self._calculate_similarity(headline, seen_headline)
                    if similarity > 0.85:  # 85% similarity threshold
                        logger.debug(f"Duplicate content (similarity: {similarity:.2f}): {headline[:50]}")
                        is_duplicate = True
                        break
            
            if is_duplicate:
                continue
            
            # Add to unique signals
            unique_signals.append(signal)
            seen_ids.add(signal_id)
            if source_url:
                seen_urls.add(source_url)
            seen_content.append((headline, date))
        
        return unique_signals
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings (0.0 to 1.0)"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def _get_cutoff_date(self, days_lookback: int) -> str:
        """Get cutoff date for filtering"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days_lookback)
        return cutoff.strftime('%Y-%m-%d')
    
    def handle_conflicting_information(
        self,
        signals: List[Dict],
        conflict_field: str = 'description'
    ) -> List[Dict]:
        """
        Handle conflicting information from multiple sources
        
        Strategy:
        1. Group signals by topic (same event)
        2. For conflicts, prefer higher confidence sources
        3. Merge complementary information
        4. Flag unresolved conflicts
        """
        logger.info("Analyzing signals for conflicts...")
        
        # Group signals by similarity
        signal_groups = self._group_similar_signals(signals)
        
        resolved_signals = []
        
        for group in signal_groups:
            if len(group) == 1:
                # No conflict
                resolved_signals.append(group[0])
            else:
                # Multiple signals about same topic - resolve conflict
                resolved = self._resolve_conflict(group)
                resolved_signals.append(resolved)
        
        return resolved_signals
    
    def _group_similar_signals(self, signals: List[Dict]) -> List[List[Dict]]:
        """Group signals that appear to be about the same event"""
        groups = []
        ungrouped = signals.copy()
        
        while ungrouped:
            current = ungrouped.pop(0)
            group = [current]
            
            # Find similar signals
            remaining = []
            for signal in ungrouped:
                if self._are_signals_related(current, signal):
                    group.append(signal)
                else:
                    remaining.append(signal)
            
            ungrouped = remaining
            groups.append(group)
        
        return groups
    
    def _are_signals_related(self, sig1: Dict, sig2: Dict) -> bool:
        """Determine if two signals are about the same event"""
        # Same date and similar headline
        if sig1.get('date_detected') == sig2.get('date_detected'):
            similarity = self._calculate_similarity(
                sig1.get('headline', ''),
                sig2.get('headline', '')
            )
            if similarity > 0.7:
                return True
        
        # Same source URL
        if sig1.get('source_url') and sig1.get('source_url') == sig2.get('source_url'):
            return True
        
        return False
    
    def _resolve_conflict(self, signal_group: List[Dict]) -> Dict:
        """
        Resolve conflict between multiple signals about same event
        
        Resolution strategy:
        1. Prefer highest confidence source
        2. Use most detailed description
        3. Combine unique information
        4. Add conflict flag if unresolvable
        """
        # Sort by confidence
        confidence_order = {'high': 3, 'medium': 2, 'low': 1}
        sorted_signals = sorted(
            signal_group,
            key=lambda x: confidence_order.get(x.get('confidence_level', 'low'), 0),
            reverse=True
        )
        
        # Start with highest confidence signal
        primary = sorted_signals[0].copy()
        
        # Merge information from other sources
        all_sources = [s.get('source', '') for s in signal_group]
        primary['sources'] = list(set(all_sources))
        
        # Use longest description (most detailed)
        descriptions = [s.get('description', '') for s in signal_group]
        primary['description'] = max(descriptions, key=len)
        
        # Flag if there are significant conflicts
        if len(signal_group) > 2:
            primary['note'] = f"Information aggregated from {len(signal_group)} sources: {', '.join(all_sources)}"
        
        return primary
    
    def generate_summary_report(self, signals: List[Dict]) -> Dict:
        """Generate summary report of aggregated signals"""
        
        # Count by type
        by_type = {}
        for signal in signals:
            sig_type = signal.get('signal_type', 'unknown')
            by_type[sig_type] = by_type.get(sig_type, 0) + 1
        
        # Count by source
        by_source = {}
        for signal in signals:
            source = signal.get('source', 'unknown')
            by_source[source] = by_source.get(source, 0) + 1
        
        # Count by confidence
        by_confidence = {}
        for signal in signals:
            conf = signal.get('confidence_level', 'unknown')
            by_confidence[conf] = by_confidence.get(conf, 0) + 1
        
        # Date range
        dates = [s.get('date_detected', '') for s in signals if s.get('date_detected')]
        date_range = {
            'earliest': min(dates) if dates else None,
            'latest': max(dates) if dates else None
        }
        
        return {
            'total_signals': len(signals),
            'by_type': by_type,
            'by_source': by_source,
            'by_confidence': by_confidence,
            'date_range': date_range
        }
    
    def save_aggregated_signals(
        self,
        signals: List[Dict],
        filename: str = 'aggregated_market_signals.json'
    ):
        """Save aggregated signals to file"""
        output_dir = 'outputs/aggregated'
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        # Generate summary
        summary = self.generate_summary_report(signals)
        
        output_data = {
            'metadata': {
                'aggregation_date': datetime.now().isoformat(),
                'total_signals': len(signals),
                'summary': summary
            },
            'signals': signals
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Aggregated signals saved to {filepath}")
        return filepath


# Convenience function
def aggregate_market_signals(
    max_signals: int = 15,
    min_confidence: str = 'medium',
    days_lookback: int = 90
) -> List[Dict]:
    """
    Convenience function to aggregate market signals
    
    Args:
        max_signals: Maximum number of signals to return (default: 15)
        min_confidence: Minimum confidence level - 'low', 'medium', or 'high' (default: 'medium')
        days_lookback: Only include signals from last N days (default: 90)
        
    Returns:
        List of standardized, deduplicated, high-value signals
    """
    aggregator = MarketSignalsAggregator()
    return aggregator.aggregate_market_signals(
        max_signals=max_signals,
        min_confidence=min_confidence,
        days_lookback=days_lookback
    )


if __name__ == "__main__":
    # Example usage
    print("Market Signals Aggregator")
    print("="*80)
    
    # Aggregate signals
    aggregator = MarketSignalsAggregator()
    signals = aggregator.aggregate_market_signals(max_signals=15, min_confidence='medium')
    
    # Display results
    print(f"\nAggregated {len(signals)} high-value market signals:\n")
    
    for i, signal in enumerate(signals, 1):
        print(f"{i}. [{signal['date_detected']}] {signal['signal_type'].upper()}")
        print(f"   Source: {signal['source']} | Confidence: {signal['confidence_level']}")
        print(f"   {signal['headline'][:80]}...")
        print()
    
    # Generate and display summary
    summary = aggregator.generate_summary_report(signals)
    print("\n" + "="*80)
    print("SUMMARY REPORT")
    print("="*80)
    print(f"\nTotal Signals: {summary['total_signals']}")
    print(f"\nBy Type:")
    for sig_type, count in sorted(summary['by_type'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {sig_type}: {count}")
    print(f"\nBy Source:")
    for source, count in sorted(summary['by_source'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {source}: {count}")
    print(f"\nBy Confidence:")
    for conf, count in sorted(summary['by_confidence'].items()):
        print(f"  - {conf}: {count}")
    
    # Save to file
    filepath = aggregator.save_aggregated_signals(signals)
    print(f"\nSaved to: {filepath}")
    print("="*80)
