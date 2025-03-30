from django.db import models

class Task(models.Model):
    STATUS_CHOICES =[
        ('To Do','To Do'),
        ('In Progress','In Progress'),
        ('Done','Done'),
    ]
    task = models.TextField(max_length=200)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='To Do')
    
    def __str__(self):
        return self.task        
    
class Coin(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Basket(models.Model):
    name = models.CharField(max_length=100)
    coins = models.ManyToManyField(Coin, related_name="baskets")  # M2M Relationship

    def __str__(self):
        return self.name
  
    
class History(models.Model):
    symbol = models.TextField(max_length=200)
    timestamp = models.DateField()
    close = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()

    def __str__(self):
        return self.coin