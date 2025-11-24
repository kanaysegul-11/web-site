from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('makale/', views.makale, name='makale'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('hakkimizda/', views.about, name='about'),
    path('reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('footer/', views.footer, name='footer'),
    path('proje_fikirleri/', views.proje, name='proje')

]
