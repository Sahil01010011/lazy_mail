"""
URL extractor with homograph detection.
Finds and analyzes URLs in email content.
"""
import re
from typing import List, Dict, Any, Set
from urllib.parse import urlparse
import tldextract
import logging

logger = logging.getLogger(__name__)


class URLExtractor:
    """Extract and analyze URLs from text content."""
    
    # Common URL shorteners
    URL_SHORTENERS = {
        'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly',
        'is.gd', 'buff.ly', 'adf.ly', 'short.to', 'tiny.cc'
    }
    
    # Suspicious TLDs often used in phishing
    SUSPICIOUS_TLDS = {
        'tk', 'ml', 'ga', 'cf', 'gq', 'xyz', 'top', 'club',
        'work', 'click', 'link', 'download', 'bid', 'loan'
    }
    
    # Unicode homoglyphs for ASCII characters
    HOMOGLYPHS = {
        'a': ['а', 'ạ', 'ả', 'ã', 'ā', 'ă'],  # Cyrillic 'a', Vietnamese, etc.
        'e': ['е', 'ë', 'é', 'è', 'ê', 'ē'],  # Cyrillic 'e'
        'i': ['і', 'í', 'ì', 'î', 'ï', 'ī'],  # Cyrillic 'i'
        'o': ['о', 'ó', 'ò', 'ô', 'ö', 'ō'],  # Cyrillic 'o'
        'p': ['р'],  # Cyrillic 'r' looks like 'p'
        'c': ['с'],  # Cyrillic 's' looks like 'c'
        'y': ['у'],  # Cyrillic 'u' looks like 'y'
        'x': ['х'],  # Cyrillic 'kh' looks like 'x'
    }
    
    def __init__(self, text: str, html: str = ""):
        """Initialize with text and optional HTML content."""
        self.text = text
        self.html = html
        self.urls: List[Dict[str, Any]] = []
        self._extract()
    
    def _extract_from_text(self, content: str) -> Set[str]:
        """Extract URLs using regex patterns."""
        # Pattern for http(s) URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        
        # Pattern for www URLs without protocol
        www_pattern = r'www\.[^\s<>"{}|\\^`\[\]]+'
        
        urls = set()
        
        # Find http(s) URLs
        urls.update(re.findall(url_pattern, content, re.IGNORECASE))
        
        # Find www URLs and add protocol
        www_urls = re.findall(www_pattern, content, re.IGNORECASE)
        urls.update([f'http://{url}' for url in www_urls])
        
        return urls
    
    def _extract_from_html(self, html_content: str) -> Set[str]:
        """Extract URLs from HTML anchor tags."""
        # Simple regex for href attributes
        href_pattern = r'href=["\'](https?://[^"\']+)["\']'
        return set(re.findall(href_pattern, html_content, re.IGNORECASE))
    
    def _extract(self):
        """Extract all URLs from text and HTML."""
        all_urls = set()
        
        # Extract from text
        if self.text:
            all_urls.update(self._extract_from_text(self.text))
        
        # Extract from HTML
        if self.html:
            all_urls.update(self._extract_from_html(self.html))
        
        # Analyze each URL
        for url in all_urls:
            self.urls.append(self._analyze_url(url))
    
    def _analyze_url(self, url: str) -> Dict[str, Any]:
        """Analyze a single URL for suspicious indicators."""
        parsed = urlparse(url)
        extracted = tldextract.extract(url)
        
        analysis = {
            'url': url,
            'scheme': parsed.scheme,
            'domain': parsed.netloc,
            'path': parsed.path,
            'subdomain': extracted.subdomain,
            'registered_domain': extracted.domain + '.' + extracted.suffix if extracted.suffix else extracted.domain,
            'tld': extracted.suffix,
            'is_shortener': self._is_url_shortener(parsed.netloc),
            'is_suspicious_tld': extracted.suffix in self.SUSPICIOUS_TLDS,
            'has_ip_address': self._has_ip_address(parsed.netloc),
            'has_homograph': self._has_homograph(parsed.netloc),
            'url_length': len(url),
            'subdomain_count': len(extracted.subdomain.split('.')) if extracted.subdomain else 0
        }
        
        return analysis
    
    def _is_url_shortener(self, netloc: str) -> bool:
        """Check if domain is a known URL shortener."""
        return netloc.lower() in self.URL_SHORTENERS
    
    def _has_ip_address(self, netloc: str) -> bool:
        """Check if domain is an IP address instead of domain name."""
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        # Remove port if present
        domain = netloc.split(':')[0]
        return bool(re.match(ip_pattern, domain))
    
    def _has_homograph(self, domain: str) -> bool:
        """Check for IDN homograph attack (lookalike characters)."""
        for char in domain:
            # Check if any character is in our homoglyph mapping values
            for ascii_char, homoglyphs in self.HOMOGLYPHS.items():
                if char in homoglyphs:
                    return True
        return False
    
    def get_urls(self) -> List[Dict[str, Any]]:
        """Get all extracted URLs with analysis."""
        return self.urls
    
    def get_suspicious_urls(self) -> List[Dict[str, Any]]:
        """Get URLs with suspicious indicators."""
        suspicious = []
        for url in self.urls:
            if (url['is_shortener'] or 
                url['is_suspicious_tld'] or 
                url['has_ip_address'] or 
                url['has_homograph'] or
                url['url_length'] > 100 or
                url['subdomain_count'] > 3):
                suspicious.append(url)
        return suspicious
    
    def get_domains(self) -> List[str]:
        """Get unique domains from all URLs."""
        return list(set(url['domain'] for url in self.urls))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            'urls': self.urls,
            'url_count': len(self.urls),
            'unique_domains': len(self.get_domains()),
            'suspicious_url_count': len(self.get_suspicious_urls()),
            'has_url_shorteners': any(url['is_shortener'] for url in self.urls),
            'has_ip_urls': any(url['has_ip_address'] for url in self.urls),
            'has_homographs': any(url['has_homograph'] for url in self.urls)
        }
