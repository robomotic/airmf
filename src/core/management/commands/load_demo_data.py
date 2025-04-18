from django.core.management.base import BaseCommand
from core.models import System, Capability, UseCase, User, Stakeholder
from django.db import transaction

class Command(BaseCommand):
    help = 'Loads demo data for AI systems and use cases based on the landscape diagram'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Creating demo data...')
        
        # Create main HR AI System
        hr_system = System.objects.create(
            name="HR AI Assistant",
            owner="HR Department",
            vendor="AI Solutions Inc.",
            description="AI system for HR processes including recruitment, career planning, and talent management",
            status="ACTIVE",
            version="1.0"
        )

        # Create capabilities based on the diagram
        capabilities = {
            'recruitment': Capability.objects.create(
                name="Recruitment and Talent Acquisition",
                description="AI capabilities for external and internal recruitment processes",
                type="RECRUITMENT",
                system=hr_system
            ),
            'career': Capability.objects.create(
                name="Career Development",
                description="AI capabilities for career guidance and succession planning",
                type="CAREER",
                system=hr_system
            ),
            'assessment': Capability.objects.create(
                name="Assessment and Analysis",
                description="AI capabilities for resume analysis and job fit prediction",
                type="ASSESSMENT",
                system=hr_system
            )
        }

        # Create stakeholders from the diagram (T-series)
        stakeholders = {
            'managers': Stakeholder.objects.create(
                name="Immediate Managers",
                type="INTERNAL",
                interest_or_concern="Direct oversight of team members and hiring decisions",
                impact_description="High impact on team composition and performance",
                contact_info="managers@company.com"
            ),
            'hr_partners': Stakeholder.objects.create(
                name="HR Business Partners",
                type="INTERNAL",
                interest_or_concern="Strategic HR planning and implementation",
                impact_description="Critical for HR process alignment",
                contact_info="hr.partners@company.com"
            ),
            'learning': Stakeholder.objects.create(
                name="Learning & Development Team",
                type="INTERNAL",
                interest_or_concern="Employee development and training programs",
                impact_description="Responsible for upskilling initiatives",
                contact_info="l&d@company.com"
            )
        }

        # Create use cases from the diagram (U-series)
        use_cases = [
            # External Recruitment (U-01)
            UseCase.objects.create(
                name="External Candidate Screening",
                description="AI-powered screening of external job candidates",
                business_objective="Improve recruitment efficiency and quality of hire",
                risk_level="MEDIUM",
                compliance_requirements="GDPR, Equal Employment Opportunity regulations",
                data_sensitivity="HIGH",
                status="ACTIVE"
            ),
            # Internal Mobility (U-02)
            UseCase.objects.create(
                name="Internal Talent Mobility",
                description="AI-driven internal talent matching and mobility",
                business_objective="Optimize internal talent allocation",
                risk_level="LOW",
                compliance_requirements="Internal HR policies",
                data_sensitivity="MEDIUM",
                status="ACTIVE"
            ),
            # Graduate Recruitment (U-03)
            UseCase.objects.create(
                name="Graduate Recruitment",
                description="AI-assisted graduate recruitment and assessment",
                business_objective="Identify and attract top graduate talent",
                risk_level="MEDIUM",
                compliance_requirements="Educational data protection regulations",
                data_sensitivity="MEDIUM",
                status="ACTIVE"
            ),
            # Executive Succession (U-04)
            UseCase.objects.create(
                name="Executive Succession Planning",
                description="AI-powered executive succession planning and talent pipeline",
                business_objective="Ensure leadership continuity",
                risk_level="HIGH",
                compliance_requirements="Corporate governance requirements",
                data_sensitivity="HIGH",
                status="ACTIVE"
            ),
            # Career Guidance (U-05)
            UseCase.objects.create(
                name="Career Guidance for Early-Career Employees",
                description="AI-driven career path recommendations",
                business_objective="Improve employee retention and development",
                risk_level="LOW",
                compliance_requirements="Employee data protection policies",
                data_sensitivity="MEDIUM",
                status="ACTIVE"
            ),
            # Job Descriptions (U-06)
            UseCase.objects.create(
                name="Optimizing Job Descriptions",
                description="AI-assisted job description creation and optimization",
                business_objective="Attract diverse talent pool",
                risk_level="MEDIUM",
                compliance_requirements="Equal opportunity guidelines",
                data_sensitivity="LOW",
                status="ACTIVE"
            ),
            # Candidate Evaluation (U-07)
            UseCase.objects.create(
                name="Combined Internal/External Candidate Evaluation",
                description="Unified AI evaluation framework for all candidates",
                business_objective="Ensure fair comparison of all candidates",
                risk_level="HIGH",
                compliance_requirements="Equal opportunity and internal fairness policies",
                data_sensitivity="HIGH",
                status="ACTIVE"
            )
        ]

        # Link use cases with capabilities
        for use_case in use_cases:
            if "recruitment" in use_case.name.lower():
                use_case.capabilities.add(capabilities['recruitment'])
            if "career" in use_case.name.lower():
                use_case.capabilities.add(capabilities['career'])
            if "evaluation" in use_case.name.lower() or "screening" in use_case.name.lower():
                use_case.capabilities.add(capabilities['assessment'])
            
            # Link stakeholders to use cases
            use_case.stakeholders.add(*stakeholders.values())

        # Create demo users
        users = [
            User.objects.create(
                name="Jane Smith",
                role="HR Manager",
                department="Human Resources",
                contact_info="jane.smith@company.com"
            ),
            User.objects.create(
                name="John Doe",
                role="Hiring Manager",
                department="Engineering",
                contact_info="john.doe@company.com"
            )
        ]

        # Link users to use cases
        for user in users:
            user.use_cases.add(*use_cases)

        self.stdout.write(self.style.SUCCESS('Successfully created demo data'))