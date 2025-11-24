from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category,ReadabilityInfo,Vote, Tag
from .forms import CommentReplyForm
import feedparser
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
import re

def index(request):
    news_items = get_milliyet_tech_news()
    homepage_post = get_object_or_404(Post, slug='makale')  # tam burada çağrılır
    comments = Comment.objects.filter(post=homepage_post).order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = homepage_post  # işte bu satır kritik
            comment.save()
            return redirect('blog:index')
    else:
        form = CommentForm()

    return render(request, 'blog/index.html', {
        'news_items': news_items,
        'comments': comments,
        'form': form
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    readability = ReadabilityInfo.objects.filter(post=post).first()
    votes = Vote.objects.filter(post=post)
    helpful_count = votes.filter(is_helpful=True).count()
    not_helpful_count = votes.filter(is_helpful=False).count()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'readability': readability,
        'helpful_count': helpful_count,
        'not_helpful_count': not_helpful_count
    })

def makale(request):
    posts = Post.objects.order_by('-created_at')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'blog/makale.html', {
        'posts': posts,
        'categories': categories,
        'tags': tags
    })
def about(request):
    return render(request, 'blog/about.html')
def footer(request):
    return render(request, 'blog/footer.html')
def proje(request):
    return render(request, 'blog/proje.html')

def get_milliyet_tech_news():
    url = "https://www.milliyet.com.tr/rss/rssNew/teknolojiRss.xml"
    feed = feedparser.parse(url)
    news_items = []

    for entry in feed.entries[:3]:  # kaç haber göstereceksen
        # Önce media_content dene
        image = entry.get('media_content', [{}])[0].get('url', '')

        # Eğer boşsa summary içinden <img> ara
        if not image and 'summary' in entry:
            match = re.search(r'<img[^>]+src="([^"]+)"', entry.summary)
            if match:
                image = match.group(1)

        news_items.append({
            'title': entry.title,
            'summary': re.sub(r'<[^>]+>', '', entry.summary),  # HTML tag temizle
            'link': entry.link,
            'image': image or "https://via.placeholder.com/300x200"
        })

    return news_items

def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.author = request.user.username  # ✅ kullanıcı adı buraya yazılıyor
            reply.save()

    if comment.post.slug == 'makale':
        return redirect('blog:index')
    else:
        return redirect('blog:post_detail', slug=comment.post.slug)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return redirect('makale')
