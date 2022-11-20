from django.db import models


class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    #upload_by = models.ForeignKey('auth.User', related_name='uploaded_documents')

    class Meta:
        db_table = 'Document'
# Create your models here.
