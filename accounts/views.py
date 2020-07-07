from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import Product,Order,Customer
from .forms import *
from django.views.generic import ListView

# Create your views here.
class HomeView(ListView):
    # Generic Class based view

    # Set the template_name
    template_name="accounts/dashboard.html"

    # Rename context object name. By default the name is 'objects'.
    context_object_name='customers'

    # Override the get_queryset method
    def get_queryset(self):
        return Customer.objects.all()

    # Override the get_context_data() method to add more than one model
    def get_context_data(self,**kwargs):
        context=super(HomeView,self).get_context_data(**kwargs)

        # Store the 5 most recent created orders.
        orders=Order.objects.all()

        # Store total count of orders as well as those in delivered and pending status
        context['total_orders']=orders.count()
        context['delivered']=orders.filter(status='Delivered').count()
        context['pending']=orders.filter(status='Pending').count()

        # Store total customer count
        context['total_customers']=Customer.objects.all().count()

        # Store the 5 most recent created orders.
        context['orders']=orders.order_by("-date_created")[:5]
       
        return context

def products(request):
    # Function based view

    # Retrive all the Products in the database
    products=Product.objects.all()

    # Add the products to the context variable
    context={'products':products}

    # Render the reponse to the template along with the context.
    return render(request,"accounts/products.html",context=context)

def customer(request,pk):
    # Function based view
    customer=Customer.objects.get(id=pk)

    # Filter Order by customers and count the number of orders
    orders=Order.objects.filter(customer=customer)
    order_count=orders.count()
    context={'customer':customer,'order_count':order_count,'orders':orders}
    return render(request,"accounts/customer.html",context=context)

def create_order(request,pk):
    # Creating a form set with 10 forms. Customer is the parent and Order is the Child
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form=OrderForm(initial={"customer":customer})
    context={'formset':formset,'customer':customer}

    if request.method =='POST':
        print("Printing POST:",request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request,"accounts/order_form.html",context=context)

def update_order(request,pk):
    # Update order using primary key of customer
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    context={'form':form}

    if request.method =='POST':
        print("Printing POST:",request.POST)
        form=OrderForm(request.POST,instance=order)
        context={'form':form}
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,"accounts/order_form.html",context=context)

def delete_order(request,pk):
    # Delete order using primary key of customer
    order=Order.objects.get(id=pk)
    context={'item':order}

    if request.method == "POST":
        order.delete()
        return redirect("/")
    return render(request,"accounts/delete.html",context=context)