from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.Cloth)
admin.site.register(models.Color)
admin.site.register(models.Size)
admin.site.register(models.Review)
admin.site.register(models.Category)
admin.site.register(models.ClothWishList)
admin.site.register(models.ClothCartList)
