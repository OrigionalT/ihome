# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View

from address.models import Area
from users.response_code import RET


class AreaView(View):
    # {
    #     "errmsg": "OK",
    #     "errno": "0",
    #     "data": [
    #         {
    #             "aid": 1,
    #             "aname": "东城区"
    #         },
    #         {
    #             "aid": 2,
    #             "aname": "西城区"
    #         },
    #         {
    #             "aid": 3,
    #             "aname": "朝阳区"
    #         }
    #     ]
    # }
    def get(self,requset):

        try:
            areas = Area.objects.all()
        except Exception as e:
            return http.JsonResponse({'errno':RET.DBERR,'errmsg':'获取参数失败'})
        data = []
        for area in areas:
            data_dict = {
                'aid':area.id,
                'aname':area.name
            }
            data.append(data_dict)

        return http.JsonResponse({'data':data,'errno':RET.OK,'errmsg':'OK'})