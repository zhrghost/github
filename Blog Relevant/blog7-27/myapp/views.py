from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator
from .models import *

# Create your views here.


# 显示文章数据
def show_Articles_data(request):
    data=Article.objects.all()
    # 得到get请求中的页码参数
    page_num = request.GET.get('page', 1)
    # 实例化一个分页器
    paginator = Paginator(data, 5)
    # 通过页码获得对应的文章，可以使用paginator.page， 但是这个方法不能对get获得的数据进行筛选，所以使用get_page
    article_list = paginator.get_page(page_num)
    # 前端页面参数字典
    context = {}
    context['data'] = article_list.object_list
    context['obj'] = article_list
    # 判断是否当前页是否是第一页
    if int(article_list.number) == 1:
        # 总页数超过3页
        if (int(article_list.number) + 2) <= paginator.num_pages:
            context["page_num"] = range(int(article_list.number), int(article_list.number) + 3)
        else:
            context["page_num"]=range(int(article_list.number), int(paginator.num_pages) + 1)
    # 判断是否是最后一页
    elif not article_list.has_next():
        if (int(article_list.number) - 2) > 0:
            context["page_num"]=range(int(article_list.number) - 2, int(article_list.number) + 1)
        else:
            context["page_num"]=range(1, int(article_list.number) + 1)
    else:
        if (int(article_list.number) - 1) > 0 and (int(article_list.number) + 1) <= paginator.num_pages:
            context['page_num'] = range(int(article_list.number) - 1, int(article_list.number) + 2)
        elif (int(article_list.number) - 1) <= 0 and (int(article_list.number) + 1) <= paginator.num_pages:
            context['page_num']=range(1, int(article_list.number) + 2)
        else:
            context['page_num']=range(1, int(article_list.number) + 1)
    return render(request, 'index.html', context)


def content(request):
    pk = request.GET.get('pk')
    try:
        # 通过获得get请求中的数据查询文本内容，根据判断长度来确定是否查找到数据（数据是否存在）
        # 存在数据，则在原数据的基础上加1
        articles=Article.objects.get(pk=pk)
        if Read_Num.objects.filter(article=articles).count():
            articles.read_num.read_num_data += 1
            articles.read_num.save()
            # 不存在数据，创建对象，并且使阅读数设置为0
        else:
            readnum = Read_Num()
            readnum.article = articles
            readnum.read_num_data = 1
            readnum.save()
        text = articles.text
        context = {}
        context['text'] = text
        return render(request, 'content_template.html', context)
    except:
        return HttpResponse('404')