from django.db import models

# Create your models here.
from django.utils import timezone


class Patient(models.Model):
    pat_id=models.CharField(max_length=20,primary_key=True)
    pat_name=models.CharField(max_length=200)
    pat_age=models.IntegerField()
    pat_sex=models.CharField(max_length=20)
    pat_address=models.TextField()
    pat_phone=models.CharField(max_length=200)
    pat_password=models.CharField(max_length=200)

class Doctor(models.Model):
    doc_id=models.CharField(max_length=20,primary_key=True)
    doc_img=models.ImageField(upload_to='doc',default='暂无')
    img_path=models.TextField(default="null")
    doc_name=models.CharField(max_length=20)
    ranks=models.CharField(max_length=20,default="医师")
    subject=models.CharField(max_length=20,default="视网膜病变")
    doc_age=models.IntegerField()
    doc_text=models.TextField()
    doc_password=models.CharField(max_length=20)

class Appointment(models.Model):
    pat_id = models.CharField(max_length=20)
    doc_id = models.CharField(max_length=20)

class IMG(models.Model):
    pat_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, default='未诊断')
    img = models.ImageField(upload_to='img', default='暂无')
    after_img = models.TextField(default='null')
    date = models.DateTimeField('保存日期', default=timezone.now)
    name = models.CharField(max_length=100, default='暂无')
    oc = models.CharField(max_length=20, default='null')
    dr_rate = models.CharField(max_length=20, default='null')
    oc_rate = models.CharField(max_length=20, default='null')
    advice = models.TextField(default='暂无')
    propose = models.TextField(default='暂无')



class Dr(models.Model):
    dr_id=models.CharField(max_length=20)
    dr_name=models.CharField(max_length=20)
    advice=models.TextField()
    describe = models.CharField(max_length=20,default='暂无')

# class Oc(models.Model):
#     oc_id=models.CharField(max_length=20)
#     dr_name=models.CharField(max_length=20)
#     advice=models.TextField()
#     describe = models.CharField(max_length=20,default='暂无')