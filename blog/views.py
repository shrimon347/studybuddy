from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .form import *
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Post, Category, Comment, Like
from django.utils.text import slugify
from django.contrib import messages

# Create your views here.
def index(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    post_comment = Comment.objects.filter(
        Q(post__comment__comment__icontains = q)
    )[0:5]
    posts = Post.objects.filter(
        Q(category__title__icontains=q) |
        Q(title__icontains = q) |
        Q(content__icontains = q)
    )
    blog_count = Post.objects.filter(status=True).count()
    page = Paginator(posts, 5)
    page_number = request.GET.get('page' , 1)
    postPagefianal= page.get_page(page_number)
    totalpage = postPagefianal.paginator.num_pages
    categorys = Category.objects.all()[0:5]
    context = {'posts' : postPagefianal,"categorys":categorys,"blog_count":blog_count,
               'postdata':postPagefianal, 'lastpage':totalpage,'totalpagelist':[n+1 for n in range (totalpage)],'page':page_number,
               'post_comment':post_comment
               }
    return render(request,'blog/index.html', context)

def detail(request, slug):
    post = Post.objects.get(slug=slug)
    posts = Post.objects.exclude(id__exact= post.id)[:5]
    blog_comments = post.comment_set.all()
    

    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            comment = request.POST.get('body')
        )
        return redirect('detail', slug=slug)

    context = {'post' : post,'posts' : posts, 'blog_comments':blog_comments}
    return render(request,'blog/detail.html', context)


@login_required(login_url='login')
def create_blog(request):
    form = PostFrom()
    update = "Create"
    categorys = Category.objects.all()
    if request.method == "POST":    
        form = PostFrom(request.POST, request.FILES)
        title_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(title=title_name)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.writer = request.user
            post.category = category
            post.save()
            messages.info(request, 'Article createrd successfully')
            return redirect('index')
        else:
            messages.error(request, 'Article not createrd')
    context = {'form':form,'update':update, 'categorys':categorys}
    return render(request,'blog/create.html', context)


@login_required(login_url='login')
def updatePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostFrom(instance=post)
    update = "Update"
    if request.user != post.writer:
        return HttpResponse('Your are not allowed here!!')
    if request.method == "POST":
        form = PostFrom(request.POST, request.FILES,instance=post)
        if form.is_valid:
            form.save()
            return redirect('detail', slug=post.slug)
    
    context = {'form':form, 'update':update}
    return render(request,'blog/create.html', context)

@login_required(login_url='login')
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostFrom(instance=post)
    
    if request.user != post.writer:
        return HttpResponse('Your are not allowed here!!')

    if request.method == "POST":
        post.delete()
        return redirect('index')
    context = {'form':form, 'obj':post}
    return render(request, 'blog/delete.html', context)


def categoryPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    categorys = Category.objects.filter(title__icontains=q)
    return render(request, 'blog/allCategory.html', {'categorys': categorys})

@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    data = 'Comment'
    if request.user != comment.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        comment.delete()
        return redirect('index')
    return render(request, 'blog/delete.html', {'obj': comment, 'data':data})

@login_required(login_url='login')
def like_post (request):
    user = request.user 
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id = post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)

        else:
            post_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user = user, post_id = post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = "Like"
        like.save()
    return redirect('index')