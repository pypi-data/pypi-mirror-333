from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator:
    """
    Validates file size against maximum allowed MB
    Example usage: FileSizeValidator(5)  # 5MB max
    """

    def __init__(self, max_size_mb):
        self.max_size_bytes = max_size_mb * 1024 * 1024

    def __call__(self, value):
        if value and hasattr(value, 'size'):
            if value.size > self.max_size_bytes:
                raise ValidationError(
                    _("Maximum file size exceeded. Allowed: %(max)s MB. Current: %(current)s MB") % {
                        'max': self.max_size_bytes // (1024 * 1024),
                        'current': round(value.size / (1024 * 1024), 2)
                    }
                )
