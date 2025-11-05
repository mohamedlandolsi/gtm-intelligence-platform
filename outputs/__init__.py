"""
Outputs Package
Report and recommendations generation modules
"""

from .report_generator import ReportGenerator
from .recommendations_generator import RecommendationsGenerator

__all__ = [
    'ReportGenerator',
    'RecommendationsGenerator'
]
