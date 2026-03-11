"""
Job Domain Detection - Detects job category from extracted skills.
Maps skills.json categories to domain_weights.json domain keys.
"""

import json
import os

BASE_DIR = os.path.dirname(__file__)
DOMAIN_WEIGHTS_PATH = os.path.join(BASE_DIR, "domain_weights.json")

# Maps skills.json category -> domain_weights key (domain that best fits)
# Built from domain_weights.json structure; domains from that file
CATEGORY_TO_DOMAIN = {
    # IT Software
    "programming_languages": "IT_SOFTWARE_DEVELOPMENT",
    "backend_frameworks": "IT_SOFTWARE_DEVELOPMENT",
    "backend_technologies": "IT_SOFTWARE_DEVELOPMENT",
    "frontend_frameworks_libraries": "IT_SOFTWARE_DEVELOPMENT",
    "frontend_styling_ui": "IT_SOFTWARE_DEVELOPMENT",
    "databases_sql": "IT_SOFTWARE_DEVELOPMENT",
    "databases_nosql": "IT_SOFTWARE_DEVELOPMENT",
    "software_architecture": "IT_SOFTWARE_DEVELOPMENT",
    "design_patterns": "IT_SOFTWARE_DEVELOPMENT",
    "software_development_methodologies": "IT_SOFTWARE_DEVELOPMENT",
    "version_control": "IT_SOFTWARE_DEVELOPMENT",
    "build_tools": "IT_SOFTWARE_DEVELOPMENT",
    "package_managers": "IT_SOFTWARE_DEVELOPMENT",
    "development_tools": "IT_SOFTWARE_DEVELOPMENT",
    "web_servers": "IT_SOFTWARE_DEVELOPMENT",
    "api_development_integration": "IT_SOFTWARE_DEVELOPMENT",
    "testing_frameworks_tools": "IT_SOFTWARE_DEVELOPMENT",
    "software_testing": "IT_SOFTWARE_DEVELOPMENT",
    "qa_management": "IT_SOFTWARE_DEVELOPMENT",
    "system_design_concepts": "ARCHITECTURE_ENGINEERING",
    "object_oriented_concepts": "IT_SOFTWARE_DEVELOPMENT",
    "functional_programming": "IT_SOFTWARE_DEVELOPMENT",
    "data_structures": "IT_SOFTWARE_DEVELOPMENT",
    "algorithms": "IT_SOFTWARE_DEVELOPMENT",
    "content_management_systems": "IT_SOFTWARE_DEVELOPMENT",
    "ecommerce_platforms": "IT_SOFTWARE_DEVELOPMENT",
    "web_components": "IT_SOFTWARE_DEVELOPMENT",
    "progressive_web_apps": "IT_SOFTWARE_DEVELOPMENT",
    "web_apis": "IT_SOFTWARE_DEVELOPMENT",
    "browser_apis": "IT_SOFTWARE_DEVELOPMENT",
    "ide_extensions": "IT_SOFTWARE_DEVELOPMENT",
    "scripting_languages": "IT_SOFTWARE_DEVELOPMENT",
    "shell_environments": "IT_SOFTWARE_DEVELOPMENT",
    "command_line_tools": "IT_SOFTWARE_DEVELOPMENT",
    "agile_ceremonies": "PROJECT_PRODUCT_MANAGEMENT",
    "agile_roles": "PROJECT_PRODUCT_MANAGEMENT",
    "development_paradigms": "IT_SOFTWARE_DEVELOPMENT",
    "development_approaches": "IT_SOFTWARE_DEVELOPMENT",
    # IT Ops / Infra
    "cloud_platforms": "IT_OPS_INFRASTRUCTURE",
    "aws_services": "IT_OPS_INFRASTRUCTURE",
    "azure_services": "IT_OPS_INFRASTRUCTURE",
    "google_cloud_services": "IT_OPS_INFRASTRUCTURE",
    "devops_tools": "IT_OPS_INFRASTRUCTURE",
    "container_orchestration": "IT_OPS_INFRASTRUCTURE",
    "cicd_tools": "IT_OPS_INFRASTRUCTURE",
    "infrastructure_as_code": "IT_OPS_INFRASTRUCTURE",
    "monitoring_observability": "IT_OPS_INFRASTRUCTURE",
    "system_administration": "IT_OPS_INFRASTRUCTURE",
    "network_administration": "IT_OPS_INFRASTRUCTURE",
    "database_administration": "IT_OPS_INFRASTRUCTURE",
    "virtualization_technologies": "IT_OPS_INFRASTRUCTURE",
    "it_service_management": "IT_OPS_INFRASTRUCTURE",
    "operating_systems": "IT_OPS_INFRASTRUCTURE",
    "networking_protocols": "IT_OPS_INFRASTRUCTURE",
    "containerization": "IT_OPS_INFRASTRUCTURE",
    "orchestration": "IT_OPS_INFRASTRUCTURE",
    "service_mesh": "CLOUD_ARCHITECTURE",
    "serverless_computing": "CLOUD_ARCHITECTURE",
    "edge_computing": "CLOUD_ARCHITECTURE",
    "site_reliability_engineering": "IT_OPS_INFRASTRUCTURE",
    # Data Science / AI
    "data_science_machine_learning": "DATA_SCIENCE_AI",
    "machine_learning_platforms": "DATA_SCIENCE_AI",
    "deep_learning_frameworks": "DATA_SCIENCE_AI",
    "computer_vision": "DATA_SCIENCE_AI",
    "natural_language_processing": "DATA_SCIENCE_AI",
    "big_data_technologies": "DATA_SCIENCE_AI",
    "stream_processing": "DATA_SCIENCE_AI",
    "mlops_tools": "DATA_SCIENCE_AI",
    "reinforcement_learning": "DATA_SCIENCE_AI",
    "chatbot_development": "DATA_SCIENCE_AI",
    "voice_technology": "DATA_SCIENCE_AI",
    "augmented_intelligence": "DATA_SCIENCE_AI",
    "generative_ai": "EMERGING_TECHNOLOGIES",
    "llm_technologies": "DATA_SCIENCE_AI",
    "graph_databases": "DATA_SCIENCE_AI",
    "time_series_databases": "DATA_SCIENCE_AI",
    "search_engines": "IT_SOFTWARE_DEVELOPMENT",
    # Data Analytics
    "data_analytics_visualization": "DATA_ANALYTICS_BI",
    "business_intelligence": "DATA_ANALYTICS_BI",
    "data_engineering": "DATA_ANALYTICS_BI",
    "data_warehousing": "DATA_ANALYTICS_BI",
    "data_lake": "DATA_ANALYTICS_BI",
    "statistical_analysis": "DATA_ANALYTICS_BI",
    "data_visualization": "DATA_ANALYTICS_BI",
    # Security
    "security_cybersecurity": "CYBERSECURITY",
    "security_tools_frameworks": "CYBERSECURITY",
    "application_security": "CYBERSECURITY",
    "cloud_security": "CYBERSECURITY",
    "network_security": "CYBERSECURITY",
    "identity_access_management": "CYBERSECURITY",
    "compliance_standards": "CYBERSECURITY",
    "security_compliance": "CYBERSECURITY",
    # Mobile
    "mobile_development": "MOBILE_DEVELOPMENT",
    "cross_platform_development": "MOBILE_DEVELOPMENT",
    "android_development": "MOBILE_DEVELOPMENT",
    "ios_development": "MOBILE_DEVELOPMENT",
    # Emerging
    "blockchain_technologies": "EMERGING_TECHNOLOGIES",
    "internet_of_things": "EMERGING_TECHNOLOGIES",
    "embedded_systems": "EMERGING_TECHNOLOGIES",
    "robotics": "EMERGING_TECHNOLOGIES",
    "ar_vr_development": "EMERGING_TECHNOLOGIES",
    "quantum_computing": "EMERGING_TECHNOLOGIES",
    "game_development": "EMERGING_TECHNOLOGIES",
    # Project / Product
    "project_management_methodologies": "PROJECT_PRODUCT_MANAGEMENT",
    "project_management_tools": "PROJECT_PRODUCT_MANAGEMENT",
    "product_management": "PROJECT_PRODUCT_MANAGEMENT",
    # UX/UI
    "ux_ui_design": "UX_UI_DESIGN",
    "design_tools": "UX_UI_DESIGN",
    # Enterprise
    "customer_relationship_management": "ENTERPRISE_SYSTEMS",
    "enterprise_resource_planning": "ENTERPRISE_SYSTEMS",
    "low_code_no_code": "ENTERPRISE_SYSTEMS",
    # Professional
    "communication_skills": "PROFESSIONAL_SKILLS",
    "leadership_skills": "PROFESSIONAL_SKILLS",
    "problem_solving": "PROFESSIONAL_SKILLS",
    "analytical_skills": "PROFESSIONAL_SKILLS",
    "decision_making": "PROFESSIONAL_SKILLS",
    "time_management": "PROFESSIONAL_SKILLS",
    # Other domains from domain_weights
    "healthcare_medical": "HEALTHCARE_MEDICAL",
    "pharmaceutical": "HEALTHCARE_MEDICAL",
    "biotechnology": "HEALTHCARE_MEDICAL",
    "mechanical_engineering": "ENGINEERING_TRADITIONAL",
    "electrical_engineering": "ENGINEERING_TRADITIONAL",
    "civil_engineering": "ENGINEERING_TRADITIONAL",
    "architecture": "CONSTRUCTION_ARCHITECTURE",
    "construction_management": "CONSTRUCTION_ARCHITECTURE",
    "agriculture": "AGRIBUSINESS",
    "culinary_arts": "FOOD_CULINARY",
    "hospitality_management": "HOSPITALITY_TOURISM",
    "supply_chain_management": "SUPPLY_CHAIN_LOGISTICS",
    "logistics_management": "SUPPLY_CHAIN_LOGISTICS",
    "finance": "BUSINESS_FINANCE",
    "accounting": "BUSINESS_FINANCE",
    "marketing": "MARKETING_SALES",
    "sales": "MARKETING_SALES",
    "human_resources": "HUMAN_RESOURCES",
    "law": "LEGAL_COMPLIANCE",
    "education": "EDUCATION_TRAINING",
    "graphic_design": "CREATIVE_ARTS",
    "media_journalism": "MEDIA_COMMUNICATIONS",
    "content_writing": "MEDIA_COMMUNICATIONS",
}

DEFAULT_DOMAIN = "IT_SOFTWARE_DEVELOPMENT"


def detect_domain(job_skills):
    """
    Detect job domain from extracted job skills.
    Returns a domain key that exists in domain_weights.json.

    Args:
        job_skills: dict of category -> list of skills (from skill extractor)

    Returns:
        str: Domain key e.g. "IT_SOFTWARE_DEVELOPMENT", "DATA_SCIENCE_AI"
    """
    if not job_skills or not isinstance(job_skills, dict):
        return DEFAULT_DOMAIN

    domain_scores = {}

    for category, skills in job_skills.items():
        domain = CATEGORY_TO_DOMAIN.get(category)
        if not domain:
            continue

        count = len(skills) if isinstance(skills, (list, set)) else 0
        domain_scores[domain] = domain_scores.get(domain, 0) + count

    if not domain_scores:
        return DEFAULT_DOMAIN

    return max(domain_scores, key=domain_scores.get)
