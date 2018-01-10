from django.contrib import admin

from .models import Product, Variation, ProductImage, Category, FeaturedProduct


# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1
    max_num = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'price']
    inlines = [
        VariationInline,
        ProductImageInline,
    ]


admin.site.register(Variation)
admin.site.register(FeaturedProduct)
admin.site.register(ProductImage)
admin.site.register(Category)
