"""
URL configuration for aims project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from core.views import DashboardView, SystemDetailView, add_risk_assessment, SystemMapView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", DashboardView.as_view(), name="dashboard"),
    path("system/<int:pk>/", SystemDetailView.as_view(), name="system_detail"),
    path("system/<int:system_id>/add-risk-assessment/", add_risk_assessment, name="add_risk_assessment"),
    path("system-map/", SystemMapView.as_view(), name="system_map"),
]
