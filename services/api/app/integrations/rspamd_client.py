"""
Rspamd integration client using normal worker port.
"""
import httpx
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class RspamdClient:
    """Client for interacting with Rspamd spam filter."""
    
    def __init__(self):
        # IMPORTANT: Use port 11333 (normal worker, no auth needed)
        # NOT 11334 (controller, requires auth)
        self.base_url = "http://localhost:11333"
        self.timeout = 10.0
    
    async def check_email(self, raw_email: bytes) -> Dict[str, Any]:
        """Submit email to Rspamd for analysis."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/checkv2",
                    content=raw_email,
                    headers={"Content-Type": "text/plain"}
                )
                
                if response.status_code == 200:
                    return self._parse_response(response.json())
                else:
                    logger.error(f"Rspamd status {response.status_code}: {response.text[:200]}")
                    return self._get_fallback_response(f"HTTP {response.status_code}")
                    
        except httpx.TimeoutException:
            logger.error("Rspamd request timed out")
            return self._get_fallback_response("timeout")
        except Exception as e:
            logger.error(f"Rspamd error: {e}")
            return self._get_fallback_response(str(e))
    
    def _parse_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Rspamd JSON response."""
        symbols = data.get('symbols', {})
        
        symbol_list = []
        for name, info in symbols.items():
            symbol_list.append({
                'name': name,
                'score': info.get('score', 0.0),
                'description': info.get('description', '')
            })
        
        action = data.get('action', 'no action').lower()
        classification = self._action_to_classification(action)
        
        return {
            'score': data.get('score', 0.0),
            'required_score': data.get('required_score', 15.0),
            'action': action,
            'classification': classification,
            'symbols': symbol_list,
            'symbol_names': list(symbols.keys()),
            'is_spam': action in ['reject', 'rewrite subject', 'add header'],
            'is_available': True
        }
    
    def _action_to_classification(self, action: str) -> str:
        """Convert Rspamd action to our classification."""
        action_map = {
            'reject': 'spam',
            'rewrite subject': 'spam',
            'add header': 'suspicious',
            'greylist': 'suspicious',
            'no action': 'ham',
            'soft reject': 'suspicious'
        }
        return action_map.get(action, 'unknown')
    
    def _get_fallback_response(self, error: str) -> Dict[str, Any]:
        """Return fallback response when Rspamd is unavailable."""
        return {
            'score': 0.0,
            'required_score': 15.0,
            'action': 'no action',
            'classification': 'unknown',
            'symbols': [],
            'symbol_names': [],
            'is_spam': False,
            'is_available': False,
            'error': error
        }
    
    async def ping(self) -> bool:
        """Check if Rspamd is available."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/ping")
                return response.status_code == 200
        except Exception:
            return False
