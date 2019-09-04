# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

# Create your views here.
import random
import re


from django import http
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django_redis import get_redis_connection
from pymysql import DatabaseError

from libs.captcha.captcha import captcha
from users.models import User
import logging

from users.response_code import RET

logger = logging.getLogger()


class ImageCodeView(View):

    def get(self, request):
        '''
        生成图形验证码, 保存到redis中, 另外返回图片
        :param request:
        :param uuid:
        :return:
        '''
        # 当前图片验证码UUID
        cur = request.GET.get('cur')
        # 上一次图片验证码UUID
        pre = request.GET.get('pre')
        print('cur',cur)
        print(pre)
        if not all([cur, pre]):
            return http.JsonResponse({'errno': RET.PARAMERR,
                                      'errmsg': '参数错误'})
        # 1.生成图形验证码
        text, image = captcha.generate_captcha()

        # 2.链接redis, 获取链接对象
        redis_conn = get_redis_connection('verify_code')

        # 3.利用链接对象, 保存数据到redis
        # redis_conn.setex('key', 'expire', 'value')
        redis_conn.setex('img_{}'.format(cur), 300, text)
        # redis_conn.setex('img_{}'.format(pre), 300, text)
        image_code_server = redis_conn.get('img_{}'.format(cur))
        print('image_code', image_code_server)
        # 4.返回(图片)
        return http.HttpResponse(image, content_type='image/jpg')


class SMSCodeView(View):

    def post(self, request):
        dict = json.loads(request.body)
        user = User
        mobile = dict.get('mobile')
        image_code = dict.get('image_code')
        image_code_id = dict.get('image_code_id')
        redis_conn = get_redis_connection('verify_code')
        if not all([image_code_id, image_code]):
            return http.JsonResponse({'errno': RET.PARAMERR,
                                      'errmsg': '参数错误'})
        if not re.match(r'^1[345789]\d{9}$', mobile):
            return http.JsonResponse({'errno': RET.PARAMERR,
                                      'errmsg': '手机号码错误'})

        # if not user.objects.get(mobile=mobile):
        #     return http.JsonResponse({'errno': RET.PARAMERR,
        #                               'errmsg': '手机号已注册错误'})

        '''
                接收手机号+uuid+图形验证码, 进行验证, 如果通过,发送短信验证码
                :param request:
                :param mobile:
                :return:
                '''

        # 0. 从redis中取值:
        flag = redis_conn.get('send_flag_{}'.format(mobile))
        if flag:
            return http.JsonResponse({'code': RET.THROTTLINGERR,
                                      'errmsg': '发送短信过于频繁'})

        # 4.从redis中取出图形验证码
        image_code_server = redis_conn.get('img_{}'.format(image_code_id))
        if not image_code_server:
            return http.JsonResponse({'errno': RET.DBERR, 'errmsg': '验证码过期'})

        # 5.删除redis中的图形验证码
        try:
            redis_conn.delete('img_{}'.format(image_code_id))
        except Exception as e:
            logger.error(e)
            # logger.info(e)
        print('image_code_ID',image_code_id)
        print('image_code',image_code)
        print('imas',image_code_server.decode().lower())
        # 6.把 前端传入的和redis中的进行对比
        if image_code.lower() != image_code_server.decode().lower():
            return http.JsonResponse({'code': RET.DBERR,
                                      'errmsg': '验证码输入错误'})

        # 7.生成一个随机数, 作为短信验证码(6)
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)
        print('sms',sms_code)
        pl = redis_conn.pipeline()

        # 8.往redis中存储
        pl.setex('send_sms_{}'.format(mobile),
                 300,
                 sms_code)

        pl.setex('send_flag_{}'.format(mobile),
                 60,
                 1)

        # 指定管道:
        pl.execute()

        # 10.返回结果(json)
        return http.JsonResponse({'code': RET.OK,
                                  'errmsg': 'ok'})

        # else:
        #     return http.JsonResponse({'code': RETCODE.OK,
        #                               'errmsg': 'ok'})

class RegisterView(View):

    def post(self,request):
        json_dict = json.loads(request.body)
        mobile =json_dict.get('mobile')
        phonecode =json_dict.get('phonecode')
        password =json_dict.get('password')
        password2 =json_dict.get('password2')
        sms_code_client = json_dict.get('sms_code')

        # 2.校验参数(总体 + 单个)
        # 2.1查看是否有为空的参数:
        if not all([mobile, password, password2, phonecode]):
            return http.HttpResponseForbidden('缺少必传参数')

        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('密码为8-20位的字符串')

        if password != password2:
            return http.HttpResponseForbidden('密码不一致')

        if not re.match(r'^1[345789]\d{9}$', mobile):
            return http.HttpResponseForbidden('手机号格式不正确')


        # 补充: 检验短信验证码的逻辑:
        # 链接redis, 获取链接对象
        redis_conn = get_redis_connection('verify_code')

        # 从redis取保存的短信验证码
        sms_code_server = redis_conn.get('send_sms_%s' % mobile)
        if sms_code_server is None:
            return http.JsonResponse({'errno':RET.DBERR,'errmsg': '无效的短信验证码'})

        # 对比
        if sms_code_client != sms_code_server.decode():
            return http.JsonResponse({'errno':RET.DBERR,'sms_code_errmsg': '输入的短信验证码有误'})

        # 3.往mysql保存数据
        try:
            user = User.objects.create_user(password=password,
                                            username=mobile)
        except DatabaseError:
            return http.JsonResponse({'errno':RET.DBERR,'register_errmsg': '注册失败'})

        # 实现状态保持: session:
        login(request, user)

        # 4.返回结果, 成功则跳转到首页
        # return HttpResponse('跳转到首页没有完成')
        # return redirect(reverse('contents:index'))

        # 生成响应对象
        response = http.HttpResponse()

        # 在响应对象中设置用户名信息.
        # 将用户名写入到 cookie，有效期 15 天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        # 返回响应结果
        return response