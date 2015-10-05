from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings 
import mistune
# Create your views here.
from miniblog.models import Article, Author, Tag, Classification, RootClassification
from miniblog.forms import ArticleForm
from miniblog.forms import TagForm

def blog_note_show(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    #article.content = mistune.markdown(article.content)
    if request.is_ajax():
        return render(request, 'miniblog/blog_note_show_ajax.html', {"article": article})
    else:
        articles_list = Article.objects.all()
        articles_list = pagination(request, articles_list)
        classes_list = Classification.objects.all()
        rootClass_list = RootClassification.objects.all()
        return render(request, 'miniblog/blog_note_show.html', {
            "classes":classes_list, 
            "articles": articles_list, 
            "article": article,
            "current_class": "all",
            "root_classes": rootClass_list
        })

def blog_note_all(request):
    articles_list = Article.objects.all()
    articles_list = pagination(request, articles_list)
    # if is ajax request
    if request.is_ajax():
        return render(request, 'miniblog/blog_note_article_list_ajax.html', 
            {"articles": articles_list, "current_class": "all"})
    # not an ajax request should return the whole page
    else:
        classes_list = Classification.objects.all()
        rootClass_list = RootClassification.objects.all()
        return render(request, 'miniblog/blog_note.html', {
            "classes":classes_list, 
            "articles": articles_list,
            "current_class": "all",
            "root_classes": rootClass_list
        })
def blog_note_by_class(request, class_id):
    try:
        classobject = Classification.objects.get(pk = int(class_id))
        rootClass_list = RootClassification.objects.all()
        articles_list = classobject.article_set.all()
        articles_list = pagination(request, articles_list)
        if request.is_ajax():
            return render(request, 'miniblog/blog_note_article_list_ajax.html', 
                {"articles": articles_list, "current_class": class_id})
        else:
            classes_list = Classification.objects.all()
            return render(request, 'miniblog/blog_note.html', {
                "classes":classes_list, 
                "articles": articles_list, 
                "current_class": class_id, 
                "root_classes": rootClass_list
            })
    # if no article or no class is found
    except ObjectDoesNotExist:
        return blog_note_all(request)

def pagination(request, queryset):
    if settings.PAGINATION == True:
        pageNO = request.GET.get('page', 1)
        num_in_page = settings.NUM_IN_PAGE
        paginator = Paginator(queryset, num_in_page)
        articles_list = queryset
        try:
            articles_list = paginator.page(pageNO)
            print '%r' %('pagevalid')
        except PageNotAnInteger:
            articles_list = paginator.page(1)
            print '%r' %('PageNotAnInteger')
        except EmptyPage:
            print '%r' %('EmptyPage')
            articles_list = paginator.page(paginator.num_pages)
        finally:
            return articles_list
    else:
        return queryset

def blog_note(request):
    class_id = request.GET.get('class', 'all')
    # if no filter is specified
    if class_id == 'all':
        return blog_note_all(request)
    # the classname is specified
    else:
        return blog_note_by_class(request, int(class_id))

def article_list(request):
    articles_list = Article.objects.all()
    paginator = Paginator(articles_list, 1)
    page = request.GET.get('page')
    tags = Tag.objects.all()
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    return render(request, 'miniblog/article_list.html', {"articles": articles, "tags": tags})

def article_show(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.content = mistune.markdown(article.content)
    return render(request, 'miniblog/article_show.html', {"article": article})

def article_filter(request, tag_id = ''):
    tags = Tag.objects.all()
    tag = Tag.objects.get(id = tag_id)
    articles = tag.article_set.all()
    return render(request, 'miniblog/article_filter.html', {
        "articles": articles, 
        "tag": tag,
        "tags": tags
    })

@csrf_exempt
def article_add(request):
    if request.method == 'POST':
        # form = ArticleForm(request.POST)
        # tag = TagForm(request.POST)
        # if form.is_valid() and tag.is_valid():
        #     cd = form.cleaned_data
        #     cdtag = tag.cleaned_data
        #     tagname = cdtag['tag_name']
        #     for taglist in tagname.split():
        #         Tag.objects.get_or_create(tag_name=taglist.strip())
        #     title = cd['caption']
        #     author = Author.objects.get(id=1)
        #     content = cd['content']
        #     article = Article(caption=title, author=author, content=content)
        #     article.save()
        #     for taglist in tagname.split():
        #         article.tags.add(Tag.objects.get(tag_name=taglist.strip()))
        #         article.save()
        #     id = Article.objects.order_by('-publish_time')[0].id
        #     return HttpResponseRedirect('/miniblog/article/%s' % id)
        try:
            blogTitle = request.POST.get("blogTitle")
            blogAuthor = Author.objects.get(name = request.POST.get("blogAuthor"))
            blogContent = request.POST.get("blogContent")
            blogClass = Classification.objects.get(pk = int(request.POST.get("blogClass")))
            article = Article(caption=blogTitle, author=blogAuthor, content=blogContent, classification=blogClass)
            article.save()
            response = HttpResonse('success')
            response['Access-Control-Allow-Origin'] = "http://localhost:3000"
            print response
            return response
        except KeyError:
            response = HttpResonse('failed')
            response['Access-Control-Allow-Origin'] = "http://localhost:3000"
            return response
    else:
        form = ArticleForm()
        tag = TagForm(initial = {'tag_name': 'notages'})
    return render(request, 'miniblog/article_add.html',{'form': form, 'tag': tag})

def article_update(request, article_id = ""):
    id = article_id
    # if the form is submitted
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data
            cdtag = tag.cleaned_data
            tagname = cdtag['tag_name']
            tagnamelist = tagname.split()
            for taglist in tagnamelist:
                Tag.objects.get_or_create(tag_name=taglist.strip())
            title = cd['caption']
            content = cd['content']
            article = Article.objects.get(id=id)
            if article:
                article.caption = title
                article.content = content
                article.save()
                # add the new tags
                for taglist in tagnamelist:
                    article.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                    article.save()
                tags = article.tags.all()
                # delete the old tags
                for tagname in tags:
                    tagname = unicode(str(tagname), "utf-8")
                    if tagname not in tagnamelist:
                        notag = article.tags.get(tag_name=tagname)
                        article.tags.remove(notag)
            else:
                # create an new article 
                article = article(caption=article.caption, content=article.content)
                article.save()
            return HttpResponseRedirect('/miniblog/article/%s' % id)
    # if the form is not submitted
    else:
        # if cannot find the article
        try:
            article = article.objects.get(id=id)
        except Exception:
            raise Http404
        # create the first form
        form = articleForm(initial={'caption': article.caption, 'content': article.content}, auto_id=False)
        tags = article.tags.all()
        # if the article has tags then populate the form with the tags
        if tags:
            taginit = ''
            for x in tags:
                taginit += str(x) + ' '
            tag = TagForm(initial={'tag_name': taginit})
        # else create an empty form
        else:
            tag = TagForm()
    return render(request, 'miniblog/article_add.html', {'article': article, 'form': form,
        'id': id, 'tag': tag})
    # this is equal to the render() method
    # render_to_response('article_add.html',
    #     {'article': article, 'form': form, 'id': id, 'tag': tag},
    #     context_instance=RequestContext(request))

def article_delete(request, article_id=""):
    try:
        article = Article.objects.get(id = article_id)
    except Exception:
        raise Http404
    # if find the article
    if article:
        article.delete()
        return HttpResponseRedirect("/miniblog/articlelist/")
    # if cannot find the article
    articles = Article.objects.all()
    return render(request, 'miniblog/article_list.html', {"articles": articles})