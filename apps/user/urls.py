from django.conf.urls import url
# from django.contrib.auth.decorators import login_required
# from user import views
from user.views import RegisterView, LoginView, LogoutView, UserInfoView, UserOrderView, AddressView
# from itsdangerous import TimedJSONWebSignatureSerializer
# from user.views import RegisterView, ActiveView, LoginView, LogoutView, UserInfoView, UserOrderView, AddressView
# from django.contrib.auth.views import login from . import views
urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    # url(r'^order$', UserOrderView.as_view(), name='order'),
    url(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'), # 用户中心-订单页
    url(r'^address$', AddressView.as_view(), name='address'),
    url(r'^$', UserInfoView.as_view(), name='user'),
]

app_name = "user"



