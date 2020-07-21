from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    '''文章分类'''
    name = models.CharField(max_length=200)

    class Meta:
        '''定义模型的一些属性'''
        verbose_name = '分类' # 中文名
        verbose_name_plural = verbose_name # 复数形式
        ordering = ['name'] # 排序依据

    def __str__(self):
        '''返回模型的信息'''
        return self.name

class Tag(models.Model):
    '''文章标签'''
    name = models.CharField(max_length=100)

    class Meta:
        '''定义模型的一些属性'''
        verbose_name = '标签' # 中文名
        verbose_name_plural = verbose_name # 复数形式
        ordering = ['name'] # 排序依据

    def __str__(self):
        '''返回模型的信息'''
        return self.name

class Article(models.Model):
    '''文章模型，储存文章内容'''
    title = models.CharField(max_length=200) # 文章标题
    body = models.TextField()                # 正文

    slug = models.SlugField(unique=True)    # 文章url
    create_date = models.DateTimeField()    # 创建时间
    modify_date = models.DateTimeField()   # 修改时间

    summary = models.TextField('摘要', max_length=400, blank=True)# 摘要，可以为空
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # 分类和标签
    tags = models.ManyToManyField(Tag, blank=True)
    views = models.IntegerField('阅览量', default=0)

    author = models.ForeignKey(User, verbose_name='作者',on_delete=models.CASCADE)   # 作者

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        '''如果有摘要则显示摘要，否则显示文章前50个字'''
        if len(self.summary):
            return self.summary
        else:
            return self.body[:50]+'...'

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])
