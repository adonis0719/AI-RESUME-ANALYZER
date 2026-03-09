"""
Job Domain Detection - Detects job category from extracted skills.
"""

# Map skill categories from skills.json to domain names
CATEGORY_TO_DOMAIN = {
    # IT
    "programming_languages": "IT",
    "frontend": "IT",
    "backend": "IT",
    "databases": "IT",
    "devops": "IT",
    "cloud": "IT",
    "mobile": "IT",
    "testing": "IT",
    "version_control": "IT",
    "security": "IT",
    "software_concepts": "IT",
    # DATA_SCIENCE
    "data_science_ai": "DATA_SCIENCE",
    "data_analytics_bi": "DATA_SCIENCE",
    # ACCOUNTING
    "accounting_finance": "ACCOUNTING",
    "erp_crm": "ACCOUNTING",
    # FINANCE
    "finance": "FINANCE",
    "banking": "FINANCE",
    "insurance": "FINANCE",
    # MARKETING
    "marketing": "MARKETING",
    "sales": "MARKETING",
    "creative_design": "MARKETING",
    # CUSTOMER_SUPPORT
    "customer_service": "CUSTOMER_SUPPORT",
    "retail": "CUSTOMER_SUPPORT",
    # MANAGEMENT
    "human_resources": "MANAGEMENT",
    "soft_skills": "MANAGEMENT",
    "procurement": "MANAGEMENT",
    # Other domains mapped for completeness
    "healthcare": "HEALTHCARE",
    "engineering": "ENGINEERING",
    "logistics_supply_chain": "LOGISTICS",
    "legal": "LAW",
    "education": "EDUCATION",
}

# Fallback domain when no strong signal
DEFAULT_DOMAIN = "IT"


def detect_domain(job_skills):
    """
    Detect job domain from extracted job skills.
    Counts skills per domain and returns the domain with highest score.

    Args:
        job_skills: dict of category -> list of skills (from skill extractor)

    Returns:
        str: Domain name e.g. "IT", "DATA_SCIENCE", "ACCOUNTING", "MARKETING"
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
