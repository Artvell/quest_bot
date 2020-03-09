from django.db import models

# Create your models here.

class Quest(models.Model):
    choices=[(1,"Да"),
              (0,"Нет")]
    name=models.CharField(max_length=150,verbose_name="Название")
    company=models.CharField(max_length=150,verbose_name="Компания")
    genre=models.CharField(max_length=100,verbose_name="Жанры")
    stock=models.IntegerField(verbose_name="Акции",default=0,choices=choices) #акции
    longitude=models.CharField(max_length=25,verbose_name="Долгота") #долгота
    latitude=models.CharField(max_length=25,verbose_name="Широта") #широта
    image_link=models.CharField(max_length=150,verbose_name="Картинка")
    admin_id=models.IntegerField(verbose_name="Айди")
    text=models.TextField(verbose_name="Описание",default="Text")
