# ventures/admin.py
from django.contrib import admin
from .models import Sector, Venture, Product, Brand, VentureDetail, Gallery, AreaOfWorking


# ══════════════════════════════════════════════════════════════════════════════
# SECTOR
# ══════════════════════════════════════════════════════════════════════════════
@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}


# ══════════════════════════════════════════════════════════════════════════════
# VENTURE INLINES
# All inlines with an ImageField use StackedInline so the file-picker
# widget renders correctly (TabularInline clips the upload input).
# ══════════════════════════════════════════════════════════════════════════════

class VentureDetailInline(admin.StackedInline):
    """Has banner_image → StackedInline required for image upload to work."""
    model  = VentureDetail
    extra  = 0
    fields = ['title', 'description', 'banner_image', 'order']
    verbose_name        = "Venture Detail"
    verbose_name_plural = "3. Venture Details"


class ProductInline(admin.StackedInline):
    model  = Product
    extra  = 0
    fields = ['name', 'description', 'image', 'order']
    verbose_name        = "Product"
    verbose_name_plural = "4. Products"


class BrandInline(admin.StackedInline):
    model  = Brand
    extra  = 0
    fields = ['name', 'description', 'logo', 'order']
    verbose_name        = "Brand"
    verbose_name_plural = "5. Brands"


class GalleryInline(admin.StackedInline):
    model  = Gallery
    extra  = 0
    fields = ['title', 'description', 'image', 'year', 'order']
    verbose_name        = "Gallery Item"
    verbose_name_plural = "6. Galleries"


class AreaOfWorkingInline(admin.StackedInline):
    model  = AreaOfWorking
    extra  = 1
    fields = ['name', 'area_image', 'is_operational', 'order']
    verbose_name        = "Area of Working"
    verbose_name_plural = "7. Areas of Working"


# ══════════════════════════════════════════════════════════════════════════════
# VENTURE
# ══════════════════════════════════════════════════════════════════════════════
@admin.register(Venture)
class VentureAdmin(admin.ModelAdmin):
    list_display  = ['name', 'sector', 'slug', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter   = ['sector', 'is_active']
    search_fields = ['name']
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
        VentureDetailInline,
        ProductInline,
        BrandInline,
        GalleryInline,
        AreaOfWorkingInline,
    ]


# ══════════════════════════════════════════════════════════════════════════════
# STANDALONE ADMINS
# ══════════════════════════════════════════════════════════════════════════════
@admin.register(VentureDetail)
class VentureDetailAdmin(admin.ModelAdmin):
    list_display  = ['title', 'venture', 'order']
    list_editable = ['order']
    list_filter   = ['venture']
    search_fields = ['title']
    fields        = ['venture', 'title', 'description', 'banner_image', 'order']


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