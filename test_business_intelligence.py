"""
Test script for Stripe Business Intelligence Module
Demonstrates data collection and structure
"""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_sources.stripe_business_intelligence import (
    StripeBusinessIntelligence,
    collect_stripe_intelligence,
    get_example_data_structure
)


def test_example_structure():
    """Test 1: Show example data structure"""
    print("\n" + "="*80)
    print("TEST 1: Example Data Structure")
    print("="*80)
    
    example = get_example_data_structure()
    print(json.dumps(example, indent=2))
    print("\nData structure includes:")
    print("- signal_type: Type of intelligence (hiring, funding, partnership, etc.)")
    print("- description: Human-readable summary")
    print("- date: When the signal occurred (YYYY-MM-DD)")
    print("- source: Where the data came from (Crunchbase, LinkedIn, etc.)")
    print("- source_url: URL to verify the information")
    print("- confidence_level: high/medium/low based on source credibility")
    print("- metadata: Additional structured data specific to signal type")


def test_crunchbase_collection():
    """Test 2: Collect Crunchbase data"""
    print("\n" + "="*80)
    print("TEST 2: Crunchbase Data Collection")
    print("="*80)
    
    collector = StripeBusinessIntelligence()
    signals = collector.get_crunchbase_data()
    
    print(f"\nCollected {len(signals)} Crunchbase signals\n")
    
    # Show first 3 signals
    for i, signal in enumerate(signals[:3], 1):
        print(f"\nSignal {i}:")
        print(f"  Type: {signal['signal_type']}")
        print(f"  Date: {signal['date']}")
        print(f"  Description: {signal['description'][:100]}...")
        print(f"  Confidence: {signal['confidence_level']}")
        if 'metadata' in signal:
            print(f"  Metadata keys: {list(signal['metadata'].keys())}")


def test_linkedin_collection():
    """Test 3: Collect LinkedIn data"""
    print("\n" + "="*80)
    print("TEST 3: LinkedIn Data Collection")
    print("="*80)
    
    collector = StripeBusinessIntelligence()
    signals = collector.get_linkedin_insights()
    
    print(f"\nCollected {len(signals)} LinkedIn signals\n")
    
    # Show first 3 signals
    for i, signal in enumerate(signals[:3], 1):
        print(f"\nSignal {i}:")
        print(f"  Type: {signal['signal_type']}")
        print(f"  Date: {signal['date']}")
        print(f"  Description: {signal['description'][:100]}...")
        print(f"  Confidence: {signal['confidence_level']}")
        if 'metadata' in signal:
            print(f"  Metadata keys: {list(signal['metadata'].keys())}")


def test_full_collection():
    """Test 4: Collect all intelligence"""
    print("\n" + "="*80)
    print("TEST 4: Full Intelligence Collection")
    print("="*80)
    
    intelligence = collect_stripe_intelligence()
    
    print("\nCollection Summary:")
    summary = intelligence.get('summary', {})
    print(f"  Total signals: {summary.get('total_signals', 0)}")
    
    print("\n  By signal type:")
    for signal_type, count in sorted(summary.get('by_type', {}).items()):
        print(f"    - {signal_type}: {count}")
    
    print("\n  By confidence level:")
    for confidence, count in sorted(summary.get('by_confidence', {}).items()):
        print(f"    - {confidence}: {count}")
    
    print("\n  By source:")
    for source, count in sorted(summary.get('by_source', {}).items()):
        print(f"    - {source}: {count}")
    
    date_range = summary.get('date_range', {})
    print(f"\n  Date range: {date_range.get('earliest')} to {date_range.get('latest')}")


def test_filtered_queries():
    """Test 5: Filtered data queries"""
    print("\n" + "="*80)
    print("TEST 5: Filtered Data Queries")
    print("="*80)
    
    collector = StripeBusinessIntelligence()
    
    # Get hiring signals
    print("\nFetching hiring signals...")
    hiring_signals = collector.get_signals_by_type('hiring')
    print(f"Found {len(hiring_signals)} hiring signals")
    
    if hiring_signals:
        print("\nExample hiring signal:")
        signal = hiring_signals[0]
        print(f"  {signal['description']}")
        if 'metadata' in signal:
            print(f"  Details: {json.dumps(signal['metadata'], indent=4)}")
    
    # Get recent signals (last 90 days)
    print("\n\nFetching recent signals (last 90 days)...")
    recent = collector.get_recent_signals(days=90)
    print(f"Found {len(recent)} recent signals")
    
    # Get high confidence signals
    print("\n\nFetching high-confidence signals...")
    high_conf = collector.get_high_confidence_signals()
    print(f"Found {len(high_conf)} high-confidence signals")


def test_data_structure_detail():
    """Test 6: Show detailed data structure for each signal type"""
    print("\n" + "="*80)
    print("TEST 6: Signal Type Examples")
    print("="*80)
    
    intelligence = collect_stripe_intelligence()
    by_type = intelligence.get('by_signal_type', {})
    
    # Show one example of each signal type
    signal_types_shown = set()
    
    for signal_type, signals in by_type.items():
        if signal_type not in signal_types_shown and signals:
            print(f"\n{signal_type.upper()} Signal Example:")
            print("-" * 60)
            signal = signals[0]
            print(json.dumps(signal, indent=2))
            signal_types_shown.add(signal_type)


def run_all_tests():
    """Run all tests"""
    print("\n")
    print("="*80)
    print(" STRIPE BUSINESS INTELLIGENCE MODULE - TEST SUITE")
    print("="*80)
    
    tests = [
        test_example_structure,
        test_crunchbase_collection,
        test_linkedin_collection,
        test_full_collection,
        test_filtered_queries,
        test_data_structure_detail
    ]
    
    for test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"\nError in {test_func.__name__}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print(" ALL TESTS COMPLETE")
    print("="*80)
    print("\nData file saved to: outputs/raw_data/stripe_business_intelligence.json")
    print("You can review the complete dataset in JSON format.")
    print("="*80 + "\n")


if __name__ == "__main__":
    run_all_tests()
