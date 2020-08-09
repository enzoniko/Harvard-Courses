from django.contrib import admin
from .models import Category,Regular_pizza,Sicilian_pizza,Topping,Sub,Pasta,Salad,Dinner_platter,Order2,User_order,Order_counter
# Register your models here.

admin.site.register(Category)
admin.site.register(Regular_pizza)
admin.site.register(Sicilian_pizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner_platter)
admin.site.register(Order2)
admin.site.register(User_order)
admin.site.register(Order_counter)