from django.contrib import admin
from django import forms
from decimal import Decimal, ROUND_HALF_UP
from django.utils.html import format_html
from .models import (
    JourneyMilestone, TeamMember, Brand, JobRole, CareerApplication,
    MapLocation, MapConnection, Testimonial,
    ProgramCategory, ProgramEvent, ProgramImage, HeroBanner
)

# ProgramGallery is the old (legacy) model. Import it only if it exists in models.py,
# so the admin never crashes with "cannot import name 'ProgramGallery'".
try:
    from .models import ProgramGallery
except ImportError:
    ProgramGallery = None


# ── HOME BANNER ──────────────────────────────────
@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ['preview', '__str__', 'media_type', 'order', 'is_active', 'updated_at']
    list_display_links = ['preview', '__str__']
    list_editable = ['order', 'is_active']
    list_filter = ['media_type', 'is_active']
    search_fields = ['title', 'subtitle', 'description']
    readonly_fields = ['preview_large']
    fieldsets = (
        ('Photo / Video', {
            'fields': ('media', 'preview_large'),
            'description': 'Upload a photo or a video — the type is detected automatically. '
                           'Videos play muted and looping in the background.',
        }),
        ('Text on the banner', {
            'fields': ('subtitle', 'title', 'description', 'link_url'),
            'description': 'Title tips: press Enter to start a new line. Put stars around a word to show it in red. '
                           'Up to 3 lines, about 28 letters each, so every banner looks the same size.',
        }),
        ('Display Settings', {'fields': ('order', 'is_active')}),
    )

    def _media_html(self, obj, height):
        if not obj or not obj.media:
            return '—'
        if obj.is_video:
            return format_html('<video src="{}#t=0.1" height="{}" muted loop autoplay playsinline '
                               'style="border-radius:6px;background:#000;max-width:100%;"></video>',
                               obj.media.url, height)
        return format_html('<img src="{}" height="{}" style="border-radius:6px;object-fit:cover;max-width:100%;">',
                           obj.media.url, height)

    def preview(self, obj):
        return self._media_html(obj, 50)
    preview.short_description = 'Preview'

    def preview_large(self, obj):
        return self._media_html(obj, 220)
    preview_large.short_description = 'Current'


# ── MAP ──────────────────────────────────────────
class MapLocationAdminForm(forms.ModelForm):
    """
    Google Maps gives coordinates with 7 decimals (e.g. 10.6039532).
    The database column stores 6 decimals, so the default form rejected them with
    "Ensure that there are no more than 6 decimal places" and the location was never saved.
    This form accepts extra decimals, checks the valid range, and rounds to 6 decimals.
    """
    latitude = forms.DecimalField(
        max_digits=15, decimal_places=10,
        widget=forms.NumberInput(attrs={'step': 'any'}),
        help_text="Example: 10.603953  (first number when you copy from Google Maps)",
    )
    longitude = forms.DecimalField(
        max_digits=15, decimal_places=10,
        widget=forms.NumberInput(attrs={'step': 'any'}),
        help_text="Example: 76.480123  (second number when you copy from Google Maps)",
    )

    class Meta:
        model = MapLocation
        fields = '__all__'

    @staticmethod
    def _round6(value):
        return value.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)

    def clean_latitude(self):
        value = self.cleaned_data['latitude']
        if not Decimal('-90') <= value <= Decimal('90'):
            raise forms.ValidationError("Latitude must be between -90 and 90.")
        return self._round6(value)

    def clean_longitude(self):
        value = self.cleaned_data['longitude']
        if not Decimal('-180') <= value <= Decimal('180'):
            raise forms.ValidationError("Longitude must be between -180 and 180.")
        return self._round6(value)


@admin.register(MapLocation)
class MapLocationAdmin(admin.ModelAdmin):
    form = MapLocationAdminForm
    list_display = ['name', 'location_type', 'latitude', 'longitude', 'is_active', 'display_order']
    list_editable = ['display_order', 'is_active']
    list_filter = ['location_type', 'is_active']
    search_fields = ['name', 'address']

@admin.register(MapConnection)
class MapConnectionAdmin(admin.ModelAdmin):
    list_display = ['from_location', 'to_location', 'color', 'is_active']
    list_editable = ['is_active']


# ── TESTIMONIALS ─────────────────────────────────
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'platform']
    search_fields = ['name', 'review']
    list_editable = ['order', 'is_active']
    fieldsets = (
        ('Person Info', {'fields': ('name', 'avatar')}),
        ('Review', {'fields': ('review',)}),
        ('Platform', {'fields': ('platform', 'platform_url')}),
        ('Display Settings', {'fields': ('order', 'is_active')}),
    )


# ── CAREER ───────────────────────────────────────
@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ['title', 'vacancy_count', 'posted_date', 'order', 'is_active', 'show_in_recent']
    list_filter = ['is_active', 'show_in_recent']
    search_fields = ['title']
    list_editable = ['vacancy_count', 'order', 'is_active', 'show_in_recent']
    date_hierarchy = 'posted_date'

@admin.register(CareerApplication)
class CareerApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'job_role', 'status', 'applied_date']
    list_filter = ['status', 'job_role']
    search_fields = ['full_name', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['applied_date']
    actions = ['mark_as_reviewed', 'mark_as_shortlisted', 'mark_as_rejected']

    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
    def mark_as_shortlisted(self, request, queryset):
        queryset.update(status='shortlisted')
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')


# ── BRAND ─────────────────────────────────────────
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'preview', 'order', 'is_active']
    list_editable = ['order', 'is_active']

    def preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" height="40">', obj.logo.url)
        return '-'
    preview.short_description = 'Logo'


# ── JOURNEY ──────────────────────────────────────
@admin.register(JourneyMilestone)
class JourneyMilestoneAdmin(admin.ModelAdmin):
    list_display = ['year', 'label', 'order', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['year', 'label', 'title']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'year']


# ── TEAM ─────────────────────────────────────────
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'position_type', 'order', 'is_active']
    list_filter = ['is_active', 'position_type']
    search_fields = ['name', 'position']
    list_editable = ['order', 'is_active']


# ══════════════════════════════════════════════════
#   PROGRAMS GALLERY ADMIN  (photos + videos)
# ══════════════════════════════════════════════════

def media_preview(obj, height=60):
    """Small preview: photo, playable video, or YouTube thumbnail."""
    if not obj or not obj.pk:
        return '—'
    if obj.is_video:
        if obj.image:   # uploaded video file
            return format_html(
                '<video src="{}#t=0.5" height="{}" muted preload="metadata" controls '
                'style="border-radius:6px;background:#000;max-width:160px;"></video>',
                obj.image.url, height,
            )
        thumb = obj.thumbnail_url
        if thumb:       # YouTube
            return format_html(
                '<a href="{}" target="_blank" style="position:relative;display:inline-block;">'
                '<img src="{}" height="{}" style="border-radius:6px;object-fit:cover;">'
                '<span style="position:absolute;inset:0;display:flex;align-items:center;'
                'justify-content:center;color:#fff;font-size:22px;'
                'text-shadow:0 0 6px rgba(0,0,0,.8);">▶</span></a>',
                obj.video_url, thumb, height,
            )
        return format_html(
            '<a href="{}" target="_blank" style="background:#fdecea;color:#c62828;'
            'padding:3px 10px;border-radius:12px;font-weight:700;">▶ Video link</a>',
            obj.video_url,
        )
    if obj.image:
        return format_html(
            '<img src="{}" height="{}" style="border-radius:6px;object-fit:cover;">',
            obj.image.url, height,
        )
    return '—'


class ProgramImageInline(admin.TabularInline):
    """
    Photos & videos inside ProgramEvent — just choose a file.
    A jpg/png becomes a photo, an mp4/webm/mov becomes a video automatically.
    """
    model = ProgramImage
    extra = 5
    fields = ['image', 'video_url', 'caption', 'order', 'is_active', 'preview']
    readonly_fields = ['preview']
    ordering = ['order']
    verbose_name = "Photo / Video"
    verbose_name_plural = "Photos & Videos  (choose a photo or video file — or paste a YouTube / Vimeo link)"

    def preview(self, obj):
        return media_preview(obj, 60)
    preview.short_description = 'Preview'


class ProgramEventInline(admin.TabularInline):
    """Events shown inline inside Category admin"""
    model = ProgramEvent
    extra = 1
    fields = ['title', 'year', 'order', 'is_active']
    show_change_link = True  # link to full event edit page


@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'event_count',
                    'total_images', 'total_videos', 'cover_preview']
    list_editable = ['order', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProgramEventInline]

    fieldsets = (
        ('Category Info', {
            'fields': ('name', 'slug', 'description', 'cover_image')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def event_count(self, obj):
        return obj.events.filter(is_active=True).count()
    event_count.short_description = 'Events'

    def total_images(self, obj):
        return obj.total_images
    total_images.short_description = 'Photos'

    def total_videos(self, obj):
        return obj.total_videos
    total_videos.short_description = 'Videos'

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" height="40" style="border-radius:4px;">', obj.cover_image.url)
        return '—'
    cover_preview.short_description = 'Cover'


@admin.register(ProgramEvent)
class ProgramEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'year', 'order', 'is_active',
                    'media_counts', 'cover_preview', 'updated_at']
    list_filter = ['is_active', 'year', 'category']
    search_fields = ['title', 'description', 'category__name']
    list_editable = ['category', 'year', 'order', 'is_active']
    ordering = ['-year', 'order']
    inlines = [ProgramImageInline]   # ← Add photos & videos right here

    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'category', 'year')
        }),
        ('Cover Image', {
            'fields': ('cover_image',),
            'description': 'Optional. If left blank, the first photo is used as cover.'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def media_counts(self, obj):
        return format_html(
            '<span style="background:#e8f5e9;color:#2e7d32;padding:2px 8px;border-radius:12px;font-weight:700;">{} 📷</span> '
            '<span style="background:#fdecea;color:#c62828;padding:2px 8px;border-radius:12px;font-weight:700;">{} 🎬</span>',
            obj.image_count, obj.video_count,
        )
    media_counts.short_description = 'Photos / Videos'

    def cover_preview(self, obj):
        url = obj.get_cover
        if url:
            return format_html('<img src="{}" height="50" style="border-radius:6px;object-fit:cover;">', url)
        return '—'
    cover_preview.short_description = 'Cover'


@admin.register(ProgramImage)
class ProgramImageAdmin(admin.ModelAdmin):
    list_display = ['event', 'media_type', 'caption', 'order', 'is_active', 'preview']
    list_filter = ['media_type', 'is_active', 'event__category', 'event__year']
    search_fields = ['event__title', 'caption']
    list_editable = ['order', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('event', 'image', 'video_url', 'caption'),
            'description': 'Choose a photo or video file (type is detected automatically), '
                           'or paste a YouTube / Vimeo link instead.',
        }),
        ('Display Settings', {'fields': ('order', 'is_active')}),
    )

    def preview(self, obj):
        return media_preview(obj, 50)
    preview.short_description = 'Preview'


if ProgramGallery is not None:
    @admin.register(ProgramGallery)
    class ProgramGalleryAdmin(admin.ModelAdmin):
        list_display = ['title', 'year', 'order', 'is_active', 'preview']
        list_filter = ['is_active', 'year']
        search_fields = ['title']
        list_editable = ['year', 'order', 'is_active']

        def preview(self, obj):
            if obj.image:
                return format_html('<img src="{}" height="40" style="border-radius:4px;">', obj.image.url)
            return '—'
        preview.short_description = 'Preview'