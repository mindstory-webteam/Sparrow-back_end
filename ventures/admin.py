# ventures/admin.py
from django.contrib import admin
from .models import Sector, Venture, Product, Brand, VentureDetail, Gallery, AreaOfWorking


# ── Sector ────────────────────────────────────────────────────────────────────
@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}


# ── Venture inlines ───────────────────────────────────────────────────────────
class VentureDetailInline(admin.TabularInline):
    model = VentureDetail
    extra = 0
    fields = ['title', 'description', 'order']


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ['name', 'image', 'order']


class BrandInline(admin.TabularInline):
    model = Brand
    extra = 0
    fields = ['name', 'logo', 'order']


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 0
    fields = ['title', 'image', 'year', 'order']


class AreaOfWorkingInline(admin.TabularInline):
    """
    Add / edit areas directly inside the Venture admin page.
    Each area has its own image uploaded here.
    """
    model = AreaOfWorking
    extra = 1
    fields = ['name', 'area_image', 'is_operational', 'order']
    verbose_name = "Area of Working"
    verbose_name_plural = "Areas of Working"


# ── Venture ───────────────────────────────────────────────────────────────────
@admin.register(Venture)
class VentureAdmin(admin.ModelAdmin):
    list_display = ['name', 'sector', 'slug', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['sector', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (None, {
            'fields': ('sector', 'name', 'slug', 'description', 'is_active', 'order')
        }),
        ('Images', {
            'fields': ('banner_image',),
        }),
    )

    inlines = [VentureDetailInline, ProductInline, BrandInline, GalleryInline, AreaOfWorkingInline]


# ── Standalone admins ─────────────────────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'venture', 'order']
    list_editable = ['order']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'venture', 'order']
    list_editable = ['order']


@admin.register(VentureDetail)
class VentureDetailAdmin(admin.ModelAdmin):
    list_display = ['title', 'venture', 'order']
    list_editable = ['order']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'venture', 'year', 'order']
    list_editable = ['order']


@admin.register(AreaOfWorking)
class AreaOfWorkingAdmin(admin.ModelAdmin):
    list_display = ['name', 'venture', 'is_operational', 'order']
    list_editable = ['is_operational', 'order']
    list_filter = ['venture', 'is_operational']
    search_fields = ['name']
    fields = ['venture', 'name', 'area_image', 'is_operational', 'order']