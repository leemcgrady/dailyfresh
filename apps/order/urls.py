from django.conf.urls import url
from order.views import OrderPlaceView

urlpatterns = [

    url(r'^place$', OrderPlaceView.as_view(), name='place'),  # 商品列表
]

# app_name = 'order'