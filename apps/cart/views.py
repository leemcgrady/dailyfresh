from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from goods.models import GoodsSKU
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin

# Create your views here.


class CartAddView(View):

    def post(self, request):

        user = request.user

        if not user.is_authenticated:
            return JsonResponse({"res": 0, "errmsg": "请先登录"})

        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")

        if not all([sku_id, count]):
            return JsonResponse({"res": 1, "errmsg": "数据不完整"})

        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({"res": 2, "errmsg": "数量出错"})

        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({"res": 3, "errmsg": "商品不存在"})

        conn = get_redis_connection("default")

        cart_key = "cart_%d" % user.id

        cart_count = conn.hget(cart_key, sku_id)

        if cart_count:
            count = count + int(cart_count)

        if count > sku.stock:
            return JsonResponse({"res": 4, "errmsg": "商品库存不足"})

        conn.hset(cart_key, sku_id, count)

        total_count = conn.hlen(cart_key)

        return JsonResponse({"res": 5, "total_count": total_count, "message": "添加成功"})


class CartInfoView(View):

    def get(self, requset):

        return render(requset, "cart.html")

