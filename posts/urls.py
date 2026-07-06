from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("favorites/", views.FavoritePostListView.as_view(), name="favorite_posts"),
    path("posts/create", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("posts/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
]