from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import PostsList, PostDetail, SearchList, PostCreateView, PostUpdateView, PostDeleteView, \
    CategorySubscribeView, subscribe_category

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', SearchList.as_view(), name='post_search'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('subscribe/', CategorySubscribeView.as_view()),
    path('subscribe/<int:pk>', subscribe_category, name='subscribe_category'),
]

