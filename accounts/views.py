from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Order,Customer
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

    orders=Order.objects.filter(customer=customer)
    order_count=orders.count()
    context={'customer':customer,'order_count':order_count,'orders':orders}
    return render(request,"accounts/customer.html",context=context)