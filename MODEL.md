# AI Management System (AIMS) – Data Model & Use Case Skeleton

## Core Entities

### 1. System
- **Fields:** id, name, owner, vendor, description, status, version, last_reviewed
- **Relationships:** Has many Capabilities, supports many Use Cases

### 2. Capability
- **Fields:** id, name, description, type (e.g., NLP, vision, recommendation), associated_system_id
- **Relationships:** Belongs to System, supports many Use Cases

### 3. Use Case
- **Fields:** id, name, description, business_objective, risk_level, compliance_requirements, data_sensitivity, status
- **Relationships:** Uses many Capabilities, has many Users, affects many Stakeholders

### 4. User
- **Fields:** id, name, role, department, contact_info
- **Relationships:** Engages with Use Cases

### 5. Stakeholder
- **Fields:** id, name, type (internal/external), interest_or_concern, impact_description, contact_info
- **Relationships:** Impacted by Use Cases

### 6. Model Card
- **Fields:** id, model_name, version, description, intended_use, limitations, performance_metrics, ethical_considerations, training_data_summary, evaluation_data_summary, owner, last_updated, related_system_id
- **Relationships:** Linked to a System (and possibly to Capabilities or Use Cases

**Purpose:**  
Model Cards provide a standardized way to document and communicate key details about each AI model in your inventory, supporting governance, risk management, and compliance.

### 7. AI Risk Assessment
- **Fields:** id, related_entity_type (System/Capability/UseCase/ModelCard), related_entity_id, risk_type, risk_description, risk_level, likelihood, impact, mitigation_measures, risk_owner, review_date, status, references (e.g., ISO/IEC 23894)
- **Relationships:** Linked to Systems, Capabilities, Use Cases, or Model Cards

**Purpose:**  
To systematically document, assess, and manage AI-related risks in accordance with ISO/IEC 23894, supporting responsible AI governance and compliance.

## Example Relationships
- A System provides multiple Capabilities.
- A Capability can be used in multiple Use Cases.
- A Use Case involves multiple Users and affects multiple Stakeholders.

## Key Use Cases

1. **Inventory Management**
   - Add, update, and review Systems, Capabilities, Use Cases, Users, and Stakeholders.
   - Maintain version history and audit trails for changes.

2. **Stakeholder Mapping**
   - Identify and document all stakeholders for each use case, including their interests and potential impacts.

3. **Risk & Compliance Tracking**
   - Assign risk levels and compliance requirements to use cases.
   - Link risk assessments to specific systems and capabilities.

4. **Operational Oversight**
   - Track ownership and review cycles for systems and use cases.
   - Document operational processes and escalation paths.

5. **Relationship Mapping**
   - Visualize and query relationships between systems, capabilities, use cases, users, and stakeholders.
