"""Test complete email analysis."""
import pytest
from app.analysis.email_analyzer import EmailAnalyzer


@pytest.mark.asyncio
async def test_phishing_email_analysis():
    """Test complete analysis of a phishing email."""
    
    phishing_email = b"""From: "PayPal Security" <security@paypa1-verify.tk>
To: victim@company.com
Reply-To: attacker@evil.com
Subject: URGENT! Account will be suspended
Message-ID: <phish123@evil.com>
Date: Thu, 09 Oct 2025 12:00:00 +0000
Received-SPF: fail
Authentication-Results: dkim=none; dmarc=fail
Content-Type: text/html

<html><body>
<h1>URGENT Account Alert!</h1>
<p>Your account will be SUSPENDED within 24 hours!</p>
<a href="http://192.168.1.100/paypal/verify">Verify Now</a>
<a href="https://bit.ly/fake123">Alternative Link</a>
</body></html>
"""
    
    analyzer = EmailAnalyzer()
    result = await analyzer.analyze(phishing_email)
    
    print("\n" + "="*70)
    print("COMPLETE PHISHING EMAIL ANALYSIS")
    print("="*70)
    
    print("\n📧 EMAIL INFO:")
    print(f"  Subject: {result['email']['subject']}")
    print(f"  From: {result['email']['sender']}")
    
    print("\n🔍 HEADER ANALYSIS:")
    print(f"  Risk Score: {result['analysis']['header']['risk_score']}/100")
    print(f"  SPF: {result['analysis']['header']['spf']}")
    print(f"  DKIM: {result['analysis']['header']['dkim']}")
    print(f"  DMARC: {result['analysis']['header']['dmarc']}")
    
    print("\n🔗 URL ANALYSIS:")
    print(f"  Total URLs: {result['analysis']['urls']['total_count']}")
    print(f"  Suspicious: {result['analysis']['urls']['suspicious_count']}")
    print(f"  Has shorteners: {result['analysis']['urls']['has_shorteners']}")
    print(f"  Has IP URLs: {result['analysis']['urls']['has_ip_urls']}")
    
    print("\n📄 HTML ANALYSIS:")
    print(f"  Risk Score: {result['analysis']['html']['risk_score']}/100")
    print(f"  Links: {result['analysis']['html']['link_count']}")
    
    print("\n🛡️  RSPAMD ANALYSIS:")
    print(f"  Score: {result['analysis']['rspamd']['score']}")
    print(f"  Action: {result['analysis']['rspamd']['action']}")
    print(f"  Is Spam: {result['analysis']['rspamd']['is_spam']}")
    if result['analysis']['rspamd']['available']:
        print(f"  Symbols: {len(result['analysis']['rspamd']['top_symbols'])}")
    
    print("\n⚖️  FINAL VERDICT:")
    print(f"  Classification: {result['verdict']['classification'].upper()}")
    print(f"  Combined Risk: {result['verdict']['combined_risk_score']:.1f}/100")
    print(f"  Confidence: {result['verdict']['confidence']:.1f}%")
    print(f"  Is Phishing: {result['verdict']['is_phishing']}")
    print(f"  Action: {result['verdict']['recommended_action'].upper()}")
    
    print("\n" + "="*70)
    
    # Assertions
    assert result['verdict']['is_phishing'] is True
    assert result['verdict']['combined_risk_score'] > 50
    print("\n✓ Phishing correctly detected!\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_phishing_email_analysis())
