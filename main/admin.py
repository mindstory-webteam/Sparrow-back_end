from django.contrib import admin
from .models import (
    JourneyMilestone, TeamMember, Brand, JobRole, CareerApplication,
    MapLocation, MapConnection, Testimonial, ProgramGallery
)


# -------------(MAP)-------------------------------
@admin.register(MapLocation)
class MapLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location_type', 'is_active', 'display_order']
    list_editable = ['display_order', 'is_active']


@admin.register(MapConnection)
class MapConnectionAdmin(admin.ModelAdmin):
    list_display = ['from_location', 'to_location', 'color', 'is_active']
    list_editable = ['is_active']


# -------------(TESTIMONIALS)-------------------------------
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'platform']
    search_fields = ['name', 'review']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'created_at']

    fieldsets = (
        ('Person Info', {
            'fields': ('name', 'avatar')
        }),
        ('Review', {
            'fields': ('review',)
        }),
        ('Platform', {
            'fields': ('platform', 'platform_url')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )


# ------------Career page----------------
@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ['title', 'vacancy_count', 'posted_date', 'order', 'is_active', 'show_in_recent']
    list_filter = ['is_active', 'show_in_recent', 'posted_date']
    search_fields = ['title', 'description']
    list_editable = ['vacancy_count', 'order', 'is_active', 'show_in_recent']
    date_hierarchy = 'posted_date'

    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'description', 'vacancy_count', 'image', 'posted_date')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active', 'show_in_recent')
        }),
    )

    def get_list_display_links(self, request, list_display):
        return ['title']


@admin.register(CareerApplication)
class CareerApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'job_role', 'status', 'applied_date']
    list_filter = ['status', 'job_role', 'applied_date']
    search_fields = ['full_name', 'email', 'phone', 'job_role', 'message']
    list_editable = ['status']
    date_hierarchy = 'applied_date'
    readonly_fields = ['applied_date']

    fieldsets = (
        ('Applicant Information', {
            'fields': ('full_name', 'email', 'phone', 'job_role')
        }),
        ('Application Details', {
            'fields': ('message', 'applied_date')
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes')
        }),
    )

    actions = ['mark_as_reviewed', 'mark_as_shortlisted', 'mark_as_rejected']

    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
        self.message_user(request, f"{queryset.count()} applications marked as reviewed.")
    mark_as_reviewed.short_description = "Mark selected as Reviewed"

    def mark_as_shortlisted(self, request, queryset):
        queryset.update(status='shortlisted')
        self.message_user(request, f"{queryset.count()} applications marked as shortlisted.")
    mark_as_shortlisted.short_description = "Mark selected as Shortlisted"

    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} applications marked as rejected.")
    mark_as_rejected.short_description = "Mark selected as Rejected"


# ----------------Brand----------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'preview', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    fields = ('name', 'logo', 'order', 'is_active')

    def preview(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" height="40">'
        return '-'
    preview.allow_tags = True


# ----------------Journey----------------
@admin.register(JourneyMilestone)
class JourneyMilestoneAdmin(admin.ModelAdmin):
    list_display = ['year', 'label', 'order', 'is_active', 'updated_at']
    list_filter = ['is_active', 'year']
    search_fields = ['year', 'label', 'title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'year']

    fieldsets = (
        ('Basic Information', {
            'fields': ('year', 'label', 'title')
        }),
        ('Content', {
            'fields': ('description',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_at', 'updated_at']
        return []


# ----------------Team----------------
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'position_type', 'order', 'is_active', 'updated_at']
    list_filter = ['is_active', 'position_type']
    search_fields = ['name', 'position', 'bio', 'email']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'position_type', 'photo')
        }),
        ('Biography', {
            'fields': ('bio',)
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'linkedin_url'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_at', 'updated_at']
        return []


# ----------------Programs Gallery----------------
@admin.register(ProgramGallery)
class ProgramGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'order', 'is_active', 'preview', 'updated_at']
    list_filter = ['is_active', 'year']
    search_fields = ['title', 'description']
    list_editable = ['year', 'order', 'is_active']
    ordering = ['-year', 'order']

    fieldsets = (
        ('Program Information', {
            'fields': ('title', 'description', 'image', 'year')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" height="50" style="border-radius:4px;">'
        return '-'
    preview.allow_tags = True
    preview.short_description = 'Preview'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_at', 'updated_at']
        return []