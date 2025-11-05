"""
Report Generator for GTM Intelligence
Generates comprehensive reports and visualizations
"""

import json
import os
from typing import Dict, List
from datetime import datetime
import pandas as pd


class ReportGenerator:
    """Generates reports from intelligence data"""
    
    def __init__(self):
        self.report_templates = {
            'executive': 'executive_report_template',
            'detailed': 'detailed_analysis_template',
            'category': 'category_specific_template'
        }
    
    def generate_executive_report(self, intelligence: Dict, company_name: str) -> str:
        """
        Generate executive summary report
        
        Args:
            intelligence: Full intelligence dictionary
            company_name: Name of the target company
            
        Returns:
            Formatted report text
        """
        report = []
        report.append(f"GTM INTELLIGENCE REPORT: {company_name.upper()}")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("\n")
        
        # Company Overview
        overview = intelligence.get('company_overview', {})
        if overview:
            report.append("COMPANY OVERVIEW")
            report.append("-" * 80)
            report.append(f"Name: {overview.get('name', 'N/A')}")
            report.append(f"Description: {overview.get('description', 'N/A')}")
            report.append(f"Categories: {', '.join(overview.get('categories', []))}")
            report.append(f"Founded: {overview.get('founded', 'N/A')}")
            report.append(f"Headquarters: {overview.get('headquarters', 'N/A')}")
            report.append(f"Employees: {overview.get('employees', 'N/A')}")
            report.append(f"Total Funding: {overview.get('funding_total', {}).get('value', 'N/A')}")
            report.append("\n")
        
        # GTM Signals
        report.append("KEY GTM SIGNALS")
        report.append("-" * 80)
        gtm_signals = intelligence.get('gtm_signals', {})
        
        # Sort signals by strength
        sorted_signals = sorted(
            gtm_signals.items(),
            key=lambda x: x[1].get('strength', 0),
            reverse=True
        )
        
        for signal_type, signal_data in sorted_signals[:5]:
            strength = signal_data.get('strength', 0)
            strength_bar = '█' * int(strength * 20)
            
            report.append(f"\n{signal_type.replace('_', ' ').title()}")
            report.append(f"Strength: {strength_bar} ({strength:.2f})")
            report.append(f"Summary: {signal_data.get('summary', 'N/A')}")
            report.append(f"Evidence: {signal_data.get('evidence_count', 0)} data points")
        
        report.append("\n")
        
        # Growth Indicators
        report.append("GROWTH INDICATORS")
        report.append("-" * 80)
        growth = intelligence.get('growth_indicators', {})
        
        team_growth = growth.get('team_growth', {})
        if team_growth:
            report.append(f"Total Employees: {team_growth.get('total_employees', 'N/A')}")
            report.append(f"6-Month Growth: {team_growth.get('growth_6m', 'N/A')}")
            report.append(f"1-Year Growth: {team_growth.get('growth_1y', 'N/A')}")
        
        hiring = growth.get('hiring_velocity', {})
        if hiring:
            report.append(f"\nActive Job Postings: {hiring.get('total_postings', 0)}")
            report.append(f"GTM Roles: {hiring.get('gtm_roles', 0)}")
            report.append(f"Hiring Departments: {', '.join(hiring.get('departments_hiring', []))}")
        
        report.append("\n")
        
        # Developer Ecosystem
        dev_eco = intelligence.get('developer_ecosystem', {})
        if dev_eco:
            report.append("DEVELOPER ECOSYSTEM")
            report.append("-" * 80)
            report.append(f"Total Repositories: {dev_eco.get('total_repositories', 0)}")
            report.append(f"SDK Libraries: {dev_eco.get('sdk_count', 0)}")
            report.append(f"Total GitHub Stars: {dev_eco.get('total_stars', 0)}")
            report.append(f"Languages: {', '.join(dev_eco.get('languages', []))}")
            report.append(f"Developer Traction Score: {dev_eco.get('developer_traction', 0):.1f}/100")
            report.append("\n")
        
        # Top Recommendations
        report.append("TOP RECOMMENDATIONS")
        report.append("-" * 80)
        recommendations = intelligence.get('recommendations', [])
        
        for idx, rec in enumerate(recommendations[:5], 1):
            report.append(f"\n{idx}. {rec.get('title')} [{rec.get('priority', 'medium').upper()}]")
            report.append(f"   Description: {rec.get('description')}")
            report.append(f"   Action: {rec.get('action')}")
        
        report.append("\n")
        report.append("=" * 80)
        report.append("END OF REPORT")
        
        return "\n".join(report)
    
    def generate_detailed_report(self, intelligence: Dict, company_name: str) -> str:
        """
        Generate detailed analysis report
        
        Args:
            intelligence: Full intelligence dictionary
            company_name: Name of the target company
            
        Returns:
            Formatted detailed report
        """
        report = []
        report.append(f"DETAILED GTM ANALYSIS: {company_name.upper()}")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("\n")
        
        # Strategic Initiatives Timeline
        report.append("STRATEGIC INITIATIVES (RECENT)")
        report.append("-" * 80)
        
        initiatives = intelligence.get('strategic_initiatives', [])
        # Sort by date
        sorted_initiatives = sorted(
            [i for i in initiatives if i.get('date')],
            key=lambda x: x.get('date', ''),
            reverse=True
        )
        
        for initiative in sorted_initiatives[:15]:
            report.append(f"\n[{initiative.get('date', 'N/A')}] {initiative.get('title')}")
            report.append(f"Type: {initiative.get('type', 'N/A')}")
            report.append(f"Categories: {', '.join(initiative.get('categories', []))}")
            if initiative.get('relevance'):
                report.append(f"Relevance: {initiative.get('relevance'):.2f}")
            if initiative.get('url'):
                report.append(f"Source: {initiative.get('url')}")
        
        report.append("\n")
        
        # Detailed GTM Signals
        report.append("DETAILED SIGNAL ANALYSIS")
        report.append("-" * 80)
        
        gtm_signals = intelligence.get('gtm_signals', {})
        for signal_type, signal_data in gtm_signals.items():
            report.append(f"\n{signal_type.replace('_', ' ').upper()}")
            report.append(f"Strength: {signal_data.get('strength', 0):.2f}")
            report.append(f"Evidence Count: {signal_data.get('evidence_count', 0)}")
            report.append(f"Summary: {signal_data.get('summary')}")
            
            # Show top evidence
            evidence = signal_data.get('evidence', [])
            if evidence:
                report.append("\nTop Evidence:")
                for idx, ev in enumerate(evidence[:3], 1):
                    report.append(f"  {idx}. {ev.get('title', 'N/A')}")
                    if ev.get('date'):
                        report.append(f"     Date: {ev.get('date')}")
        
        report.append("\n")
        
        # Department Analysis
        growth = intelligence.get('growth_indicators', {})
        team_growth = growth.get('team_growth', {})
        dept_dist = team_growth.get('department_distribution', {})
        
        if dept_dist:
            report.append("DEPARTMENT DISTRIBUTION")
            report.append("-" * 80)
            
            # Sort departments by size
            sorted_depts = sorted(dept_dist.items(), key=lambda x: x[1], reverse=True)
            
            total = sum(dept_dist.values())
            for dept, count in sorted_depts:
                percentage = (count / total * 100) if total > 0 else 0
                bar = '█' * int(percentage / 2)
                report.append(f"{dept:.<30} {count:>5} ({percentage:>5.1f}%) {bar}")
        
        report.append("\n")
        report.append("=" * 80)
        report.append("END OF DETAILED REPORT")
        
        return "\n".join(report)
    
    def generate_category_report(self, intelligence: Dict, category: str, company_name: str) -> str:
        """
        Generate category-specific report
        
        Args:
            intelligence: Full intelligence dictionary
            category: Category to focus on
            company_name: Name of the target company
            
        Returns:
            Formatted category report
        """
        report = []
        report.append(f"CATEGORY ANALYSIS: {category.upper()}")
        report.append(f"Company: {company_name}")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("\n")
        
        # Get category-specific signal data
        gtm_signals = intelligence.get('gtm_signals', {})
        signal_data = gtm_signals.get(category, {})
        
        if signal_data:
            report.append("OVERVIEW")
            report.append("-" * 80)
            report.append(f"Signal Strength: {signal_data.get('strength', 0):.2f}")
            report.append(f"Total Evidence: {signal_data.get('evidence_count', 0)} data points")
            report.append(f"Summary: {signal_data.get('summary')}")
            report.append("\n")
            
            report.append("DETAILED EVIDENCE")
            report.append("-" * 80)
            
            evidence = signal_data.get('evidence', [])
            for idx, ev in enumerate(evidence, 1):
                report.append(f"\n{idx}. {ev.get('title')}")
                report.append(f"   Date: {ev.get('date', 'N/A')}")
                report.append(f"   Type: {ev.get('type', 'N/A')}")
                report.append(f"   Source: {ev.get('source', 'N/A')}")
                if ev.get('url'):
                    report.append(f"   URL: {ev.get('url')}")
        else:
            report.append(f"No significant signals found for category: {category}")
        
        report.append("\n")
        
        # Category-specific recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 80)
        
        recommendations = intelligence.get('recommendations', [])
        category_recs = [
            rec for rec in recommendations 
            if category in rec.get('related_categories', [])
        ]
        
        if category_recs:
            for idx, rec in enumerate(category_recs, 1):
                report.append(f"\n{idx}. {rec.get('title')} [{rec.get('priority', 'medium').upper()}]")
                report.append(f"   {rec.get('description')}")
                report.append(f"   Action: {rec.get('action')}")
        else:
            report.append("No specific recommendations for this category.")
        
        report.append("\n")
        report.append("=" * 80)
        report.append("END OF CATEGORY REPORT")
        
        return "\n".join(report)
    
    def generate_csv_export(self, intelligence: Dict, company_name: str) -> pd.DataFrame:
        """
        Generate CSV export of key data points
        
        Args:
            intelligence: Full intelligence dictionary
            company_name: Name of the target company
            
        Returns:
            DataFrame with exportable data
        """
        data = []
        
        # Extract strategic initiatives
        for initiative in intelligence.get('strategic_initiatives', []):
            data.append({
                'company': company_name,
                'date': initiative.get('date'),
                'type': initiative.get('type'),
                'title': initiative.get('title'),
                'categories': ', '.join(initiative.get('categories', [])),
                'source': initiative.get('source'),
                'url': initiative.get('url'),
                'relevance': initiative.get('relevance'),
                'sentiment': initiative.get('sentiment')
            })
        
        df = pd.DataFrame(data)
        return df
    
    def save_report(self, report_text: str, filename: str):
        """Save report to text file"""
        output_path = os.path.join('outputs', 'reports', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(f"Saved report to {output_path}")
    
    def save_csv(self, df: pd.DataFrame, filename: str):
        """Save DataFrame to CSV file"""
        output_path = os.path.join('outputs', 'reports', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Saved CSV to {output_path}")


if __name__ == "__main__":
    # Load intelligence data
    with open('outputs/categorized/full_intelligence.json', 'r') as f:
        intelligence = json.load(f)
    
    generator = ReportGenerator()
    company_name = "Stripe"
    
    # Generate all report types
    exec_report = generator.generate_executive_report(intelligence, company_name)
    generator.save_report(exec_report, f'{company_name.lower()}_executive_report.txt')
    
    detailed_report = generator.generate_detailed_report(intelligence, company_name)
    generator.save_report(detailed_report, f'{company_name.lower()}_detailed_report.txt')
    
    # Generate CSV export
    df = generator.generate_csv_export(intelligence, company_name)
    generator.save_csv(df, f'{company_name.lower()}_data_export.csv')
    
    print("Report generation complete")
