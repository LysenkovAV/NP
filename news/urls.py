from django.urls import path
from .views import (
    PostList, PostDetail, PostCreate, PostEdit, PostDelete, CategoryPostList, subscribe
)


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('categories/<int:pk>', CategoryPostList.as_view(), name='category_post_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]