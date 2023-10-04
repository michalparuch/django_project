from django.contrib import admin
from olx_website import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Item)
admin.site.register(models.Condition)
admin.site.register(models.Room)
admin.site.register(models.Message)