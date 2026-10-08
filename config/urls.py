"""
Root URL Configuration for FoodFlow.
"""

from django.contrib import admin
from django.urls import path, include
from accounts.views import home_view

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Public / Home
    path('', home_view, name='home'),

    # Accounts App (Auth, Profiles, Dashboards)
    path('', include('accounts.urls')),

    # Locations App
    path('locations/', include('locations.urls')),

    # Listings App (Donor listings & Recipient browsing)
    path('', include('listings.urls')),

    # Claims App (Claiming food & Pickup verification)
    path('', include('claims.urls')),

    # Notifications App
    path('notifications/', include('notifications.urls')),
]
