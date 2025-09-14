from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import ScanResult  # Make sure this import exists
from .utils.url_parser import extract_domain_from_url
from .utils.ssl_checker import check_ssl
from .utils.domain_checker import get_domain_age
from .utils.risk_calculator import calculate_risk

@csrf_exempt
@require_POST
def scan_url(request):
    try:
        data = json.loads(request.body)
        url = data.get('url', '').strip()
        
        if not url:
            return JsonResponse({'error': 'URL is required'}, status=400)
        
        domain = extract_domain_from_url(url)
        
        # Perform security checks
        ssl_data = check_ssl(domain)
        domain_data = get_domain_age(domain)
        risk_level = calculate_risk(ssl_data, domain_data)
        
        # Determine risk category based on risk level
        if risk_level >= 80:
            risk_category = 'critical'
        elif risk_level >= 60:
            risk_category = 'high'
        elif risk_level >= 30:
            risk_category = 'medium'
        else:
            risk_category = 'low'
        
        # ✅ SAVE TO DATABASE - Create ScanResult object
        scan_result = ScanResult.objects.create(
            url=url,
            domain=domain,
            risk_level=risk_level,
            risk_category=risk_category,
            ssl_grade=ssl_data.get('grade', 'N/A'),
            domain_age=domain_data.get('age', 0),
            # Add other fields if available from your checks
            ssl_valid=ssl_data.get('valid', False),
            security_score=100 - risk_level,  # Inverse of risk level
            trust_score=max(0, 100 - risk_level)  # Higher risk = lower trust
        )
        
        # Prepare response data
        response_data = {
            'riskLevel': risk_level,
            'riskCategory': risk_category,
            'sslGrade': ssl_data.get('grade', 'N/A'),
            'domainAge': domain_data.get('age', 0),
            'domain': domain,
            'scanId': scan_result.id,  # Include the database ID
            'message': 'Scan completed and saved to database'
        }
        
        return JsonResponse(response_data)
        
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Internal server error: ' + str(e)}, status=500)