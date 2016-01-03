from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


from www import settings


class RPiPin(models.Model):
	pin = models.SmallIntegerField(blank=False, null=False)
	label = models.CharField(max_length=50, blank=False, null=False)
	def __unicode__(self):
		return "%s - %s" % (self.pin, self.label)
	class Meta:
		verbose_name = _("RPi Pin")
		unique_together = ('pin', 'label')

# Create your models here.
