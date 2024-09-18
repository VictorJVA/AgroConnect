from django.contrib import admin
from pages.models import Post,Truck,User,Farmer
# Register your models here.
admin.site.register(Post)
admin.site.register(Truck)
admin.site.register(Farmer)
admin.site.register(User)