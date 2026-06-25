from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# ---------------------(MAP)-------------------
class MapLocation(models.Model):
    """Locations to display on the map"""
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
    """Visual connections between locations on the map"""
    from_location = models.ForeignKey(MapLocation, related_name='connections_from', on_delete=models.CASCADE)
    to_location = models.ForeignKey(MapLocation, related_name='connections_to', on_delete=models.CASCADE)
    color = models.CharField(max_length=7, default='#dc2626')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['from_location', 'to_location']
    
    def __str__(self):
        return f"{self.from_location.name} → {self.to_location.name}"

# ---------------------(MAP)-------------------


class Brand(models.Model):
    """Model for brand logos only"""
    
    name = models.CharField(
        max_length=100,
        help_text="Brand name (for admin reference only)"
    )
    logo = models.ImageField(
        upload_to='brands/',
        help_text="Brand logo image"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Show/Hide brand"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Brand Logo"
        verbose_name_plural = "Brand Logos"

    def __str__(self):
        return self.name


class JourneyMilestone(models.Model):
    """Model for company journey milestones"""
    
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        unique=True,
        help_text="Year of the milestone"
    )
    label = models.CharField(
        max_length=100,
        help_text="Short label for the milestone (e.g., 'The Beginning')"
    )
    title = models.CharField(
        max_length=200,
        help_text="Main title for the milestone"
    )
    description = models.TextField(
        help_text="Detailed description of what happened this year"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether to display this milestone"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'year']
        verbose_name = "Journey Milestone"
        verbose_name_plural = "Journey Milestones"

    def __str__(self):
        return f"{self.year} - {self.label}"


class TeamMember(models.Model):
    """Model for team members"""
    
    POSITION_CHOICES = [
        ('founder', 'Founder & Managing Director'),
        ('co_founder', 'Co-Founder & Director'),
        ('director', 'Director'),
        ('manager', 'Manager'),
        ('executive', 'Executive'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(
        max_length=100,
        help_text="Full name of the team member"
    )
    position = models.CharField(
        max_length=100,
        help_text="Job title/position"
    )
    position_type = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='other',
        help_text="Position category"
    )
    bio = models.TextField(
        blank=True,
        help_text="Short biography or description"
    )
    photo = models.ImageField(
        upload_to='team/',
        blank=True,
        null=True,
        help_text="Team member photo"
    )
    email = models.EmailField(
        blank=True,
        help_text="Email address (optional)"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Phone number (optional)"
    )
    linkedin_url = models.URLField(
        blank=True,
        help_text="LinkedIn profile URL (optional)"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether to display this team member"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.position}"


class JobRole(models.Model):
    """Model for available job roles/positions"""
    
    title = models.CharField(
        max_length=200,
        help_text="Job title/position"
    )
    description = models.TextField(
        blank=True,
        help_text="Job description (optional)"
    )
    vacancy_count = models.PositiveIntegerField(
        default=1,
        help_text="Number of openings for this position"
    )
    image = models.ImageField(
        upload_to='jobs/',
        blank=True,
        null=True,
        help_text="Job thumbnail image (optional)"
    )
    posted_date = models.DateField(
        default=timezone.now,
        help_text="Job posting date"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Show in dropdown and recent jobs"
    )
    show_in_recent = models.BooleanField(
        default=True,
        help_text="Show in 'Recent Jobs' sidebar"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-posted_date']
        verbose_name = "Job Role"
        verbose_name_plural = "Job Roles"

    def __str__(self):
        return f"{self.title} ({self.vacancy_count} position{'s' if self.vacancy_count > 1 else ''})"


class CareerApplication(models.Model):
    """Model for career applications submitted through the form"""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    
    full_name = models.CharField(
        max_length=200,
        help_text="Applicant's full name"
    )
    email = models.EmailField(
        help_text="Email address"
    )
    phone = models.CharField(
        max_length=20,
        help_text="Phone number"
    )
    job_role = models.CharField(
        max_length=200,
        help_text="Applied job role"
    )
    message = models.TextField(
        blank=True,
        help_text="Cover letter or message"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        help_text="Application status"
    )
    applied_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date of application"
    )
    notes = models.TextField(
        blank=True,
        help_text="Internal notes (not visible to applicant)"
    )
    
    class Meta:
        ordering = ['-applied_date']
        verbose_name = "Career Application"
        verbose_name_plural = "Career Applications"

    def __str__(self):
        return f"{self.full_name} - {self.job_role} ({self.applied_date.strftime('%Y-%m-%d')})"


# ---------------------(TESTIMONIALS)-------------------

class Testimonial(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'Via X-Twitter'),
        ('facebook', 'Via Facebook'),
        ('instagram', 'Via Instagram'),
        ('linkedin', 'Via LinkedIn'),
        ('google', 'Via Google'),
        ('other', 'Other'),
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

# ---------------------(TESTIMONIALS)-------------------


# ---------------------(PROGRAMS GALLERY)-------------------

class ProgramGallery(models.Model):
    """Model for Programs Gallery images with year-based filtering"""

    title = models.CharField(
        max_length=200,
        help_text="Program title / name"
    )
    description = models.TextField(
        blank=True,
        help_text="Short description of the program (optional)"
    )
    image = models.ImageField(
        upload_to='programs/',
        help_text="Program image"
    )
    year = models.IntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        default=timezone.now().year,
        help_text="Year the program took place"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether to display this program"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', 'order', 'title']
        verbose_name = "Program Gallery"
        verbose_name_plural = "Program Gallery"

    def __str__(self):
        return f"{self.title} ({self.year})"

# ---------------------(PROGRAMS GALLERY)-------------------