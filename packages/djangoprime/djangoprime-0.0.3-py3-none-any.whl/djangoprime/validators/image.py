from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ImageDimensionsValidator:
    """
    Validates image dimensions and aspect ratio constraints
    Example usage:
    ImageDimensionsValidator(
        min_width=1200,
        max_width=4096,
        min_height=630,
        max_height=2160,
        min_ratio=1.77,  # 16:9
        max_ratio=1.91   # Open Graph ratio
    )
    """

    def __init__(self, min_width=None, max_width=None,
                 min_height=None, max_height=None,
                 min_ratio=None, max_ratio=None):
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio

    def __call__(self, value):
        if not value:
            return

        try:
            width, height = self._get_image_dimensions(value)
        except (TypeError, AttributeError, Image.DecompressionBombError):
            raise ValidationError(_("Invalid or corrupted image file"))

        errors = []

        # Width validation
        if self.min_width is not None and width < self.min_width:
            errors.append(_("Minimum width required: %(min)s px. Current: %(current)s px") % {
                'min': self.min_width, 'current': width})
        if self.max_width is not None and width > self.max_width:
            errors.append(_("Maximum width allowed: %(max)s px. Current: %(current)s px") % {
                'max': self.max_width, 'current': width})

        # Height validation
        if self.min_height is not None and height < self.min_height:
            errors.append(_("Minimum height required: %(min)s px. Current: %(current)s px") % {
                'min': self.min_height, 'current': height})
        if self.max_height is not None and height > self.max_height:
            errors.append(_("Maximum height allowed: %(max)s px. Current: %(current)s px") % {
                'max': self.max_height, 'current': height})

        # Aspect ratio validation
        if width and height:
            ratio = round(width / height, 2)
            if self.min_ratio is not None and ratio < self.min_ratio:
                errors.append(_("Minimum aspect ratio required: %(min_ratio)s. Current: %(current)s") % {
                    'min_ratio': self.min_ratio, 'current': ratio})
            if self.max_ratio is not None and ratio > self.max_ratio:
                errors.append(_("Maximum aspect ratio allowed: %(max_ratio)s. Current: %(current)s") % {
                    'max_ratio': self.max_ratio, 'current': ratio})

        if errors:
            raise ValidationError(errors)

    def _get_image_dimensions(self, file):
        """Extract dimensions while handling large files safely"""
        try:
            file.seek(0)
            width, height = get_image_dimensions(file)
            if not width or not height:
                raise ValidationError(_("Unable to determine image dimensions"))
            return width, height
        finally:
            file.seek(0)
