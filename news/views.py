from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from .models import Post
from .filters import PostFilter
from .forms import PostForm, BaseRegisterForm, ProfileEditForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class PostList(ListView):
    model = Post 
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = '-time_create'


class PostListSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = '-time_create'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        request_copy = self.request.GET.copy()
        parameters = request_copy.pop('page', True) and request_copy.urlencode()
        context['parameters'] = parameters  # хвост get запроса для коррктной работы пагинатора
        context['form'] = PostForm()
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    template_name = 'post_create.html'
    form_class = PostForm
    success_url = '/search/'

    def get_object(self, **kwargs):
        _id = self.kwargs.get('pk')
        return Post.objects.get(pk=_id)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    template_name = 'post_create.html'
    form_class = PostForm
    success_url = '/search/'

    def get_object(self, **kwargs):
        _id = self.kwargs.get('pk')
        return Post.objects.get(pk=_id)


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/search/'


class BaseRegisterView(CreateView):
    model = User
    template_name = 'registration/signup.html'
    form_class = BaseRegisterForm
    success_url = '/'


class UserUpdateView(UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileEditForm
    success_url = '/'

    def get_object(self):
        return self.request.user


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')
