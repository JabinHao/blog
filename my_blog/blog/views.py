from django.shortcuts import render
from django.views import generic
from django.utils.text import slugify
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Article, Category, Tag
from django.core.cache import cache

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
            'mdx_math',
            TocExtension(slugify=slugify),
            ])
        obj.body = md.convert(obj.body)
        obj.toc = md.toc
        return obj

def test(request):
    return render(request, 'transformation.html')
