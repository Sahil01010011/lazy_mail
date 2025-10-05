"""
HTML normalizer - clean and extract text from HTML emails.
"""
from bs4 import BeautifulSoup
import re
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class HTMLNormalizer:
    """Clean and normalize HTML content from emails."""
    
    def __init__(self, html: str):
        """Initialize with raw HTML content."""
        self.raw_html = html
        self.soup = None
        self.clean_text = ""
        self.analysis: Dict[str, Any] = {}
        self._parse()
    
    def _parse(self):
        """Parse and analyze HTML."""
        if not self.raw_html:
            return
        
        try:
            self.soup = BeautifulSoup(self.raw_html, 'html.parser')
            self._remove_dangerous_elements()
            self.clean_text = self._extract_text()
            self.analysis = self._analyze_content()
        except Exception as e:
            logger.error(f"Failed to parse HTML: {e}")
            self.clean_text = self.raw_html  # Fallback to raw
    
    def _remove_dangerous_elements(self):
        """Remove potentially dangerous HTML elements."""
        if not self.soup:
            return
        
        # Remove scripts
        for script in self.soup.find_all('script'):
            script.decompose()
        
        # Remove iframes
        for iframe in self.soup.find_all('iframe'):
            iframe.decompose()
        
        # Remove forms
        for form in self.soup.find_all('form'):
            form.decompose()
        
        # Remove objects and embeds
        for obj in self.soup.find_all(['object', 'embed']):
            obj.decompose()
    
    def _extract_text(self) -> str:
        """Extract clean text from HTML."""
        if not self.soup:
            return ""
        
        # Get text
        text = self.soup.get_text(separator='\n', strip=True)
        
        # Clean up whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Multiple newlines to double
        text = re.sub(r' +', ' ', text)  # Multiple spaces to single
        
        return text.strip()
    
    def _analyze_content(self) -> Dict[str, Any]:
        """Analyze HTML for suspicious patterns."""
        if not self.soup:
            return {}
        
        # Count various elements
        links = self.soup.find_all('a')
        images = self.soup.find_all('img')
        scripts = self.soup.find_all('script')
        iframes = self.soup.find_all('iframe')
        forms = self.soup.find_all('form')
        
        # Check for hidden elements
        hidden_elements = self.soup.find_all(style=re.compile(r'display:\s*none', re.I))
        hidden_elements += self.soup.find_all(style=re.compile(r'visibility:\s*hidden', re.I))
        
        # Calculate text-to-HTML ratio
        html_length = len(self.raw_html)
        text_length = len(self.clean_text)
        html_to_text_ratio = text_length / html_length if html_length > 0 else 0
        
        return {
            'link_count': len(links),
            'image_count': len(images),
            'has_javascript': len(scripts) > 0,
            'has_iframes': len(iframes) > 0,
            'has_forms': len(forms) > 0,
            'hidden_element_count': len(hidden_elements),
            'html_length': html_length,
            'text_length': text_length,
            'html_to_text_ratio': round(html_to_text_ratio, 3)
        }
    
    def get_text(self) -> str:
        """Get cleaned plain text."""
        return self.clean_text
    
    def get_analysis(self) -> Dict[str, Any]:
        """Get HTML analysis results."""
        return self.analysis
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            'clean_text': self.clean_text,
            'analysis': self.analysis
        }
    
    def get_risk_score(self) -> float:
        """Calculate risk score based on HTML analysis (0-100)."""
        if not self.analysis:
            return 0.0
        
        score = 0.0
        
        # JavaScript presence (0-20 points)
        if self.analysis.get('has_javascript', False):
            score += 20
        
        # Iframes (0-20 points)
        if self.analysis.get('has_iframes', False):
            score += 20
        
        # Forms (0-15 points)
        if self.analysis.get('has_forms', False):
            score += 15
        
        # Hidden elements (0-15 points)
        hidden_count = self.analysis.get('hidden_element_count', 0)
        if hidden_count > 0:
            score += min(hidden_count * 3, 15)
        
        # Low HTML-to-text ratio (0-15 points)
        ratio = self.analysis.get('html_to_text_ratio', 1.0)
        if ratio < 0.1:
            score += 15
        elif ratio < 0.2:
            score += 10
        
        # Excessive links (0-15 points)
        link_count = self.analysis.get('link_count', 0)
        if link_count > 20:
            score += 15
        elif link_count > 10:
            score += 10
        elif link_count > 5:
            score += 5
        
        return min(score, 100.0)
