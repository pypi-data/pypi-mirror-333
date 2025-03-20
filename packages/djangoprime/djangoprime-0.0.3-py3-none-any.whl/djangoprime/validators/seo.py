from dateutil.parser import parse as parse_date

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class AdvancedSchemaMarkupValidator:
    """
    An advanced JSON‑LD schema markup validator that acts like Django’s built‑in validators.

    It validates structured JSON‑LD data (either a single object or list of objects) for common
    schema types (Article, Product, Organization, Person, Event). It supports:
      - Multiple types in the '@type' field (string or list)
      - Recursive validation of nested objects (e.g. 'offers' in Product)
      - Data type checking and basic date/time parsing for fields suggesting date/time content

    To extend, simply update the SCHEMA_DEFINITIONS dictionary.
    """

    message = _('Invalid JSON‑LD structured data')
    code = 'invalid'

    SCHEMA_DEFINITIONS = {
        'Article': {
            'required': {
                'headline': str,
                'datePublished': str,
            },
        },
        'Product': {
            'required': {
                'name': str,
                'description': str,
                'offers': {
                    'required': {
                        'price': (int, float, str),  # Accept numeric or string representations
                        'priceCurrency': str,
                    }
                }
            },
        },
        'Organization': {
            'required': {
                'name': str,
                'logo': str,
                'url': str,
            },
        },
        'Person': {
            'required': {
                'name': str,
                'jobTitle': str,
            },
        },
        'Event': {
            'required': {
                'name': str,
                'startDate': str,
                'location': {
                    'required': {
                        'name': str,
                        'address': dict,  # For further enhancement, address can be validated in-depth.
                    }
                }
            },
        },
    }

    def __init__(self, schema_definitions=None):
        """
        Optionally override the default schema definitions.
        """
        self.schema_definitions = schema_definitions or self.SCHEMA_DEFINITIONS

    def __call__(self, value):
        errors = []
        if isinstance(value, list):
            for index, item in enumerate(value):
                if not isinstance(item, dict):
                    errors.append(
                        _("Item at index %(index)d is not a valid JSON object") % {'index': index}
                    )
                else:
                    item_errors = self.validate_single_schema(item)
                    if item_errors:
                        errors.append(
                            _("Errors in item at index %(index)d: %(errors)s") %
                            {'index': index, 'errors': "; ".join(item_errors)}
                        )
        elif isinstance(value, dict):
            errors.extend(self.validate_single_schema(value))
        else:
            raise ValidationError(_("Structured data must be a valid JSON object or a list of objects"))

        if errors:
            raise ValidationError(errors)

    def validate_field(self, value, expected, path):
        errors = []
        if isinstance(expected, dict):
            if not isinstance(value, dict):
                errors.append(_("Field '%(field)s' must be an object") % {'field': path})
            else:
                errors.extend(self.validate_object_against_schema(value, expected, path=path + "."))
        else:
            expected_types = expected if isinstance(expected, tuple) else (expected,)
            if not any(isinstance(value, t) for t in expected_types):
                errors.append(
                    _("Field '%(field)s' should be of type %(expected)s but got %(actual)s") %
                    {'field': path, 'expected': ', '.join([t.__name__ for t in expected_types]), 'actual': type(value).__name__}
                )
            # Attempt basic date/time parsing if field name implies date/time content.
            if 'date' in path.lower() or 'time' in path.lower():
                try:
                    parse_date(value)
                except Exception:
                    errors.append(_("Field '%(field)s' must be a valid date/time string") % {'field': path})
        return errors

    def validate_object_against_schema(self, obj, schema_definition, path=''):
        errors = []
        required_fields = schema_definition.get('required', {})
        for field, expected in required_fields.items():
            current_path = f"{path}{field}"
            if field not in obj:
                errors.append(
                    _("Missing required field '%(field)s' at path '%(path)s'") %
                    {'field': field, 'path': path.rstrip('.') or 'root'}
                )
            else:
                errors.extend(self.validate_field(obj[field], expected, current_path))
        return errors

    def validate_single_schema(self, obj):
        errors = []
        if '@type' not in obj:
            errors.append(_("Missing '@type' property"))
            return errors

        types = obj.get('@type')
        if isinstance(types, str):
            types = [types]
        elif not isinstance(types, list):
            errors.append(_("Property '@type' must be a string or list"))
            return errors

        for schema_type in types:
            if schema_type in self.schema_definitions:
                errors.extend(self.validate_object_against_schema(obj, self.schema_definitions[schema_type]))
            else:
                errors.append(
                    _("No advanced schema definition available for type '%(type)s'. Skipping detailed validation for this type.") %
                    {'type': schema_type}
                )
        return errors

    def __eq__(self, other):
        return isinstance(other, AdvancedSchemaMarkupValidator) and self.schema_definitions == other.schema_definitions
