from urllib.parse import urlparse

def extract_domain_from_url(url):
    """
    Extract domain from URL
    """
    try:
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        # Remove www. if present
        if domain.startswith('www.'):
            domain = domain[4:]
            
        return domain
    except Exception as e:
        raise ValueError(f"Invalid URL: {str(e)}")