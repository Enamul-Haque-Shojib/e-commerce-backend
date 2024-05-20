from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Color(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)
    def __str__(self):
        return self.name  

class Size(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)
    def __str__(self):
        return self.name
    

    
class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)
    # image = models.ImageField(upload_to='static/images', null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.name
    

class Cloth(models.Model):
    clothid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField()
    color = models.ManyToManyField(Color)
    Size = models.ManyToManyField(Size)
    rating = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='static/images')
    image = models.URLField()
    image2 = models.URLField(null=True, blank=True)


    def __str__(self) -> str:
        return f"{self.name}"
    
#----------------------------------------------------------------
# class Category(models.Model):
#     categoryId = models.IntegerField(primary_key=True)
#     parent_category = models.CharField(max_length=30)
#     sub_category = models.CharField(max_length=30)
#     slug = models.SlugField(max_length=40)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return self.categoryId
    

# class Product(models.Model):
#     productId = models.IntegerField(primary_key=True)
#     title = models.CharField(max_length=50)
#     price = models.IntegerField()
#     discount_price = models.IntegerField()
#     quantity = models.IntegerField()
#     summary = models.TextField()
#     description = models.TextField()
#     rating = models.FloatField(default=0.0)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     vendor = models.ForeignKey(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='static/images')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)


#     def __str__(self) -> str:
#         return f"{self.name}"
    
# ----------------------------------------------------------------
    
class ClothWishList(models.Model):
    clothid = models.IntegerField(null=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField()
    color = models.ManyToManyField(Color)
    Size = models.ManyToManyField(Size)
    rating = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='static/images')
    image = models.URLField()


    def __str__(self) -> str:
        return f"{self.name}"

class ClothCartList(models.Model):
    clothid = models.IntegerField(null=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField()
    color = models.ManyToManyField(Color)
    Size = models.ManyToManyField(Size)
    rating = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='static/images')
    image = models.URLField()


    def __str__(self) -> str:
        return f"{self.name}"

       




STAR_CHOICES =[
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
]

class Review(models.Model):
    cloth = models.ForeignKey(Cloth, on_delete = models.CASCADE, related_name= 'reviews')
    author = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(choices = STAR_CHOICES, max_length=10)

    def __str__(self):
        # return f"{self.author.first_name} {self.author.last_name}"
        return self.body

