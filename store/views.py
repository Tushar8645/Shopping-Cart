from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

from store.models import Product, Category, Customer, Order
from store.middlewares import auth_middleware


class HomeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        cart = request.session.get('cart')

        if not cart:
            request.session['cart'] = dict()

        products = None
        categories = Category.get_all_category()
        category_id = request.GET.get("category")

        if category_id:
            products = Product.get_all_products_by_categoryid(category_id)
        else:
            products = Product.get_all_products()

        context = {}
        context["products"] = products
        context["categories"] = categories

        # print('You are -', request.session.get('customer'))
        # print('You are -', request.session.get('customer_email'))

        return render(request, "store/index.html",  context)

    def post(self, request):
        product = request.POST.get('product_value')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)

            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = dict()
            cart[product] = 1

        request.session['cart'] = cart

        print(request.session.items())

        return redirect('store:index')


class SignupView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, "store/signup.html")

    def post(self, request):
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Previous Values
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
        }

        # Ready to store data in database
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password,
        )

        # Validation
        error_message = self.validateCustomer(customer)

        # Saving
        if not error_message:
            # Store in database
            customer.password = make_password(customer.password)
            customer.save()

            return redirect('store:index')
        else:
            context = {
                'error': error_message,
                'value': value,
            }

            return render(request, 'store/signup.html', context)

    def validateCustomer(self, customer):
        error_message = None

        if not customer.first_name:
            error_message = 'First Name Required!!'
        elif len(customer.first_name) < 2:
            error_message = 'First name must be longer than 2 character'
        if not customer.last_name:
            error_message = 'Last Name Required!!'
        elif len(customer.last_name) < 2:
            error_message = 'Last name must be longer than 2 character'
        if not customer.phone:
            error_message = 'Phone Number Required!!'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 character long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 character long'
        elif customer.isExists():
            error_message = 'Email Address Already Register...'

        return error_message


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    return_url = None

    def get(self, request):
        LoginView.return_url = request.GET.get('return_url')
        print(LoginView.return_url)
        
        return render(request, 'store/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            customer = Customer.objects.get(email=email)
        except:
            customer = False

        error_message = None

        if customer:
            flag = check_password(password, customer.password)

            if flag:
                request.session['customer'] = customer.pk

                if LoginView.return_url:
                    return HttpResponseRedirect(LoginView.return_url)
                else:
                    LoginView.return_url = None

                    return redirect('store:index')
            else:
                error_message = 'Password Invalid!!!'
        else:
            error_message = 'Email and Password Invalid!!!'

        return render(request, 'store/login.html', {'error': error_message})


def logout(request):
    request.session.clear()

    return redirect('store:login')


class CartView(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        context = {
            'products': products,
        }

        return render(request, 'store/cart.html', context)


class CheckoutView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CheckoutView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            order = Order(
                customer=Customer(id=customer),
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=cart.get(str(product.id)),
            )
            order.save()

        request.session['cart'] = {}

        return redirect('store:cart')


class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        context = {
            'orders': orders,
        }

        return render(request, 'store/order.html', context)

    def post(self, request):
        pass
