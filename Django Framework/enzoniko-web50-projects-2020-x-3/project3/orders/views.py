from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum
from .models import Category,Regular_pizza,Sicilian_pizza,Topping,Sub,Pasta,Salad,Dinner_platter,Order2,User_order,Order_counter

# Create your views here.
counter = Order_counter.objects.first()
if counter==None:
    set_counter=Order_counter(counter=1)
    set_counter.save()
superuser = User.objects.filter(is_superuser=True)
if superuser.count() == 0:
    superuser=User.objects.create_user("admin","admin@admin.com","adminadmin")
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.save()
    set_superuser=User_order(user=superuser,order_number=counter.counter)
    set_superuser.save()

def index(request):
    if not request.user.is_authenticated:
        return render(request,"login.html",{"message":None})
    order_number=User_order.objects.get(user=request.user,status='initiated').order_number
    context = {
        "user":request.user,
        "Checkout":Order2.objects.filter(user=request.user,number=order_number),
        "Checkout_category":Order2.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(Order2.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "Category": Category.objects.all(),
        "Order_number":order_number

    }
    return render(request,"index.html",context) 

def login_view(request):
    username=request.POST["username"]
    password=request.POST["password"]
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"login.html",{"message":"Invalid credentials"}) 

def logout_view(request):
    logout(request)
    return render(request,"login.html",{"message":"Logged out."})

def signin_view(request):
    if request.method == "POST":
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        password2=request.POST["password2"]
        if not password==password2:
            return render(request,"signin.html",{"message":"Passwords don't match."})
        user=User.objects.create_user(username,email,password)
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        counter=Order_counter.objects.first()
        order_number=User_order(user=user,order_number=counter.counter)
        order_number.save()
        counter.counter=counter.counter+1
        counter.save()
        
        
        return render(request,"login.html",{"message":"Registered. You can log in now."}) 
    return render(request,"signin.html") 

def menu(request,category):
    menu,columns=findTable(category)
    order_number=User_order.objects.get(user=request.user,status='initiated').order_number
    context = {
        "user":request.user,
        "Checkout":Order2.objects.filter(user=request.user,number=order_number),
        "Checkout_category":Order2.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(Order2.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "Category": Category.objects.all(),
        "Active_category":category,
        "Menu": menu,
        "Columns":columns,
        "Topping_price": 0.00,
        "Order_number":order_number
    }
    return render(request,"menu.html",context) 

def add(request,category,name,price):
    menu,columns=findTable(category)
    order_number=User_order.objects.get(user=request.user,status='initiated').order_number
    topping_allowance=User_order.objects.get(user=request.user,status='initiated')
    context = {
        "Checkout":Order2.objects.filter(user=request.user,number=order_number),
        "Checkout_category":Order2.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(Order2.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Category.objects.all(),
        "Active_category":category,
        "Menu": menu,
        "Columns":columns,
        "Topping_price": 0.00,
        "Order_number":order_number
    }
    if (category == 'Regular Pizza' or category == 'Sicilian Pizza'):
        if name =="1 topping":
            topping_allowance.topping_allowance+=1
            topping_allowance.save()
        if name =="2 toppings":
            topping_allowance.topping_allowance+=2
            topping_allowance.save()
        if name =="3 toppings":
            topping_allowance.topping_allowance+=3    
            topping_allowance.save()
    if category == "Toppings" and topping_allowance.topping_allowance == 0:
        return render(request,"menu.html",context) 
    if category == "Toppings" and topping_allowance.topping_allowance > 0:
        topping_allowance.topping_allowance-=1
        topping_allowance.save()

    add=Order2(user=request.user,number=order_number,category=category,name=name,price=price) 
    add.save()      
    context2 = {
        "Checkout":Order2.objects.filter(user=request.user,number=order_number),
        "Checkout_category":Order2.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(Order2.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Category.objects.all(),
        "Active_category":category,
        "Menu": menu,
        "Columns":columns,
        "Topping_price": 0.00,
        "Order_number":order_number
    }       
    return render(request,"menu.html",context2) 

def delete(request,category,name,price):
    menu,columns=findTable(category)
    order_number=User_order.objects.get(user=request.user,status='initiated').order_number
    topping_allowance=User_order.objects.get(user=request.user,status='initiated')
    if (category == 'Regular Pizza' or category == 'Sicilian Pizza'):
        if name =="1 topping":
            topping_allowance.topping_allowance-=1
            topping_allowance.save()
        if name =="2 toppings":
            topping_allowance.topping_allowance-=2
            topping_allowance.save()
        if name =="3 toppings":
            topping_allowance.topping_allowance-=3    
            topping_allowance.save()
        topping_allowance.topping_allowance=0
        topping_allowance.save()
        delete_all_toppings=Order2.objects.filter(user=request.user,category="Toppings")
        delete_all_toppings.delete()
    if category == "Toppings":
        topping_allowance.topping_allowance+=1
        topping_allowance.save()

    
    find_order=Order2.objects.filter(user=request.user,category=category,name=name,price=price)[0]
    find_order.delete()                
    context = {
        "Checkout":Order2.objects.filter(user=request.user,number=order_number),
        "Checkout_category":Order2.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(Order2.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Category.objects.all(),
        "Active_category":category,
        "Menu": menu,
        "Columns":columns,
        "Topping_price": 0.00,
        "Order_number":order_number
    }
    return render(request,"menu.html",context)

def my_orders(request,order_number):
    context = {
        "Checkout":Order2.objects.filter(user=request.user,number=order_number),
        "Checkout_category":Order2.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
        "Total":list(Order2.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Category.objects.all(),
        "Order_number":order_number,
        "All_orders":User_order.objects.filter(user=request.user),
        "Status":User_order.objects.get(user=request.user,order_number=order_number).status
    }
    return render(request,"my_orders.html",context)


def orders_manager(request,user,order_number):
    user=User.objects.get(username=user)
    context = {
        "Checkout":Order2.objects.filter(user=user,number=order_number),
        "Checkout_category":Order2.objects.filter(user=user,number=order_number).values_list('category').distinct(),
        "Total":list(Order2.objects.filter(user=user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Category.objects.all(),
        "Order_number":order_number,
        "All_orders":User_order.objects.exclude(status='initiated')
    }
    return render(request,"orders_manager.html",context)

def complete_order(request,user,order_number):
    user=User.objects.get(username=user)
    complete=User_order.objects.get(user=user,order_number=order_number)
    complete.status='completed'
    complete.save()

    context = {
        "Checkout":Order2.objects.filter(user=user,number=order_number),
        "Checkout_category":Order2.objects.filter(user=user,number=order_number).values_list('category').distinct(),
        "Total":list(Order2.objects.filter(user=user,number=order_number).aggregate(Sum('price')).values())[0],
        "user":request.user,
        "Category": Category.objects.all(),
        "Order_number":order_number,
        "All_orders":User_order.objects.exclude(status='initiated')
    }
    return render(request,"orders_manager.html",context)

def confirmed(request,order_number):
    status=User_order.objects.get(user=request.user,status='initiated')
    status.status='pending'
    status.save()

    counter=Order_counter.objects.first()
    new_order_number=User_order(user=request.user,order_number=counter.counter)
    new_order_number.save()
    counter.counter=counter.counter+1
    counter.save()
    
    return my_orders(request,order_number)
    #return render(request,"my_orders.html",context)

def findTable(category):
    if category == "Regular Pizza":
        menu=Regular_pizza.objects.all()
        columns=3
    elif category == "Sicilian Pizza":
        menu=Sicilian_pizza.objects.all()
        columns=3
    elif category == "Toppings":
        menu=Topping.objects.all()
        columns=1
    elif category == "Subs":
        menu=Sub.objects.all()
        columns=3
    elif category == "Pasta":
        menu=Pasta.objects.all()
        columns=2
    elif category == "Salad":
        menu=Salad.objects.all()
        columns=2
    elif category == "Dinner Platters":
        menu=Dinner_platter.objects.all()
        columns=3

    return menu,columns
