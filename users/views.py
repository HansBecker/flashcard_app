from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from .forms import LoginForm


class LoginView(View):
    template_name = "users/login.html"
    form = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template_name, context={"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data["email"], password=form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return render(request, self.template_name, context={"form": form})
        else:
            return render(request, self.template_name, context={"form": form})
