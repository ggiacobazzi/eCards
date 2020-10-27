from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column


class RegisterFormNormalUser(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Choose your password wisely'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Choose your password wisely'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'is_vendor', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'Custom-User-Crispy-Form'
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(Column('username')),
            Row(
                Column('first_name', css_class="form-group col-md-6 mb-0"),
                Column('last_name', css_class="form-group col-md-6 mb-0"),
                css_class="form-row"
            ),
            'email',
            Row(
                Column('password1', css_class="form-group col-md-6 mb-0"),
                Column('password2', css_class="form-group col-md-6 mb-0"),
                css_class="form-row"
            ),
            Submit('submit', 'Sign Up', css_class='btn-success mt-2')
        )


class RegisterFormVendor(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Choose your password wisely'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Choose your password wisely'}))
    address = forms.CharField(max_length=50)
    telephone = forms.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'address',
                  'telephone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'Custom-User-Vendor-Crispy-Form'
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(Column('username')),
            Row(
                Column('first_name', css_class="form-group col-md-6 mb-0"),
                Column('last_name', css_class="form-group col-md-6 mb-0"),
                css_class="form-row"
            ),
            'email',
            Row(
                Column('password1', css_class="form-group col-md-6 mb-0"),
                Column('password2', css_class="form-group col-md-6 mb-0"),
                css_class="form-row"
            ),
            Row(
                Column('address', css_class="form-group col-md-6 mb-0"),
                Column('telephone', css_class="form-group col-md-6 mb-0"),
                css_class="form-row"
            ),
            Submit('submit', 'Sign Up', css_class='btn-success mt-2')
        )

    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        user.save()
        return user


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if email and password:
                user = authenticate(email=email, password=password)
                if not user:
                    raise forms.ValidationError("User does not exist")
                elif not user.check_password(password):
                    raise forms.ValidationError("Wrong password")
                elif not user.is_active:
                    raise forms.ValidationError("This user is not active")

