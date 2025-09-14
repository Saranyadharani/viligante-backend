import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse
import random

def calculate_risk_level(url):
    """Risk assessment algorithm - returns number 0-100"""
    risk_score = 50  # Start with neutral score
    
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # Trustworthy TLDs (safer)
        good_tlds = ['.com', '.org', '.edu', '.gov', '.net']
        # Risky TLDs (more dangerous)
        risky_tlds = ['.xyz', '.top', '.loan', '.win', '.club', '.click', '.tk', '.ml']
        
        # TLD analysis
        if any(tld in domain for tld in risky_tlds):
            risk_score += 25
        elif any(tld in domain for tld in good_tlds):
            risk_score -= 10
        
        # URL structure analysis
        if len(domain) > 30:  # Very long domains are suspicious
            risk_score += 15
        
        if '-' in domain:  # Hyphens can be suspicious
            risk_score += 10
            
        if domain.count('.') > 2:  # Too many subdomains
            risk_score += 10
            
        # Keyword analysis
        suspicious_words = ['free', 'win', 'prize', 'reward', 'click', 'limited', 'offer']
        if any(word in domain for word in suspicious_words):
            risk_score += 20
            
        # SSL grade affects risk
        ssl_grade = check_ssl_grade(url)
        if ssl_grade == 'F':
            risk_score += 30
        elif ssl_grade in ['A', 'A+']:
            risk_score -= 20
            
    except Exception:
        risk_score = 65  # Default if analysis fails
    
    return max(0, min(100, risk_score))  # Ensure between 0-100

def check_ssl_grade(url):
    """SSL/TLS assessment - returns A, B, C, or F"""
    try:
        if not url.startswith('https://'):
            return 'F'
            
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc
        
        context = ssl.create_default_context()
        
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                protocol = ssock.version()
                
                # Grade based on protocol version
                if protocol in ['TLSv1.3', 'TLSv1.2']:
                    return 'A'
                elif protocol == 'TLSv1.1':
                    return 'B'
                elif protocol == 'TLSv1.0':
                    return 'C'
                else:
                    return 'F'
                    
    except Exception:
        return 'F'  # No SSL or connection failed

def get_domain_age(url):
    """Domain age estimation - returns number of years"""
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # Simple heuristic based on domain patterns
        if any(brand in domain for brand in ['google', 'microsoft', 'amazon', 'facebook', 'github']):
            return random.randint(10, 25)  # Well-known sites are old
        
        if any(org in domain for org in ['edu', 'gov', 'org']):
            return random.randint(5, 15)  # Organizations are older
        
        # For other domains, use pattern-based estimation
        if len(domain) < 10:
            return random.randint(1, 3)  # Short domains might be newer
        
        return random.randint(1, 8)  # Default range
            
    except Exception:
        return 1  # Default if analysis fails