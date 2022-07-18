from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum
from .models import Category,Regular_pizza,Sicilian_pizza,Topping,Basquete,Tênis,Futebol,Vôlei,Order2,User_order,Order_counter, ValidaCpfCnpj, Frequência
import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import Union
import qrcode
import time
import re

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

# Create your views here.
counter = Order_counter.objects.first()
if counter is None:
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
    if user is None:
        return render(request,"login.html",{"message":"Invalid credentials"})
    login(request,user)
    return HttpResponseRedirect(reverse("index")) 

def logout_view(request):
    logout(request)
    return render(request,"login.html",{"message":"Logged out."})

def signin_view(request):
    if request.method == "POST":
        #first_name=request.POST["first_name"]
        #last_name=request.POST["last_name"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        #password2=request.POST["password2"]
        #if not password==password2:
            #return render(request,"signin.html",{"message":"Passwords don't match."})
        user=User.objects.create_user(username,email,password)
        #user.first_name=first_name
        #user.last_name=last_name
        user.last_name='0'
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

def test_view(request):
    
    user=User.objects.get(username=request.user)
    email = user.email
    lastname = user.last_name
    firstname = user.first_name
    period=request.POST["period"]
    sala=request.POST["sala"]
    data=request.POST["date"]
    if firstname == '':
        cpf=request.POST["cpf"]
        cpf1=request.POST["cpf1"]
        cpf2=request.POST["cpf2"]
        CPF = ValidaCpfCnpj(cpf)
        if (CPF.valida() and cpf1 == '' and cpf2 == ''):
            CPFstatus = "Válido"
            firstname = cpf
            user.first_name = firstname
            user.save()
            userCPF = user.first_name
            cpfs = userCPF 
        if cpf1 != '' and cpf2 == '':
            CPF1 = ValidaCpfCnpj(cpf1)
            if (CPF1.valida()):
                CPFstatus = "Válido"
                firstname = cpf
                user.first_name = firstname
                user.save()
                userCPF = user.first_name
                cpfs = userCPF + '-' + cpf1
        if cpf2 != '' and cpf1 == '':
            CPF2 = ValidaCpfCnpj(cpf2)
            if (CPF2.valida()):
                firstname = cpf
                user.first_name = firstname
                user.save()
                userCPF = user.first_name
                CPFstatus = "Válido"
                cpfs = userCPF + '-' + cpf2
        if cpf1 != '' and cpf2 != '':
            CPF1 = ValidaCpfCnpj(cpf1)
            CPF2 = ValidaCpfCnpj(cpf2)
            if (CPF1.valida() and CPF2.valida() and CPF.valida()):
                CPFstatus = "Válido"
                firstname = cpf
                user.first_name = firstname
                user.save()
                userCPF = user.first_name
                cpfs = userCPF + '-' + cpf1 + '-' + cpf2
       
            if (CPF.valida() == False or CPF1.valida() == False or CPF2.valida() == False):
                CPFstatus = "Inválido"

    if firstname != '':
        cpf = firstname
        userCPF = user.first_name
        cpf1=request.POST["cpf1"]
        cpf2=request.POST["cpf2"]
        CPF = ValidaCpfCnpj(cpf)
        if (CPF.valida() and cpf1 == '' and cpf2 == ''):
            CPFstatus = "Válido"
            cpfs = userCPF 
        if cpf1 != '' and cpf2 == '':
            CPF1 = ValidaCpfCnpj(cpf1)
            if (CPF1.valida()):
                CPFstatus = "Válido"
                cpfs = userCPF + '-' + cpf1
        if cpf2 != '' and cpf1 == '':
            CPF2 = ValidaCpfCnpj(cpf2)
            if (CPF2.valida()):
                CPFstatus = "Válido"
                cpfs = userCPF + '-' + cpf2
        if cpf1 != '' and cpf2 != '':
            CPF1 = ValidaCpfCnpj(cpf1)
            CPF2 = ValidaCpfCnpj(cpf2)
            if (CPF1.valida() and CPF2.valida()):
                CPFstatus = "Válido"
                cpfs = userCPF + '-' + cpf1 + '-' + cpf2
       
            if (CPF.valida() == False or CPF1.valida() == False or CPF2.valida() == False):
                CPFstatus = "Inválido"

    
    


    if (sala == ' Vôlei - Quadra Guarapuvu'):
        sala_id = '2'
    elif (sala == ' Vôlei - Quadra Araucária'):
        sala_id = '3'
    elif (sala == ' Vôlei - Quadra Pinus'):
        sala_id = '4'
    elif (sala == ' Tênis - Quadra Campeche'):
        sala_id = '5'
    elif (sala == ' Tênis - Quadra Joaquina'):
        sala_id = '6'
    elif (sala == ' Basquete - Quadra Atlata'):
        sala_id = '7'
    elif (sala == ' Basquete - Quadra Philadelphia'):
        sala_id = '8'
    elif (sala == ' Futebol - Salão Orquídia'):
        sala_id = '9'
    elif (sala == ' Futebol - Salão Camélia'):
        sala_id = '10'
    elif (sala == ' Futebol - Campo Lírios'):
        sala_id = '11'
    elif (sala == ' Futebol - Campo Jasmim'):
        sala_id = '12'
    
    if (period == 'À tarde das 14:00 - 18:00 H'):
        
        data_inicial = data.strip() + 'T14:00:00Z'
        data_final = data.strip() + 'T18:00:00Z'
    elif (period == 'De manhã das 8:00 - 12:00 H'):
        data_inicial = data.strip() + 'T8:00:00Z'
        data_final = data.strip() + 'T12:00:00Z'
    elif (period == 'À noite das 20:00 - 24:00 H'):
        data_inicial = data.strip() + 'T20:00:00Z'
        data_final = data.strip() + 'T23:59:00Z'


    url = "http://127.0.0.1:7000/agenda/?data_inicial=" + data_inicial.strip() + "&data_final=" + data_final.strip() + "&sala=" + sala_id.strip()
    
    r = requests.get(url)
    r = r.text

    if (r != '[]' and CPFstatus == 'Válido'):
        message = 'This sport court is already in use ):'
        url = "http://127.0.0.1:7000/agenda/?data_inicial=" + data_inicial.strip() + "&data_final=" + data_final.strip() + "&sala=" + sala_id.strip()
        r2 = requests.get(url)
        r2 = r2.text
        qr = qrcode.make(r2)
        qr2 = qr
    elif (CPFstatus == 'Inválido'):
        message = 'Your CPF is invalid (;'
        url = "http://127.0.0.1:7000/agenda/?data_inicial=" + data_inicial.strip() + "&data_final=" + data_final.strip() + "&sala=" + sala_id.strip()
        r2 = requests.get(url)
        r2 = r2.text
        qr = qrcode.make(r2)
        qr2 = qr
    elif (CPFstatus == 'Inválido' and r == '[]'):
        message = 'Your CPF is invalid (;'
        url = "http://127.0.0.1:7000/agenda/?data_inicial=" + data_inicial.strip() + "&data_final=" + data_final.strip() + "&sala=" + sala_id.strip()
        r2 = requests.get(url)
        r2 = r2.text
        qr = qrcode.make(r2)
        qr2 = qr
    elif (r == '[]' and CPFstatus == 'Válido'):
        message = 'Your reservation has been successfully scheduled (: The QR code is in your Email.'
        url2 = "http://127.0.0.1:7000/agenda/"
        headers = {'content-type': 'application/json'}
        data = {'titulo': str(request.user) + ' ' + sala.strip() + ' - ' + period.strip(),'sala': sala_id,'date_init': data_inicial.strip(),'date_end': data_final.strip(),}
        r2 = requests.post(url2, data=json.dumps(data), headers=headers)
        r2 = r2.text + cpfs
        qr = qrcode.make(r2)
        qr.save('orders/static/' + 'QR' + sala.strip() + cpfs.strip() + period.strip() + '.png')
        qr = 'QR' + sala.strip() + cpfs.strip() + period.strip() + '.png'
        qr2 = 'orders/static/' + 'QR' + sala.strip() + cpfs.strip() + period.strip() + '.png'
        
        fromaddr = EMAIL_ADDRESS
        toaddr = email
        
        msg = MIMEMultipart() 

        msg['From'] = fromaddr 
        
        msg['To'] = toaddr 

        msg['Subject'] = 'QR code confirmation of your rent'
        body = 'Use the QR code attached to unlock the space you rented'

        msg.attach(MIMEText(body, 'plain'))

        filename = qr
        attachment = open(qr2, "rb") 

        p = MIMEBase('application', 'octet-stream')

        p.set_payload((attachment).read()) 

        encoders.encode_base64(p)

        p.add_header('Content-Disposition', 'attachment', filename=filename)

        msg.attach(p) 

        s = smtplib.SMTP('smtp.gmail.com', 587) 

        s.starttls() 

        s.login(fromaddr, EMAIL_PASSWORD)

        text = msg.as_string() 

        s.sendmail(fromaddr, toaddr, text) 

        s.quit()

        os.remove(qr2)

        lastname = str(int(lastname) + 1)
        user.last_name=lastname
        user.save()
        


        

    
    context = {
        'r':r2,
        'response':r,
        'message':message,
        'user':request.user,
        'qr':qr,
        'Freq':lastname,
        
      
    }








    return render(request,"test2.html",context)
    

def cancel_view(request):
    if not request.user.is_authenticated:
        return render(request,"login.html",{"message":'Please, log in again'})
   
    if request.method == 'POST':
        user=User.objects.get(username=request.user)
        order_number=User_order.objects.get(user=request.user,status='initiated').order_number
        RentID = request.POST["id"]
        userCPF = user.first_name
        message = ''
        url1 = "http://127.0.0.1:7000/agenda/" + RentID.strip()
        r = requests.get(url1)
        r = r.text
     
        if (r != '[]'):
            checkUSER = re.search(user.username, r)
            
            if checkUSER:
                url = "http://127.0.0.1:7000/agenda/" + RentID.strip()
                r = requests.delete(url)
                r = r.text
                message = 'Rent canceled! Your QR code is not valid anymore!'
            else:
                url = "http://127.0.0.1:7000/agenda/" + RentID.strip()
                r = requests.get(url)
                r = r.text
                message = 'This is not your rent!'
        else:
            message = 'This rent does not exist!'
            
        
        
        context = {
            "user":request.user,
            "Checkout":Order2.objects.filter(user=request.user,number=order_number),
            "Checkout_category":Order2.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
            "Total":list(Order2.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
            "Category": Category.objects.all(),
            "Order_number":order_number,
            "message":message,
            "r":r,
            


        }
        return render(request,"cancel.html", context)

    user=User.objects.get(username=request.user)
    order_number=User_order.objects.get(user=request.user,status='initiated').order_number
    context = {
            "user":request.user,
            "Checkout":Order2.objects.filter(user=request.user,number=order_number),
            "Checkout_category":Order2.objects.filter(user=request.user,number=order_number).values_list('category').distinct(),
            "Total":list(Order2.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
            "Category": Category.objects.all(),
            "Order_number":order_number,
            }
    return render(request,"cancel.html", context)


def add(request,category,name,price):
    menu,columns=findTable(category)
    order_number=User_order.objects.get(user=request.user,status='initiated').order_number
    topping_allowance=User_order.objects.get(user=request.user,status='initiated')
    dia = 'De manhã das 8:00 - 12:00 H'
    tarde = 'À tarde das 14:00 - 18:00 H'
    noite = 'À noite das 20:00 - 24:00 H'
    if (category == 'Basquete' and price == '40.00'):
        period = noite
    elif (category == 'Basquete' and price == '30.00'):
        period = tarde
    elif (category == 'Basquete' and price == '20.00'):
        period = dia
    elif (category == 'Tênis' and price == '50.00'):
        period = noite
    elif (category == 'Tênis' and price == '40.00'):
        period = tarde
    elif (category == 'Tênis' and price == '30.00'):
        period = dia
    elif (category == 'Futebol' and price == '40.00' or price == '90.00'):
        period = noite
    elif (category == 'Futebol' and price == '30.00' or price == '80.00'):
        period = tarde
    elif (category == 'Futebol' and price == '20.00' or price == '70.00'):
        period = dia
    elif (category == 'Vôlei' and price == '40.00'):
        period = noite
    elif (category == 'Vôlei' and price == '30.00'):
        period = tarde
    elif (category == 'Vôlei' and price == '20.00'):
        period = dia
 
    user=User.objects.get(username=request.user)
    lastname = user.last_name
    if lastname >= '10':
        price = str(float(price) - 5)

    if lastname >= '20':
        price = str(float(price) - 10)

    if lastname >= '30':
        price = str(float(price) - 15)

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
        "Order_number":order_number,
        "Period":period
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
        return render(request,"test.html",context) 
    if category == "Toppings" and topping_allowance.topping_allowance > 0:
        topping_allowance.topping_allowance-=1
        topping_allowance.save()

    add=Order2(user=request.user,number=order_number,category=category,name=name,price=price) 
    add.save()      
    user=User.objects.get(username=request.user)
    lastname = user.last_name
    if lastname >= '10':
        price = str(float(price) - 5)

    if lastname >= '20':
        price = str(float(price) - 10)

    if lastname >= '30':
        price = str(float(price) - 15)
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
        "Order_number":order_number,
        "Period":period
    }       
    return render(request,"test.html",context2) 

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
        "All_orders":User_order.objects.filter(user=request.user),
    }
    return render(request,"orders_manager.html",context)

def complete_order(request,user,order_number):
    user=User.objects.get(username=user)
    cancel=User_order.objects.get(user=user,order_number=order_number)
    
    cancel.save()

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
    elif category == "Basquete":
        menu=Basquete.objects.all()
        columns=4
    elif category == "Tênis":
        menu=Tênis.objects.all()
        columns=4
    elif category == "Futebol":
        menu=Futebol.objects.all()
        columns=4
    elif category == "Vôlei":
        menu=Vôlei.objects.all()
        columns=4

    return menu,columns
