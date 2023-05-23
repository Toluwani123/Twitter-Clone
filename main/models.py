from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(null=False, blank=False, max_length=500)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="pictures/")
    followers = models.ManyToManyField("self", related_name = 'followed_by', blank=True, symmetrical=False)

    def __str__(self):
        return self.user.username
    def total_followers(self):
        return self.followers.count()
    def total_following(self):
        return self.followed_by.count()
    


class Talks(models.Model):
    user = models.ForeignKey(User, related_name="talks", on_delete=models.DO_NOTHING)
    body = models.TextField(null=False, blank=False, max_length=500)
    image = models.ImageField(null=True, blank=True, upload_to="talk-pictures/")
    talked_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="talk_likes")

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user}  " f"{self.talked_at:%Y-%m-%d %H:%M}:  " f"{self.body}"

@receiver(post_save, sender=User)
def auto_create(sender, instance, created, **kwargs):
    if created:
        user_profile = Person(user=instance)

        user_profile.save()
        user_profile.followers.set([instance.person.user.id])
        user_profile.save()
post_save.connect(auto_create, sender=User)
