from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):  
    model = OrderItem  
    extra = 1  # Número de filas vacías para agregar más productos en la orden  

class OrderAdmin(admin.ModelAdmin):  
    list_display = ('id', 'user', 'status', 'total')  
    inlines = [OrderItemInline]  # Muestra los productos dentro de la orden  

admin.site.register(Order, OrderAdmin)
