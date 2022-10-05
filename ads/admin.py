from django.contrib import admin
from ads.models import User, Location, Ad, Category

admin.site.register(User)
admin.site.register(Location)
admin.site.register(Ad)
admin.site.register(Category)

# Register your models here.
