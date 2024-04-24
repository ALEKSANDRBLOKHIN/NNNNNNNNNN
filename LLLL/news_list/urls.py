from django.urls import path,include,reverse
from .views import article_detail, ProfileUpdateView, news_list, search, register, \
    PostCreateView, PostUpdateView  # PostCreateView, PostUpdateView, PostDeleteView, \
from .views import create_post, edit_post, delete_post,home,become_author,subscribe_to_category,unsubscribe_from_category,categories_list
from .models import Post
from .views import user_login,author_granted
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('news/', news_list, name='news_list'),
    path('news/<int:article_id>/', article_detail, name='news_detail'),
    path('news/search', search, name='news_search'),
    path('news/create/', login_required(create_post), {'post_type': Post.NEWS}, name='create_news'),
    path('news/<int:pk>/edit/', edit_post, {'post_type': Post.NEWS}, name='edit_news'),
    path('news/<int:pk>/delete/', delete_post, {'post_type': Post.NEWS}, name='delete_news'),
    path('articles/create/', create_post, {'post_type': Post.ARTICLE}, name='create_article'),
    path('articles/<int:pk>/edit/', edit_post, {'post_type': Post.ARTICLE}, name='edit_article'),
    path('articles/<int:pk>/delete/', delete_post, {'post_type': Post.ARTICLE}, name='delete_article'),
    path('', home, name='home'),
    path('author_granted/', author_granted, name='author_granted'),
    path('profile/',ProfileUpdateView.as_view(),name='profile'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('accounts/', include('allauth.urls')),
    #path('profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile-update'),
    path('become-author/', become_author, name='become_author'),
    path('category/<int:category_id>/subscribe/', subscribe_to_category, name='subscribe_to_category'),
    path('category/<int:category_id>/unsubscribe/', unsubscribe_from_category, name='unsubscribe_from_category'),
    path('categories/', categories_list, name='categories_list'),
    path('news/createClass/', PostCreateView.as_view(), {'post_type': Post.NEWS}, name='create_news_class'),
    path('news/updateClass/', PostUpdateView.as_view(), {'post_type': Post.NEWS}, name='update_news_class'),


]


