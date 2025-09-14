import whois
from datetime import datetime

def get_domain_age(domain):
    try:
        # Query WHOIS information
        domain_info = whois.whois(domain)
        
        # Get creation date (handle cases where it might be a list)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        
        if creation_date:
            # Calculate age in years
            age_delta = datetime.now() - creation_date
            age_years = age_delta.days / 365.25
            
            return {
                'age': int(age_years),
                'created': creation_date.strftime('%Y-%m-%d'),
                'registrar': domain_info.registrar or 'Unknown',
                'expiration': domain_info.expiration_date.strftime('%Y-%m-%d') if domain_info.expiration_date else 'Unknown'
            }
        else:
            return {'age': 0, 'error': 'Creation date not found'}
            
    except Exception as e:
        return {'age': 0, 'error': str(e)}