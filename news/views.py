from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from .models import Post
from .filters import PostFilter
from .forms import PostForm, BaseRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView


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


class PostCreate(LoginRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    success_url = '/search/'


class PostUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    success_url = '/search/'

    def get_object(self, **kwargs):
        _id = self.kwargs.get('pk')
        return Post.objects.get(pk=_id)


class PostDelete(LoginRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/search/'


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'
