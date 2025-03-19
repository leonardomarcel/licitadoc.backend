from django.db import models

# Create your models here.

class Document(models.Model):
    document = models.FileField(upload_to='documents/%Y/%m/%d')
    title = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-created_at']

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    
