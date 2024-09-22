import os
from dotenv import load_dotenv
from django.urls import path
from .views import home, about, shop, services, blog, contact, cart, RegistorPageView, LoginPageView, LogoutPageView, profile, admin
from .views import ProductListView, CreateProductView, DeleteProductView,  search_view



load_dotenv()
admin_url = os.getenv('ADMIN_PAGE_URL')

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('shop/', shop, name='shop'),
    path('services/', services, name='services'),
    path('blog/', blog, name='blog'),
    path('contact/', contact, name='contact'),
    path('cart/', cart, name='cart'),
    path('profile/', profile, name='profile'),
    path('search/', search_view, name='search'),

    # Registration
    path('register/', RegistorPageView.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutPageView.as_view(), name='logout'),

    # admin Product CRUD
    path(f'{admin_url}/products/', ProductListView.as_view(), name='product_list'),
    path(f'{admin_url}/create-product/', CreateProductView.as_view(), name='create_product'),
    path(f'{admin_url}/delete-product/<slug:product_slug>/', DeleteProductView.as_view(), name='delete_product'),


    path(f'{admin_url}/', admin, name='admin'),
]
