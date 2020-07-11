from django.contrib.auth.models import User
from .models import User, Customer
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            name=instance.username,
        )
        print("User created!!")
