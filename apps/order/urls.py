from django.conf.urls import url
from order.views import OrderPlaceView, OrderCommitView, OrderPayView,CheckPayView

urlpatterns = [

    url(r'^place$', OrderPlaceView.as_view(), name='place'),  # 商品列表
    url(r'^commit$', OrderCommitView.as_view(), name='commit'),  # 提交订单
    url(r'^pay$', OrderPayView.as_view(), name='pay'),  # 支付
    url(r'^check$', CheckPayView.as_view(), name='check'),  # 车讯结果
]

# app_name = 'order'