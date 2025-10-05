"""Test CRUD operations on Message model."""
import asyncio
from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.db.models.message import Message
from app.db.models.verdict import Verdict


async def test_crud():
    """Test Create, Read, Update, Delete operations."""
    
    async with AsyncSessionLocal() as session:
        print("=== Testing CRUD Operations ===\n")
        
        # CREATE
        print("[1/4] Creating test message...")
        test_message = Message(
            message_id=f"test-{uuid4()}@example.com",
            account_id="test@gmail.com",
            subject="Test Phishing Email",
            sender="attacker@evil.com",
            recipients=["victim@company.com"],
            body_text="Urgent! Click here to verify your account!",
            body_html="<p>Urgent! <a href='http://phish.com'>Click here</a></p>",
            headers={"From": "attacker@evil.com", "To": "victim@company.com"},
            has_attachments=False,
            attachment_count=0,
            spf_result="fail",
            dkim_result="none",
            dmarc_result="fail",
            received_date=datetime.utcnow(),
            analysis_status="pending"
        )
        
        session.add(test_message)
        await session.commit()
        await session.refresh(test_message)
        print(f"✓ Created message with ID: {test_message.id}")
        print(f"  Message-ID: {test_message.message_id}")
        print(f"  Subject: {test_message.subject}\n")
        
        # READ
        print("[2/4] Reading message from database...")
        result = await session.execute(
            select(Message).where(Message.id == test_message.id)
        )
        retrieved_message = result.scalar_one()
        print(f"✓ Retrieved message: {retrieved_message.message_id}")
        print(f"  Sender: {retrieved_message.sender}")
        print(f"  SPF: {retrieved_message.spf_result}\n")
        
        # UPDATE
        print("[3/4] Updating message status...")
        retrieved_message.analysis_status = "completed"
        retrieved_message.analyzed_at = datetime.utcnow()
        await session.commit()
        print(f"✓ Updated status to: {retrieved_message.analysis_status}\n")
        
        # CREATE VERDICT
        print("[3.5/4] Creating verdict for message...")
        verdict = Verdict(
            message_id=test_message.id,
            classification="phishing",
            confidence=0.95,
            risk_score=87.5,
            rspamd_score=12.5,
            rspamd_action="reject",
            rspamd_symbols=["PHISHING_URL", "SPF_FAIL", "DMARC_FAIL"],
            auth_score=10.0,
            url_score=25.0,
            content_score=35.0,
            stylometry_score=17.5,
            explanation=[
                "SPF authentication failed",
                "Suspicious URL detected",
                "High urgency language"
            ],
            threat_indicators=["phish.com", "urgent language"],
            action_taken="quarantine"
        )
        session.add(verdict)
        await session.commit()
        print(f"✓ Created verdict: {verdict.classification} (risk: {verdict.risk_score})\n")
        
        # READ with relationship
        print("[3.8/4] Reading message with verdict...")
        result = await session.execute(
            select(Message).where(Message.id == test_message.id)
        )
        message_with_verdict = result.scalar_one()
        
        result = await session.execute(
            select(Verdict).where(Verdict.message_id == message_with_verdict.id)
        )
        related_verdict = result.scalar_one()
        print(f"✓ Message: {message_with_verdict.subject}")
        print(f"  Verdict: {related_verdict.classification}")
        print(f"  Risk Score: {related_verdict.risk_score}\n")
        
        # DELETE
        print("[4/4] Deleting test data...")
        await session.delete(related_verdict)
        await session.delete(message_with_verdict)
        await session.commit()
        print("✓ Deleted test message and verdict\n")
        
        # Verify deletion
        result = await session.execute(
            select(Message).where(Message.id == test_message.id)
        )
        deleted_message = result.scalar_one_or_none()
        
        if deleted_message is None:
            print("✓ Verified: Message no longer exists in database\n")
        else:
            print("✗ Error: Message still exists!\n")
    
    print("=== All CRUD operations successful! ===")


if __name__ == "__main__":
    asyncio.run(test_crud())
