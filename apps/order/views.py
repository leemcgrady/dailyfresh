from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.db import transaction
from django.conf import settings
from django.views.generic import View

from user.models import Address
from goods.models import GoodsSKU
from order.models import OrderInfo, OrderGoods

from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin
from datetime import datetime

import os


class OrderPlaceView(LoginRequiredMixin, View):

    def post(self, request):

        user = request.user

        sku_ids = request.POST.getlist('sku_ids') # [1,26]

        if not sku_ids:
            return redirect(reverse("cart:show"))

        conn = get_redis_connection("default")

        cart_key = "cart_%d" % user.id

        skus = []

        total_count = 0
        total_price = 0

        # 遍历sku_ids获取用户要购买的商品的信息
        for sku_id in sku_ids:
            # 根据商品的id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            # 获取用户所要购买的商品的数量
            count = conn.hget(cart_key, sku_id)
            # 计算商品的小计
            amount = sku.price*int(count)
            # 动态给sku增加属性count,保存购买商品的数量
            sku.count = int(count)
            # 动态给sku增加属性amount,保存购买商品的小计
            sku.amount = amount
            # 追加
            skus.append(sku)
            # 累加计算商品的总件数和总价格
            total_count += int(count)
            total_price += amount

        # 运费:实际开发的时候，属于一个子系统
        transit_price = 10  # 写死

        # 实付款
        total_pay = total_price + transit_price


        # 获取用户的收件地址
        addrs = Address.objects.filter(user=user)

        sku_ids = ",".join(sku_ids)

        context = {'skus':skus,
                   'total_count':total_count,
                   'total_price':total_price,
                   'transit_price':transit_price,
                   'total_pay':total_pay,
                   'addrs':addrs,
                   'sku_ids':sku_ids}

        # 使用模板
        return render(request, 'place_order.html', context)


class OrderCommitView(View):

    @transaction.atomic
    def post(self, request):

        user = request.user

        if not user.is_authenticated:

            return JsonResponse({"res": 0, "errmsg": "请先登录"})


        # 接收参数
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids') # 1,3

        # 校验参数
        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res':1, 'errmsg':'参数不完整'})

        # 校验支付方式
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return JsonResponse({'res':2, 'errmsg':'非法的支付方式'})

        # 校验地址
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            # 地址不存在
            return JsonResponse({'res':3, 'errmsg':'地址非法'})

        order_id = datetime.now().strftime("%Y%h%m%H%M%S") + str(user.id)

        transit_price = 10

        total_count = 0
        total_price = 0

        save_id = transaction.savepoint()

        try:

            order = OrderInfo.objects.create(order_id=order_id,
                                             user=user,
                                             addr=addr,
                                             pay_method=pay_method,
                                             total_count=total_count,
                                             total_price=total_price,
                                             transit_price=transit_price)

            conn = get_redis_connection("default")

            cart_key = "cart_%d" % user.id

            sku_ids = sku_ids.split(",")

            for sku_id in sku_ids:

                try:
                    sku = GoodsSKU.objects.select_for_update().get(id=sku_id)

                except:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 4, 'errmsg':'商品不存在'})

                count = conn.hget(cart_key, sku_id)

                if int(count) > sku.stock:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 6, 'errmsg':'商品库存不足'})

                OrderGoods.objects.create(order=order,
                                          sku=sku,
                                          count=count,
                                          price=sku.price)
                sku.stock -= 1
                sku.sales += 1
                sku.save()

                amount = sku.price * int(count)
                total_count += int(count)
                total_price += amount

            order.total_count = total_count
            order.total_price = total_price
            order.save()

        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res':7, 'errmsg':'下单失败'})

        transaction.savepoint_commit(save_id)

        conn.hdel(cart_key, *sku_ids)

        return JsonResponse({'res':5, 'message':'创建成功'})



