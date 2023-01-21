from django.urls import path
from customer import views

urlpatterns=[
    path('customers/register',views.RegistrationView.as_view(),name='register'),
    path('',views.SignInView.as_view(),name='signin'),
    path('customers/home',views.ProductsListView.as_view(),name="user-home"),
    path('products/details/<int:id>',views.ProductDetailView.as_view(),name='product-detail'),
    path('product/cart/<int:id>/add',views.add_to_cart,name='add-cart'),
    path('carts/all',views.CartListView.as_view(),name='carts-all'),
    path('carts/<int:id>/delobj',views.CartDeleteView.as_view(),name='carts-delobj'),
    path('logoutuser',views.signout,name='user-logout'),
    path('orders/add/<int:cid>/<int:pid>',views.OrderView.as_view(),name="place-order"),
    path('myorders',views.MyOrdersView.as_view(),name='my-order-list'),
    path('order/<int:id>/removed',views.ordercancel,name='order-cancel')


]