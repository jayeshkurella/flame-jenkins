# from django.contrib import admin
# from django.contrib.admin import AdminSite
# from .models import data

# # Custom admin site class
# class CustomAdminSite(AdminSite):
#     site_header = 'Flame Admin Panel'

# # Instantiate custom admin site
# admin_site = CustomAdminSite(name='custom_admin')
# admin.site = admin_site

# # Register your models here (replace with your actual models)
# admin.site.register(data)

# # ...

from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import data

# Custom admin site class
class CustomAdminSite(AdminSite):
    site_header = 'Flame Admin Panel'

# Instantiate custom admin site
admin_site = CustomAdminSite(name='custom_admin')
admin.site = admin_site

# Register your models here (replace with your actual models)
admin.site.register(data)