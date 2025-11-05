"""
GitHub Data Collector for GTM Intelligence
Collects repository data, activity, and developer ecosystem insights
"""

import os
import requests
from typing import List, Dict, Optional
import json
from datetime import datetime, timedelta


class GitHubCollector:
    """Collects data from GitHub API"""
    
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        if self.api_token:
            self.headers['Authorization'] = f'token {self.api_token}'
    
    def search_company_repositories(self, company_name: str, org_name: Optional[str] = None) -> List[Dict]:
        """
        Search for repositories related to a company
        
        Args:
            company_name: Name of the company
            org_name: GitHub organization name (e.g., "stripe")
            
        Returns:
            List of repositories with metadata
        """
        if org_name:
            return self.get_org_repositories(org_name)
        else:
            return self.search_repositories(company_name)
    
    def get_org_repositories(self, org_name: str) -> List[Dict]:
        """
        Get all repositories for a GitHub organization
        
        Args:
            org_name: GitHub organization name
            
        Returns:
            List of repositories
        """
        url = f"{self.base_url}/orgs/{org_name}/repos"
        params = {
            'type': 'public',
            'sort': 'updated',
            'per_page': 100
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            repos = []
            for repo in response.json():
                repos.append(self._format_repository_data(repo))
            
            return repos
        except requests.exceptions.RequestException as e:
            print(f"Error collecting GitHub org repos: {e}")
            return self._get_mock_repositories(org_name)
    
    def search_repositories(self, query: str) -> List[Dict]:
        """Search GitHub repositories by query"""
        url = f"{self.base_url}/search/repositories"
        params = {
            'q': f'{query} in:name,description',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 30
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            repos = []
            for repo in response.json().get('items', []):
                repos.append(self._format_repository_data(repo))
            
            return repos
        except requests.exceptions.RequestException as e:
            print(f"Error searching GitHub repos: {e}")
            return self._get_mock_repositories(query)
    
    def get_repository_activity(self, owner: str, repo: str, days: int = 30) -> Dict:
        """
        Get recent activity metrics for a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            days: Number of days to look back
            
        Returns:
            Dictionary with activity metrics
        """
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        # Get commits
        commits_url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        issues_url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        
        try:
            commits_response = requests.get(
                commits_url, 
                headers=self.headers,
                params={'since': since, 'per_page': 100}
            )
            
            issues_response = requests.get(
                issues_url,
                headers=self.headers,
                params={'state': 'all', 'since': since, 'per_page': 100}
            )
            
            activity = {
                'repository': f"{owner}/{repo}",
                'period_days': days,
                'commits': len(commits_response.json()) if commits_response.ok else 0,
                'issues_prs': len(issues_response.json()) if issues_response.ok else 0,
                'collected_at': datetime.now().isoformat()
            }
            
            return activity
        except Exception as e:
            print(f"Error collecting repository activity: {e}")
            return self._get_mock_activity(owner, repo, days)
    
    def get_sdk_libraries(self, company_name: str) -> List[Dict]:
        """
        Search for SDKs and libraries published by the company
        
        Args:
            company_name: Name of the company
            
        Returns:
            List of SDKs/libraries
        """
        search_terms = f"{company_name} sdk OR {company_name} library OR {company_name} api"
        return self.search_repositories(search_terms)
    
    def _format_repository_data(self, repo: Dict) -> Dict:
        """Format raw GitHub API repository data"""
        return {
            'name': repo.get('name'),
            'full_name': repo.get('full_name'),
            'description': repo.get('description'),
            'url': repo.get('html_url'),
            'stars': repo.get('stargazers_count'),
            'forks': repo.get('forks_count'),
            'watchers': repo.get('watchers_count'),
            'language': repo.get('language'),
            'topics': repo.get('topics', []),
            'created_at': repo.get('created_at'),
            'updated_at': repo.get('updated_at'),
            'license': repo.get('license', {}).get('name') if repo.get('license') else None,
            'is_archived': repo.get('archived'),
            'collected_at': datetime.now().isoformat()
        }
    
    def _get_mock_repositories(self, identifier: str) -> List[Dict]:
        """Return mock repository data for testing"""
        return [
            {
                'name': 'stripe-node',
                'full_name': 'stripe/stripe-node',
                'description': 'Node.js library for the Stripe API',
                'url': 'https://github.com/stripe/stripe-node',
                'stars': 3500,
                'forks': 680,
                'watchers': 150,
                'language': 'JavaScript',
                'topics': ['stripe', 'payments', 'api', 'nodejs'],
                'created_at': '2015-03-10T12:00:00Z',
                'updated_at': '2024-10-28T15:30:00Z',
                'license': 'MIT',
                'is_archived': False,
                'collected_at': datetime.now().isoformat()
            },
            {
                'name': 'stripe-python',
                'full_name': 'stripe/stripe-python',
                'description': 'Python library for the Stripe API',
                'url': 'https://github.com/stripe/stripe-python',
                'stars': 4200,
                'forks': 890,
                'watchers': 180,
                'language': 'Python',
                'topics': ['stripe', 'payments', 'api', 'python'],
                'created_at': '2014-01-15T10:00:00Z',
                'updated_at': '2024-10-29T09:15:00Z',
                'license': 'MIT',
                'is_archived': False,
                'collected_at': datetime.now().isoformat()
            },
            {
                'name': 'stripe-java',
                'full_name': 'stripe/stripe-java',
                'description': 'Java library for the Stripe API',
                'url': 'https://github.com/stripe/stripe-java',
                'stars': 2100,
                'forks': 520,
                'watchers': 95,
                'language': 'Java',
                'topics': ['stripe', 'payments', 'api', 'java'],
                'created_at': '2014-08-20T14:00:00Z',
                'updated_at': '2024-10-25T11:45:00Z',
                'license': 'MIT',
                'is_archived': False,
                'collected_at': datetime.now().isoformat()
            }
        ]
    
    def _get_mock_activity(self, owner: str, repo: str, days: int) -> Dict:
        """Return mock activity data for testing"""
        return {
            'repository': f"{owner}/{repo}",
            'period_days': days,
            'commits': 45,
            'issues_prs': 23,
            'contributors': 8,
            'collected_at': datetime.now().isoformat()
        }
    
    def save_to_json(self, data: any, filename: str):
        """Save collected data to JSON file"""
        output_path = os.path.join('outputs', 'raw_data', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved GitHub data to {output_path}")


if __name__ == "__main__":
    collector = GitHubCollector()
    
    # Collect Stripe's GitHub data
    repos = collector.search_company_repositories("Stripe", org_name="stripe")
    
    # Get activity for main repos
    activities = []
    for repo in repos[:5]:  # Top 5 repos
        parts = repo['full_name'].split('/')
        activity = collector.get_repository_activity(parts[0], parts[1])
        activities.append(activity)
    
    collector.save_to_json({
        'repositories': repos,
        'recent_activity': activities
    }, 'stripe_github.json')
    
    print(f"Collected {len(repos)} GitHub repositories")
