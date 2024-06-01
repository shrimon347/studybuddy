from django.db import models
from base.models import User
# Create your models here.


BRANCH_CHOICES = ( 
    ("CSE", "CSE"), 
    ("EEE", "EEE"), 
    ("CIVIL", "CIVIL"), 
    ("MECHANICAL", "MECHANICAL"), 
    ("IT", "IT"), 
    ("NETWORKING", "NETWORKING"), 
    ("ECE", "ECE"), 
    ("OTHER", "OTHER"), 
) 

FILETYPE_CHOICES = (
    ("pdf", "PDF"), 
    ("doc", "DOC/DOCX"), 
    ("CIVIL", "CIVIL"), 
    ("ppt", "PPT/WORD"), 
    ("zip", "ZIP"), 
    ("image", "IMAGE"),  
    ("OTHER", "OTHER"), 
)

class AllSubject(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    uploadingdate = models.DateField(auto_now_add = True)
    branch = models.CharField(max_length=30,  choices = BRANCH_CHOICES, default = 'CSE')
    subject = models.ForeignKey(AllSubject, on_delete=models.SET_NULL, blank=True, null=True)
    notesfile = models.FileField(null=True,upload_to='note')
    filetype = models.CharField(max_length=30, choices = FILETYPE_CHOICES, default = 'pdf')
    description = models.CharField(max_length=200, null=True)
    status = models.BooleanField('Approved', default = False)
    downloads = models.IntegerField(default=0)  # Add this field
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-update', '-created']

    def __str__(self):
        return str(self.subject)

class Contact(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,default="")
    notesfile = models.FileField(null=True,upload_to='contacy')
    description = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=12)
