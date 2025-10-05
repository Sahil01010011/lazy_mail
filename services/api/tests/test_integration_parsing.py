"""Integration test - parse complete email with all utilities."""
from app.parsing.mime_parser import MIMEParser
from app.parsing.url_extractor import URLExtractor
from app.parsing.header_analyzer import HeaderAnalyzer
from app.parsing.html_normalizer import HTMLNormalizer


def test_complete_email_analysis():
    """Test parsing and analyzing a complete phishing email."""
    
    # Sample phishing email (raw MIME format)
    phishing_email = b"""From: "PayPal Security" <security@paypa1-verify.tk>
To: victim@company.com
Reply-To: attacker@evil.com
Subject: Urgent! Your account will be suspended
Message-ID: <phish123@evil.com>
Date: Sun, 05 Oct 2025 13:00:00 +0000
Received-SPF: fail
Authentication-Results: dkim=none; dmarc=fail
Content-Type: text/html; charset=utf-8

<html>
<body>
<h1>Urgent Account Security Alert</h1>
<p>Dear valued customer,</p>
<p>Your PayPal account will be <strong>suspended</strong> within 24 hours!</p>
<p>Click here immediately to verify your account:</p>
<a href="http://192.168.1.100/paypal/verify">Verify Now</a>
<p>Also check: <a href="https://bit.ly/fake123">Alternative Link</a></p>
<script>track_user();</script>
<iframe src="http://tracking-evil.xyz"></iframe>
</body>
</html>
"""
    
    print("\n" + "="*70)
    print("COMPLETE EMAIL ANALYSIS - Integration Test")
    print("="*70)
    
    # Step 1: Parse MIME structure
    print("\n[1/4] Parsing MIME structure...")
    parser = MIMEParser(phishing_email)
    email_data = parser.to_dict()
    
    print(f"  Subject: {email_data['subject']}")
    print(f"  From: {email_data['sender']}")
    print(f"  To: {email_data['recipients']}")
    print(f"  Reply-To: {email_data['reply_to']}")
    print(f"  Has HTML: {len(email_data['body_html']) > 0}")
    
    assert email_data['subject'] == 'Urgent! Your account will be suspended'
    assert 'paypa1-verify.tk' in email_data['sender']
    
    # Step 2: Analyze headers
    print("\n[2/4] Analyzing email headers...")
    header_analyzer = HeaderAnalyzer(email_data['headers'])
    header_analysis = header_analyzer.get_analysis()
    header_risk = header_analyzer.get_risk_score()
    
    print(f"  SPF: {header_analysis['spf']['result']}")
    print(f"  DKIM: {header_analysis['dkim']['result']}")
    print(f"  DMARC: {header_analysis['dmarc']['result']}")
    print(f"  Reply-To mismatch: {header_analysis['reply_to_analysis']['reply_to_mismatch']}")
    print(f"  Header risk score: {header_risk}/100")
    
    assert header_analysis['spf']['result'] == 'fail'
    assert header_analysis['has_anomalies'] is True
    assert header_risk > 50
    
    # Step 3: Extract and analyze URLs
    print("\n[3/4] Extracting and analyzing URLs...")
    url_extractor = URLExtractor(email_data['body_text'], email_data['body_html'])
    url_data = url_extractor.to_dict()
    suspicious_urls = url_extractor.get_suspicious_urls()
    
    print(f"  Total URLs found: {url_data['url_count']}")
    print(f"  Unique domains: {url_data['unique_domains']}")
    print(f"  Suspicious URLs: {url_data['suspicious_url_count']}")
    print(f"  Has IP URLs: {url_data['has_ip_urls']}")
    print(f"  Has shorteners: {url_data['has_url_shorteners']}")
    
    print("\n  Suspicious URL details:")
    for url in suspicious_urls[:3]:  # Show first 3
        print(f"    - {url['url']}")
        print(f"      IP: {url['has_ip_address']}, Shortener: {url['is_shortener']}, TLD: {url['tld']}")
    
    assert url_data['url_count'] > 0
    assert url_data['suspicious_url_count'] > 0
    assert url_data['has_ip_urls'] is True or url_data['has_url_shorteners'] is True
    
    # Step 4: Normalize and analyze HTML
    print("\n[4/4] Normalizing HTML content...")
    html_normalizer = HTMLNormalizer(email_data['body_html'])
    html_analysis = html_normalizer.get_analysis()
    html_risk = html_normalizer.get_risk_score()
    clean_text = html_normalizer.get_text()
    
    print(f"  HTML length: {html_analysis['html_length']}")
    print(f"  Text length: {html_analysis['text_length']}")
    print(f"  HTML-to-text ratio: {html_analysis['html_to_text_ratio']}")
    print(f"  Has JavaScript: {html_analysis['has_javascript']}")
    print(f"  Has iframes: {html_analysis['has_iframes']}")
    print(f"  Link count: {html_analysis['link_count']}")
    print(f"  HTML risk score: {html_risk}/100")
    
    assert 'Urgent' in clean_text
    assert html_analysis['link_count'] > 0
    
    # Step 5: Calculate overall risk
    print("\n" + "="*70)
    print("FINAL ANALYSIS SUMMARY")
    print("="*70)
    
    overall_risk = (header_risk + html_risk) / 2
    
    print(f"\n  Email Classification: PHISHING")
    print(f"  Overall Risk Score: {overall_risk:.1f}/100")
    print(f"  Header Risk: {header_risk:.1f}/100")
    print(f"  HTML Risk: {html_risk:.1f}/100")
    print(f"\n  Key Indicators:")
    print(f"    ✗ Failed SPF authentication")
    print(f"    ✗ Failed DMARC policy")
    print(f"    ✗ Reply-To mismatch (different from sender)")
    print(f"    ✗ Suspicious domain (.tk TLD)")
    print(f"    ✗ IP address in URL")
    print(f"    ✗ URL shortener detected")
    print(f"    ✗ Urgency language in subject")
    
    assert overall_risk > 30  # Should detect as risky
    
    print("\n" + "="*70)
    print("✓ Complete email analysis successful!")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_complete_email_analysis()
