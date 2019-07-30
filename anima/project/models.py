from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
# Create your models here.

source_type = (('qq', "qq群"),
               ('referral', "内部转介绍"),
               ('website', "官方网站"),
               ('baidu_ads', "百度推广"),
               ('office_direct', "直接上门"),
               ('WoM', "口碑"),
               ('public_class', "公开课"),
               ('others', "其它"),)

enroll_status_choices = (('signed', "已报名"),
                         ('unregistered', "未报名"),
                         ('studying', '学习中'),
                         ('paid_in_full', "学费已交齐"))

course_status_choices = (('publish', "已发布"),
                         ('unpublished', "未发布"),
                         ('deleted', "已经删除"))

# AbstractUser 继承user表
class UserInfo(AbstractUser):
    #销售,管理员,咨询师
    telephone = models.CharField(max_length=32, null=True)
    roles = models.ManyToManyField(to='Role', verbose_name='用户所拥有的角色', blank=True)

# 角色表
class Role(models.Model):
    # 角色名字
    name = models.CharField(max_length=32, verbose_name='角色名称')
    # 角色权限
    permissions = models.ManyToManyField(to='Permission', verbose_name='角色所拥有的权限', blank=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    """
    菜单表
    """
    title = models.CharField(max_length=32, verbose_name='一级菜单', null=True,blank=True)
    icon = models.CharField(max_length=32, verbose_name='一级菜单图标', null=True,blank=True)

class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(max_length=32, verbose_name='标题')
    url = models.CharField(max_length=132, verbose_name='权限')

    menu = models.ForeignKey('Menu', null=True)
    pid = models.ForeignKey('self', null=True)

    class Meta:
        verbose_name_plural = '权限表'
        verbose_name = '权限表'

    def __str__(self):
        return self.title

class Customer(models.Model):
    """
    客户表（最开始的时候大家都是客户，销售就不停的撩你，你还没交钱就是个客户）
    """
    qq = models.CharField(verbose_name='QQ', max_length=64, unique=True, help_text='QQ号必须唯一')
    qq_name = models.CharField('QQ昵称', max_length=64, blank=True, null=True)
    name = models.CharField('姓名', max_length=32, blank=True, null=True, help_text='学员报名后，请改为真实姓名')
    sex_type = (('male', '男'), ('female', '女'))
    sex = models.CharField("性别", choices=sex_type, max_length=16, default='male', blank=True, null=True) #存的是male或者female，字符串
    birthday = models.DateField('出生日期', default=None, help_text="格式yyyy-mm-dd", blank=True, null=True)
    phone = models.CharField('手机号', blank=True, null=True, max_length=32)
    source = models.CharField('客户来源', max_length=64, choices=source_type, default='qq')
    introduce_from = models.ForeignKey('self', verbose_name="转介绍自学员", blank=True, null=True)  #self指的就是自己这个表，和下面写法是一样的效果

    course = models.ForeignKey(to='Course', verbose_name="课程报名", null=True) #多选，并且存成一个列表的格式
    # class_type = models.CharField("班级类型", max_length=64, choices=class_type_choices, default='fulltime')
    customer_note = models.TextField("客户备注", blank=True, null=True, )
    status = models.CharField("状态", choices=enroll_status_choices, max_length=64, default="unregistered",help_text="选择客户此时的状态") #help_text这种参数基本都是针对admin应用里面用的

    date = models.DateTimeField("咨询日期", auto_now_add=True)

    def __str__(self):
        return self.name+":"+self.qq  #主要__str__最好是个字符串昂，不然你会遇到很多的坑，还有我们返回的这两个字段填写数据的时候必须写上数据，必然相加会报错，null类型和str类型不能相加等错误信息。


class Course(models.Model):
    """
    课程表（后端和咨询师可以发布课程）
    """
    uid = models.CharField(max_length=64, verbose_name='发布人id')
    course_name = models.CharField(max_length=32, verbose_name='课程名字')
    start_time = models.DateTimeField("开始时间", auto_now_add=True)
    end_time = models.DateTimeField("结束时间", auto_now_add=True)
    status = models.CharField("状态", choices=course_status_choices, max_length=64, default="unpublished")
    address = models.CharField(max_length=64, verbose_name="课程地址")
    content = models.TextField("课程详情", blank=True, null=True)

    def __str__(self):
        return self.course_name






