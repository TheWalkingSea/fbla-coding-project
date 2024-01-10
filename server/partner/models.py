from django.db import models
from organization.models import Organization
from contact.models import Contact


class Partner(models.Model):
    role = models.TextField()
    description = models.TextField()
    expertise = models.TextField()
    organization_fk = models.ForeignKey(Organization, on_delete=models.CASCADE)
    contact_fk = models.ForeignKey(Contact, on_delete=models.CASCADE)

class PartnerTag(models.Model):
    partner_fk = models.ForeignKey(Partner, on_delete=models.CASCADE)
    tagname = models.TextField()
    tagcolor = models.CharField(max_length=6)