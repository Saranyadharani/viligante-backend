def calculate_risk(ssl_data, domain_data):
    """
    Calculate risk score on a scale of 1-100
    Lower score = lower risk, Higher score = higher risk
    """
    risk_score = 0  # Start with 0, we'll add points for risks
    
    # SSL factors (50% weight - 50 points max)
    ssl_grade = ssl_data.get('grade', 'N/A')
    if ssl_grade == 'A':
        risk_score += 0  # Excellent - no risk points
    elif ssl_grade == 'B':
        risk_score += 15  # Good - low risk
    elif ssl_grade == 'C':
        risk_score += 30  # Fair - medium risk
    elif ssl_grade == 'F':
        risk_score += 50  # Poor - high risk
    else:  # N/A or other
        risk_score += 50  # Unknown - assume high risk
    
    # Domain age factors (30% weight - 30 points max)
    domain_age = domain_data.get('age', 0)
    if domain_age > 5:
        risk_score += 0  # Established domain - no risk
    elif domain_age > 2:
        risk_score += 10  # Moderately new - low risk
    elif domain_age > 0:
        risk_score += 20  # New domain - medium risk
    else:
        risk_score += 30  # Unknown age - high risk
    
    # Additional factors (20% weight - 20 points max)
    # Add points for other potential risks
    if ssl_data.get('protocol') in ['TLSv1', 'TLSv1.1']:
        risk_score += 10  # Outdated protocol
    
    if ssl_data.get('days_until_expiry', 0) < 15:
        risk_score += 10  # Expiring very soon
    
    # Ensure score is between 1-100
    risk_score = max(1, min(100, risk_score))
    
    return risk_score