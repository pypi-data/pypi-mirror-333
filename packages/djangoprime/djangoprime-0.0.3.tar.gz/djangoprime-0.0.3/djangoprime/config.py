from django.conf import settings

BASE_URL = getattr(settings, 'BASE_URL', '')
MAX_IMAGE_SIZE_MB = getattr(settings, 'MAX_IMAGE_SIZE_MB', 5)  # Default: 5 MB
MAX_VIDEO_SIZE_MB = getattr(settings, 'MAX_VIDEO_SIZE_MB', 256)  # Default: 256 MB
MAX_AUDIO_SIZE_MB = getattr(settings, 'MAX_AUDIO_SIZE_MB', 50)  # Default: 50 MB
