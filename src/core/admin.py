from django.contrib import admin
from .models import System, Capability, UseCase, User, Stakeholder, ModelCard, AIRiskAssessment

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'vendor', 'status', 'version', 'last_reviewed')
    search_fields = ('name', 'owner', 'vendor')
    list_filter = ('status',)

@admin.register(Capability)
class CapabilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'system')
    search_fields = ('name', 'type')
    list_filter = ('type', 'system')

@admin.register(UseCase)
class UseCaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'risk_level', 'status')
    search_fields = ('name', 'business_objective')
    list_filter = ('risk_level', 'status')
    filter_horizontal = ('capabilities',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'department')
    search_fields = ('name', 'role', 'department')
    list_filter = ('role', 'department')
    filter_horizontal = ('use_cases',)

@admin.register(Stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    search_fields = ('name', 'interest_or_concern')
    list_filter = ('type',)
    filter_horizontal = ('use_cases',)

@admin.register(ModelCard)
class ModelCardAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'version', 'owner', 'last_updated')
    search_fields = ('model_name', 'owner')
    list_filter = ('last_updated',)

@admin.register(AIRiskAssessment)
class AIRiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ('risk_type', 'related_entity_type', 'risk_level', 'risk_owner', 'status')
    search_fields = ('risk_type', 'risk_description', 'risk_owner')
    list_filter = ('risk_level', 'status', 'related_entity_type')
