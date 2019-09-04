# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ihome.settings.dev")

django.setup()
from users.models import User

if __name__ == '__main__':
    user = User.objects.get(id=1)
    # 获取我发布的房源
    user_house_info = user.house_set.filter(user=user).order_by('-create_time')
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
        print(data)
