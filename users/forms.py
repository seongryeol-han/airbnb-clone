from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)  # 패스워드 가려주는거임.

    def clean(self):  # 모든 field를 정리할 때 "clean_변수명"
        email = self.cleaned_data.get("email")  # email을 clean하는거임.
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(
                email=email
            )  # username = email인 object만 가져 온다.
            if user.check_password(password):
                return self.cleaned_data

            else:
                self.add_error("password", forms.ValidationError("Password is worng"))

        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):  # model에 채우는 폼, uniqueness를 검증한다.
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    # password는 따로 적어줘야함. 암호화 되어있기 때문에. 그리고 model에 없으니까.
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    # model에서 username에 email 넣고 password 저장하고
    def save(self, *args, **kwargs):
        user = super().save(
            commit=False
        )  # (아직 데이터베이스에 올릴필요없으니까)commit=False란 의미는, 장고 object에는 데이터가 올라가는데 데이터베이스에는 올라가지 않게 하는것임.
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)  # 비번 암호화
        user.save()  # 여기서는 commit=True가 포함.
