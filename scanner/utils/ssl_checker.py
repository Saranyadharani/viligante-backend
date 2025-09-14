import ssl
import socket
from datetime import datetime

def check_ssl(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                # Get certificate expiration
                expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_until_expiry = (expire_date - datetime.now()).days
                
                # Get protocol version
                protocol = ssock.version()
                
                # Grade the SSL certificate
                grade = calculate_ssl_grade(cert, protocol, days_until_expiry)
                
                return {
                    'grade': grade,
                    'valid': True,
                    'valid_from': cert['notBefore'],
                    'valid_to': cert['notAfter'],
                    'issuer': get_issuer_name(cert),
                    'days_until_expiry': days_until_expiry,
                    'protocol': protocol
                }
    except Exception as e:
        return {'grade': 'N/A', 'error': str(e)}

def calculate_ssl_grade(cert, protocol, days_until_expiry):
    if days_until_expiry <= 0:
        return 'F'  # Expired
    
    if days_until_expiry < 30:
        return 'C'  # Expiring soon
    
    # Check for weak protocols
    if protocol in ['TLSv1', 'TLSv1.1']:
        return 'B'  # Outdated protocol
    
    return 'A'  # Good certificate

def get_issuer_name(cert):
    """Extract issuer name from certificate"""
    if 'issuer' in cert:
        # issuer is a list of tuples
        for field in cert['issuer']:
            if field[0][0] == 'organizationName':
                return field[0][1]
    return 'Unknown'