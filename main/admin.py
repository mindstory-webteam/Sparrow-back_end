from django.contrib import admin
from django.utils.html import format_html
from .models import (
    JourneyMilestone, TeamMember, Brand, JobRole, CareerApplication,
    MapLocation, MapConnection, Testimonial,
    ProgramCategory, ProgramEvent, ProgramImage, ProgramGallery
)


# ── MAP ──────────────────────────────────────────
@admin.register(MapLocation)
class MapLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location_type', 'is_active', 'display_order']
    list_editable = ['display_order', 'is_active']

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
#   PROGRAMS GALLERY ADMIN
#
#   How the client uses it (simple 2-step flow):
#   1. Program Categories  → create "Onam", "Christmas", etc.
#   2. Program Events      → create "Onam 2025", pick category,
#                            and upload ALL photos on the SAME page
#                            (scroll down to the Images section).
# ══════════════════════════════════════════════════

class ProgramImageInline(admin.TabularInline):
    """Photo upload rows shown inside the Event page."""
    model = ProgramImage
    extra = 5                       # 5 empty upload slots ready by default
    fields = ['preview', 'image', 'caption', 'order', 'is_active']
    readonly_fields = ['preview']
    ordering = ['order']
    verbose_name = "Photo"
    verbose_name_plural = "Photos (upload event photos here)"

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" height="60" style="border-radius:6px;object-fit:cover;">',
                obj.image.url
            )
        return '—'
    preview.short_description = 'Preview'


@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_count', 'total_photos', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}   # slug fills itself while typing

    fieldsets = (
        ('Category', {
            'fields': ('name', 'slug'),
            'description': 'Example categories: Onam, Christmas, Sports Day, Annual Meet.'
        }),
        ('Optional', {
            'fields': ('description', 'cover_image'),
            'classes': ('collapse',),           # hidden by default — keeps the form clean
        }),
        ('Display Settings', {'fields': ('order', 'is_active')}),
    )

    def event_count(self, obj):
        return obj.events.filter(is_active=True).count()
    event_count.short_description = 'Events'

    def total_photos(self, obj):
        return obj.total_images
    total_photos.short_description = 'Photos'


@admin.register(ProgramEvent)
class ProgramEventAdmin(admin.ModelAdmin):
    list_display = ['cover_preview', 'title', 'category', 'year', 'photo_count', 'order', 'is_active']
    list_display_links = ['cover_preview', 'title']
    list_filter = ['category', 'year', 'is_active']
    search_fields = ['title', 'description', 'category__name']
    list_editable = ['order', 'is_active']
    list_select_related = ['category']
    ordering = ['-year', 'order']
    save_on_top = True                      # save button also at the top
    inlines = [ProgramImageInline]          # ← photos are added right here

    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'category', 'year', 'description'),
        }),
        ('Cover Image (optional)', {
            'fields': ('cover_image',),
            'description': 'If left blank, the first uploaded photo below is used as the cover automatically.',
            'classes': ('collapse',),
        }),
        ('Display Settings', {'fields': ('order', 'is_active')}),
    )

    def photo_count(self, obj):
        return format_html(
            '<span style="background:#e8f5e9;color:#2e7d32;padding:2px 10px;'
            'border-radius:12px;font-weight:700;">{} photos</span>',
            obj.image_count
        )
    photo_count.short_description = 'Photos'

    def cover_preview(self, obj):
        url = obj.get_cover
        if url:
            return format_html(
                '<img src="{}" height="50" width="70" style="border-radius:6px;object-fit:cover;">', url
            )
        return '—'
    cover_preview.short_description = 'Cover'


@admin.register(ProgramImage)
class ProgramImageAdmin(admin.ModelAdmin):
    """
    Usually not needed — photos are managed inside each Event.
    Kept here so all photos can be searched/filtered in one place.
    """
    list_display = ['preview', 'event', 'caption', 'order', 'is_active']
    list_display_links = ['preview', 'event']
    list_filter = ['event__category', 'event__year', 'is_active']
    search_fields = ['event__title', 'caption']
    list_editable = ['order', 'is_active']
    list_select_related = ['event', 'event__category']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" style="border-radius:6px;">', obj.image.url)
        return '—'
    preview.short_description = 'Photo'


# ── Legacy single-image gallery (old data only) ──
# Delete this block once old entries are migrated to Events.
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