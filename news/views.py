from django.http import HttpResponse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from .models import Post, Category, Subscriber, Author, PostCategory
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


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):

        # класс для передачи в страницу - категория и признак полписки польщователя
        class Sublist:
            def __init__(self, news_category, subscribed):
                self.category = news_category       # категория
                self.is_subscribed = subscribed     # признак подписки пользоывателя на данную категорию

        context = super().get_context_data(**kwargs)
        # формируем список объектов Sublist(категория, признак подписки) для передачи в страницу
        user_cat = list(Subscriber.objects.filter(user=self.request.user).values('category__topic').distinct())
        all_cat = list(Category.objects.all().values('topic'))                      # список всех категорий
        user_cat_list = list(map(lambda cat: cat['category__topic'], user_cat))     # список подписных категорий
        subscribed_list = list(map(lambda cat: Sublist(cat['topic'], cat['topic'] in user_cat_list), all_cat))
        context['subscribed'] = subscribed_list
        return context


@login_required
def subscribe(request, *args, **kwargs):
    user = request.user
    category = Category.objects.get(id=kwargs.get('pk'))
    subscriber = Subscriber()
    subscriber.add_subscriber(category, user)
    return redirect('/categories')


@login_required
def unsubscribe(request, *args, **kwargs):
    user = request.user
    category = Category.objects.get(id=kwargs.get('pk'))
    subscriber = Subscriber()
    subscriber.delete_subscriber(category, user)
    return redirect('/categories')


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
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
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

    def post(self, request, *args, **kwargs):
        if Author.objects.filter(user=request.user).exists():
            author = Author.objects.get(user=request.user)        # автор зарегистрирован
        else:
            author = Author.objects.create(user=request.user)     # создаем пользователя
        try:
            news = Post.objects.create(
                author=author,
                type=request.POST['type'],
                heading=request.POST['heading'],
                body=request.POST['body']
            )
        except Warning:
            return redirect('/error')
        else:
            category = Category.objects.get(id=request.POST['category'])
            postcategory = PostCategory(post=news, category=category)
            postcategory.save()
        return redirect('/search')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


# сообщение об ошибке при создании больее трех статей за сутки.
def restriction_num_posts(request):
    return HttpResponse(f"<h2> Запрещено создавать больше трех статей за сутки! </h2>")
