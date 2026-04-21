# ventures/models.py
from django.db import models
from django.utils.text import slugify


class Sector(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    banner_image = models.ImageField(upload_to='sectors/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Sector"
        verbose_name_plural = "1. Sectors"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Venture(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='ventures')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField()
    banner_image = models.ImageField(upload_to='ventures/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Venture"
        verbose_name_plural = "2. Ventures"

    def __str__(self):
        return f"{self.sector.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class VentureDetail(models.Model):
    venture = models.ForeignKey(Venture, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Venture Detail"
        verbose_name_plural = "3. Venture Details"

    def __str__(self):
        return self.title


class Product(models.Model):
    venture = models.ForeignKey(Venture, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Product"
        verbose_name_plural = "4. Products"

    def __str__(self):
        return self.name


class Brand(models.Model):
    venture = models.ForeignKey(Venture, on_delete=models.CASCADE, related_name='brands')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Brand"
        verbose_name_plural = "5. Brands"

    def __str__(self):
        return self.name


class Gallery(models.Model):
    venture = models.ForeignKey(Venture, on_delete=models.CASCADE, related_name='gallery')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    year = models.IntegerField(default=2024)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-year', 'order']
        verbose_name = "Gallery Item"
        verbose_name_plural = "6. Galleries"

    def __str__(self):
        return f"{self.title} ({self.year})"


class AreaOfWorking(models.Model):
    """
    Each area/district listed in the left panel.
    Each area has its OWN map image shown on the right panel when selected.
    """
    venture = models.ForeignKey(
        Venture,
        on_delete=models.CASCADE,
        related_name='areas_of_working'
    )
    name = models.CharField(
        max_length=200,
        help_text="Area / district name shown in the left list."
    )
    area_image = models.ImageField(
        upload_to='areas_of_working/',
        blank=True,
        null=True,
        help_text="Map or area image displayed on the right panel when this area is selected."
    )
    is_operational = models.BooleanField(
        default=True,
        help_text="Toggle to mark this area as active / inactive."
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Area of Working"
        verbose_name_plural = "7. Areas of Working"

    def __str__(self):
        return f"{self.venture.name} – {self.name}"