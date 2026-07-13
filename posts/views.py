from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DeleteView, DetailView
from .models import Comment, Post

from django.views import View
from django.urls import reverse_lazy



def validate_post_data(request):
    title = request.POST.get("title", "").strip()
    text = request.POST.get("text", "").strip()
    errors = {}

    if not title:
        errors["title"] = "Введите заголовок."

    if not text:
        errors["text"] = "Введите текст поста."

    return {"title": title, "text": text}, errors


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 10


class FavoritePostListView(LoginRequiredMixin, ListView):
    template_name = "posts/favorite_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.favorite_posts.all()
    

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        
        self.object = self.get_object()
        comment_text = request.POST.get("text", "").strip()

        if comment_text:
            Comment.objects.create(
                post = self.object,
                author = request.user,
                text = comment_text
            )
            return redirect(self.object)
        
        context = self.get_context_data(object = self.object)
        context["comment_text"] = comment_text
        context["comment_error"] = "Введите текст комментария"
        return self.render_to_response(context)
    

class PostCreateView(LoginRequiredMixin, View):
    template_name = "posts/post_form.html"

    def get(self, request):
        return render(request, self.template_name, {"title_value": "", "text_value": "", "errors": {}})
    
    def post(self, request):
        data, errors = validate_post_data(request)

        if errors:
            return render(request, self.template_name, {"title_value": data["title"], "text_value": data["text"], "errors": errors})
        
        post = Post.objects.create(
            title = data["title"],
            text = data["text"],
            author = request.user
        )

        return redirect(post)
    

class AuthorRequiredMixin(UserPassesTestMixin):
    def get_object(self, queryset = None):
        if not hasattr(self, "object"):
            self.object = get_object_or_404(Post, pk = self.kwargs["pk"])
        return self.object
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request_user
    

class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, View):
    template_name = "posts/post_form.html"

    def get(self, request, pk):
        post = self.get_object()
        return render(request, self.template_name, {"object": post, "title_value": post.title, "text_value": post.text, "errors": {}})
    
    def post(self, request, pk):
        post = self.get_object()
        data, errors = validate_post_data(request)

        if errors:
            return render(
                request, self.template_name, {"object": post, "title_value": data["title"], "text_value": data["title"], "errors": errors})
        
        post.title = data["title"]
        post.text = data["text"]
        post.save()

        return redirect(post)
    

class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        return super().form_valid(form)
    

class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk = pk)

        if post.favorites.filter(pk = request.user.pk).exists():
            post.favorites.remove(request.user)
        else:
            post.favorites.add(request.user)

        return redirect(post)
    
toggle_favorite = ToggleFavoriteView.as_view()
