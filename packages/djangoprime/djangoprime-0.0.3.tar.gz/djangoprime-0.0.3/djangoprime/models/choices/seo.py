from django.db import models
from django.utils.translation import gettext_lazy as _


class SEOChangeFreqChoices(models.TextChoices):
    ALWAYS = 'always', _('Always')
    HOURLY = 'hourly', _('Hourly')
    DAILY = 'daily', _('Daily')
    WEEKLY = 'weekly', _('Weekly')
    MONTHLY = 'monthly', _('Monthly')
    YEARLY = 'yearly', _('Yearly')
    NEVER = 'never', _('Never')


class TwitterCardTypeChoices(models.TextChoices):
    SUMMARY = 'summary', _('Summary Card')
    SUMMARY_LARGE_IMAGE = 'summary_large_image', _('Large Image Card')
    PLAYER = 'player', _('Player Card')
    APP = 'app', _('App Card')
    PRODUCT = 'product', _('Product Card')  # For Twitter's newer product cards

class SEOOpenGraphContentTypeChoices(models.TextChoices):
    """Comprehensive list of all Open Graph content types."""
    # Web-Based Choices
    ARTICLE = "article", _("Article")
    BLOG = "blog", _("Blog")
    WEBSITE = "website", _("Website")

    # Entertainment Choices
    BOOK = "book", _("Book")
    GAME = "game", _("Game")
    MOVIE = "movie", _("Movie")
    FOOD = "food", _("Food")
    TV_SHOW = "tv_show", _("TV Show")

    # Place Choices
    PLACE = "place", _("Place")
    CITY = "city", _("City")
    COUNTRY = "country", _("Country")
    ATTRACTION = "attraction", _("Attraction")
    LANDMARK = "landmark", _("Landmark")

    # People Choices
    ACTOR = "actor", _("Actor")
    AUTHOR = "author", _("Author")
    POLITICIAN = "politician", _("Politician")
    ATHLETE = "athlete", _("Athlete")
    MUSICIAN = "musician", _("Musician")

    # Business Choices
    COMPANY = "company", _("Company")
    HOTEL = "hotel", _("Hotel")
    RESTAURANT = "restaurant", _("Restaurant")
    BUSINESS = "business.business", _("Business")
    BAR = "bar", _("Bar")
    CAFE = "cafe", _("Cafe")

    # Video Choices
    VIDEO_MOVIE = "video.movie", _("Video Movie")
    VIDEO_EPISODE = "video.episode", _("Video Episode")
    VIDEO_TV_SHOW = "video.tv_show", _("Video TV Show")
    VIDEO_OTHER = "video.other", _("Video Other")

    # Music Choices
    MUSIC_SONG = "music.song", _("Music Song")
    MUSIC_ALBUM = "music.album", _("Music Album")
    MUSIC_PLAYLIST = "music.playlist", _("Music Playlist")
    MUSIC_RADIO_STATION = "music.radio_station", _("Music Radio Station")

    # Profile Choice
    PROFILE = "profile", _("Profile")

    # Product Choices
    PRODUCT = "product", _("Product")
    PRODUCT_ITEM = "product.item", _("Product Item")
    PRODUCT_GROUP = "product.group", _("Product Group")

    # Event Choice
    EVENT = "event", _("Event")

    # Sports Choices
    SPORT = "sport", _("Sport")
    SPORTS_LEAGUE = "sports_league", _("Sports League")
    SPORTS_TEAM = "sports_team", _("Sports Team")

    # Education Choices
    SCHOOL = "school", _("School")
    UNIVERSITY = "university", _("University")
    COURSE = "course", _("Course")

    # Non-Profit Choice
    NONPROFIT = "nonprofit", _("Non-Profit")

    # Government Choice
    GOVERNMENT = "government", _("Government")

    # App Choice
    APP = "app", _("App")

    # Group Choice
    GROUP = "group", _("Group")
