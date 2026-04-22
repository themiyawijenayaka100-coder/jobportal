from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    resume_link = models.URLField(blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"


class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-sent_at"]

    def __str__(self) -> str:
        return f"From {self.sender.username} to {self.recipient.username}: {self.subject}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Ensure a profile exists even for pre-existing users
        UserProfile.objects.get_or_create(user=instance)
