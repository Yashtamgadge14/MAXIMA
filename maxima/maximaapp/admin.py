from django.contrib import admin
from maximaapp.models import product
# Register your models here.
class productadmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails']
    list_filter=['cat','is_active']
admin.site.register(product,productadmin)
