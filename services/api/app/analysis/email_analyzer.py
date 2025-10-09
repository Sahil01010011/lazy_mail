"""
Complete email analysis combining all detection layers.
"""
from typing import Dict, Any
import logging

from app.parsing.mime_parser import MIMEParser
from app.parsing.url_extractor import URLExtractor
from app.parsing.header_analyzer import HeaderAnalyzer
from app.parsing.html_normalizer import HTMLNormalizer
from app.integrations.rspamd_client import RspamdClient

logger = logging.getLogger(__name__)


class EmailAnalyzer:
    """Comprehensive email analysis combining multiple detection layers."""
    
    def __init__(self):
        self.rspamd_client = RspamdClient()
    
    async def analyze(self, raw_email: bytes) -> Dict[str, Any]:
        """Perform complete email analysis."""
        # Layer 1: Parse MIME
        mime_parser = MIMEParser(raw_email)
        email_data = mime_parser.to_dict()
        
        # Layer 2: Analyze headers
        header_analyzer = HeaderAnalyzer(email_data['headers'])
        header_analysis = header_analyzer.to_dict()
        header_risk = header_analyzer.get_risk_score()
        
        # Layer 3: Extract URLs
        url_extractor = URLExtractor(email_data['body_text'], email_data['body_html'])
        url_analysis = url_extractor.to_dict()
        
        # Layer 4: Normalize HTML
        html_normalizer = HTMLNormalizer(email_data['body_html'])
        html_data = html_normalizer.to_dict()
        html_analysis = html_data.get('analysis', {})
        html_risk = html_normalizer.get_risk_score()
        
        # Layer 5: Rspamd
        rspamd_result = await self.rspamd_client.check_email(raw_email)
        
        # Calculate combined risk
        combined_risk = self._calculate_combined_risk(
            header_risk=header_risk,
            html_risk=html_risk,
            url_risk=url_analysis['suspicious_url_count'],
            rspamd_score=rspamd_result['score'],
            rspamd_available=rspamd_result['is_available']
        )
        
        # Classify
        classification = self._classify(combined_risk, rspamd_result)
        
        return {
            'email': {
                'subject': email_data['subject'],
                'sender': email_data['sender'],
                'recipients': email_data['recipients'],
                'message_id': email_data['message_id'],
                'date': email_data['date']
            },
            'analysis': {
                'header': {
                    'risk_score': header_risk,
                    'spf': header_analysis['spf']['result'],
                    'dkim': header_analysis['dkim']['result'],
                    'dmarc': header_analysis['dmarc']['result'],
                    'has_anomalies': header_analysis['has_anomalies']
                },
                'urls': {
                    'total_count': url_analysis['url_count'],
                    'suspicious_count': url_analysis['suspicious_url_count'],
                    'has_shorteners': url_analysis['has_url_shorteners'],
                    'has_ip_urls': url_analysis['has_ip_urls'],
                    'details': url_analysis['urls'][:10]
                },
                'html': {
                    'risk_score': html_risk,
                    'has_javascript': html_analysis.get('has_javascript', False),
                    'has_iframes': html_analysis.get('has_iframes', False),
                    'link_count': html_analysis.get('link_count', 0)
                },
                'rspamd': {
                    'score': rspamd_result['score'],
                    'action': rspamd_result['action'],
                    'is_spam': rspamd_result['is_spam'],
                    'top_symbols': rspamd_result['symbols'][:10],
                    'available': rspamd_result['is_available']
                }
            },
            'verdict': {
                'classification': classification,
                'combined_risk_score': combined_risk,
                'confidence': self._calculate_confidence(rspamd_result['is_available']),
                'is_phishing': classification in ['phishing', 'spam'],
                'recommended_action': self._recommend_action(classification)
            }
        }
    
    def _calculate_combined_risk(self, header_risk: float, html_risk: float, url_risk: int, rspamd_score: float, rspamd_available: bool) -> float:
        """Calculate combined risk score (0-100)."""
        base_risk = (header_risk * 0.4) + (html_risk * 0.3)
        url_risk_score = min(url_risk * 10, 30)
        rspamd_risk = min((rspamd_score / 15.0) * 40, 40) if rspamd_available else 0
        total = base_risk + url_risk_score + rspamd_risk
        return min(total, 100.0)
    
    def _classify(self, risk_score: float, rspamd_result: Dict[str, Any]) -> str:
        """Classify email based on risk score."""
        if rspamd_result['is_available'] and rspamd_result['action'] == 'reject':
            return 'spam'
        if risk_score >= 75:
            return 'phishing'
        elif risk_score >= 50:
            return 'suspicious'
        elif risk_score >= 30:
            return 'questionable'
        else:
            return 'legitimate'
    
    def _calculate_confidence(self, rspamd_available: bool) -> float:
        """Calculate confidence level."""
        return 95.0 if rspamd_available else 75.0
    
    def _recommend_action(self, classification: str) -> str:
        """Recommend action."""
        action_map = {
            'phishing': 'quarantine',
            'spam': 'quarantine',
            'suspicious': 'flag',
            'questionable': 'warn',
            'legitimate': 'deliver'
        }
        return action_map.get(classification, 'review')
