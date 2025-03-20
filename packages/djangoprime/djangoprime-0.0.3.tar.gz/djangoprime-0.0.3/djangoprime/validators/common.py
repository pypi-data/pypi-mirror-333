from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

@deconstructible
class KeywordLimitValidator:
    """
    Validates maximum number of keywords in JSON array
    Example usage: KeywordLimitValidator(10)  # Max 10 keywords
    """

    def __init__(self, max_keywords):
        self.max_keywords = max_keywords

    def __call__(self, value):
        if not isinstance(value, list):
            raise ValidationError(_("Keywords must be a JSON array"))

        if len(value) > self.max_keywords:
            raise ValidationError(
                _("Too many keywords. Maximum allowed: %(max)s. Current: %(current)s") % {
                    'max': self.max_keywords,
                    'current': len(value)
                }
            )

        if any(not isinstance(kw, str) for kw in value):
            raise ValidationError(_("All keywords must be strings"))

        if any(len(kw) > 50 for kw in value):
            raise ValidationError(_("Keywords cannot exceed 50 characters"))
