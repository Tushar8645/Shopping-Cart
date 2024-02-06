from django.urls import path

from store import views
from store.middlewares import auth_middleware


app_name = 'store'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('check-out/', views.CheckoutView.as_view(), name='checkout'),
    path('order/', auth_middleware(views.OrderView.as_view()), name='order'),
]
