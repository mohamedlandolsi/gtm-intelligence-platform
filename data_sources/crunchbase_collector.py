"""
Crunchbase API Collector for GTM Intelligence
Collects company data, funding rounds, and acquisitions from Crunchbase
"""

import os
import requests
from typing import Dict, List, Optional
import json
from datetime import datetime


class CrunchbaseCollector:
    """Collects data from Crunchbase API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('CRUNCHBASE_API_KEY')
        self.base_url = "https://api.crunchbase.com/api/v4"
        
    def get_organization_data(self, company_name: str) -> Dict:
        """
        Get comprehensive organization data from Crunchbase
        
        Args:
            company_name: Name or permalink of the company
            
        Returns:
            Dictionary with organization data
        """
        if not self.api_key:
            print("Warning: No API key provided. Using mock data.")
            return self._get_mock_organization_data(company_name)
        
        headers = {
            'X-cb-user-key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        # Search for organization
        search_url = f"{self.base_url}/searches/organizations"
        search_payload = {
            "field_ids": [
                "identifier",
                "location_identifiers",
                "short_description",
                "rank_org_company"
            ],
            "query": [
                {
                    "type": "predicate",
                    "field_id": "facet_ids",
                    "operator_id": "includes",
                    "values": ["company"]
                },
                {
                    "type": "predicate",
                    "field_id": "identifier",
                    "operator_id": "contains",
                    "values": [company_name.lower()]
                }
            ],
            "limit": 1
        }
        
        try:
            response = requests.post(search_url, headers=headers, json=search_payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error collecting Crunchbase data: {e}")
            return self._get_mock_organization_data(company_name)
    
    def get_funding_rounds(self, org_uuid: str) -> List[Dict]:
        """Get funding rounds for an organization"""
        if not self.api_key:
            return self._get_mock_funding_data()
        
        url = f"{self.base_url}/entities/organizations/{org_uuid}/funding_rounds"
        headers = {
            'X-cb-user-key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get('cards', {}).get('funding_rounds', [])
        except requests.exceptions.RequestException as e:
            print(f"Error collecting funding data: {e}")
            return []
    
    def _get_mock_organization_data(self, company_name: str) -> Dict:
        """Return mock organization data for testing"""
        return {
            'entities': [{
                'uuid': 'mock-uuid-123',
                'properties': {
                    'identifier': {
                        'value': company_name.lower(),
                        'permalink': company_name.lower()
                    },
                    'short_description': f'{company_name} is a leading fintech company',
                    'categories': ['Financial Services', 'Payments', 'FinTech'],
                    'founded_on': '2010-01-01',
                    'employee_count': '5000-10000',
                    'headquarters_location': 'San Francisco, CA',
                    'website_url': f'https://www.{company_name.lower()}.com',
                    'funding_total': {'value': 2000000000, 'currency': 'USD'},
                    'last_funding_type': 'Series H'
                }
            }],
            'collected_at': datetime.now().isoformat()
        }
    
    def _get_mock_funding_data(self) -> List[Dict]:
        """Return mock funding data for testing"""
        return [
            {
                'announced_on': '2023-01-15',
                'funding_type': 'Series H',
                'money_raised': {'value': 250000000, 'currency': 'USD'},
                'investor_count': 5
            }
        ]
    
    def save_to_json(self, data: Dict, filename: str):
        """Save collected data to JSON file"""
        output_path = os.path.join('outputs', 'raw_data', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved Crunchbase data to {output_path}")


if __name__ == "__main__":
    collector = CrunchbaseCollector()
    org_data = collector.get_organization_data("Stripe")
    collector.save_to_json(org_data, 'stripe_crunchbase.json')
    print("Collected Crunchbase data")
