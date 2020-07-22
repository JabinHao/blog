from django.contrib import admin
from .models import Article, Category, Tag, Carousel, FriendLink

# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
        # 筛选器，这里我们选择按创建时间筛选
        date_hierarchy = 'create_date'

        exclude = ('views',)

        # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
        list_display = ('id', 'title', 'author', 'create_date', 'modify_date')

        # 设置需要添加<a>标签的字段
        list_display_links = ('title',)

        # 过滤器
        list_filter = ('create_date', 'category')

        list_per_page = 50  # 控制每页显示的对象数量，默认是100

        filter_horizontal = ('tags',) # 编辑界面动作选项

        # 限制用户权限，只能看到自己编辑的文章
        def get_queryset(self, request):
            qs = super(ArticleAdmin, self).get_queryset(request)
            if request.user.is_superuser:
                return qs
            return qs.filter(author=request.user)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'content', 'img_url', 'url')

@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'link', 'create_date', 'is_active', 'is_show')
    date_hierarchy = 'create_date'
    list_filter = ('is_active', 'is_show')


# 其他设置

# 调整页面头部内容和标题
admin.site.site_header = 'Jacob的网站后台管理系统'  # 此处设置页面显示标题
admin.site.site_title = '博客后台'  # 此处设置页面头部标题
