from django.conf.urls import url
# from django.contrib.auth.decorators import login_required
from goods import views

urlpatterns = [
    url(r'^$', views.index, name='index'),  # 首页
    # url(r'^register$', RegisterView.as_view(), name = 'register')
]

app_name = 'goods'