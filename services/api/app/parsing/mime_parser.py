from email import message_from_bytes
from email.message import Message
from email.header import decode_header
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class MIMEParser:
    def __init__(self, raw_email: bytes):
        self.raw_email = raw_email
        self.message: Optional[Message] = None
        self._parse()
    
    def _parse(self):
        try:
            self.message = message_from_bytes(self.raw_email)
        except Exception as e:
            logger.error(f"Failed to parse: {e}")
            raise ValueError(f"Unable to parse email: {e}")
    
    def _decode_header(self, header_value: str) -> str:
        if not header_value:
            return ""
        decoded_parts = []
        for part, encoding in decode_header(header_value):
            if isinstance(part, bytes):
                decoded_parts.append(part.decode(encoding or 'utf-8', errors='ignore'))
            else:
                decoded_parts.append(str(part))
        return ' '.join(decoded_parts)
    
    def get_header(self, name: str, default: str = "") -> str:
        if not self.message:
            return default
        value = self.message.get(name, default)
        return self._decode_header(value) if value else default
    
    def get_headers(self) -> Dict[str, Any]:
        """Extract all email headers."""
        if not self.message:
            return {}
        headers = {}
        for key, value in self.message.items():
            decoded_value = self._decode_header(value)
            if key in headers:
                if isinstance(headers[key], list):
                    headers[key].append(decoded_value)
                else:
                    headers[key] = [headers[key], decoded_value]
            else:
                headers[key] = decoded_value
        return headers
    
    def get_subject(self) -> str:
        return self.get_header('Subject', '')
    
    def get_from(self) -> str:
        return self.get_header('From', '')
    
    def get_to(self) -> List[str]:
        to_header = self.get_header('To', '')
        return [addr.strip() for addr in to_header.split(',') if addr.strip()]
    
    def get_cc(self) -> List[str]:
        """Get CC email addresses."""
        cc_header = self.get_header('Cc', '')
        return [addr.strip() for addr in cc_header.split(',') if addr.strip()]
    
    def get_reply_to(self) -> str:
        """Get Reply-To address."""
        return self.get_header('Reply-To', '')
    
    def get_message_id(self) -> str:
        """Get RFC 5322 Message-ID."""
        return self.get_header('Message-ID', '')
    
    def get_date(self) -> str:
        """Get email date."""
        return self.get_header('Date', '')
    
    def get_body_text(self) -> str:
        if not self.message:
            return ""
        text_parts = []
        if self.message.is_multipart():
            for part in self.message.walk():
                if part.get_content_type() == 'text/plain':
                    payload = part.get_payload(decode=True)
                    if payload:
                        text_parts.append(payload.decode('utf-8', errors='ignore'))
        else:
            if self.message.get_content_type() == 'text/plain':
                payload = self.message.get_payload(decode=True)
                if payload:
                    text_parts.append(payload.decode('utf-8', errors='ignore'))
        return '\n\n'.join(text_parts)
    
    def get_body_html(self) -> str:
        if not self.message:
            return ""
        html_parts = []
        if self.message.is_multipart():
            for part in self.message.walk():
                if part.get_content_type() == 'text/html':
                    payload = part.get_payload(decode=True)
                    if payload:
                        html_parts.append(payload.decode('utf-8', errors='ignore'))
        else:
            if self.message.get_content_type() == 'text/html':
                payload = self.message.get_payload(decode=True)
                if payload:
                    html_parts.append(payload.decode('utf-8', errors='ignore'))
        return '\n\n'.join(html_parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert parsed email to dictionary."""
        return {
            'message_id': self.get_message_id(),
            'subject': self.get_subject(),
            'sender': self.get_from(),
            'recipients': self.get_to(),
            'cc': self.get_cc(),
            'reply_to': self.get_reply_to(),
            'date': self.get_date(),
            'body_text': self.get_body_text(),
            'body_html': self.get_body_html(),
            'headers': self.get_headers(),
            'has_attachments': False,
            'attachment_count': 0
        }
