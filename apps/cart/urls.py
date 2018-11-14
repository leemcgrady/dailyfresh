from django.conf.urls import url
# from django.contrib.auth.decorators import login_required
from cart.views import CartAddView, CartInfoView, CartUpdateView, CartDeleteView

urlpatterns = [

    url(r'^add$', CartAddView.as_view(), name='add'),  # 添加购物车记录
    url(r'^$', CartInfoView.as_view(), name='show'),  # 购物车页面显示
    url(r'^update$', CartUpdateView.as_view(), name='update'),  # 购物车更新
    url(r'^delete', CartDeleteView.as_view(), name='delete'),  # 购物车更新
]


# app_name = 'cart'