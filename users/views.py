import os
import requests
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
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
    messages.info(request, "See you later")
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


def github_login(request):  # user를 github으로 보내고
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass
    # 동일 이메일이 있을떄....


def github_callback(request):  # github에서 user를 우리 app으로 가져온다.
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get authorization code.")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",  # 여기다가 요청하고
                    headers={
                        "Authorization": f"token {access_token}",  # 이건 약간 암호 같은거.
                        "Accept": "application/json",  # json 형태로 보내주세요.
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    name = username if name is None else name
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    bio = "" if bio is None else bio
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            first_name=name,
                            bio=bio,
                            email=email,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))

                else:
                    raise GithubException("Can't get your profile")

        else:
            raise GithubException("Can't get code")

    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):  # user를 github으로 보내고
    client_id = os.environ.get("KAKAO_ID")  # REST API Key
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"  # 다시 되받는곳.
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )  # 여기로 오는거다.


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        print(profile_json)
        properties = profile_json.get("kakao_account")
        email = properties.get("email", None)
        if email is None:
            raise KakaoException("Please also give me your email")
        nickname = properties.get("profile").get("nickname")
        profile_image = properties.get("profile").get("profile_image_url")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar",
                    ContentFile(
                        photo_request.content
                    ),  # content는 바이트로 되어있는건데 ContentFile로 그 정보를 담을 수 있다.
                )  # 이거 뒤에 또 user.save 안해줘도 됨.
        messages.success(request, f"Welcome back {user.first_name}")
        login(request, user)
        return redirect(reverse("core:home"))

    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"  # 이걸 설정해줘야함 왜냐하면, 룸디테일에서 다른 사람 유저를 눌렀을 때 그사람 프로파일로 가는데, 그 때 로그인한 사람의 프로파일을 누르면 그 룸 호스트의 프로필로 간다. (user를 그 페이지의 호스트로 바꿔주기 때문,)
    # 이것을 방지하기 위해 context_object_name을 쓴다.


class UpdateProfileView(UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )

    def get_object(self, queryset=None):
        return self.request.user  # UpdateProfileView 이걸 불러온다면 user에 대해서만 반환해주는것임..

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        return form


class UpdatePasswordView(PasswordChangeView):
    template_name = "users/update-password.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form