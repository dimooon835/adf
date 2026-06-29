from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def post_detail(request):
    return render(request, 'post_detail.html')


def user_login(request):
    return render(request, "users/login.html")


def user_register(request):
    return render(request, "users/register.html")


def post_form(request):
    return render(request, "posts/post_form.html")


def favorite_list(request):
    return render(request, "posts/favorite_list.html")