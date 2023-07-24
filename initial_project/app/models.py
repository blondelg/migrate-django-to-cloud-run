from django.db.models import Model, ImageField

class Image(Model):  
    upload = ImageField(upload_to ='')