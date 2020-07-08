from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import Product, Order, Customer
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .forms import *
from django.views.generic import ListView
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import unauthenticated_user, allowed_users


@unauthenticated_user
def register_page(request):
    """ If the user is authenticated, redirect the user to the home page.
    Else , register the user and if there the user is registered successfully,
    redirect the user to the login page."""

    form = CreateUserForm()
    context = {'form': form}

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user)
            messages.success(request, "Account was created for " + username)
            return redirect("/login/")

    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")

        else:
            messages.info(request, "Username or password is incorrect!!")
            return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html')


def logout_page(request):
    logout(request)
    messages.info(request, "User has been logged out!!")
    return redirect('/login/')


class HomeView(LoginRequiredMixin, ListView):
    # Generic Class based view

    login_url = '/login/'

    # Set the template_name
    template_name = "accounts/dashboard.html"

    # Rename context object name. By default the name is 'objects'.
    context_object_name = 'customers'

    # Override the get_queryset method
    def get_queryset(self):
        return Customer.objects.all()

    # Override the get_context_data() method to add more than one model
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # Store the 5 most recent created orders.
        orders = Order.objects.all()

        # Store total count of orders as well as those in delivered and pending status
        context['total_orders'] = orders.count()
        context['delivered'] = orders.filter(status='Delivered').count()
        context['pending'] = orders.filter(status='Pending').count()

        # Store total customer count
        context['total_customers'] = Customer.objects.all().count()

        # Store the 5 most recent created orders.
        context['orders'] = orders.order_by("-date_created")[:5]

        return context


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def products(request):
    # Function based view

    # Retrive all the Products in the database
    products = Product.objects.all()

    # Add the products to the context variable
    context = {'products': products}

    # Render the reponse to the template along with the context.
    return render(request, "accounts/products.html", context=context)


@login_required(login_url='/login/')
def customer(request, pk):
    # Function based view
    customer = Customer.objects.get(id=pk)

    # Filter Order by customers and count the number of orders
    orders = Order.objects.filter(customer=customer)
    order_count = orders.count()

    # Using the Filter class
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    context = {'customer': customer, 'order_count': order_count,
               'orders': orders, 'my_filter': my_filter}
    return render(request, "accounts/customer.html", context=context)


@login_required(login_url='/login/')
def create_order(request, pk):
    # Creating a form set with 10 forms. Customer is the parent and Order is the Child
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form=OrderForm(initial={"customer":customer})
    context = {'formset': formset, 'customer': customer}

    if request.method == 'POST':
        print("Printing POST:", request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request, "accounts/order_form.html", context=context)


@login_required(login_url='/login/')
def update_order(request, pk):
    # Update order using primary key of customer
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    context = {'form': form}

    if request.method == 'POST':
        print("Printing POST:", request.POST)
        form = OrderForm(request.POST, instance=order)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, "accounts/order_form.html", context=context)


@login_required(login_url='/login/')
def delete_order(request, pk):
    # Delete order using primary key of customer
    order = Order.objects.get(id=pk)
    context = {'item': order}

    if request.method == "POST":
        order.delete()
        return redirect("/")
    return render(request, "accounts/delete.html", context=context)


@login_required(login_url="/login/")
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()
    print("Order ", orders)
    context = {'orders': orders}
    return render(request, "accounts/user.html", context=context)
