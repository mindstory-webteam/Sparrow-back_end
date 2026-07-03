from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


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
#   PROGRAMS GALLERY  (Category → Event → Images)
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

    @property
    def total_images(self):
        return ProgramImage.objects.filter(event__category=self, event__is_active=True, is_active=True).count()


class ProgramEvent(models.Model):
    """
    A specific event within a category e.g. "Onam 2024", "Christmas Party 2023".
    Each event can have multiple images.
    """
    category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE,
        related_name='events', help_text="Which category this event belongs to")
    title = models.CharField(max_length=200, help_text="Event title e.g. 'Onam Celebrations 2024'")
    description = models.TextField(blank=True, help_text="Short description (optional)")
    year = models.IntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        default=timezone.now().year,
        help_text="Year the event took place"
    )
    cover_image = models.ImageField(upload_to='program_events/', blank=True, null=True,
        help_text="Cover image for this event card (if blank, first uploaded image is used)")
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
        """Return cover_image if set, else first active image"""
        if self.cover_image:
            return self.cover_image.url
        first = self.images.filter(is_active=True).first()
        return first.image.url if first else None

    @property
    def active_images(self):
        return self.images.filter(is_active=True).order_by('order')

    @property
    def image_count(self):
        return self.images.filter(is_active=True).count()


class ProgramImage(models.Model):
    """Individual image belonging to a ProgramEvent"""
    event = models.ForeignKey(ProgramEvent, on_delete=models.CASCADE,
        related_name='images', help_text="Which event this image belongs to")
    image = models.ImageField(upload_to='program_images/',
        help_text="Upload image")
    caption = models.CharField(max_length=200, blank=True,
        help_text="Optional caption for this image")
    order = models.IntegerField(default=0, help_text="Display order within event")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Program Image"
        verbose_name_plural = "Program Images"

    def __str__(self):
        return f"Image {self.order} — {self.event.title}"


# Keep ProgramGallery for backward compatibility (old single-image model)
class ProgramGallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='programs/')
    year = models.IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2100)], default=timezone.now().year)
    category = models.ForeignKey(ProgramCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='legacy_programs')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', 'order', 'title']
        verbose_name = "Program Gallery (Legacy)"
        verbose_name_plural = "Program Gallery (Legacy)"

    def __str__(self):
        return f"{self.title} ({self.year})"