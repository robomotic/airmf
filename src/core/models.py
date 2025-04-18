from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class System(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    last_reviewed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} v{self.version}"

    class Meta:
        verbose_name_plural = "systems"


class Capability(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=100)
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='capabilities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

    class Meta:
        verbose_name_plural = "capabilities"


class UseCase(models.Model):
    RISK_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('REVIEW', 'Under Review'),
        ('ACTIVE', 'Active'),
        ('SUSPENDED', 'Suspended'),
        ('RETIRED', 'Retired'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    business_objective = models.TextField()
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    compliance_requirements = models.TextField()
    data_sensitivity = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    capabilities = models.ManyToManyField(Capability, related_name='use_cases')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    contact_info = models.TextField()
    use_cases = models.ManyToManyField(UseCase, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.role})"


class Stakeholder(models.Model):
    STAKEHOLDER_TYPES = [
        ('INTERNAL', 'Internal'),
        ('EXTERNAL', 'External'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=STAKEHOLDER_TYPES)
    interest_or_concern = models.TextField()
    impact_description = models.TextField()
    contact_info = models.TextField()
    use_cases = models.ManyToManyField(UseCase, related_name='stakeholders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class ModelCard(models.Model):
    model_name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    description = models.TextField()
    intended_use = models.TextField()
    limitations = models.TextField()
    performance_metrics = models.TextField()
    ethical_considerations = models.TextField()
    training_data_summary = models.TextField()
    evaluation_data_summary = models.TextField()
    owner = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='model_cards')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_name} v{self.version}"


class AIRiskAssessment(models.Model):
    RISK_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('OBSOLETE', 'Obsolete'),
    ]

    ENTITY_TYPES = [
        ('SYSTEM', 'System'),
        ('CAPABILITY', 'Capability'),
        ('USECASE', 'Use Case'),
        ('MODELCARD', 'Model Card'),
    ]

    related_entity_type = models.CharField(max_length=20, choices=ENTITY_TYPES)
    related_entity_id = models.PositiveIntegerField()
    risk_type = models.CharField(max_length=100)
    risk_description = models.TextField()
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    likelihood = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    impact = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    mitigation_measures = models.TextField()
    risk_owner = models.CharField(max_length=255)
    review_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    references = models.TextField(help_text="e.g., ISO/IEC 23894 references")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.risk_type} Risk - {self.get_risk_level_display()}"

    class Meta:
        verbose_name_plural = "AI risk assessments"
