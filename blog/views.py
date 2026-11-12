from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category


def post_list(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    posts = Post.objects.filter(status='published')

    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=active_category)

    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories,
        'active_category': active_category,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        body = request.POST.get('body')
        if name and email and body:
            post.comments.create(name=name, email=email, body=body)
            return redirect('post_detail', slug=post.slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
    })