from django.db import models
from .validators import validate_document_file, validate_picture_file


class MembershipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    document = models.FileField(upload_to='documents/', validators=[validate_document_file])
    picture = models.ImageField(upload_to='pictures/', validators=[validate_picture_file])
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.full_name} ({self.email}) - {self.status}"

