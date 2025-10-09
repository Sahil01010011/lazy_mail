"""Test analysis service with database storage."""
import pytest
from sqlalchemy import select

from app.services.analysis_service import AnalysisService
from app.db.models.message import Message
from app.db.models.verdict import Verdict
from app.db.models.feature import Feature


@pytest.mark.asyncio
async def test_analyze_and_store(db_session):
    """Test complete analysis with database storage."""
    
    # Sample phishing email
    phishing_email = b"""From: security@paypa1.com
To: victim@company.com
Subject: Urgent account verification
Message-ID: <test123@evil.com>
Date: Thu, 09 Oct 2025 12:00:00 +0000

Your account will be suspended! Click: http://192.168.1.1/verify
"""
    
    service = AnalysisService()
    result = await service.analyze_and_store(
        db_session,
        phishing_email,
        source="test"
    )
    
    print("\n=== Analysis Service Test ===")
    print(f"Message ID: {result['message_id']}")
    print(f"Verdict ID: {result['verdict_id']}")
    print(f"Classification: {result['analysis']['verdict']['classification']}")
    print(f"Risk Score: {result['analysis']['verdict']['combined_risk_score']:.1f}")
    
    # Verify message was stored
    message_result = await db_session.execute(
        select(Message).where(Message.id == result['message_id'])
    )
    message = message_result.scalar_one()
    
    assert message is not None
    assert message.subject == "Urgent account verification"
    print(f"✓ Message stored: {message.subject}")
    
    # Verify verdict was stored
    verdict_result = await db_session.execute(
        select(Verdict).where(Verdict.message_id == result['message_id'])
    )
    verdict = verdict_result.scalar_one()
    
    assert verdict is not None
    assert verdict.is_phishing is True
    print(f"✓ Verdict stored: {verdict.classification}")
    
    # Verify features were stored
    feature_result = await db_session.execute(
        select(Feature).where(Feature.message_id == result['message_id'])
    )
    feature = feature_result.scalar_one()
    
    assert feature is not None
    assert feature.features['is_phishing'] is True
    print(f"✓ Features stored: {len(feature.features)} features")
    
    print("\n✓ All data stored successfully!\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_analyze_and_store())
