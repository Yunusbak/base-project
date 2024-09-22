from django import forms

# USER REGISTRATION FORM


class RegistrationForm(forms.Form):
    username = forms.CharField(label='username', max_length=50, widget = forms.TextInput())
    password = forms.CharField(label='password', max_length=50, widget = forms.PasswordInput())
    password2 = forms.CharField(label='password2', widget = forms.PasswordInput())
    phone_number = forms.CharField(label='phone_number', max_length=50, widget = forms.TextInput())


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=50, widget = forms.TextInput())
    password = forms.CharField(label='password', max_length=50, widget = forms.PasswordInput())








# --- ADMIN CRUD PRODUCTS FORM --------------


class ProductCreateForm(forms.Form):
    name = forms.CharField(max_length=255, label='Product Name')
    price = forms.IntegerField(label='Price')
    category_slug = forms.CharField(max_length=255, label='Product category')


class ProductUpdateForm(forms.Form):
    name = forms.CharField(max_length=255, label='Product Name')
    price = forms.IntegerField(label='Price')
    category_slug = forms.CharField(max_length=255, label='Product category')




