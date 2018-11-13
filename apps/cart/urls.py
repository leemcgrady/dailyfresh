from django.conf.urls import url
# from django.contrib.auth.decorators import login_required
from cart.views import CartAddView, CartInfoView

urlpatterns = [

    url(r'^add$', CartAddView.as_view(), name='add'),  # 添加购物车记录
    url(r'^$', CartInfoView.as_view(), name='show'),  # 购物车页面显示
]


# app_name = 'cart'