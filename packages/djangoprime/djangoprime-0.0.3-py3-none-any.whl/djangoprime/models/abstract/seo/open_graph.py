import json
from urllib.parse import urljoin

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator, FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoprime.config import MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB, MAX_AUDIO_SIZE_MB, BASE_URL
from djangoprime.models.choices.seo import SEOOpenGraphContentTypeChoices
from djangoprime.validators import ImageDimensionsValidator, FileSizeValidator


class SeoOpenGraphModel(models.Model):
    """
    A model that implements Open Graph (OG) protocol metadata for SEO purposes.

    This abstract model allows you to define and manage the core Open Graph properties,
    such as content type, title, description, media files (image, video, audio), and
    structured data. It also validates and handles content and media type restrictions
    to ensure the data complies with Open Graph requirements.

    Fields:
        - `og_content_type`: Specifies the content type according to the OG protocol.
        - `og_title`: The title of your content for the OG protocol.
        - `og_description`: The description of the content for OG.
        - `og_url`: The canonical URL for the content.
        - `og_site_name`: The name of your site or brand for OG.
        - `og_image`: The image URL associated with the content.
        - `og_image_alt`: Alternative text for the image, used for accessibility.
        - `og_video_type`: Specifies the video type for the content (MP4, MOV, WEBM, OGG).
        - `og_video`: The video file associated with the content.
        - `og_audio`: The audio file associated with the content.
        - `og_locale`: The locale of the content (default is "en_US").
        - `og_locale_alternate`: List of alternate locales for the content.
        - `og_see_also`: A list of related URLs to the content.
        - `og_structured_data`: A JSON field for additional OG metadata.

    Validators:
        - `FileSizeValidator`: Ensures that the uploaded media (image, video, audio) does not exceed size limits.
        - `ImageDimensionsValidator`: Ensures that the image meets the required dimensions and aspect ratio for OG.
        - `FileExtensionValidator`: Ensures that only supported file types (e.g., MP4, MP3) are uploaded.
    """

    # Core OG Properties
    og_content_type = models.CharField(
        _("Open Graph Type"),
        max_length=50,
        blank=True,
        null=True,
        choices=SEOOpenGraphContentTypeChoices.choices,
        help_text=_("The type of your content according to OG protocol (required for object recognition)")
    )
    og_title = models.CharField(
        _("OG Title"),
        max_length=255,
        blank=True,
        validators=[MinLengthValidator(30), MaxLengthValidator(90)],
        help_text=_("The title of your content without branding (60-90 chars)")
    )
    og_description = models.TextField(
        _("OG Description"),
        blank=True,
        validators=[MinLengthValidator(150), MaxLengthValidator(300)],
        help_text=_("Concise description of the content (150-300 chars)")
    )
    og_url = models.URLField(
        _("Canonical URL"),
        blank=True,
        help_text=_("Permanent URL for this content (defaults to current URL)")
    )
    og_site_name = models.CharField(
        _("Site Name"),
        max_length=255,
        blank=True,
        help_text=_("The name of your overall website/social media brand (e.g., IMDb)")
    )

    # Media Properties
    og_image = models.ImageField(
        _("OG Image"),
        upload_to="og_images/",
        blank=True,
        validators=[
            FileSizeValidator(MAX_IMAGE_SIZE_MB),
            ImageDimensionsValidator(min_width=600, min_height=315, max_ratio=1.91, min_ratio=1.91)
        ],
        help_text=_("Primary image (1200×630px, 1.91:1 ratio, max 5MB JPG/PNG/WEBP)")
    )
    og_image_alt = models.CharField(
        _("Image Alt Text"),
        max_length=1255,
        blank=True,
        validators=[MaxLengthValidator(1255)],
        help_text=_("Description of image for accessibility and SEO (max 1255 chars)")
    )

    # Video/Audio Content
    og_video_type = models.CharField(
        _("Video Type"),
        max_length=50,
        blank=True,
        choices=[('video/mp4', 'MP4'), ('video/quicktime', 'MOV'), ('video/webm', 'WEBM'), ('video/ogg', 'OGG')]
    )
    og_video = models.FileField(
        _("OG Video"),
        upload_to="og_videos/",
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'mov', 'ogg']),
            FileSizeValidator(MAX_VIDEO_SIZE_MB)
        ],
        help_text=_("URL to video file (MP4 recommended, max %(max)sMB)") % {'max': MAX_VIDEO_SIZE_MB}
    )

    og_audio = models.FileField(
        _("OG Audio"),
        upload_to="og_audio/",
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg']),
            FileSizeValidator(MAX_AUDIO_SIZE_MB)
        ],
        help_text=_("URL to audio file (MP3/WAV/OGG, max {MAX_AUDIO_SIZE_MB}MB)")
    )

    # Localization
    og_locale = models.CharField(
        _("Locale"),
        max_length=10,
        default="en_US",
        validators=[RegexValidator(r'^[a-z]{2}_[A-Z]{2}$')],
        help_text=_("Content locale (format: en_US)")
    )
    og_locale_alternate = models.JSONField(
        _("Alternate Locales"),
        default=list,
        help_text=_("List of alternate locales (e.g., ['fr_FR', 'es_ES'])")
    )

    # Structured Properties
    og_see_also = models.JSONField(
        _("Related Content"),
        default=list,
        help_text=_("List of URLs of related content")
    )
    og_structured_data = models.JSONField(
        _("Extended OG Data"),
        default=dict,
        help_text=_("Additional Open Graph properties in JSON format")
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['og_content_type']),
            models.Index(fields=['og_locale']),
        ]

    def clean(self):
        """
        Custom validation method to ensure that content fields meet the necessary conditions.
        - Ensures required fields for articles are filled (title, description, image).
        - Validates that video type is provided when a video is uploaded.
        - Checks the format of alternate locales.
        """
        super().clean()

        # Validate required fields for specific content types
        if self.og_content_type == 'article':
            if not all([self.og_title, self.og_description, self.og_image]):
                raise ValidationError(_("Articles require title, description, and image"))

        # Validate video/audio relationships
        if self.og_video and not self.og_video_type:
            raise ValidationError({'og_video_type': _("Video type is required when adding video content")})

        # Validate locale alternates format
        if not isinstance(self.og_locale_alternate, list):
            raise ValidationError({'og_locale_alternate': _("Must be a list of locale strings")})

    def get_og_json(self) -> str:
        """
        Returns the Open Graph data as a JSON string. This method generates an Open Graph JSON
        object based on the fields in the model and returns it in a format suitable for
        embedding into HTML.

        Returns:
            str: JSON string representing the Open Graph data for the content.
        """
        try:
            base_url = BASE_URL
            og_data = {
                '@context': 'https://ogp.me/ns#',
                '@type': self.og_content_type,
                'og:title': self.og_title,
                'og:description': self.og_description,
                'og:url': self.og_url,
                'og:site_name': self.og_site_name,
                'og:locale': self.og_locale,
                'og:see_also': self.og_see_also,
                **self.og_structured_data
            }

            # Add image, video, and alternate locale data if available
            if self.og_image:
                og_data['og:image'] = [{
                    'url': urljoin(base_url, self.og_image.url),
                    'secure_url': urljoin(base_url, self.og_image.url),
                    'width': 1200,
                    'height': 630,
                    'alt': self.og_image_alt,
                    'type': 'image/webp'
                }]
            if self.og_video:
                og_data['og:video'] = {
                    'url': urljoin(base_url, self.og_video.url),
                    'secure_url': urljoin(base_url, self.og_video.url),
                    'type': self.og_video_type,
                    'width': 1920,
                    'height': 1080
                }
            if self.og_locale_alternate:
                og_data['og:locale:alternate'] = self.og_locale_alternate

            return json.dumps(og_data, indent=2, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'error': str(e)})
