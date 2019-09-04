# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ihome.settings.dev")
# project_name 项目名称
django.setup()
# Create your tests here.
from address.models import Area

if __name__ == '__main__':

    areas = Area.objects.all()

        # return http.JsonResponse({'errno': RET.DBERR, 'errmsg': '获取参数失败'})
    data = []
    for area in areas:
        data_dict = {
            'aid': area.id,
            'aname': area.name
        }
        data.append(data_dict)
    print(data)