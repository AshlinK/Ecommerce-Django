from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''
    This function is a receiver. Whenever the sender(Model) calls this function, we will check
    the first instance , in our case its 'created'
    '''
    if created:
        Profile.objects.create(user=instance)
        print("Profile created")

# post_save.connect(receiver=create_profile, sender=User)


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    '''
    This function is a receiver. Whenever the sender(Model) calls this function, we will check 
    the first instance , in our case its 'created'
    '''
    if not created:
        instance.profile.save()
        print("Profile updated !!")
