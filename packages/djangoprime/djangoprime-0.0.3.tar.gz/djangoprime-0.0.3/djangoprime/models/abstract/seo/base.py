from django.core.validators import (
    MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoprime.models.abstract.seo.open_graph import SeoOpenGraphModel
from djangoprime.models.abstract.seo.twitter_card import SeoTwitterCardModel
from djangoprime.models.choices.seo import SEOChangeFreqChoices
from djangoprime.validators import KeywordLimitValidator, AdvancedSchemaMarkupValidator


class SeoBaseModel(SeoOpenGraphModel, SeoTwitterCardModel):
    meta_title = models.CharField(
        _("Meta Title"),
        max_length=120,
        validators=[MinLengthValidator(30), MaxLengthValidator(120)],
        help_text=_("Primary title for SERPs (include primary keyword)"),
    )
    meta_description = models.TextField(
        _("Meta Description"),
        max_length=320,
        validators=[MinLengthValidator(150), MaxLengthValidator(320)],
        help_text=_("Compelling summary for search results (include keywords naturally)"),
    )
    meta_keywords = models.JSONField(
        _("Meta Keywords"),
        default=list,
        validators=[KeywordLimitValidator(10)],
        help_text=_("List of focus keywords (max 10)"),
    )
    canonical_url = models.URLField(
        _("Canonical URL"),
        max_length=2048,
        blank=True,
        help_text=_("Canonical URL to prevent duplicate content (auto-generated if blank)"),
    )
    robots_meta = models.JSONField(
        _("Robots Meta"),
        default=dict,
        help_text=_("Key-value pairs for robots meta tags (e.g., {'googlebot': 'noarchive'})"),
    )
    priority = models.DecimalField(
        _("Sitemap Priority"),
        max_digits=3,
        decimal_places=2,
        default=0.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )
    change_frequency = models.CharField(
        _("Change Frequency"),
        max_length=25,
        choices=SEOChangeFreqChoices.choices,
        default=SEOChangeFreqChoices.WEEKLY.value,
        help_text=_(
            "Indicates how frequently this content is updated. This setting informs search engines and sitemap generators about the expected update frequency (e.g., daily, weekly, monthly)."
        ),
    )
    auto_generate_structured_data = models.BooleanField(
        _("Auto-generate Schema.org Markup"),
        default=True,
        help_text=_(
            "If enabled, the Schema.org markup (JSON‑LD) for rich snippets will be automatically generated from the available Open Graph metadata. "
            "If disabled, you can provide custom markup in the structured_data field."
        ),
    )
    structured_data = models.JSONField(
        _("Schema.org Markup"),
        blank=True,
        null=True,
        default=dict,
        validators=[AdvancedSchemaMarkupValidator()],
        help_text=_(
            "JSON‑LD structured data for rich snippets. If auto-generation is enabled, this field will be populated automatically from your Open Graph data."
        ),
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['meta_title']),
        ]

    def get_seo_score(self):
        """Calculate SEO quality score."""
        raise NotImplementedError("SEO score calculation not implemented.")

    def get_meta_tags(self):
        """Generate meta tags."""
        raise NotImplementedError("Meta tags generation not implemented.")

    def get_canonical_url(self):
        """Generate canonical URL."""
        raise NotImplementedError("Canonical URL generation not implemented.")
