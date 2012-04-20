from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Rota(models.Model):
    """Class for each invdividual 'rota'. This is assumed to
    consist of a purpose .e.g. music group, and have associated with it
    a number of slots for which members of the rota are asked to 
    signup to."""

    label = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    owners = models.ManyToManyField(User, related_name='owner_set')
    users = models.ManyToManyField(User, related_name='user_set')

class RotaSlot(models.Model):
    """A particular labeled slot for a chosen day. This must
    be associated with a particular rota."""
    
    rota = models.ForeignKey(Rota)
    label = models.CharField(max_length=30)
    date = models.DateField()


class UserSlotAssoc(models.Model):
    """The data structure used to link together users and a particular
    rota slot as there may well be more than one person signing up for a particular
    rota slot."""

    user = models.ForeignKey(User)
    rota_slot = models.ForeignKey(RotaSlot)

    # 0 = No, 1 = yes, 2 = maybe
    option = models.SmallIntegerField()
    
    # Indicating whether the user has been 'selected' for this slot, and
    # so composed on any lists that are produced for this slot.
    selected = models.BooleanField()
