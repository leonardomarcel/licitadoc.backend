from django.db import models
import uuid
# Create your models here.



class Document(models.Model):
    original_file = models.FileField(upload_to='documents/')
    uuid = models.CharField(max_length=36, blank=True)
    pdf_file_version = models.FileField(upload_to='documents/', blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            uuid_str = str(uuid.uuid4())
            self.original_file.name = f'{uuid_str}/{uuid_str}'+'.'+self.original_file.name.split('.')[1]
            self.uuid = uuid_str
            #self.pdf_file_version.name = f'documents/{uuid_str}'+'.'+self.pdf_file_version.name.split('.')[1]
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-created_at']
        permissions = [
            ("can_download_document", "Can download document"),
            ("can_view_document", "Can view document"),
            
        ]

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    
