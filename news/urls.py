from django.urls import path
from .views import UserView, PostListSearch, PostDetail, PostUpdate, PostDelete, PostCreate, BaseRegisterView
from .views import UserUpdateView, CategoryList
from django.contrib.auth.views import LoginView, LogoutView
from .views import upgrade_me, subscribe, unsubscribe, restriction_num_posts


urlpatterns = [
    path('',  PostListSearch.as_view(), name='post_search'),
    path('<int:pk>/', PostDetail.as_view(), name = 'post'),
    path('search/', PostListSearch.as_view(), name='post_search'),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('user/', UserView.as_view(), name='user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign/signup/', BaseRegisterView.as_view(), name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('<int:pk>/profile/', UserUpdateView.as_view(), name='profile'),
    path('categories/', CategoryList.as_view(), name='categories'),
    path('scategories/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('scategories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
    path('error/', restriction_num_posts, name='restriction_num_posts'),
]
