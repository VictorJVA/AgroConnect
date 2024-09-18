from django.contrib import admin
from pages.models import Post,Truck,User,Farmer,Driver
# Register your models here.
admin.site.register(Driver)
admin.site.register(Post)
admin.site.register(Truck)
admin.site.register(Farmer)
admin.site.register(User)