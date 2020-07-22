from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    body = models.TextField('正文')                # 正文

    slug = models.SlugField(unique=True)    # 文章url
    create_date = models.DateTimeField(default=timezone.now)    # 创建时间
    modify_date = models.DateTimeField(auto_now=True)   # 修改时间

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

    def get_pre(self):
        return Article.objects.filter(id__lt=self.id).order_by('-id').first()

    def get_next(self):
        return Article.objects.filter(id__gt=self.id).order_by('id').first()

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug':self.slug})

# 首页轮播
class Carousel(models.Model):
    number = models.IntegerField('编号', help_text='编号决定图片播放的顺序，图片不要多于5张')
    title = models.CharField('标题', max_length=20, blank=True, null=True, help_text='标题可以为空')
    content = models.CharField('描述', max_length=80)
    img_url = models.CharField('图片地址', max_length=200)
    url = models.CharField('跳转链接', max_length=200, default='#', help_text='图片跳转的超链接，默认#表示不跳转')

    class Meta:
        verbose_name = '图片轮播'
        verbose_name_plural = verbose_name
        # 编号越小越靠前，添加的时间约晚约靠前
        ordering = ['number', '-id']

    def __str__(self):
        return self.content[:25]

# 友情链接
class FriendLink(models.Model):
    name = models.CharField('网站名称', max_length=50)
    description = models.CharField('网站描述', max_length=100, blank=True)
    link = models.URLField('友链地址', help_text='请填写http或https开头的完整形式地址')
    logo = models.URLField('网站LOGO', help_text='请填写http或https开头的完整形式地址', blank=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('是否有效', default=True)
    is_show = models.BooleanField('是否首页展示', default=False)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['create_date']

    def __str__(self):
        return self.name

    def get_home_url(self):
        '''提取友链的主页'''
        u = re.findall(r'(http|https://.*?)/.*?', self.link)
        home_url = u[0] if u else self.link
        return home_url

    def active_to_false(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def show_to_false(self):
        self.is_show = True
        self.save(update_fields=['is_show'])
