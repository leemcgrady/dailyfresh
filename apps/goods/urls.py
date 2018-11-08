from django.conf.urls import url
# from django.contrib.auth.decorators import login_required
from goods.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),  # 首页
    # url(r'^register$', RegisterView.as_view(), name = 'register')
]

app_name = 'goods'