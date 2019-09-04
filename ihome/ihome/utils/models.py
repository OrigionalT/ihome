from django.db import models

class BaseModel(models.Model):

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 更新时间
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        # 当前的类时抽象类: 抽象类的特点: 不会生成表,就是为了让别人继承的
        abstract = True