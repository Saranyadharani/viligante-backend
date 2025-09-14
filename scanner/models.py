from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re
from urllib.parse import urlparse

def validate_ssl_grade(value):
    """Validate that SSL grade follows the correct format"""
    valid_grades = ['A+', 'A', 'B', 'C', 'F', 'N/A']
    if value not in valid_grades:
        raise ValidationError(
            f'Invalid SSL grade. Must be one of: {", ".join(valid_grades)}'
        )

class ScanResult(models.Model):
    # URL information
    url = models.URLField(max_length=500)
    domain = models.CharField(max_length=255, blank=True)
    
    # Risk assessment
    risk_level = models.IntegerField(help_text="Risk score from 0-100")
    
    # SSL GRADE (ONLY A+, A, B, C, F)
    ssl_grade = models.CharField(
        max_length=10, 
        default="N/A", 
        help_text="SSL Security Grade (A+, A, B, C, F)",
        validators=[validate_ssl_grade]
    )
    
    # Domain information
    domain_age = models.IntegerField(help_text="Domain age in years")
    domain_created = models.DateField(null=True, blank=True)
    
    # Security metrics
    ssl_valid = models.BooleanField(default=False)
    has_contact_info = models.BooleanField(default=False)
    security_score = models.IntegerField(default=0, help_text="Overall security score 0-100")
    
    # Report card data
    report_card = models.JSONField(default=dict, help_text="Structured report card data")
    
    # Additional metrics
    trust_score = models.IntegerField(default=0, help_text="Trustworthiness score")
    
    # Categorization
    RISK_CATEGORY_CHOICES = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
    ]
    risk_category = models.CharField(max_length=20, choices=RISK_CATEGORY_CHOICES, default='medium')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.url} - SSL: {self.ssl_grade} - Risk: {self.risk_level}%"
    
    def get_ssl_grade_color(self):
        """Return CSS color class based on SSL grade"""
        if self.ssl_grade in ['A+', 'A']:
            return 'success'  # Green - Excellent
        elif self.ssl_grade in ['B', 'C']:
            return 'warning'  # Yellow - Warning
        elif self.ssl_grade == 'F':
            return 'danger'   # Red - Danger
        else:
            return 'secondary'  # Gray - Unknown
    
    def get_ssl_grade_description(self):
        """Return description based on SSL grade"""
        if self.ssl_grade in ['A+', 'A']:
            return "Excellent. This site uses top-tier security. You can browse and shop with confidence."
        elif self.ssl_grade in ['B', 'C']:
            return "Warning. The security is outdated or weak. Be cautious about entering sensitive information."
        elif self.ssl_grade == 'F':
            return "Danger. This site's security is broken or missing. Do not enter any personal details."
        else:
            return "Grade not available."
    
    def save(self, *args, **kwargs):
        # Auto-extract domain from URL
        if self.url and not self.domain:
            parsed_url = urlparse(self.url)
            self.domain = parsed_url.netloc
        
        # Auto-set risk category based on risk_level
        if self.risk_level >= 80:
            self.risk_category = 'critical'
        elif self.risk_level >= 60:
            self.risk_category = 'high'
        elif self.risk_level >= 30:
            self.risk_category = 'medium'
        else:
            self.risk_category = 'low'
            
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']


class SecurityReport(models.Model):
    scan_result = models.ForeignKey(ScanResult, on_delete=models.CASCADE, related_name='security_reports')
    
    # Report sections
    grade_guide = models.TextField(
        default="🟢 A or A+ Grade: Excellent. This site uses top-tier security. You can browse and shop with confidence.\n"
                "🟡 B or C Grade: Warning. The security is outdated or weak. Be cautious about entering sensitive information.\n"
                "🔴 F Grade: Danger. This site's security is broken or missing. Do not enter any personal details.",
        help_text="SSL GRADE GUIDE explanation"
    )
    
    # Recommendations
    recommendations = models.TextField(blank=True, help_text="Security recommendations")
    warnings = models.TextField(blank=True, help_text="Specific warnings")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Security Report for {self.scan_result.url}"


class CommunityReport(models.Model):
    scan_result = models.ForeignKey(ScanResult, on_delete=models.CASCADE, related_name='community_reports')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    accurate = models.BooleanField(default=True, help_text="Whether the report was accurate")
    comments = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        status = "Accurate" if self.accurate else "Inaccurate"
        return f"Community Report for {self.scan_result.url} - {status}"


class CommunityStory(models.Model):
    # Story information
    title = models.CharField(max_length=200, help_text="Title of your story")
    story = models.TextField(help_text="Tell us what happened. Your story could help protect others...")
    
    # Contact information involved in scam (optional)
    website_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        validators=[URLValidator()],
        help_text="Website URL involved in the scam (optional)"
    )
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Phone number involved in the scam (optional)"
    )
    
    # Scam type/category
    SCAM_TYPE_CHOICES = [
        ('tech_support', 'Fake Tech Support'),
        ('phishing', 'Phishing Scam'),
        ('investment', 'Investment Scam'),
        ('social_media', 'Social Media Scam'),
        ('online_shopping', 'Online Shopping Fraud'),
        ('romance', 'Romance Scam'),
        ('lottery', 'Lottery/Sweepstakes'),
        ('other', 'Other Scam Type')
    ]
    scam_type = models.CharField(
        max_length=50, 
        choices=SCAM_TYPE_CHOICES, 
        default='other',
        help_text="Type of scam experienced"
    )
    
    # User information (optional - can submit anonymously)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    author_name = models.CharField(max_length=100, blank=True, help_text="Your name (optional)")
    is_anonymous = models.BooleanField(default=False, help_text="Submit anonymously")
    
    # Status and moderation
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('featured', 'Featured Story'),
        ('rejected', 'Rejected')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_public = models.BooleanField(default=True, help_text="Make this story visible to the community")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_scam_type_display()}"
    
    def save(self, *args, **kwargs):
        # Clean phone number format
        if self.phone_number:
            self.phone_number = re.sub(r'[^\d+]', '', self.phone_number)
        
        # Set anonymous flag if no user and no author name
        if not self.user and not self.author_name:
            self.is_anonymous = True
            
        super().save(*args, **kwargs)
    
    def get_short_story(self):
        """Return abbreviated version of the story for listings"""
        if len(self.story) > 150:
            return self.story[:150] + "..."
        return self.story
    
    def get_display_name(self):
        """Get display name for the story author"""
        if self.is_anonymous:
            return "Anonymous"
        elif self.author_name:
            return self.author_name
        elif self.user:
            return self.user.username
        return "Community Member"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Community Story"
        verbose_name_plural = "Community Stories"