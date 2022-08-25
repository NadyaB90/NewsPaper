from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from datetime import datetime
from .models import Category, Post
from .filters import PostFilter 
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    ordering = ['-created_date']
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}',
                        None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)


class SearchList(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'
    ordering = ['-created_date']
    paginate_by = 10

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['news_list'] = Post.objects.all()
        context['filter'] = self.get_filter()
        context['categories'] = Category.objects.all()
        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    permission_required = ('news.add_post',)
    model = Post
    template_name = 'post_create.html'


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    form_class = PostForm
    permission_required = ('news.delete_post',)
    queryset = Post.objects.all()
    success_url = '/news/'


class CategorySubscribeView(ListView):
    model = Category
    template_name = 'news/post_category.html'
    context_object_name = 'post_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def subscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    id_u = request.user.id
    email = category.subscribers.get(id=id_u).email
    send_mail(
        subject=f'News Portal: подписка на обновления категории {category}',
        message=f'«{request.user}», вы подписались на обновление категории: «{category}».',
        from_email='lady.nadya20@mail.ru',
        recipient_list=[f'{email}', ],
    )
    return redirect('/news')

