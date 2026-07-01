from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views import View
from .forms import RegisterForm

class LoginView(View):
    template_name = "users/login.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {"username_value": "",
             "errors": {},
             "non_field_errors": {}}
        )

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"username_value": request.POST.get("username", "").strip(),
                "errors": form.errors,
                "non_field_errors": form.non_field_errors()}
        )

        login(request, form.get_user())
        messages.success(request, "Вход выполнен")
        return redirect("/")
    
class RegisterView(View):
    template_name = "users/register.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {"username_value": "",
             "email_value": "",
             "errors": {},
             "non_field_errors": {}}
        )
    
    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"username_value": request.POST.get("username", "").strip(),
                 "email_value": request.POST.get("email", "").strip(),
                 "errors": form.errors,
                 "non_field_errors": form.non_field_errors()}
        )

        user = form.save()
        login(request, user)
        messages.success(request, "Регистрация выполнена")
        return redirect("/")