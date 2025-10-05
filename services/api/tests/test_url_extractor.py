"""Test URL extractor."""
from app.parsing.url_extractor import URLExtractor


def test_basic_url_extraction():
    """Test basic URL extraction from text."""
    text = """
    Please visit https://example.com for more info.
    Also check www.test.com
    Or click http://phishing-site.xyz/login
    """
    
    extractor = URLExtractor(text)
    urls = extractor.get_urls()
    
    print("\n=== Basic URL Extraction ===")
    print(f"Found {len(urls)} URLs:")
    for url in urls:
        print(f"  - {url['url']}")
        print(f"    Domain: {url['domain']}, TLD: {url['tld']}")
    
    assert len(urls) >= 3
    print("✓ Basic extraction works!\n")


def test_phishing_url_detection():
    """Test detection of suspicious URLs."""
    text = """
    Verify your account: http://paypa1.com.phishing-site.tk/verify
    Click here: http://192.168.1.1/login
    Short link: https://bit.ly/abc123
    """
    
    extractor = URLExtractor(text)
    suspicious = extractor.get_suspicious_urls()
    
    print("=== Phishing URL Detection ===")
    print(f"Found {len(suspicious)} suspicious URLs:")
    for url in suspicious:
        print(f"  - {url['url']}")
        print(f"    Shortener: {url['is_shortener']}")
        print(f"    Suspicious TLD: {url['is_suspicious_tld']}")
        print(f"    IP Address: {url['has_ip_address']}")
    
    assert len(suspicious) > 0
    print("✓ Phishing detection works!\n")


def test_html_url_extraction():
    """Test URL extraction from HTML."""
    html = '''
    <a href="https://legitimate-site.com">Click here</a>
    <a href="http://evil-phishing.xyz/steal">Verify Account</a>
    '''
    
    extractor = URLExtractor("", html)
    urls = extractor.get_urls()
    
    print("=== HTML URL Extraction ===")
    print(f"Found {len(urls)} URLs from HTML:")
    for url in urls:
        print(f"  - {url['url']}")
    
    assert len(urls) == 2
    print("✓ HTML extraction works!\n")


if __name__ == "__main__":
    print("Running URL Extractor Tests...\n")
    test_basic_url_extraction()
    test_phishing_url_detection()
    test_html_url_extraction()
    print("=== All URL Extractor Tests Passed! ===")
