from django.contrib import admin
from goods.models import Goods, GoodsType, IndexGoodsBanner, IndexPromotionBanner, GoodsSKU

# Register your models here.


class GoodsAdmin(admin.ModelAdmin):

    fields = ('name', 'detail')
    list_display = ('name', 'detail')
    search_fields = ('name', )
    list_per_page = 20


class GoodsTypeAdmin(admin.ModelAdmin):

    list_display = ('name', 'logo')


class IndexGoodsBannerAdmin(admin.ModelAdmin):
    list_display = ('sku', )


class GoodsSKUAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Goods, GoodsAdmin)

admin.site.register(GoodsType,GoodsTypeAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner)
admin.site.register(GoodsSKU, GoodsSKUAdmin)
