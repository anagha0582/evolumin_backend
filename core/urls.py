from django.urls import path
from .views import (
    WasteTypeListView,
    WasteRequestListCreateView,
    AvailableRidersListView,
    CorrectViewClassForUpdateLocation,
    CollectionHubListView,
    UserLocationView,
    EducationalContentListView,
    EnvironmentalImpactView,
    RewardListView,
    UserAchievementListView,
    UserProgressView,
    WasteCollectionView,
    UserProfileView,
    UserDashboardView,  # Added UserDashboardView
    WasteRequestListCreateView,  # Admin view
    WasteRequestDetailView,  # Admin view
    RiderListCreateView,  # Admin view
    RiderDetailView,  # Admin view
    WasteTypeListCreateView,  # Admin view
    WasteTypeDetailView  # Admin view
)

urlpatterns = [
    # User Accessible Views
    path('waste-types/', WasteTypeListView.as_view(), name='waste_types'),
    path('waste-request/', WasteRequestListCreateView.as_view(), name='waste_request_create'),
    path('available-riders/', AvailableRidersListView.as_view(), name='available_riders'),
    path('update-location/', CorrectViewClassForUpdateLocation.as_view(), name='update_location'),
    path('collection-hubs/', CollectionHubListView.as_view(), name='collection_hubs-list'),
    path('user-location/', UserLocationView.as_view(), name='user_location'),
    path('educational-content/', EducationalContentListView.as_view(), name='educational_content'),
    path('environmental-impact/', EnvironmentalImpactView.as_view(), name='environmental_impact'),
    path('rewards/', RewardListView.as_view(), name='reward_list'),
    path('user/achievements/', UserAchievementListView.as_view(), name='user_achievements'),
    path('user/progress/', UserProgressView.as_view(), name='user_progress'),
    path('waste-collection/', WasteCollectionView.as_view(), name='waste_collection'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('user/dashboard/', UserDashboardView.as_view(), name='user_dashboard'),

    # Admin Accessible Views
    path('api/waste-requests/', WasteRequestListCreateView.as_view(), name='waste-request-list-create'),
    path('api/waste-requests/<int:pk>/', WasteRequestDetailView.as_view(), name='waste-request-detail'),
    path('api/riders/', RiderListCreateView.as_view(), name='rider-list-create'),
    path('api/riders/<int:pk>/', RiderDetailView.as_view(), name='rider-detail'),
    path('api/waste-types/', WasteTypeListCreateView.as_view(), name='waste-type-list-create'),
    path('api/waste-types/<int:pk>/', WasteTypeDetailView.as_view(), name='waste-type-detail'),
]