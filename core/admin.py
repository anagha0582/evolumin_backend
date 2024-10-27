from django.contrib import admin
from .models import (
    User,
    Rider,
    WasteType,
    WasteRequest,
    EducationalContent,
    EnvironmentalImpact,
    Reward,
    UserAchievement,
    Achievement  # Ensure Achievement model is imported
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_rider', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_rider',)  # Added filter for is_rider

@admin.register(WasteType)
class WasteTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ('user', 'lat', 'lng', 'availability_status', 'waste_type')  # Added waste_type
    search_fields = ('user__username',)
    list_filter = ('availability_status', 'waste_type')  # Added filter for availability_status and waste_type

@admin.register(WasteRequest)
class WasteRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'rider', 'waste_type', 'quantity', 'status', 'pickup_address', 'timestamp')
    list_filter = ('status', 'waste_type', 'rider')  # Added filter for rider
    search_fields = ('user__username', 'pickup_address')

@admin.register(EducationalContent)
class EducationalContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

@admin.register(EnvironmentalImpact)
class EnvironmentalImpactAdmin(admin.ModelAdmin):
    list_display = ('user', 'waste_type', 'recycled_amount', 'general_waste_amount', 'co2_saved', 'created_at')
    list_filter = ('waste_type',)  # Filter by waste type
    search_fields = ('user__username',)

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'points')
    search_fields = ('name',)

class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_achievement_name', 'achieved_at')

    def get_achievement_name(self, obj):
        return obj.achievement.name  # Assuming 'name' is a field in Achievement model
    get_achievement_name.short_description = 'Achievement'  # Optional: Set display name

    # Added filter for achieved_at
    list_filter = ('achieved_at',)

admin.site.register(UserAchievement, UserAchievementAdmin)