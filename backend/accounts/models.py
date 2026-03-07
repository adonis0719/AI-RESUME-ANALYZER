from django.db import models

class EmailOTP(models.Model):

    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    



from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_name = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username