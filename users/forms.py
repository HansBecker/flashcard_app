from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.widgets.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.widgets.PasswordInput(attrs={"placeholder": "Password"})
    )
