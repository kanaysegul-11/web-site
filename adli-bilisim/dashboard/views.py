from django.shortcuts import render
from blog.models import Post, Category

def dashboard_home(request):
    total_posts = Post.objects.count()
    total_categories = Category.objects.count()
    recent_posts = Post.objects.order_by('-created_at')[:5]
   
    return render(request, 'dashboard/home.html', {
        'total_posts': total_posts,
        'total_categories': total_categories,
        'recent_posts': recent_posts,
    })
