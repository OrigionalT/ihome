# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import django.http
from django.shortcuts import render

# Create your views here.
from django import http
from ihome.utils.views import *


class HousesView(LoginRequiredJSONMixin, View):
    # {
    #     'data':[
    #         {
    #               'address':'房屋地址'，
    #               'area_name':'东城区'，
    #               'ctime':'2019-11-12'，
    #               'house_id':'1'，
    #               'img_url':'房屋图片地址'，
    #               'order_count':0，
    #               'price':1000，
    #               'room_count':1，
    #               'title':'国贸CBD三里屯地铁阳光超赞大卧室'，
    #               'user_avatar':'用户图像地址'，
    #         },
    #         {
    #
    #         },
    #         ......
    #     ],
    #     'errmsg':'OK',
    #     'errno':'0',
    # }

    def get(self, request):
        # 获取user
        user = request.user
        # 获取我发布的房源
        user_house_info = user.house_set.all().order_by('-create_time')
        # 创建data列表
        data = []
        # 迭代数据对象获取数据
        for house in user_house_info:
            data_dict = {
                'address': house.address,
                'area_name': house.area,
                'ctime': house.create_time.strftime('%Y-%m-%d'),
                'house_id': house.id,
                'img_url': house.index_image_url,
                'order_count': house.order_count,
                'price': house.price,
                'room_count': house.room_count,
                'title': house.title,
                'user_avatar': user.avatar_url,
            }
            data.append(data_dict)
        return http.JsonResponse({'data':data,'errno':RET.OK,'errmsg':'OK'})

class HousesView(LoginRequiredJSONMixin,View):
    def post(self, request):
        '''
        发布新房源API
        :param request:
        :return: json
        '''
        json_dict = json.loads(request.body)


