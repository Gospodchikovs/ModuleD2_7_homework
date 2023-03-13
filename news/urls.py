from django.urls import path
from .views import IndexView, PostListSearch, PostDetail, PostUpdate, PostDelete, PostCreate, BaseRegisterView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', IndexView.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostListSearch.as_view(), name='post_search'),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('login/',
         LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='registration/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='registration/signup.html'),
         name='signup'),
]
