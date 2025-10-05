"""Test header analyzer."""
from app.parsing.header_analyzer import HeaderAnalyzer


def test_authentication_checks():
    """Test SPF/DKIM/DMARC checks."""
    headers = {
        'From': 'sender@example.com',
        'Received-SPF': 'pass (domain of example.com designates sender)',
        'Authentication-Results': 'dkim=pass; dmarc=pass',
        'DKIM-Signature': 'v=1; a=rsa-sha256; d=example.com'
    }
    
    analyzer = HeaderAnalyzer(headers)
    analysis = analyzer.get_analysis()
    
    print("\n=== Authentication Checks ===")
    print(f"SPF: {analysis['spf']['result']}")
    print(f"DKIM: {analysis['dkim']['result']}")
    print(f"DMARC: {analysis['dmarc']['result']}")
    print(f"Has anomalies: {analysis['has_anomalies']}")
    print(f"Risk score: {analyzer.get_risk_score()}")
    
    assert analysis['spf']['result'] == 'pass'
    assert analysis['dkim']['result'] == 'pass'
    assert analysis['has_anomalies'] is False
    print("✓ Authentication checks work!\n")


def test_phishing_detection():
    """Test detection of phishing indicators."""
    headers = {
        'From': 'security@paypa1.com',
        'Reply-To': 'attacker@evil.com',
        'Received-SPF': 'fail',
        'Authentication-Results': 'dkim=none; dmarc=fail'
    }
    
    analyzer = HeaderAnalyzer(headers)
    analysis = analyzer.get_analysis()
    risk_score = analyzer.get_risk_score()
    
    print("=== Phishing Detection ===")
    print(f"SPF: {analysis['spf']['result']}")
    print(f"DKIM: {analysis['dkim']['result']}")
    print(f"DMARC: {analysis['dmarc']['result']}")
    print(f"Reply-To mismatch: {analysis['reply_to_analysis']['reply_to_mismatch']}")
    print(f"Has anomalies: {analysis['has_anomalies']}")
    print(f"Risk score: {risk_score}")
    
    assert analysis['has_anomalies'] is True
    assert risk_score > 50
    print("✓ Phishing detection works!\n")


def test_display_name_spoofing():
    """Test detection of display name spoofing."""
    headers = {
        'From': '"admin@paypal.com" <attacker@evil.com>',
        'Authentication-Results': 'dkim=pass; dmarc=pass'
    }
    
    analyzer = HeaderAnalyzer(headers)
    analysis = analyzer.get_analysis()
    
    print("=== Display Name Spoofing ===")
    print(f"Display name: {analysis['sender_analysis']['display_name']}")
    print(f"Actual email: {analysis['sender_analysis']['email']}")
    print(f"Display name mismatch: {analysis['sender_analysis']['display_name_mismatch']}")
    
    assert analysis['sender_analysis']['display_name_mismatch'] is True
    print("✓ Display name spoofing detected!\n")


if __name__ == "__main__":
    print("Running Header Analyzer Tests...\n")
    test_authentication_checks()
    test_phishing_detection()
    test_display_name_spoofing()
    print("=== All Header Analyzer Tests Passed! ===")
