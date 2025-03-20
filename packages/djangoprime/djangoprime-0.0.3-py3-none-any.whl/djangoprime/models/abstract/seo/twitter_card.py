from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxLengthValidator, RegexValidator
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoprime.models.choices.seo import TwitterCardTypeChoices
from djangoprime.config import MAX_IMAGE_SIZE_MB
from djangoprime.validators import ImageDimensionsValidator, FileSizeValidator


class SeoTwitterCardModel(models.Model):
    TWITTER_HANDLE_VALIDATOR = RegexValidator(
        r'^@?(\w){1,15}$',
        _("Enter a valid Twitter handle (@username)")
    )

    twitter_card = models.CharField(
        _("Twitter Card Type"),
        max_length=20,
        choices=TwitterCardTypeChoices.choices,
        default=TwitterCardTypeChoices.SUMMARY_LARGE_IMAGE.value,
        help_text=_("Type of Twitter card to use")
    )
    twitter_title = models.CharField(
        _("Title"),
        max_length=70,
        blank=True,
        validators=[MaxLengthValidator(70)],
        help_text=_("Title for Twitter card (70 characters max)")
    )
    twitter_description = models.TextField(
        _("Description"),
        max_length=200,
        blank=True,
        validators=[MaxLengthValidator(200)],
        help_text=_("Description for Twitter card (200 characters max)")
    )
    twitter_site = models.CharField(
        _("Site Handle"),
        max_length=15,
        blank=True,
        validators=[TWITTER_HANDLE_VALIDATOR],
        help_text=_("Your site's Twitter handle (@username)")
    )
    twitter_creator = models.CharField(
        _("Creator Handle"),
        max_length=15,
        blank=True,
        validators=[TWITTER_HANDLE_VALIDATOR],
        help_text=_("Content creator's Twitter handle (@username)")
    )
    # Media Properties
    twitter_image = models.ImageField(
        _("Card Image"),
        upload_to="twitter_cards/",
        blank=True,
        validators=[
            ImageDimensionsValidator(min_width=1200, min_height=628, max_ratio=1.91, min_ratio=1.91),
            FileSizeValidator(MAX_IMAGE_SIZE_MB)
        ],
        help_text=_("Main image for Twitter card (1200×628px JPG/PNG)")
    )
    twitter_image_alt = models.CharField(
        _("Image Alt Text"),
        max_length=420,
        blank=True,
        validators=[MaxLengthValidator(420)],
        help_text=_("Alt text for visually impaired (420 characters max)")
    )

    # Player Properties
    twitter_player = models.URLField(
        _("Player URL"),
        blank=True,
        help_text=_("HTTPS URL to iframe player (required for Player cards)")
    )
    twitter_player_ratio = models.CharField(
        _("Aspect Ratio"),
        max_length=10,
        blank=True,
        choices=[('16:9', '16:9'), ('4:3', '4:3'), ('1:1', '1:1')],
        help_text=_("Player aspect ratio")
    )

    # Engagement Tracking
    twitter_cta = models.CharField(
        _("Call to Action"),
        max_length=50,
        blank=True,
        choices=[('watch', 'Watch Video'), ('read', 'Read More'), ('shop', 'Shop Now')],
        help_text=_("Primary CTA for engagement tracking")
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['twitter_card']),
            models.Index(fields=['twitter_site']),
        ]

    def clean(self):
        super().clean()
        # Validate card-specific requirements
        if self.twitter_card == TwitterCardTypeChoices.PLAYER.value:
            if not self.twitter_player:
                raise ValidationError({'twitter_player': _("Required for Player cards")})
            if not self.twitter_player_ratio:
                raise ValidationError({'twitter_player_ratio': _("Aspect ratio required for Player cards")})
        if self.twitter_card in [TwitterCardTypeChoices.SUMMARY_LARGE_IMAGE.value,
                                 TwitterCardTypeChoices.SUMMARY.value] and not self.twitter_image:
            raise ValidationError({'twitter_image': _("Required for Summary cards")})

    def get_twitter_card_json_data(self) -> dict:
        data = {
            'twitter:card': self.twitter_card,
            'twitter:title': self.twitter_title,
            'twitter:description': self.twitter_description,
            'twitter:site': self._format_handle(self.twitter_site),
            'twitter:creator': self._format_handle(self.twitter_creator),
        }
        if self.twitter_image:
            data.update({
                'twitter:image': self.twitter_image.url,
                'twitter:image:alt': self.twitter_image_alt,
            })
        if self.twitter_card == TwitterCardTypeChoices.PLAYER.value:
            data.update({
                'twitter:player': self.twitter_player,
                'twitter:player:ratio': self.twitter_player_ratio,
            })
            # Optionally include a player stream if available from the OG video field in SeoOpenGraphModel
            if hasattr(self, 'og_video') and self.og_video:
                data['twitter:player:stream'] = self.og_video.url
        if self.twitter_cta:
            data['twitter:cta'] = self.twitter_cta.upper()
        return {k: v for k, v in data.items() if v}

    @staticmethod
    def _format_handle(handle: str) -> str:
        return f'@{handle.lstrip("@")}' if handle else ''
