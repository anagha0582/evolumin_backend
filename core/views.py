from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views import View
from django.http import JsonResponse
from .models import (
    User,
    Rider,
    WasteType,
    WasteRequest,
    CollectionHub,
    UserLocation,
    EducationalContent,
    EnvironmentalImpact,
    Reward,
    UserAchievement,
    UserProfile
)
from .permissions import IsRider
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    RiderSerializer,
    WasteRequestSerializer,
    WasteTypeSerializer,
    CollectionHubSerializer,
    UserLocationSerializer,
    EducationalContentSerializer,
    EnvironmentalImpactSerializer,
    RewardSerializer,
    UserAchievementSerializer,
    UserProfileSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.db.models import F
from geopy.distance import geodesic
from rest_framework.pagination import PageNumberPagination

# Custom response handling
def custom_response(data, status_code):
    return Response(data, status=status_code)

# Admin permission class
class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access certain views.
    Admins can be defined by user roles in the User model.
    """

    def has_permission(self, request, view):
        # Allow access if user is staff
        if request.user.is_staff:
            return True
        
        # Additional logic based on user roles, e.g., if you have roles in the User model
        # Check if the user has an admin role, you can adjust this according to your User model
        return hasattr(request.user, 'role') and request.user.role in ['admin', 'super_admin']

# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return custom_response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'username': user.username,
                'is_rider': user.is_rider
            }, status.HTTP_201_CREATED)
        return custom_response(serializer.errors, status.HTTP_400_BAD_REQUEST)

# List all Waste Types
class WasteTypeListView(generics.ListAPIView):
    queryset = WasteType.objects.all()
    serializer_class = WasteTypeSerializer
    permission_classes = [permissions.AllowAny]

# Admin Waste Type Views
class WasteTypeListCreateView(generics.ListCreateAPIView):
    queryset = WasteType.objects.all()
    serializer_class = WasteTypeSerializer
    permission_classes = [IsAdminUser]

class WasteTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WasteType.objects.all()
    serializer_class = WasteTypeSerializer
    permission_classes = [IsAdminUser]

class UserLocationView(generics.ListCreateAPIView):
    queryset = UserLocation.objects.all()
    serializer_class = UserLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

class CollectionHubListView(generics.ListAPIView):
    queryset = CollectionHub.objects.all()
    serializer_class = CollectionHubSerializer
    permission_classes = [permissions.AllowAny]

# Environmental Impact View with Pagination
class EnvironmentalImpactPagination(PageNumberPagination):
    page_size = 10

class EnvironmentalImpactView(generics.ListAPIView):
    queryset = EnvironmentalImpact.objects.all()
    serializer_class = EnvironmentalImpactSerializer
    pagination_class = EnvironmentalImpactPagination

class UserProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Your logic here
        return Response({"message": "User progress"})

class RewardListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can access this view
    queryset = Reward.objects.all()  # Fetches all instances of the Reward model
    serializer_class = RewardSerializer  # Specifies the serializer to be used for the Reward model

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'rewards': serializer.data}, status=status.HTTP_200_OK)

# Create or Update a Waste Request
class WasteCollectionView(generics.CreateAPIView):
    serializer_class = WasteRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        items = request.data.get('items', {})
        total_amount = 0

        for waste_type_id, quantity in items.items():
            try:
                waste_type = WasteType.objects.get(id=waste_type_id)
                total_amount += waste_type.price_per_item * quantity
            except WasteType.DoesNotExist:
                return custom_response({"error": f"WasteType with id {waste_type_id} not found."}, 
                                       status=status.HTTP_404_NOT_FOUND)

        waste_request = WasteRequest.objects.create(
            user=request.user,
            quantity=sum(items.values()),
            status='Pending',
            pickup_address=request.data.get('pickup_address'),
        )

        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return custom_response({"error": "UserProfile not found."}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')

        if action == 'top_up':
            user_profile.account_balance += total_amount
            user_profile.save()
            return custom_response({
                "message": "Waste request created and amount topped up to your account!",
                "total_amount": total_amount
            }, status=status.HTTP_201_CREATED)

        elif action == 'claim_discount':
            if user_profile.account_balance < total_amount:
                return custom_response({"error": "Insufficient balance to claim discount."}, 
                                       status=status.HTTP_400_BAD_REQUEST)
            user_profile.account_balance -= total_amount
            user_profile.save()
            return custom_response({
                "message": "Waste request created and discount claimed!",
                "total_amount": total_amount
            }, status=status.HTTP_201_CREATED)

        return custom_response({"error": "Action not specified."}, status=status.HTTP_400_BAD_REQUEST)

# Admin Waste Request Views
class WasteRequestListCreateView(generics.ListCreateAPIView):
    queryset = WasteRequest.objects.all()
    serializer_class = WasteRequestSerializer
    permission_classes = [IsAdminUser]

class WasteRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WasteRequest.objects.all()
    serializer_class = WasteRequestSerializer
    permission_classes = [IsAdminUser]

# Educational Content List View
class EducationalContentListView(generics.ListAPIView):
    queryset = EducationalContent.objects.all()
    serializer_class = EducationalContentSerializer
    permission_classes = [permissions.AllowAny]

# Get Available Riders by Waste Type and Distance using Haversine formula
class AvailableRidersListView(generics.ListAPIView):
    serializer_class = RiderSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        waste_type_id = self.request.query_params.get('waste_type')
        user_lat = self.request.query_params.get('lat')
        user_lng = self.request.query_params.get('lng')
        
        if waste_type_id and user_lat and user_lng:
            user_location = (float(user_lat), float(user_lng))
            riders = Rider.objects.filter(
                waste_type__id=waste_type_id,
                availability_status=True
            )
            available_riders = [
                rider for rider in riders
                if geodesic(user_location, (rider.lat, rider.lng)).km <= 5  # 5 km radius
            ]
            return available_riders
        return Rider.objects.none()

# Admin Rider Views
class RiderListCreateView(generics.ListCreateAPIView):
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer
    permission_classes = [IsAdminUser]

class RiderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer
    permission_classes = [IsAdminUser]

# Update Location View
class CorrectViewClassForUpdateLocation(generics.UpdateAPIView):
    serializer_class = UserLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user_location, created = UserLocation.objects.get_or_create(user=self.request.user)
        return user_location

    def update(self, request, *args, **kwargs):
        user_location = self.get_object()
        serializer = self.get_serializer(user_location, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return custom_response(serializer.data, status=status.HTTP_200_OK)
        
        return custom_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Profile View
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

# User Dashboard View
class UserDashboardView(View):
    def get(self, request):
        waste_requests = WasteRequest.objects.filter(user=request.user)
        rewards = Reward.objects.filter(user=request.user)
        environmental_impacts = EnvironmentalImpact.objects.filter(user=request.user)  # Adjust logic as necessary

        return render(request, 'user_dashboard.html', {
            'waste_requests': waste_requests,
            'rewards': rewards,
            'environmental_impacts': environmental_impacts
        })

# User Achievement List View
class UserAchievementListView(generics.ListAPIView):
    serializer_class = UserAchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAchievement.objects.filter(user=self.request.user)