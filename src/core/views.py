from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from .models import System, UseCase, Capability, Stakeholder, AIRiskAssessment, User
from django.contrib import messages
import json

class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get systems data
        context['systems'] = System.objects.all()
        
        # Get use cases with related data
        context['use_cases'] = UseCase.objects.prefetch_related('capabilities', 'stakeholders').all()
        
        # Add choices for filters
        context['risk_level_choices'] = UseCase.RISK_LEVELS
        context['status_choices'] = UseCase.STATUS_CHOICES
        
        # Calculate risk level distribution
        risk_distribution = UseCase.objects.values('risk_level').annotate(count=Count('id'))
        risk_levels = []
        risk_counts = []
        for item in risk_distribution:
            risk_levels.append(item['risk_level'])
            risk_counts.append(item['count'])
        context['risk_levels'] = json.dumps(risk_levels)
        context['risk_counts'] = json.dumps(risk_counts)
        
        # Calculate capabilities distribution
        capabilities = Capability.objects.annotate(use_case_count=Count('use_cases'))
        capability_names = []
        capability_counts = []
        for cap in capabilities:
            capability_names.append(cap.name)
            capability_counts.append(cap.use_case_count)
        context['capability_names'] = json.dumps(capability_names)
        context['capability_counts'] = json.dumps(capability_counts)

        # Status distribution
        status_dist = UseCase.objects.values('status').annotate(count=Count('id'))
        context['status_distribution'] = json.dumps(list(status_dist))

        # Stakeholder involvement
        stakeholder_dist = Stakeholder.objects.annotate(
            use_case_count=Count('use_cases'),
            high_risk_count=Count('use_cases', filter=Q(use_cases__risk_level='HIGH'))
        ).values('name', 'type', 'use_case_count', 'high_risk_count')
        context['stakeholder_distribution'] = json.dumps(list(stakeholder_dist))

        # Risk Assessment Overview
        context['risk_assessments'] = AIRiskAssessment.objects.values('risk_level').annotate(count=Count('id'))
        context['total_high_risks'] = AIRiskAssessment.objects.filter(risk_level='HIGH').count()
        context['total_use_cases'] = UseCase.objects.count()
        context['total_capabilities'] = Capability.objects.count()
        context['total_stakeholders'] = Stakeholder.objects.count()
        
        return context

class SystemDetailView(DetailView):
    model = System
    template_name = 'core/system_detail.html'
    context_object_name = 'system'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        system = self.get_object()
        
        # Get capabilities and their use cases for this system
        context['capabilities'] = system.capabilities.prefetch_related('use_cases').all()
        
        # Get risk assessments for this system
        risk_assessments = AIRiskAssessment.objects.filter(
            related_entity_type='SYSTEM',
            related_entity_id=system.id
        )
        context['risk_assessments'] = risk_assessments
        
        # Calculate risk assessment counts
        context['high_risk_count'] = risk_assessments.filter(risk_level='HIGH').count()
        context['medium_risk_count'] = risk_assessments.filter(risk_level='MEDIUM').count()
        context['low_risk_count'] = risk_assessments.filter(risk_level='LOW').count()
        
        # Add risk level choices for the form
        context['risk_levels'] = AIRiskAssessment.RISK_LEVELS
        
        return context

def add_risk_assessment(request, system_id):
    if request.method == 'POST':
        try:
            # Create new risk assessment
            assessment = AIRiskAssessment.objects.create(
                related_entity_type=request.POST['related_entity_type'],
                related_entity_id=request.POST['related_entity_id'],
                risk_type=request.POST['risk_type'],
                risk_description=request.POST['risk_description'],
                risk_level=request.POST['risk_level'],
                likelihood=request.POST['likelihood'],
                impact=request.POST['impact'],
                mitigation_measures=request.POST['mitigation_measures'],
                risk_owner=request.POST['risk_owner'],
                review_date=request.POST['review_date'],
                references=request.POST.get('references', ''),
            )
            messages.success(request, 'Risk assessment added successfully.')
        except Exception as e:
            messages.error(request, f'Error adding risk assessment: {str(e)}')
    
    return redirect('system_detail', pk=system_id)

class SystemMapView(TemplateView):
    template_name = 'core/system_map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Prepare network data structure for Cytoscape.js
        nodes = []
        edges = []
        
        # Add Systems
        systems = System.objects.all()
        print(f"Found {systems.count()} systems")  # Debug output
        for system in systems:
            nodes.append({
                'data': {
                    'id': f'S{system.id}',
                    'label': system.name,
                    'type': 'system',
                    'color': '#212529',
                    'details': {
                        'description': system.description,
                        'owner': system.owner,
                        'vendor': system.vendor,
                        'version': system.version,
                        'status': system.status
                    }
                }
            })
        
        # Add Capabilities and connect to Systems
        capabilities = Capability.objects.all()
        print(f"Found {capabilities.count()} capabilities")  # Debug output
        for cap in capabilities:
            nodes.append({
                'data': {
                    'id': f'C{cap.id}',
                    'label': cap.name,
                    'type': 'capability',
                    'color': '#ff7043',
                    'details': {
                        'description': cap.description,
                        'type': cap.type
                    }
                }
            })
            edges.append({
                'data': {
                    'source': f'S{cap.system.id}',
                    'target': f'C{cap.id}'
                }
            })
        
        # Add Use Cases and connect to Capabilities
        use_cases = UseCase.objects.prefetch_related('capabilities', 'stakeholders', 'users').all()
        print(f"Found {use_cases.count()} use cases")  # Debug output
        for uc in use_cases:
            nodes.append({
                'data': {
                    'id': f'U{uc.id}',
                    'label': uc.name,
                    'type': 'use_case',
                    'color': '#66bb6a',
                    'details': {
                        'description': uc.description,
                        'business_objective': uc.business_objective,
                        'risk_level': uc.risk_level,
                        'status': uc.status
                    }
                }
            })
            # Connect to capabilities
            for cap in uc.capabilities.all():
                edges.append({
                    'data': {
                        'source': f'C{cap.id}',
                        'target': f'U{uc.id}'
                    }
                })
        
        # Add Stakeholders and connect to Use Cases
        stakeholders = Stakeholder.objects.all()
        print(f"Found {stakeholders.count()} stakeholders")  # Debug output
        for sh in stakeholders:
            nodes.append({
                'data': {
                    'id': f'T{sh.id}',
                    'label': sh.name,
                    'type': 'stakeholder',
                    'color': '#ab47bc',
                    'details': {
                        'type': sh.type,
                        'interest': sh.interest_or_concern,
                        'impact': sh.impact_description
                    }
                }
            })
            # Connect to use cases
            for uc in sh.use_cases.all():
                edges.append({
                    'data': {
                        'source': f'U{uc.id}',
                        'target': f'T{sh.id}'
                    }
                })
        
        # Add Users and connect to Use Cases
        users = User.objects.all()
        print(f"Found {users.count()} users")  # Debug output
        for user in users:
            nodes.append({
                'data': {
                    'id': f'P{user.id}',
                    'label': user.name,
                    'type': 'user',
                    'color': '#42a5f5',
                    'details': {
                        'role': user.role,
                        'department': user.department
                    }
                }
            })
            # Connect to use cases
            for uc in user.use_cases.all():
                edges.append({
                    'data': {
                        'source': f'U{uc.id}',
                        'target': f'P{user.id}'
                    }
                })
        
        # Add network data to context
        network_data = {
            'nodes': nodes,
            'edges': edges
        }
        
        print("Network data:", json.dumps(network_data, indent=2))  # Debug output
        context['network_data'] = json.dumps(network_data)
        
        return context
