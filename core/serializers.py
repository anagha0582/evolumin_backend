from rest_framework import serializers
from .models import (
    User,
    WasteType,
    Rider,
    WasteRequest,
    CollectionHub,
    UserLocation,
    EducationalContent,
    EnvironmentalImpact,
    Reward,
    UserAchievement,
    UserProfile
)

# Serializer for User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # or specify the fields you want to include

# Serializer for User registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_rider']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_rider=validated_data.get('is_rider', False)
        )
        return user

# Serializer for Waste Types
class WasteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteType
        fields = '__all__'

# Serializer for Rider details
class RiderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Include user details for Riders

    class Meta:
        model = Rider
        fields = '__all__'

# Serializer for Waste Requests
class WasteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteRequest
        fields = ['id', 'user', 'rider', 'waste_type', 'quantity', 'status', 'pickup_address', 'timestamp']  # Include user and rider fields

# Serializer for Collection Hubs
class CollectionHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionHub
        fields = '__all__'

# Serializer for User Location
class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = '__all__'

# Serializer for Educational Content
class EducationalContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalContent
        fields = '__all__'

# Serializer for Environmental Impact
class EnvironmentalImpactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalImpact
        fields = '__all__'

# Serializer for Rewards
class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'

# Serializer for User Achievements
class UserAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAchievement
        fields = '__all__'

# Serializer for User Profile
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Include user details
    waste_requests = WasteRequestSerializer(many=True, read_only=True)  # Include waste requests

    class Meta:
        model = UserProfile
        fields = ['user', 'account_balance', 'waste_requests']  # Include user and account_balance