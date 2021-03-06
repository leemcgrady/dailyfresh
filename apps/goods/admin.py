from django.contrib import admin
from django.core.cache import cache
from goods.models import Goods, GoodsType, IndexGoodsBanner, IndexPromotionBanner, GoodsSKU, IndexTypeGoodsBanner


# Register your models here.
class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''新增或更新表中的数据时调用'''
        super().save_model(request, obj, form, change)

        # 发出任务，让celery worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存数据
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        '''删除表中的数据时调用'''
        super().delete_model(request, obj)
        # 发出任务，让celery worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()
        cache.delete('index_page_data')


class GoodsAdmin(BaseModelAdmin):

    fields = ('name', 'detail')
    list_display = ('name', 'detail')
    search_fields = ('name', )
    list_per_page = 20


class GoodsTypeAdmin(BaseModelAdmin):

    list_display = ('name', 'logo')


class IndexGoodsBannerAdmin(BaseModelAdmin):
    list_display = ('sku', )


class GoodsSKUAdmin(BaseModelAdmin):
    list_display = ('name',)


class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    pass


class IndexPromotionBannerAdmin(BaseModelAdmin):
    pass


admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsType,GoodsTypeAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(GoodsSKU, GoodsSKUAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
