from django.db import models
import uuid
# Create your models here.


class data(models.Model):
    id=models.BigIntegerField(primary_key=True, default=uuid.uuid4)
    major=models.CharField(max_length=512,blank=True, default='null', null=True)
    submajor=models.CharField( max_length=512,blank=True, default='null', null=True)
    minor=models.CharField( max_length=512,blank=True, default='null', null=True)
    subminor=models.CharField(max_length=512, blank=True, default='null', null=True)
    grade=models.CharField(max_length=512, blank=True, default='null', null=True)
    file_formats = models.CharField(max_length=512,default='null', null=True)
    type=models.CharField( max_length=512,blank=True, default='null', null=True)
    source_description=models.CharField(max_length=512,blank=True, default='null', null=True)
    place_city=models.CharField( max_length=512,blank=True, default='null', null=True)
    year=models.CharField( max_length=512,blank=True, default='null', null=True)
    publisher=models.CharField(max_length=512, blank=True, default='null', null=True)
    path = models.CharField( max_length=512,blank=True, default='null', null=True)
    collection=models.CharField(max_length=512,blank=True, default='null', null=True)
    collection_type=models.CharField( max_length=512,blank=True, default='null', null=True)
    soi_toposheet_no=models.CharField(max_length=512, blank=True, default='null', null=True)
    grade1=models.CharField(max_length=512, blank=True, default='null', null=True)
    data_resolution=models.CharField(max_length=512, blank=True, default='null', null=True)
    ownership = models.CharField(max_length=512,default='null', null=True)
    is_processed=models.CharField(max_length=512, blank=True, default='null', null=True)
    short_descr=models.CharField(max_length=512,blank=True, default='null', null=True)
    descr=models.TextField( blank=True, default='null', null=True)
    img_service=models.TextField( blank=True, default='null', null=True)
    img_dw=models.TextField( blank=True, default='null', null=True)
    map_service = models.CharField( max_length=512,blank=True, default='null', null=True)
    map_dw=models.TextField( blank=True, default='null', null=True)
    publish_on=models.TextField( blank=True, default='null', null=True)
    thumbnail=models.TextField( blank=True, default='null', null=True)
    source = models.CharField(max_length=512, blank=True, default='null', null=True)
    created_id = models.CharField(max_length=512, blank=True, default='null', null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)#add current time in minute to the database table
    modified_id = models.CharField(max_length=50, blank=True, default='null', null=True)
    modified_date =models.DateTimeField(auto_now_add=True, null=True)# it adds the time that is currently updated
    deleted_id = models.CharField(max_length=50, blank=True, default='null', null=True)
    deleted_date = models.DateTimeField(auto_now_add=True, null=True)
  
    



# class Download_Details(models.Model):
#     down_id = models.UUIDField(default=uuid.uuid4, unique=True,)
#     data = models.ForeignKey(data, on_delete=models.CASCADE, null=True)
#     down_date = models.DateField(auto_now_add=True)
#     image_type = models.CharField(max_length=1,default='null', null=True)
#     image_name = models.CharField(max_length=255,default='null', null=True)
#     image_url = models.CharField(max_length=500,default='null', null=True)
#     email_id = models.CharField(max_length=100,default='null', null=True)
    
  
class Downloads(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4) 
    down_date = models.DateField(auto_now_add=True)
    image_type = models.CharField(max_length=250, blank=True, default='null', null=True)
    image_name = models.CharField(max_length=250, blank=True, default='null', null=True)
    image_url = models.CharField(max_length=250, blank=True, default='null', null=True)     
    country = models.CharField(max_length=250, blank=True, default='null', null=True)  
    email_id = models.CharField(max_length=100,default='null', null=True)   
    data_id = models.ForeignKey(data, on_delete=models.CASCADE, null=True)    







  
       