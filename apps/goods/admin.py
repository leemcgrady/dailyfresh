from django.contrib import admin
from goods.models import Goods

# Register your models here.


class GoodsAdmin(admin.ModelAdmin):

    fields = ('name', 'detail')
    list_display = ('name', 'detail')
    search_fields = ('name', )
    list_per_page = 20


admin.site.register(Goods, GoodsAdmin)