from django.db import models
from contact.models import Contact

class Organization(models.Model):
    description = models.TextField()
    type = models.TextField()
    url = models.URLField()
    contact_fk = models.ForeignKey(Contact, on_delete=models.CASCADE)

class OrganizationTag(models.Model):
    organization_fk = models.ForeignKey(Organization, on_delete=models.CASCADE)
    tagname = models.TextField()
    tagcolor = models.CharField(max_length=6)