from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Custom User model extending AbstractUser
class User(AbstractUser):
    is_rider = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions '
                  'granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username

# UserProfile model to store additional user information
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - Profile"

# WasteType model for different types of waste
class WasteType(models.Model):
    description = models.TextField()
    name = models.CharField(max_length=255)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

# Rider model representing a waste collection rider
class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lat = models.FloatField()
    lng = models.FloatField()
    waste_type = models.ForeignKey(WasteType, on_delete=models.SET_NULL, null=True)
    availability_status = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)
    experience_level = models.CharField(max_length=50, default="Beginner")

    def __str__(self):
        return f"{self.user.username} - {self.waste_type.name if self.waste_type else 'No Waste Type'}"

# Define Status choices using TextChoices
class Status(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    ACCEPTED = 'Accepted', 'Accepted'
    IN_PROGRESS = 'In Progress', 'In Progress'
    COMPLETED = 'Completed', 'Completed'

# WasteRequest model for waste collection requests
class WasteRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.SET_NULL, null=True, blank=True)
    waste_type = models.ForeignKey(WasteType, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    pickup_address = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.waste_type.name if self.waste_type else "No Waste Type"} ({self.status})'

# CollectionHub model to represent waste collection hubs
class CollectionHub(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# UserLocation model to store user location
class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - Location"

# EducationalContent model for various educational resources
class EducationalContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('tip', 'Tip'),
    ]
    
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# EnvironmentalImpact model to track the environmental impact of users
class EnvironmentalImpact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waste_type = models.CharField(max_length=50)
    recycled_amount = models.FloatField()
    general_waste_amount = models.FloatField()
    co2_saved = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.co2_saved} kg CO2 Saved"

# Reward model for user rewards
class Reward(models.Model):
    name = models.CharField(max_length=100)
    points = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

# Achievement and UserAchievement models
class Achievement(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    achieved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"