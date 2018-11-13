from django.conf.urls import url
# from django.contrib.auth.decorators import login_required
from cart.views import CartAddView

urlpatterns = [

    url(r'^add$', CartAddView.as_view(), name='add'),  # 添加购物车记录

]


# app_name = 'cart'