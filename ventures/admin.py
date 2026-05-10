# ventures/admin.py
from django.contrib import admin
from .models import (
    Sector, Venture, VentureAbout, VentureDetail, Feature,
    Product, Brand, Gallery, AreaOfWorking
)


# ══════════════════════════════════════════════════════════════════════════════
# SECTOR
# ══════════════════════════════════════════════════════════════════════════════
@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display        = ['name', 'slug', 'is_active', 'order']
    list_editable       = ['is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}


# ══════════════════════════════════════════════════════════════════════════════
# VENTURE INLINES
# Rule: any inline with an ImageField → StackedInline (TabularInline clips
#       the ClearableFileInput widget and breaks image uploads).
# ══════════════════════════════════════════════════════════════════════════════

class VentureAboutInline(admin.StackedInline):
    """One-to-one About block — no image, but StackedInline keeps it readable."""
    model               = VentureAbout
    extra               = 1
    max_num             = 1
    fields              = ['title', 'description']
    verbose_name        = "Venture About"
    verbose_name_plural = "3. Venture About"


class VentureDetailInline(admin.StackedInline):
    """Has banner_image → StackedInline."""
    model               = VentureDetail
    extra               = 0
    fields              = ['title', 'description', 'banner_image', 'order']
    verbose_name        = "Venture Detail"
    verbose_name_plural = "4. Venture Details"


class FeatureInline(admin.TabularInline):
    """No image field → compact TabularInline is fine."""
    model               = Feature
    extra               = 1
    fields              = ['text', 'order']
    verbose_name        = "Product Feature"
    verbose_name_plural = "9. Product Features"


class ProductInline(admin.StackedInline):
    model               = Product
    extra               = 0
    fields              = ['name', 'description', 'image', 'order']
    verbose_name        = "Product"
    verbose_name_plural = "5. Products"


class BrandInline(admin.StackedInline):
    model               = Brand
    extra               = 0
    fields              = ['name', 'description', 'logo', 'order']
    verbose_name        = "Brand"
    verbose_name_plural = "6. Brands"


class GalleryInline(admin.StackedInline):
    model               = Gallery
    extra               = 0
    fields              = ['title', 'description', 'image', 'year', 'order']
    verbose_name        = "Gallery Item"
    verbose_name_plural = "7. Galleries"


class AreaOfWorkingInline(admin.StackedInline):
    model               = AreaOfWorking
    extra               = 1
    fields              = ['name', 'area_image', 'is_operational', 'order']
    verbose_name        = "Area of Working"
    verbose_name_plural = "8. Areas of Working"


# ══════════════════════════════════════════════════════════════════════════════
# VENTURE
# ══════════════════════════════════════════════════════════════════════════════
@admin.register(Venture)
class VentureAdmin(admin.ModelAdmin):
    list_display        = ['name', 'sector', 'slug', 'is_active', 'order']
    list_editable       = ['is_active', 'order']
    list_filter         = ['sector', 'is_active']
    search_fields       = ['name']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('General', {
            'fields': ('sector', 'name', 'slug', 'description', 'is_active', 'order'),
        }),
        ('Images', {
            'fields': ('banner_image',),
        }),
    )

    inlines = [
        VentureAboutInline,
        VentureDetailInline,
        FeatureInline,
        ProductInline,
        BrandInline,
        GalleryInline,
        AreaOfWorkingInline,
    ]


# ══════════════════════════════════════════════════════════════════════════════
# STANDALONE ADMINS
# ══════════════════════════════════════════════════════════════════════════════
@admin.register(VentureAbout)
class VentureAboutAdmin(admin.ModelAdmin):
    list_display  = ['venture', 'title']
    list_filter   = ['venture']
    search_fields = ['title', 'venture__name']
    fields        = ['venture', 'title', 'description']


@admin.register(VentureDetail)
class VentureDetailAdmin(admin.ModelAdmin):
    list_display  = ['title', 'venture', 'order']
    list_editable = ['order']
    list_filter   = ['venture']
    search_fields = ['title']
    fields        = ['venture', 'title', 'description', 'banner_image', 'order']


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display  = ['text', 'venture', 'order']
    list_editable = ['order']
    list_filter   = ['venture']
    search_fields = ['text']
    fields        = ['venture', 'text', 'order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'venture', 'order']
    list_editable = ['order']
    list_filter   = ['venture']
    search_fields = ['name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display  = ['name', 'venture', 'order']
    list_editable = ['order']
    list_filter   = ['venture']
    search_fields = ['name']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display  = ['title', 'venture', 'year', 'order']
    list_editable = ['order']
    list_filter   = ['venture', 'year']
    search_fields = ['title']


@admin.register(AreaOfWorking)
class AreaOfWorkingAdmin(admin.ModelAdmin):
    list_display  = ['name', 'venture', 'is_operational', 'order']
    list_editable = ['is_operational', 'order']
    list_filter   = ['venture', 'is_operational']
    search_fields = ['name']
    fields        = ['venture', 'name', 'area_image', 'is_operational', 'order']