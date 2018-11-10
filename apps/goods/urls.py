from django.conf.urls import url
# from django.contrib.auth.decorators import login_required
from goods.views import IndexView, DetailsView

urlpatterns = [
    url(r'^index$', IndexView.as_view(), name='index'),  # 首页
    url(r'^goods/(?P<goods_id>\d+)$', DetailsView.as_view(), name='detail'),  # 详情页
]

app_name = 'goods'