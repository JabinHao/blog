from django.shortcuts import render, redirect
from django.views import generic
from django.utils.text import slugify
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Article, Category, Tag
from django.core.cache import cache
from .forms import ArticleForm
# 引入HttpResponse
from django.http import HttpResponse
# 引入login装饰器
from django.contrib.auth.decorators import login_required

from markdown.extensions.toc import TocExtension  # 锚点的拓展
import markdown
import time, datetime

# Create your views here.
class IndexView(generic.ListView):
    """
        首页视图,继承自ListVIew，用于展示从数据库中获取的文章列表
    """
    # 获取数据库中的文章列表
    model = Article
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'blog/index.html'
    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'articles'

class DetailView(generic.DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get_object(self):
        obj = super(DetailView, self).get_object()
        # 设置浏览量增加时间判断,同一篇文章两次浏览超过半小时才重新统计阅览量,作者浏览忽略
        u = self.request.user
        ses = self.request.session
        the_key = 'is_read_{}'.format(obj.id)
        is_read_time = ses.get(the_key)
        if u != obj.author:
            if not is_read_time:
                obj.update_views()
                ses[the_key] = time.time()
            else:
                now_time = time.time()
                t = now_time - is_read_time
                if t > 60 * 30:
                    obj.update_views()
                    ses[the_key] = time.time()
        # 获取文章更新的时间，判断是否从缓存中取文章的markdown,可以避免每次都转换
        '''
        ud = obj.modify_date.strftime("%Y%m%d%H%M%S")
        md_key = '{}_md_{}'.format(obj.id, ud)
        cache_md = cache.get(md_key)
        if cache_md:
            obj.body, obj.toc = cache_md
        else:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'pymdownx.arithmatex',
                #'markdown.extensions.toc',
                TocExtension(slugify=slugify),
            ])
            obj.body = md.convert(obj.body)
            obj.toc = md.toc
            cache.set(md_key, (obj.body, obj.toc), 60 * 60 * 12)
            '''
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.fenced_code',
            'mdx_math',
            TocExtension(slugify=slugify),
            ])
        obj.body = md.convert(obj.body)
        obj.toc = md.toc
        return obj

# 写文章的视图
class ArticleCreateView(generic.edit.CreateView):
    # 要使用的数据模型
    model = Article
    # 要填写的字段
    form_class = ArticleForm
    # 要使用的模板,默认为article_form.html
    tags = Tag.objects.all()
    categories = Category.objects.all()
    template_name = 'blog/article_create.html'
    context_object_name = 'articles'

    def get(self,request, *args, **kwargs):
        # 请求新建文章，创建表单类实例
        # 向模板提供数据
        context = {'categories': self.categories,'tags':self.tags}
        # 返回模板
        return render(request, 'blog/article_create.html', context)

    def post(self,request,*args, **kwargs):
        # 提交文章
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # Verify form is valid
        if form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = form.save(commit=False)
            new_article.author = self.request.user
            #new_article.tags = Article.objects.get(id=request.POST['tags'])
            #new_article.category = Article.objects.get(id=request.POST['category'])
            # 将新文章保存到数据库中
            new_article.save()
            form.save_m2m()
            # 完成后返回到文章列表
            #messages.success(request, 'Item created successfully!')
            return redirect("blog:index")
        # 如果数据不合法，返回错误信息
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        #
        model = form.save(commit=False)
        model.author = self.request.user
        model.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self,form):
        #
        self.object = None
        return HttpResponse("表单内容有误，请重新填写。")

    def get_success_url(self):
        return reverse('createview')

# s测试页面
def test(request):
    return render(request, 'blog/test.html')
