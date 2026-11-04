import os
import re

from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator, MinValueValidator, MaxValueValidator,
)
from django.db import models
from django.utils import timezone


def current_year():
    """Callable default — always returns THIS year (not the year the server started)."""
    return timezone.now().year


# ---------------------(MAP)-------------------
class MapLocation(models.Model):
    LOCATION_TYPE_CHOICES = [
        ('hq', 'Headquarters'),
        ('unit', 'Production Unit'),
        ('godown', 'Warehouse'),
    ]
    ICON_CHOICES = [
        ('🏢', 'Office Building'),
        ('🏭', 'Factory'),
        ('📦', 'Warehouse'),
    ]
    name = models.CharField(max_length=200)
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPE_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()
    icon = models.CharField(max_length=10, choices=ICON_CHOICES, default='🏢')
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} - {self.get_location_type_display()}"


class MapConnection(models.Model):
    from_location = models.ForeignKey(MapLocation, related_name='connections_from', on_delete=models.CASCADE)
    to_location = models.ForeignKey(MapLocation, related_name='connections_to', on_delete=models.CASCADE)
    color = models.CharField(max_length=7, default='#dc2626')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['from_location', 'to_location']

    def __str__(self):
        return f"{self.from_location.name} → {self.to_location.name}"


# ---------------------(BRAND)-------------------
class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Brand Logo"
        verbose_name_plural = "Brand Logos"

    def __str__(self):
        return self.name


# ---------------------(JOURNEY)-------------------
class JourneyMilestone(models.Model):
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)], unique=True)
    label = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'year']
        verbose_name = "Journey Milestone"
        verbose_name_plural = "Journey Milestones"

    def __str__(self):
        return f"{self.year} - {self.label}"


# ---------------------(TEAM)-------------------
class TeamMember(models.Model):
    POSITION_CHOICES = [
        ('founder', 'Founder & Managing Director'),
        ('co_founder', 'Co-Founder & Director'),
        ('director', 'Director'),
        ('manager', 'Manager'),
        ('executive', 'Executive'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    position_type = models.CharField(max_length=20, choices=POSITION_CHOICES, default='other')
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.position}"


# ---------------------(CAREER)-------------------
class JobRole(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    vacancy_count = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='jobs/', blank=True, null=True)
    posted_date = models.DateField(default=timezone.now)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    show_in_recent = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-posted_date']
        verbose_name = "Job Role"
        verbose_name_plural = "Job Roles"

    def __str__(self):
        return f"{self.title} ({self.vacancy_count} position{'s' if self.vacancy_count > 1 else ''})"


class CareerApplication(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'), ('reviewed', 'Reviewed'), ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'), ('rejected', 'Rejected'), ('hired', 'Hired'),
    ]
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    job_role = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    applied_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-applied_date']
        verbose_name = "Career Application"
        verbose_name_plural = "Career Applications"

    def __str__(self):
        return f"{self.full_name} - {self.job_role}"


# ---------------------(TESTIMONIALS)-------------------
class Testimonial(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'Via X-Twitter'), ('facebook', 'Via Facebook'),
        ('instagram', 'Via Instagram'), ('linkedin', 'Via LinkedIn'),
        ('google', 'Via Google'), ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='images/avatar/', blank=True, null=True)
    review = models.TextField(default='')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='other')
    platform_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.name} — {self.get_platform_display()}"


# =====================================================
#   PROGRAMS GALLERY  (Category → Event → Photos & Videos)
# =====================================================

class ProgramCategory(models.Model):
    """
    Top-level grouping e.g. Onam, Christmas, Sports Day, Annual Meeting.
    Admins create these freely from the admin panel.
    """
    name = models.CharField(max_length=100, unique=True,
        help_text="Category name e.g. Onam, Christmas, Sports Day")
    slug = models.SlugField(max_length=100, unique=True,
        help_text="Auto-filled from name. Used in URLs.")
    cover_image = models.ImageField(upload_to='program_categories/', blank=True, null=True,
        help_text="Optional cover image shown on the category card")
    description = models.TextField(blank=True,
        help_text="Short description of this category (optional)")
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Program Category"
        verbose_name_plural = "Program Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while ProgramCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def active_events(self):
        return self.events.filter(is_active=True).order_by('order', '-year')

    def _active_media(self):
        return ProgramImage.objects.filter(
            event__category=self, event__is_active=True, is_active=True
        )

    @property
    def total_images(self):
        return self._active_media().filter(media_type=ProgramImage.IMAGE).count()

    @property
    def total_videos(self):
        return self._active_media().filter(media_type=ProgramImage.VIDEO).count()

    @property
    def total_media(self):
        return self._active_media().count()


class ProgramEvent(models.Model):
    """
    A specific event within a category e.g. "Onam 2024", "Christmas Party 2023".
    Each event can have multiple photos and videos.
    """
    category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE,
        related_name='events', help_text="Which category this event belongs to")
    title = models.CharField(max_length=200, help_text="Event title e.g. 'Onam Celebrations 2024'")
    description = models.TextField(blank=True, help_text="Short description (optional)")
    year = models.IntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        default=current_year,
        help_text="Year the event took place"
    )
    cover_image = models.ImageField(upload_to='program_events/', blank=True, null=True,
        help_text="Cover image for this event card (if blank, the first photo is used)")
    order = models.IntegerField(default=0, help_text="Display order within category")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', 'order', 'title']
        verbose_name = "Program Event"
        verbose_name_plural = "Program Events"

    def __str__(self):
        return f"{self.title} ({self.year}) — {self.category.name}"

    @property
    def get_cover(self):
        """cover_image if set, else first active photo, else first video thumbnail."""
        if self.cover_image:
            return self.cover_image.url
        for item in self.active_media:
            thumb = item.thumbnail_url
            if thumb:
                return thumb
        return None

    # All active items (photos + videos) in display order — use this in templates.
    @property
    def active_media(self):
        return self.images.filter(is_active=True).order_by('order', 'created_at')

    # Kept for backwards compatibility: photos only (old templates keep working).
    @property
    def active_images(self):
        return self.active_media.filter(media_type=ProgramImage.IMAGE)

    @property
    def active_videos(self):
        return self.active_media.filter(media_type=ProgramImage.VIDEO)

    @property
    def image_count(self):
        return self.active_images.count()

    @property
    def video_count(self):
        return self.active_videos.count()

    @property
    def media_count(self):
        return self.active_media.count()

    @property
    def slide_count(self):
        """Total slides shown on the card = cover image (if any) + active photos & videos."""
        return self.media_count + (1 if self.cover_image else 0)


_YOUTUBE_RE = re.compile(
    r'(?:youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/|live/)|youtu\.be/)([\w-]{11})'
)
_VIMEO_RE = re.compile(r'vimeo\.com/(?:video/)?(\d+)')

IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']
VIDEO_EXTENSIONS = ['mp4', 'webm', 'mov', 'm4v', 'ogg', 'ogv']


def _file_ext(name):
    return os.path.splitext(name or '')[1].lower().lstrip('.')


def program_media_upload_to(instance, filename):
    """Photos go to program_images/, videos to program_videos/."""
    folder = 'program_videos' if _file_ext(filename) in VIDEO_EXTENSIONS else 'program_images'
    return f"{folder}/{filename}"


class ProgramImage(models.Model):
    """
    One gallery item of a ProgramEvent: a PHOTO or a VIDEO.

    Upload ONE file in the "Photo or Video" box:
      jpg / png / webp ...  -> shown as a photo
      mp4 / webm / mov ...  -> shown as a video (no thumbnail needed)
    Or leave the file empty and paste a YouTube / Vimeo link.
    The type is detected automatically.
    (Model name kept as ProgramImage so existing photos keep working.)
    """
    IMAGE = 'image'
    VIDEO = 'video'
    MEDIA_TYPE_CHOICES = [(IMAGE, 'Photo'), (VIDEO, 'Video')]

    event = models.ForeignKey(ProgramEvent, on_delete=models.CASCADE,
        related_name='images', help_text="Which event this item belongs to")
    image = models.FileField(
        "Photo or Video",
        upload_to=program_media_upload_to, blank=True, null=True,
        validators=[FileExtensionValidator(IMAGE_EXTENSIONS + VIDEO_EXTENSIONS)],
        help_text="Upload a photo (jpg/png/webp) or a video (mp4/webm/mov).")
    video_url = models.URLField("YouTube / Vimeo link", blank=True,
        help_text="Optional: use instead of uploading a big video.")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES,
        default=IMAGE, editable=False)          # set automatically in save()
    caption = models.CharField(max_length=200, blank=True,
        help_text="Optional caption")
    order = models.IntegerField(default=0, help_text="Display order within event")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Program Photo / Video"
        verbose_name_plural = "Program Photos & Videos"

    def __str__(self):
        kind = 'Video' if self.is_video else 'Photo'
        return f"{kind} {self.order} - {self.event.title}"

    # ---- auto-detect type ----
    def _detect_type(self):
        if self.image and _file_ext(self.image.name) in VIDEO_EXTENSIONS:
            return self.VIDEO
        if not self.image and self.video_url:
            return self.VIDEO
        return self.IMAGE

    def clean(self):
        super().clean()
        if not self.image and not self.video_url:
            raise ValidationError({'image': "Upload a photo / video, or paste a YouTube / Vimeo link."})
        if self.image and self.video_url:
            raise ValidationError({'video_url': "Use either an uploaded file OR a link, not both."})
        if self.video_url and not self.embed_url:
            raise ValidationError({'video_url': "Only YouTube or Vimeo links are supported."})

    def save(self, *args, **kwargs):
        self.media_type = self._detect_type()
        super().save(*args, **kwargs)

    # ---- helpers for templates ----
    @property
    def is_video(self):
        return self.media_type == self.VIDEO

    @property
    def is_embed(self):
        """True for a YouTube/Vimeo link (played in an <iframe>)."""
        return self.is_video and not self.image and bool(self.video_url)

    @property
    def youtube_id(self):
        m = _YOUTUBE_RE.search(self.video_url or '')
        return m.group(1) if m else None

    @property
    def embed_url(self):
        yt = self.youtube_id
        if yt:
            return f"https://www.youtube.com/embed/{yt}?rel=0"
        m = _VIMEO_RE.search(self.video_url or '')
        if m:
            return f"https://player.vimeo.com/video/{m.group(1)}"
        return ''

    @property
    def card_embed_url(self):
        """YouTube/Vimeo URL that autoplays muted + looping inside the card."""
        yt = self.youtube_id
        if yt:
            return (f"https://www.youtube.com/embed/{yt}?autoplay=1&mute=1&loop=1"
                    f"&playlist={yt}&controls=0&modestbranding=1&playsinline=1&rel=0")
        m = _VIMEO_RE.search(self.video_url or '')
        if m:
            return f"https://player.vimeo.com/video/{m.group(1)}?background=1&autoplay=1&muted=1&loop=1"
        return ''

    @property
    def video_src(self):
        """URL to play: uploaded video file, or embed URL for links."""
        if self.is_video and self.image:
            return self.image.url
        return self.embed_url

    @property
    def thumbnail_url(self):
        """Photo URL, or YouTube's own thumbnail. Uploaded videos need no thumbnail."""
        if not self.is_video and self.image:
            return self.image.url
        yt = self.youtube_id
        if yt:
            return f"https://img.youtube.com/vi/{yt}/hqdefault.jpg"
        return None


# =====================================================
#   HOME PAGE BANNER  (image or video per slide)
# =====================================================

class HeroBanner(models.Model):
    """
    One slide of the big home page banner.
    Upload a photo OR a video (mp4/webm) — the type is detected automatically.
    Videos play muted and looping in the background, like the photo banners.
    """
    IMAGE = 'image'
    VIDEO = 'video'
    MEDIA_TYPE_CHOICES = [(IMAGE, 'Photo'), (VIDEO, 'Video')]

    media = models.FileField(
        "Banner photo or video",
        upload_to='banners/',
        validators=[FileExtensionValidator(IMAGE_EXTENSIONS + VIDEO_EXTENSIONS)],
        help_text="Photo (jpg/png/webp, about 1920×1080) or video (mp4/webm, keep it short and under ~20 MB).")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES,
        default=IMAGE, editable=False)          # set automatically in save()

    subtitle = models.CharField("Small heading", max_length=150, blank=True,
        help_text="Small text above the title, e.g. 'Partnering for Your Growth'")
    title = models.TextField(blank=True,
        help_text="Up to 3 lines, about 28 letters each. Press Enter for a new line, put *stars* around a word "
                  "to make it red. Example: Building Strong Foundations / Through Experience / and *Expertise.*")
    description = models.TextField(blank=True, help_text="Short paragraph under the title (optional)")
    link_url = models.CharField("Title link", max_length=300, blank=True,
        help_text="Optional. Page to open when the title is clicked, e.g. /about/")

    order = models.IntegerField(default=0, help_text="Display order (smaller first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Home Banner"
        verbose_name_plural = "Home Banners"

    def __str__(self):
        first_line = (self.title or '').strip().splitlines()[0] if self.title else ''
        return first_line.replace('*', '') or self.subtitle or f"Banner {self.pk}"

    TITLE_MAX_LINES = 3
    TITLE_MAX_LINE_LETTERS = 28

    def clean(self):
        """Keep every title the same size as the original banner: max 3 lines, ~28 letters each."""
        super().clean()
        lines = [l.replace('*', '').strip() for l in (self.title or '').strip().splitlines() if l.strip()]
        if len(lines) > self.TITLE_MAX_LINES:
            raise ValidationError({'title': f"Use at most {self.TITLE_MAX_LINES} lines so the title fits the banner box."})
        too_long = [l for l in lines if len(l) > self.TITLE_MAX_LINE_LETTERS]
        if too_long:
            raise ValidationError({'title': f"Each line can have about {self.TITLE_MAX_LINE_LETTERS} letters. "
                                            f"Press Enter to split this line: \"{too_long[0]}\""})
        if self.description and len(self.description) > 160:
            raise ValidationError({'description': "Keep the text under the title to one sentence (160 letters max)."})

    def save(self, *args, **kwargs):
        self.media_type = (self.VIDEO if self.media and _file_ext(self.media.name) in VIDEO_EXTENSIONS
                           else self.IMAGE)
        super().save(*args, **kwargs)

    @property
    def is_video(self):
        return self.media_type == self.VIDEO

    @property
    def title_html(self):
        """Title with line breaks and *red* words, safely escaped."""
        from django.utils.html import escape
        from django.utils.safestring import mark_safe
        text = escape((self.title or '').strip()).replace('\r\n', '\n')
        text = re.sub(r'\*(.+?)\*', r'<span>\1</span>', text)
        return mark_safe(text.replace('\n', '<br>'))