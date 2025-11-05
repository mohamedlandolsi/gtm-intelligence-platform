"""
GTM Intelligence Platform - Main Orchestration Script

This script orchestrates the complete GTM intelligence pipeline:
1. Data collection from multiple sources (news, LinkedIn, GitHub, Crunchbase)
2. Signal aggregation and deduplication
3. GTM classification across 7 dimensions
4. Insight generation and executive summary
5. Export to CSV, JSON, and Markdown formats

Usage:
    python main_gtm.py

Requirements:
    - All data collector modules configured
    - Output directories will be created automatically
    - Expected execution time: 30-60 seconds
"""

import sys
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gtm_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import all pipeline modules
try:
    from collectors.news_collector import collect_news_signals
    from collectors.crunchbase_linkedin_collector import collect_business_intelligence
    from collectors.github_signals_collector import collect_github_signals
    from processing.signal_aggregator import aggregate_market_signals
    from processing.gtm_classifier import classify_gtm_signals
    from processing.gtm_insights_generator import generate_gtm_insights, generate_executive_summary
    from processing.export_utils import export_all_formats
    from processing.markdown_report_generator import create_gtm_report
    
    MODULES_LOADED = True
    logger.info("Successfully imported all pipeline modules")
except ImportError as e:
    logger.error(f"Failed to import modules: {e}")
    MODULES_LOADED = False


class GTMPipeline:
    """Orchestrates the complete GTM intelligence pipeline."""
    
    def __init__(self, company_name: str = "Stripe"):
        """
        Initialize the GTM pipeline.
        
        Args:
            company_name: Target company for intelligence gathering
        """
        self.company_name = company_name
        self.start_time = time.time()
        self.stats = {
            'news_signals': 0,
            'linkedin_signals': 0,
            'crunchbase_signals': 0,
            'github_signals': 0,
            'total_raw_signals': 0,
            'aggregated_signals': 0,
            'classified_signals': 0,
            'insights_generated': 0,
            'execution_time': 0
        }
        self.errors = []
        
        # Define output paths
        self.output_paths = {
            'news': project_root / 'outputs' / 'news' / 'news_signals.json',
            'business_intel': project_root / 'outputs' / 'business_intel' / 'business_signals.json',
            'github': project_root / 'outputs' / 'github' / 'github_signals.json',
            'aggregated': project_root / 'outputs' / 'aggregated' / 'aggregated_signals.json',
            'classified': project_root / 'outputs' / 'classified' / 'gtm_classified_signals.json',
            'insights': project_root / 'outputs' / 'insights' / 'gtm_insights_report.json',
            'executive_summary': project_root / 'outputs' / 'reports' / 'executive_summary.txt',
            'markdown_report': project_root / 'outputs' / 'reports' / f'GTM_ANALYSIS_{company_name.upper()}.md',
            'csv_signals': project_root / 'data' / 'gtm_signals.csv',
            'csv_insights': project_root / 'data' / 'gtm_insights.csv',
            'json_full': project_root / 'data' / 'gtm_analysis_full.json'
        }
        
        logger.info(f"Initialized GTM Pipeline for {company_name}")
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the complete GTM intelligence pipeline.
        
        Returns:
            Dictionary with execution results and statistics
        """
        print("\n" + "="*80)
        print(f"GTM INTELLIGENCE PLATFORM - {self.company_name.upper()}")
        print("="*80)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        try:
            # Step 1: Data Collection
            print("STEP 1: DATA COLLECTION")
            print("-" * 80)
            all_signals = self._collect_data()
            
            # Step 2: Signal Aggregation
            print("\nSTEP 2: SIGNAL AGGREGATION")
            print("-" * 80)
            aggregated_signals = self._aggregate_signals(all_signals)
            
            # Step 3: GTM Classification
            print("\nSTEP 3: GTM CLASSIFICATION")
            print("-" * 80)
            classified_signals = self._classify_signals(aggregated_signals)
            
            # Step 4: Insight Generation
            print("\nSTEP 4: INSIGHT GENERATION")
            print("-" * 80)
            insights, executive_summary = self._generate_insights(classified_signals)
            
            # Step 5: Export Results
            print("\nSTEP 5: EXPORT RESULTS")
            print("-" * 80)
            self._export_results(classified_signals, insights, executive_summary)
            
            # Step 6: Generate Markdown Report
            print("\nSTEP 6: GENERATE MARKDOWN REPORT")
            print("-" * 80)
            self._generate_markdown_report(classified_signals, insights, executive_summary)
            
            # Calculate execution time
            self.stats['execution_time'] = time.time() - self.start_time
            
            # Print final summary
            self._print_summary(classified_signals, insights)
            
            return {
                'success': True,
                'stats': self.stats,
                'errors': self.errors,
                'output_paths': {k: str(v) for k, v in self.output_paths.items()}
            }
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}", exc_info=True)
            self.errors.append(str(e))
            print(f"\n❌ Pipeline execution failed: {e}")
            return {
                'success': False,
                'stats': self.stats,
                'errors': self.errors,
                'output_paths': {}
            }
    
    def _collect_data(self) -> List[Dict[str, Any]]:
        """Collect data from all sources."""
        all_signals = []
        
        # Collect news signals
        try:
            print("Collecting news articles...", end=" ", flush=True)
            news_signals = collect_news_signals(company_name=self.company_name)
            self.stats['news_signals'] = len(news_signals)
            all_signals.extend(news_signals)
            print(f"✓ Collected {len(news_signals)} news articles")
        except Exception as e:
            error_msg = f"News collection failed: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            print(f"✗ News collection failed: {e}")
        
        # Collect business intelligence (Crunchbase + LinkedIn)
        try:
            print("Collecting business intelligence...", end=" ", flush=True)
            business_signals = collect_business_intelligence(company_name=self.company_name)
            # Separate LinkedIn and Crunchbase counts
            linkedin_count = len([s for s in business_signals if s.get('source') == 'LinkedIn'])
            crunchbase_count = len([s for s in business_signals if s.get('source') == 'Crunchbase'])
            self.stats['linkedin_signals'] = linkedin_count
            self.stats['crunchbase_signals'] = crunchbase_count
            all_signals.extend(business_signals)
            print(f"✓ Collected {linkedin_count} LinkedIn signals")
            if crunchbase_count > 0:
                print(f"✓ Collected {crunchbase_count} Crunchbase signals")
        except Exception as e:
            error_msg = f"Business intelligence collection failed: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            print(f"✗ Business intelligence collection failed: {e}")
        
        # Collect GitHub signals
        try:
            print("Collecting GitHub signals...", end=" ", flush=True)
            github_signals = collect_github_signals(company_name=self.company_name)
            self.stats['github_signals'] = len(github_signals)
            all_signals.extend(github_signals)
            print(f"✓ Collected {len(github_signals)} GitHub signals")
        except Exception as e:
            error_msg = f"GitHub collection failed: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            print(f"✗ GitHub collection failed: {e}")
        
        self.stats['total_raw_signals'] = len(all_signals)
        print(f"\nTotal raw signals collected: {len(all_signals)}")
        
        return all_signals
    
    def _aggregate_signals(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aggregate and deduplicate signals."""
        try:
            print("Aggregating signals...", end=" ", flush=True)
            
            # Count sources
            sources = set(s.get('source', 'Unknown') for s in signals)
            
            # Aggregate signals
            aggregated = aggregate_market_signals(signals)
            self.stats['aggregated_signals'] = len(aggregated)
            
            print(f"✓ Aggregated {len(aggregated)} unique signals from {len(sources)} sources")
            
            # Show deduplication stats
            duplicates_removed = len(signals) - len(aggregated)
            if duplicates_removed > 0:
                print(f"  (Removed {duplicates_removed} duplicate signals)")
            
            return aggregated
            
        except Exception as e:
            error_msg = f"Signal aggregation failed: {e}"
            logger.error(error_msg, exc_info=True)
            self.errors.append(error_msg)
            print(f"✗ Signal aggregation failed: {e}")
            return signals  # Return original signals if aggregation fails
    
    def _classify_signals(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Classify signals into GTM dimensions."""
        try:
            print("Classifying signals into GTM dimensions...", end=" ", flush=True)
            
            classified = classify_gtm_signals(signals)
            self.stats['classified_signals'] = len(classified)
            
            # Count categories
            categories = {}
            for signal in classified:
                cat = signal.get('primary_category', 'UNKNOWN')
                categories[cat] = categories.get(cat, 0) + 1
            
            print(f"✓ Classified {len(classified)} signals into GTM dimensions")
            
            # Show category breakdown
            print("  Category breakdown:")
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"    - {cat}: {count} signals")
            
            return classified
            
        except Exception as e:
            error_msg = f"Signal classification failed: {e}"
            logger.error(error_msg, exc_info=True)
            self.errors.append(error_msg)
            print(f"✗ Signal classification failed: {e}")
            return signals  # Return unclassified signals if classification fails
    
    def _generate_insights(
        self,
        classified_signals: List[Dict[str, Any]]
    ) -> tuple[Dict[str, Any], str]:
        """Generate GTM insights and executive summary."""
        insights = {}
        executive_summary = ""
        
        try:
            print("Generating GTM insights...", end=" ", flush=True)
            
            insights = generate_gtm_insights(classified_signals)
            
            # Count insights
            category_insights = sum(
                len(insights_list) 
                for insights_list in insights.get('by_category', {}).values()
            )
            cross_category = len(insights.get('cross_category_insights', []))
            total_insights = category_insights + cross_category
            
            self.stats['insights_generated'] = total_insights
            
            print(f"✓ Generated {total_insights} GTM insights")
            print(f"  ({category_insights} category-specific + {cross_category} cross-category)")
            
        except Exception as e:
            error_msg = f"Insight generation failed: {e}"
            logger.error(error_msg, exc_info=True)
            self.errors.append(error_msg)
            print(f"✗ Insight generation failed: {e}")
        
        try:
            print("Generating executive summary...", end=" ", flush=True)
            
            executive_summary = generate_executive_summary(insights, classified_signals)
            word_count = len(executive_summary.split())
            
            print(f"✓ Generated executive summary ({word_count} words)")
            
        except Exception as e:
            error_msg = f"Executive summary generation failed: {e}"
            logger.error(error_msg, exc_info=True)
            self.errors.append(error_msg)
            print(f"✗ Executive summary generation failed: {e}")
        
        return insights, executive_summary
    
    def _export_results(
        self,
        classified_signals: List[Dict[str, Any]],
        insights: Dict[str, Any],
        executive_summary: str
    ) -> None:
        """Export results to CSV and JSON formats."""
        try:
            print("Exporting to CSV and JSON...", end=" ", flush=True)
            
            export_paths = export_all_formats(
                signals=classified_signals,
                insights=insights,
                executive_summary=executive_summary,
                output_dir=str(project_root / 'data')
            )
            
            # Update output paths
            self.output_paths['csv_signals'] = Path(export_paths['signals_csv'])
            self.output_paths['csv_insights'] = Path(export_paths['insights_csv'])
            self.output_paths['json_full'] = Path(export_paths['full_json'])
            
            print(f"✓ Exported to data/")
            print(f"  - Signals CSV: {Path(export_paths['signals_csv']).name}")
            print(f"  - Insights CSV: {Path(export_paths['insights_csv']).name}")
            print(f"  - Full JSON: {Path(export_paths['full_json']).name}")
            
        except Exception as e:
            error_msg = f"Export failed: {e}"
            logger.error(error_msg, exc_info=True)
            self.errors.append(error_msg)
            print(f"✗ Export failed: {e}")
    
    def _generate_markdown_report(
        self,
        classified_signals: List[Dict[str, Any]],
        insights: Dict[str, Any],
        executive_summary: str
    ) -> None:
        """Generate markdown report."""
        try:
            print("Generating markdown report...", end=" ", flush=True)
            
            report_path = create_gtm_report(
                signals_path=str(self.output_paths['classified']),
                insights_path=str(self.output_paths['insights']),
                executive_summary_path=str(self.output_paths['executive_summary']),
                output_path=str(self.output_paths['markdown_report']),
                company_name=self.company_name
            )
            
            # Get word count
            with open(report_path, 'r', encoding='utf-8') as f:
                word_count = len(f.read().split())
            
            print(f"✓ Generated {Path(report_path).name} ({word_count} words)")
            
        except Exception as e:
            error_msg = f"Markdown report generation failed: {e}"
            logger.error(error_msg, exc_info=True)
            self.errors.append(error_msg)
            print(f"✗ Markdown report generation failed: {e}")
    
    def _print_summary(
        self,
        classified_signals: List[Dict[str, Any]],
        insights: Dict[str, Any]
    ) -> None:
        """Print final execution summary."""
        print("\n" + "="*80)
        print("EXECUTION SUMMARY")
        print("="*80)
        
        # Statistics
        print(f"\nTotal signals analyzed: {self.stats['classified_signals']}")
        print(f"Insights generated: {self.stats['insights_generated']}")
        print(f"Execution time: {self.stats['execution_time']:.1f} seconds")
        
        # Extract key findings
        print("\nKey Findings:")
        key_findings = self._extract_key_findings(insights)
        for i, finding in enumerate(key_findings[:5], 1):
            print(f"  {i}. {finding}")
        
        # Primary recommendation
        print("\nPrimary Recommendation:")
        primary_rec = self._extract_primary_recommendation(insights, classified_signals)
        print(f"  {primary_rec}")
        
        # Errors (if any)
        if self.errors:
            print(f"\n⚠️  Warnings/Errors: {len(self.errors)}")
            for error in self.errors[:3]:
                print(f"  - {error}")
        
        # Output files
        print("\nGenerated Files:")
        print(f"  - Markdown Report: {self.output_paths['markdown_report']}")
        print(f"  - CSV Exports: {self.output_paths['csv_signals'].parent}")
        print(f"  - Full JSON: {self.output_paths['json_full']}")
        
        print("\n" + "="*80)
        print("✓ PIPELINE EXECUTION COMPLETE")
        print("="*80 + "\n")
    
    def _extract_key_findings(self, insights: Dict[str, Any]) -> List[str]:
        """Extract top key findings from insights."""
        findings = []
        
        # Extract from category insights
        for category, category_insights in insights.get('by_category', {}).items():
            for insight in category_insights[:2]:  # Top 2 per category
                insight_text = insight.get('insight', '')
                if insight_text:
                    # Extract first sentence
                    first_sentence = insight_text.split('.')[0].strip()
                    if len(first_sentence) > 20:
                        findings.append(f"[{category}] {first_sentence}")
        
        # Extract from cross-category insights
        for insight in insights.get('cross_category_insights', [])[:2]:
            insight_text = insight.get('insight', '')
            if insight_text:
                first_sentence = insight_text.split('.')[0].strip()
                if len(first_sentence) > 20:
                    findings.append(f"[STRATEGIC] {first_sentence}")
        
        return findings[:5]  # Return top 5
    
    def _extract_primary_recommendation(
        self,
        insights: Dict[str, Any],
        classified_signals: List[Dict[str, Any]]
    ) -> str:
        """Extract primary strategic recommendation."""
        # Look for high-confidence insights with recommendations
        all_recommendations = []
        
        for category, category_insights in insights.get('by_category', {}).items():
            for insight in category_insights:
                if insight.get('confidence') == 'high':
                    actions = insight.get('recommended_actions', [])
                    if actions:
                        all_recommendations.append(actions[0])
        
        # Add cross-category recommendations
        for insight in insights.get('cross_category_insights', []):
            if insight.get('confidence') == 'high':
                actions = insight.get('recommended_actions', [])
                if actions:
                    all_recommendations.append(actions[0])
        
        if all_recommendations:
            # Return first high-priority recommendation
            return all_recommendations[0]
        
        # Fallback recommendation
        return "Monitor competitive developments and prepare strategic response across multiple GTM dimensions."


def main():
    """Main entry point for the GTM intelligence pipeline."""
    try:
        if not MODULES_LOADED:
            print("❌ Failed to load required modules. Please check your installation.")
            sys.exit(1)
        
        # Initialize and run pipeline
        pipeline = GTMPipeline(company_name="Stripe")
        results = pipeline.run()
        
        # Exit with appropriate code
        sys.exit(0 if results['success'] else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
