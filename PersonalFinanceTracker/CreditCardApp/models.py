from django.db import models
from AuthApp.models import AppUser  # Import custom user model

class CreditCard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='card_images/')

    def __str__(self):
        return self.name

class UserCardApplication(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} applied for {self.credit_card.name}"
