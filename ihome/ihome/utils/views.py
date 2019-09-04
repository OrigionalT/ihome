# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib.parse import urlencode

from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

import http

from django.contrib.auth.decorators import login_required

from users.response_code import RET


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        return login_required(view)


from django.utils.decorators import wraps


def login_required_json(view_func):
    """
    判断用户是否登录的装饰器，并返回 json
    :param view_func: 被装饰的视图函数
    :return: json、view_func
    """

    # 恢复 view_func 的名字和文档
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # 如果用户未登录，返回 json 数据
        if not request.user.is_authenticated():
            return http.JsonResponse({'code': RET.SESSIONERR, 'errmsg': '用户未登录'})
        else:
            # 如果用户登录，进入到 view_func 中
            return view_func(request, *args, **kwargs)

    return wrapper


class LoginRequiredJSONMixin(object):
    """验证用户是否登陆并返回 json 的扩展类"""

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required_json(view)


def get_html_file(request, file_name):
    # 判断网站的logo,不是就转跳
    if file_name != 'favicon.ico':
        file_name = '/static/html/' + file_name
    params = request.GET
    if params:
        result = urlencode(params)
    return redirect(file_name)


def index(request):
    return redirect('/static/html/index.html')
