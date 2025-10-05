"""
Email header analyzer - checks authentication and detects anomalies.
"""
import re
from typing import Dict, Any, Optional, List
from email.utils import parseaddr
import logging

logger = logging.getLogger(__name__)


class HeaderAnalyzer:
    """Analyze email headers for authentication and anomalies."""
    
    def __init__(self, headers: Dict[str, Any]):
        """Initialize with parsed email headers."""
        self.headers = headers
        self.analysis: Dict[str, Any] = {}
        self._analyze()
    
    def _analyze(self):
        """Perform all header analysis."""
        self.analysis = {
            'spf': self._check_spf(),
            'dkim': self._check_dkim(),
            'dmarc': self._check_dmarc(),
            'sender_analysis': self._analyze_sender(),
            'reply_to_analysis': self._analyze_reply_to(),
            'received_hops': self._count_received_hops(),
            'has_anomalies': False
        }
        
        # Determine if there are anomalies
        self.analysis['has_anomalies'] = (
            self.analysis['spf']['result'] == 'fail' or
            self.analysis['dkim']['result'] == 'fail' or
            self.analysis['dmarc']['result'] == 'fail' or
            self.analysis['sender_analysis']['display_name_mismatch'] or
            self.analysis['reply_to_analysis']['reply_to_mismatch']
        )
    
    def _check_spf(self) -> Dict[str, Any]:
        """Check SPF authentication result."""
        spf_header = self._get_header('Received-SPF', '')
        
        result = 'unknown'
        if 'pass' in spf_header.lower():
            result = 'pass'
        elif 'fail' in spf_header.lower():
            result = 'fail'
        elif 'softfail' in spf_header.lower():
            result = 'softfail'
        elif 'neutral' in spf_header.lower():
            result = 'neutral'
        elif 'none' in spf_header.lower():
            result = 'none'
        
        return {
            'result': result,
            'header': spf_header,
            'is_valid': result == 'pass'
        }
    
    def _check_dkim(self) -> Dict[str, Any]:
        """Check DKIM signature."""
        dkim_signature = self._get_header('DKIM-Signature', '')
        auth_results = self._get_header('Authentication-Results', '')
        
        result = 'unknown'
        if 'dkim=pass' in auth_results.lower():
            result = 'pass'
        elif 'dkim=fail' in auth_results.lower():
            result = 'fail'
        elif 'dkim=none' in auth_results.lower():
            result = 'none'
        elif not dkim_signature:
            result = 'none'
        
        return {
            'result': result,
            'has_signature': bool(dkim_signature),
            'is_valid': result == 'pass'
        }
    
    def _check_dmarc(self) -> Dict[str, Any]:
        """Check DMARC policy."""
        auth_results = self._get_header('Authentication-Results', '')
        
        result = 'unknown'
        if 'dmarc=pass' in auth_results.lower():
            result = 'pass'
        elif 'dmarc=fail' in auth_results.lower():
            result = 'fail'
        elif 'dmarc=none' in auth_results.lower():
            result = 'none'
        
        return {
            'result': result,
            'is_valid': result == 'pass'
        }
    
    def _analyze_sender(self) -> Dict[str, Any]:
        """Analyze sender address for anomalies."""
        from_header = self._get_header('From', '')
        display_name, email = parseaddr(from_header)
        
        # Extract domain from email
        email_domain = email.split('@')[1] if '@' in email else ''
        
        # Check if display name contains a different domain
        display_name_mismatch = False
        if display_name and '@' in display_name:
            # Display name contains an email address different from actual sender
            display_name_mismatch = True
        
        return {
            'display_name': display_name,
            'email': email,
            'domain': email_domain,
            'display_name_mismatch': display_name_mismatch
        }
    
    def _analyze_reply_to(self) -> Dict[str, Any]:
        """Analyze Reply-To header for mismatches."""
        from_header = self._get_header('From', '')
        reply_to = self._get_header('Reply-To', '')
        
        _, from_email = parseaddr(from_header)
        _, reply_to_email = parseaddr(reply_to)
        
        reply_to_mismatch = False
        if reply_to_email and from_email != reply_to_email:
            reply_to_mismatch = True
        
        return {
            'reply_to': reply_to_email,
            'reply_to_mismatch': reply_to_mismatch
        }
    
    def _count_received_hops(self) -> int:
        """Count number of mail server hops."""
        received_headers = self._get_header('Received', '')
        
        # Handle multiple Received headers
        if isinstance(received_headers, list):
            return len(received_headers)
        elif received_headers:
            # Count newlines as proxy for multiple headers
            return received_headers.count('\n') + 1
        
        return 0
    
    def _get_header(self, name: str, default: Any = None) -> Any:
        """Get a header value with case-insensitive lookup."""
        # Try exact match first
        if name in self.headers:
            return self.headers[name]
        
        # Try case-insensitive match
        for key, value in self.headers.items():
            if key.lower() == name.lower():
                return value
        
        return default
    
    def get_analysis(self) -> Dict[str, Any]:
        """Get complete header analysis."""
        return self.analysis
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return self.analysis
    
    def get_risk_score(self) -> float:
        """Calculate risk score based on header analysis (0-100)."""
        score = 0.0
        
        # SPF check (0-25 points)
        if self.analysis['spf']['result'] == 'fail':
            score += 25
        elif self.analysis['spf']['result'] == 'softfail':
            score += 15
        elif self.analysis['spf']['result'] in ['neutral', 'none']:
            score += 10
        
        # DKIM check (0-25 points)
        if self.analysis['dkim']['result'] == 'fail':
            score += 25
        elif self.analysis['dkim']['result'] == 'none':
            score += 15
        
        # DMARC check (0-25 points)
        if self.analysis['dmarc']['result'] == 'fail':
            score += 25
        elif self.analysis['dmarc']['result'] == 'none':
            score += 10
        
        # Sender anomalies (0-15 points)
        if self.analysis['sender_analysis']['display_name_mismatch']:
            score += 15
        
        # Reply-To mismatch (0-10 points)
        if self.analysis['reply_to_analysis']['reply_to_mismatch']:
            score += 10
        
        return min(score, 100.0)  # Cap at 100
