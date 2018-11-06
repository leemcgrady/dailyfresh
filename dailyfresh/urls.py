from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')), # 富文本编辑器
    # url(r'^user/', include('user.urls',app_name='user', namespace='user')), # 用户模块
    # url(r'^cart/', include('cart.urls',app_name='cart', namespace='cart')), # 购物车模块
    # url(r'^order/', include('order.urls',app_name='order', namespace='order')), # 订单模块
    # url(r'^', include('goods.urls',app_name='goods', namespace='goods')), # 商品模块
    # url(r'^user/', include(('user.urls',app_name='user'), namespace='user')), # 用户模块
    # url(r'^cart/', include(('cart.urls',app_name='cart'), namespace='cart')), # 购物车模块
    # url(r'^order/', include(('order.urls',app_name='order'), namespace='order')), # 订单模块
    # url(r'^', include(('goods.urls',app_name='goods'), namespace='goods')), # 商品模块
    url(r'^user/', include(('user.urls','user'), namespace='user')), # 用户模块
    # url(r'^user/', include('user.urls', namespace='user')), # 用户模块
    url(r'^cart/', include(('cart.urls','cart'), namespace='cart')), # 购物车模块
    url(r'^order/', include(('order.urls','order'), namespace='order')), # 订单模块
    url(r'^', include(('goods.urls','goods'), namespace='goods')), # 商品模块
    # url(r'^user/', include('user.urls', namespace='user')), # 用户模块
    # url(r'^cart/', include('cart.urls', namespace='cart')), # 购物车模块
    # url(r'^order/', include('order.urls', namespace='order')), # 订单模块
    # url(r'^', include('goods.urls', namespace='goods')), # 商品模块
]

# from django.urls import path
# from django.conf.urls import include, url
# from django.contrib import admin
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'', include(('learning_logs.urls', "learning_logs"), namespace="learning_logs")),
# ]