import os
from django.core.exceptions import ValidationError

def validate_document_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file type. Only {", ".join(valid_extensions)} are allowed.')

def validate_picture_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file type. Only {", ".join(valid_extensions)} are allowed.')
