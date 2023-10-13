from django.contrib import admin
from .models import OnlineShop
from django.utils.safestring import mark_safe

# Register your models here.
class OnlineShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'price', 'created_time','update_time','auction','get_html_image']
    list_filter = ['auction', 'created_time']
    actions = ['make_auction_as_false','make_auction_as_true']
    fieldsets = (
    ('Общее', {
        'fields': ('title', 'description','image','user')
    }),
    ('Финансы',{
        'fields':('price','auction'),
        'classes':['collapse']
    }
    )
    )


class PostAdmin(admin.ModelAdmin):

    readonly_fields = ["preview","image"]

    def preview(self, obj):
        return mark_safe("image")
    @admin.action(description='Убрать возможность торга')
    def make_auction_as_false(self, request, queryset):
        queryset.update(auction=False)
    @admin.action(description='Предоставить возможность торга')
    def make_auction_as_true(self, request, queryset):
        queryset.update(auction=True)


    
admin.site.register(OnlineShop, OnlineShopAdmin)    
