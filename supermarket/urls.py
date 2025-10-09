from django.urls import path
from supermarket.views import *





urlpatterns=[
    path('god',god),
    path('house',home,name='home'),
    path('searchs',search_products,name='search'),
    path('pro/<slug:slug>',product_detail,name='product_detail'), 
    path('cat/<slug:slug>', category_products,name='category_products'), 
    path('proo/<slug:slug>',product_details,name='product_details'), 
    path('login', loginpage,name='loo') ,
    path ('profile', profilepage,name='proo'),
    path ('proedit', proedit,name='edit_profile'),
    path('register',Register,name='loginn'),
    path('logout',logoutpage,name='out'),
    path("cart/", view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path('buy/<int:product_id>/', buy_product, name='buy_product'),
    path('buys/<int:product_id>/', buy_products, name='ppp'),
    path('add',add_product,name='add'),
    path("users/", user_list, name="user_list"),
    path("users/delete/<int:pk>/", delete_user, name="delete_user"),


]

    




