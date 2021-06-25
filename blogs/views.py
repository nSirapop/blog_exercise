from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Blog, Post
from .forms import BlogForm, PostForm
# Create your views here.
# redirect want a view argument, request want a template html argument

def check_owner(user, request):
    if user.owner != request.user:
        raise Http404

def index(request):
    """Home page for Blog"""
    return render(request, 'blogs/index.html') # original request and a template

@login_required
def blogs(request):
    """A page show all blogs."""
    blogs = Blog.objects.filter(owner=request.user).order_by('date_added')
    context = {'blogs': blogs}
    return render(request, 'blogs/blogs.html', context)

@login_required
def blog(request, blog_id):
    """A page for each blog"""
    blog = get_object_or_404(Blog, id=blog_id)
    check_owner(blog, request)
    posts = blog.post_set.order_by('-date_added')
    context = {'blog': blog, 'posts': posts}
    return render(request, 'blogs/blog.html', context)

@login_required
def post(request, post_id):
    """A post in the blog."""
    post = get_object_or_404(Post, id=post_id)
    blog = post.blog
    check_owner(blog, request)
    context = {'post': post, 'blog': blog}
    return render(request, 'blogs/post.html', context)

@login_required
def new_blog(request):
    """Add a new blog"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = BlogForm()
    else:
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return redirect('blogs:blogs')
# Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)
# render code will be execute for a blank form or invalid submitted form only.

@login_required
def new_post(request, blog_id):
    """Add a post into the blog"""
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return redirect('blogs:blog', blog_id=blog_id)

# Display a blank or invalid form.
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    blog = post.blog
    check_owner(blog, request)

    if request.method != 'POST':
    # This is an existing post, so I'll put an existing form
        form = PostForm(instance=post)
    else:
        # POST data submitted; after edited data.
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:post', post_id=post_id)

    context = {'post': post, 'blog': blog, 'form':form}
    return render(request, 'blogs/edit_post.html', context)
