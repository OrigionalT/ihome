# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from house.models import House
from ihome.utils.views import LoginRequiredJSONMixin
from order.models import Order
from users.response_code import RET


class OrderView(LoginRequiredJSONMixin, View):
    def put(self,request):
        pass
    def get(self, request):
        role = request.GET.get('role')
        if not role:
            return JsonResponse({ "errmsg": "参数错误", "errno": RET.PARAMERR})
        if role is 'custom':
            pass
        elif role is 'landlord':
            pass
        data={}
        orders=[]


        return JsonResponse({"data": data, "errmsg": "OK", "errno": RET.OK})

    def post(self, request):
        json_dict = json.loads(request.body)
        house_id = json_dict.get('house_id')
        start_date = json_dict.get('start_date')
        end_date = json_dict.get('end_date')

        if not all([house_id, end_date, start_date]):
            return JsonResponse({
                "errno": RET.PARAMERR,
                "errmsg": "参数缺失"})
        try:
            rent_days = (datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%I:%S')
                         - datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%I:%S')).days
            house_info = House.objects.get(id=house_id)
            order = Order.objects.create(
                begin_date=start_date,
                end_date=end_date,
                days=rent_days,
                house_price=int(house_info.price),
                amount=int(rent_days * house_info.price + house_info.deposit),
                status=Order.ORDER_STATUS_CHOICES[1],
                comment='',
                user_id=house_info.user_id,
                house_id=house_id
            )
        except:
            return JsonResponse({
                "errno": RET.DBERR,
                "errmsg": "数据库插入出错"})
        data = order.id
        return JsonResponse({"data": data,
                             "errno": RET.OK,
                             "errmsg": "OK"})
