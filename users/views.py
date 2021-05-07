from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models

# Create your views here.


# 여기서는 아이디 비번이 있는지 확인하는 작업(인증) ((html에 url이 있자나? 그 url이 어떤 view를 불러오느냐)html+form -> view 순서 로직임. 무조건 username을 사용함 아이디로.)
class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm  # forms.py에서 LoginForm을 가져온다.
    success_url = reverse_lazy("core:home")  # 인증에 성공하면 core:home 주소로 간다.

    def form_valid(self, form):  # form이 유효한지 체크하는 거임.
        email = form.cleaned_data.get("email")  # model에서 가져온다.
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)  # 인증이 되는건가 보네, 로그인 시킨다.
        return super().form_valid(form)  # 이게 되면 success_url로 돌아간다.


def log_out(request):  # 무조건 함수 뷰여야함.
    logout(request)  # 로그아웃 시킨다.
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(
        self, form
    ):  # (form이 유효하다면 form.save()를 실행시킨다.)인증해서 로그인 시킨다. 회원가입하면 바로 로그인되게 하는거구나.
        form.save()  # form 을 save 한다.
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""  # verify 된 후 secret은 삭제.
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do
        pass

    return redirect(reverse("core:home"))
