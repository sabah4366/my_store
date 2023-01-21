from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class Products(models.Model):
    name=models.CharField(max_length=150)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    image=models.ImageField(null=True,upload_to="images")


    @property
    def avg_rating(self):
        ratings=self.reviews_set.all().values_list("rating" ,flat=True)
        if ratings:
            return sum(ratings)/len(ratings)
        else:
            return 0
    @property
    def review_count(self):
        ratings=self.reviews_set.all().values_list("rating" ,flat=True)
        if ratings:
            return len(ratings)
        else:
            return 0


    def __str__(self):
        return self.name

class Carts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    options=(
        ('order-placed','order-placed'),
        ('in-cart','in-cart'),
        ('cancelled','cancelled')
        )
    status=models.CharField(max_length=200,choices=options,default='in-cart')




class Reviews(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    review=models.CharField(max_length=500)

    def __str__(self):
        return self.review

class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ('order-placed','order-placed'),
        ('despatched','despatched'),
        ('in-transit','in-transit'),
        ('cancelled','cancelled')
        )
    status=models.CharField(max_length=200,choices=options,default='order-placed')
    date=models.DateTimeField(auto_now_add=True)
    address=models.CharField(max_length=300)
    phone=models.CharField(max_length=20)



#ORM
#orm for creating a resource
#modelname.objects.create(field1=value,field2=value,...)                #Model name means class name
#products.objects.create(name="samsungprime",price=32000,descr="mobile")


#orm query for fetching all records
#variablename=modelname.objects.all()


#orm query for filtering
#varibalename=modelname.objects.filter(category="electronics")


#orm query for show without category=electronics
#varaiblename=modelname.objects.all().exclude(category="electronics")



#orm query for fetching specific record
#variablename=modelname.objects.get(id=1)

#orm query for update
#modelname.objects.filter(id=2).update(price=3000)

#orm qyuery for greater than
#modelname.objects.filter(price__lt=30000)
#__lt   -  <
#__lte  -  <=
#__gt   -  >
#__gte  -  >=

#products in a range of 15000 to 35000
#Products.objects.filter(price__gt=15000,price__lt=35000)

#return all categories
#products.objects.values_list('category',flat=True)
#flat=True means avoid tuple


#return all names
#Products.objects.values_list("name")


#return all categories with no duplications
#then use .distinct()
#Products.objects.values_list("category").distinct()


#return all categories with no duplications and that show like list
#then use inside the values_list("category",flat=True)
#Products.objects.values_list("category",flat=True).distinct()


#return the name of categories=electronics and like list
#products.objects.filter(category='electronics',flat=True).values_list("name")

#to delete a record
#products.objects.filter(id=3).delete()