"""Analysis service - coordinates email analysis and database storage."""
from typing import Dict, Any
from datetime import datetime
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.message import Message
from app.db.models.verdict import Verdict
from app.db.models.feature import Feature
from app.analysis.email_analyzer import EmailAnalyzer

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for analyzing emails and storing results."""
    
    def __init__(self):
        self.analyzer = EmailAnalyzer()
    
    async def analyze_and_store(self, db: AsyncSession, raw_email: bytes, source: str = "manual") -> Dict[str, Any]:
        """Analyze email and store results in database."""
        analysis = await self.analyzer.analyze(raw_email)
        message = await self._store_message(db, raw_email, analysis, source)
        verdict = await self._store_verdict(db, message.id, analysis)
        features = await self._store_features(db, message.id, analysis)
        await db.commit()
        
        logger.info(f"Analyzed email {message.id}: {analysis['verdict']['classification']}")
        
        return {
            'message_id': str(message.id),
            'verdict_id': verdict.id,
            'analysis': analysis
        }
    
    async def _store_message(self, db: AsyncSession, raw_email: bytes, analysis: Dict[str, Any], source: str) -> Message:
        """Store email message using correct Message model fields."""
        from app.parsing.mime_parser import MIMEParser
        
        # Re-parse to get body and headers
        parser = MIMEParser(raw_email)
        email_data = parser.to_dict()
        
        message = Message(
            message_id=analysis['email']['message_id'] or f"generated-{datetime.utcnow().timestamp()}",
            account_id=source,  # Use source as account_id
            subject=analysis['email']['subject'],
            sender=analysis['email']['sender'],
            recipients=analysis['email']['recipients'],
            body_text=email_data['body_text'],
            body_html=email_data['body_html'],
            headers=email_data['headers'],
            spf_result=analysis['analysis']['header']['spf'],
            dkim_result=analysis['analysis']['header']['dkim'],
            dmarc_result=analysis['analysis']['header']['dmarc'],
            received_date=datetime.utcnow(),
            analyzed_at=datetime.utcnow(),
            analysis_status="completed"
        )
        
        db.add(message)
        await db.flush()
        return message
    
    async def _store_verdict(self, db: AsyncSession, message_id, analysis: Dict[str, Any]) -> Verdict:
        """Store analysis verdict."""
        verdict = Verdict(
            message_id=message_id,
            classification=analysis['verdict']['classification'],
            confidence=analysis['verdict']['confidence'],
            risk_score=analysis['verdict']['combined_risk_score'],
            is_phishing=analysis['verdict']['is_phishing'],
            rspamd_score=analysis['analysis']['rspamd']['score'],
            rspamd_action=analysis['analysis']['rspamd']['action'],
            rspamd_symbols=analysis['analysis']['rspamd']['top_symbols'],
            spf_result=analysis['analysis']['header']['spf'],
            dkim_result=analysis['analysis']['header']['dkim'],
            dmarc_result=analysis['analysis']['header']['dmarc'],
            url_count=analysis['analysis']['urls']['total_count'],
            suspicious_url_count=analysis['analysis']['urls']['suspicious_count'],
            analyzed_at=datetime.utcnow(),
            analyzer_version="1.0.0"
        )
        
        db.add(verdict)
        await db.flush()
        return verdict
    
    async def _store_features(self, db: AsyncSession, message_id, analysis: Dict[str, Any]) -> Feature:
        """Store extracted features."""
        features_data = {
            'has_spf': analysis['analysis']['header']['spf'] != 'none',
            'has_dkim': analysis['analysis']['header']['dkim'] != 'none',
            'has_dmarc': analysis['analysis']['header']['dmarc'] != 'none',
            'header_anomalies': analysis['analysis']['header']['has_anomalies'],
            'url_count': analysis['analysis']['urls']['total_count'],
            'suspicious_url_count': analysis['analysis']['urls']['suspicious_count'],
            'has_url_shorteners': analysis['analysis']['urls']['has_shorteners'],
            'has_ip_urls': analysis['analysis']['urls']['has_ip_urls'],
            'html_risk_score': analysis['analysis']['html']['risk_score'],
            'has_javascript': analysis['analysis']['html']['has_javascript'],
            'has_iframes': analysis['analysis']['html']['has_iframes'],
            'rspamd_score': analysis['analysis']['rspamd']['score'],
            'combined_risk': analysis['verdict']['combined_risk_score'],
            'is_phishing': analysis['verdict']['is_phishing']
        }
        
        feature = Feature(
            message_id=message_id,
            feature_type="email_analysis",
            features=features_data,
            extracted_at=datetime.utcnow()
        )
        
        db.add(feature)
        await db.flush()
        return feature
