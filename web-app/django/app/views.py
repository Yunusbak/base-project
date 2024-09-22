import requests
import os
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, ProductCreateForm, ProductUpdateForm
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from dotenv import load_dotenv
load_dotenv()

admin_name = os.getenv('ADMIN_USERNAME')
admin_password = os.getenv('ADMIN_PASSWORD')





# USER REGISTRATION
class RegistorPageView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'auth/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            url = 'http://127.0.0.2:8001/user/register'
            data = {
                'username': form.cleaned_data['username'],
                'phone_number': form.cleaned_data['phone_number'],
                'password': form.cleaned_data['password'],
                'password2': form.cleaned_data['password2'],
            }
            response = requests.post(url, json=data)
            if response.status_code == 400:
                return render(request, 'auth/register.html', {"messageuser": "User already exists"})
            if response.status_code == 401:
                return render(request, 'auth/register.html', {"messagepassword": "Passwords do not match"})
            if response.status_code == 402:
                return render(request, 'auth/register.html', {"message": "Phone number must be 12 digits"})
            if response.json()["status"] == 201:
                return redirect('login')

        else:
            return render(request, 'auth/register.html', {'form': form, "message": "Invalid form data"})


class LoginPageView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            url = 'http://127.0.0.2:8001/user/login'
            data = {
                "username": form.cleaned_data["username"],
                "password": form.cleaned_data["password"],
            }
            response = requests.post(url, json=data)

            if data["username"] == f'{admin_name}' and data["password"] == f'{admin_password}':
                access_token = response.json()["access_token"]
                response = redirect("admin")
                response.set_cookie("access_token", access_token, httponly=True)
                return response

            if response.json()["status"] == 200:
                access_token = response.json()["access_token"]
                response = redirect("home")
                response.set_cookie("access_token", access_token, httponly=True)
                return response

            else:
                return render(request, 'auth/login.html', {'form': form, "message": "Username or password incorrect"})

        return render(request, 'auth/login.html', {'form': form})


class LogoutPageView(View):
    def get(self, request):
        response = redirect('login')
        response.delete_cookie('access_token')
        return response



# ---------------------------------------------------------------------------------------------------------------


def home(request):
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return redirect('login')

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('http://127.0.0.2:8001/user/token-verify', headers=headers)
    if response.status_code == 200:
        return render(request, 'index.html')
    if response.status_code == 401:
        response = HttpResponseRedirect('/login')
        response.delete_cookie('access_token')
        return response

    return render(request, 'index.html')


def token_verify_func(request, template):
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return redirect('login')

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('http://127.0.0.2:8001/user/token-verify', headers=headers)

    if response.status_code == 200:
        return render(request, template)
    else:
        response = HttpResponseRedirect('/login')
        response.delete_cookie('access_token')
        return response


def profile(request):
    access_token = request.COOKIES.get('access_token')

    if access_token:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get('http://127.0.0.2:8001/user/user', headers=headers)

        if response.status_code == 200:
            user = response.json().get('detail')
            return render(request, 'profile-settings.html', {'users': user})

    return redirect('login')


def about(request):
    return token_verify_func(request, 'about.html')

def shop(request):
    url = 'http://127.0.0.2:8001/user/products'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['products']
        return render(request, 'shop.html', {'products': data})

    return token_verify_func(request, 'shop.html')

def services(request):
    return token_verify_func(request, 'services.html')

def blog(request):
    return token_verify_func(request, 'blog.html')

def contact(request):
    return token_verify_func(request, 'contact.html')

def cart(request):
    return token_verify_func(request, 'cart.html')


def admin(request):
    access_token = request.COOKIES.get('access_token')

    if access_token:
        return render(request, 'admin-page.html')

    return redirect('login')


# ADMIN CRUD PRODUCTS VIEWS


class ProductListView(View):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        url = 'http://127.0.0.2:8001/admin/products'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            return render(request, 'admin/product_list.html', {'products': products})
        else:
            return render(request, 'admin/product_list.html', {'message': 'Product not found'})

class CreateProductView(View):
    def get(self, request):
        form = ProductCreateForm()
        return render(request, 'admin/create_product.html', {'form': form})

    def post(self, request):
        form = ProductCreateForm(request.POST)
        if form.is_valid():
            data = {
                "name": form.cleaned_data["name"],
                "price": form.cleaned_data["price"],
                "category_slug": form.cleaned_data["category_slug"]
            }
            url = 'http://127.0.0.2:8001/admin/create-product'
            response = requests.post(url, json=data)

            if response.status_code == 201:
                return redirect('product_list')
            else:
                return HttpResponse('---')
        return render(request, 'admin/create_product.html', {'form': form})


class DeleteProductView(View):
    def post(self, request, product_slug):
        url = f"http://127.0.0.2:8001/admin/delete-product/{product_slug}"
        response = requests.delete(url)

        if response.status_code == 200:
            return redirect('product_list')
        else:
            return HttpResponse('xatolik')



import requests
from django.shortcuts import render

def search_view(request):
    slug = request.GET.get('slug')
    product = None
    print(f"Ищем продукт с slug: {slug}")

    if slug:
        url = f'http://127.0.0.2:8001/user/products/{slug}'
        response = requests.get(url)
        print(f"Статус ответа API: {response.status_code}")

        if response.status_code == 200:
            product_data = response.json()
            product = product_data
            print(f"Продукт найден: {product}")

    return render(request, 'search.html', {'product': product})
