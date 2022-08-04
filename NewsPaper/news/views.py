from datetime import datetime
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category


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


class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


class PostUpdateView(UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    form_class = PostForm
    queryset = Post.objects.all()
    success_url = '/news/'



