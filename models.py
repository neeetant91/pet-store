from django.db import models

# Create your models here.
class Petstore(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=122,null=True)
    category=models.CharField(max_length=122,null=True)
    price=models.CharField(max_length=122,null=True)
    line=models.CharField(max_length=122,null=True)
    desc=models.TextField(null=True)
    img1=models.TextField(null=True)
    img2=models.TextField(null=True)
    img3=models.TextField(null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.IntegerField(max_length=255,null=True)
    pet_id=models.IntegerField(max_length=122,null=True)
    name=models.CharField(max_length=122,null=True)
    # category=models.CharField(max_length=122,null=True)
    line=models.CharField(max_length=122,null=True)
    # desc=models.TextField(null=True)
    img1=models.TextField(null=True)
    date=models.DateField(null=True,blank=True)

    # img2=models.TextField(null=True)
    # img3=models.TextField(null=True)

    def __str__(self):
        return self.name

class Buy(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.IntegerField(max_length=255,null=True)
    pet_id=models.IntegerField(max_length=122,null=True)
    name=models.CharField(max_length=122,null=True)
    # category=models.CharField(max_length=122,null=True)
    line=models.CharField(max_length=122,null=True)
    # desc=models.TextField(null=True)
    img1=models.TextField(null=True)
    date=models.DateField(null=True,blank=True)

    # img2=models.TextField(null=True)
    # img3=models.TextField(null=True)

    def __str__(self):
        return self.name