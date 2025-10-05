"""Test MIME parser with sample emails."""
from app.parsing.mime_parser import MIMEParser


def test_simple_email():
    """Test parsing a simple email."""
    raw_email = b"""From: sender@example.com
To: recipient@example.com
Subject: Test Email
Message-ID: <test123@example.com>
Date: Sun, 05 Oct 2025 12:00:00 +0000

This is a test email body.
"""
    
    parser = MIMEParser(raw_email)
    data = parser.to_dict()
    
    print("\n=== MIME Parser Test Results ===\n")
    print(f"Sender: {data['sender']}")
    print(f"Recipients: {data['recipients']}")
    print(f"Subject: {data['subject']}")
    print(f"Message-ID: {data['message_id']}")
    print(f"Body Text: {data['body_text'][:50]}...")
    print(f"Has Attachments: {data['has_attachments']}")
    
    # Assertions
    assert data['sender'] == 'sender@example.com', "Sender mismatch!"
    assert 'recipient@example.com' in data['recipients'], "Recipient not found!"
    assert data['subject'] == 'Test Email', "Subject mismatch!"
    assert 'test email body' in data['body_text'].lower(), "Body not found!"
    assert data['has_attachments'] is False, "Should have no attachments!"
    
    print("\n✓ All tests passed!\n")


def test_phishing_email():
    """Test parsing a phishing email sample."""
    phishing_email = b"""From: security@paypa1.com
To: victim@company.com
Subject: Urgent! Verify your account now
Message-ID: <phish456@evil.com>
Date: Sun, 05 Oct 2025 11:00:00 +0000
Content-Type: text/html; charset=utf-8

<html>
<body>
<p>Dear user,</p>
<p>Your account will be suspended! Click here to verify:</p>
<a href="http://phishing-site.com/verify">Verify Now</a>
</body>
</html>
"""
    
    parser = MIMEParser(phishing_email)
    data = parser.to_dict()
    
    print("\n=== Phishing Email Test Results ===\n")
    print(f"Sender: {data['sender']}")
    print(f"Subject: {data['subject']}")
    print(f"HTML Body: {data['body_html'][:100]}...")
    
    # Assertions
    assert 'paypa1.com' in data['sender'], "Sender domain not found!"
    assert 'Urgent' in data['subject'], "Urgency keyword not found!"
    assert 'phishing-site.com' in data['body_html'], "Phishing URL not found!"
    
    print("\n✓ Phishing email parsed correctly!\n")


if __name__ == "__main__":
    print("Running MIME Parser Tests...")
    test_simple_email()
    test_phishing_email()
    print("=== All Tests Passed! ===")
