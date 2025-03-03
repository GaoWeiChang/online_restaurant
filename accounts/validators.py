import os
from django.core.exceptions import ValidationError

# file validation
def allow_only_images_validator(value):
    extension = os.path.splitext(value.name)[1] # extension (.jpg,.png...)
    print(extension)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not extension.lower() in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Only {str(valid_extensions)} extensions are allowed.')
    