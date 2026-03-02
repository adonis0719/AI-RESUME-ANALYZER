import spacy
import re
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = {

# ================= PROGRAMMING =================
"programming_languages": [
    "python","java","c","c++","c#","javascript","typescript",
    "go","golang","rust","kotlin","swift","php","ruby","scala",
    "r","matlab","bash","shell scripting","powershell",
    "groovy","dart","objective-c","haskell","perl",
    "assembly","vba","solidity","fortran","cobol"
],

# ================= FRONTEND =================
"frontend": [
    "html","html5","css","css3","sass","scss",
    "bootstrap","tailwind","material ui","mui",
    "react","react.js","next.js","angular","vue",
    "nuxt","svelte","redux","zustand","context api",
    "jquery","webpack","vite","babel",
    "responsive design","ui/ux","figma","adobe xd"
],

# ================= BACKEND =================
"backend": [
    "node.js","nodejs","express","nestjs",
    "django","flask","fastapi",
    "spring","spring boot","hibernate",
    "laravel","codeigniter",
    "asp.net",".net core","entity framework",
    "graphql","rest api","soap","microservices",
    "jwt","oauth","authentication","authorization"
],

# ================= DATABASES =================
"databases": [
    "mysql","postgresql","sql server","t-sql",
    "mongodb","redis","oracle","sqlite",
    "cassandra","dynamodb","firebase",
    "mariadb","elasticsearch","neo4j",
    "snowflake","bigquery"
],

# ================= CLOUD =================
"cloud": [
    "aws","amazon web services","ec2","s3","lambda",
    "azure","microsoft azure","azure devops",
    "gcp","google cloud","google cloud platform",
    "heroku","digitalocean","cloudflare",
    "cloud computing","serverless"
],

# ================= DEVOPS =================
"devops": [
    "docker","kubernetes","jenkins",
    "terraform","ansible","chef","puppet",
    "ci/cd","github actions","gitlab ci",
    "travis ci","bitbucket pipelines",
    "prometheus","grafana",
    "nginx","apache","linux administration",
    "shell scripting"
],

# ================= DATA SCIENCE / AI =================
"data_science_ai": [
    "machine learning","deep learning",
    "artificial intelligence","ai",
    "nlp","computer vision",
    "pandas","numpy","scipy",
    "matplotlib","seaborn",
    "tensorflow","keras","pytorch",
    "scikit-learn","xgboost",
    "opencv","langchain","llm",
    "data analysis","data mining",
    "feature engineering","model deployment",
    "statistics","probability"
],

# ================= DATA ANALYTICS / BI =================
"data_analytics_bi": [
    "power bi","tableau","looker",
    "excel","advanced excel","pivot tables",
    "vlookup","xlookup","power query",
    "power pivot","data visualization",
    "dashboard creation","business intelligence",
    "reporting","etl","data warehousing"
],

# ================= ERP / CRM =================
"erp_crm": [
    "sap","sap hana","sap fico",
    "oracle erp","netsuite",
    "salesforce","crm","hubspot",
    "zoho crm","dynamics 365"
],

# ================= ACCOUNTING / FINANCE =================
"accounting_finance": [
    "tally","quickbooks","bookkeeping",
    "accounts payable","accounts receivable",
    "gst","taxation","financial reporting",
    "balance sheet","profit and loss",
    "bank reconciliation","payroll"
],

# ================= MOBILE =================
"mobile": [
    "android","android studio",
    "kotlin","java android",
    "ios","swift","swiftui",
    "react native","flutter","dart",
    "xamarin","ionic"
],

# ================= TESTING =================
"testing": [
    "unit testing","integration testing",
    "pytest","junit","selenium",
    "cypress","jest","mocha",
    "postman","manual testing",
    "automation testing","testng"
],

# ================= VERSION CONTROL =================
"version_control": [
    "git","github","gitlab","bitbucket","svn"
],

# ================= SECURITY =================
"security": [
    "cybersecurity","penetration testing",
    "ethical hacking","owasp",
    "jwt","oauth","encryption",
    "network security","firewall",
    "vulnerability assessment"
],

# ================= SOFTWARE CONCEPTS =================
"software_concepts": [
    "oop","object oriented programming",
    "data structures","algorithms",
    "design patterns","system design",
    "agile","scrum","kanban",
    "solid principles",
    "mvc architecture",
    "clean architecture",
    "restful services"
],

# ================= SOFT SKILLS =================
"soft_skills": [
    "communication","teamwork","leadership",
    "problem solving","critical thinking",
    "time management","adaptability",
    "analytical skills","decision making",
    "project management"
]
}

import re

def normalize_text(text):
    text = text.lower()

    # Standardize separators
    text = re.sub(r"[|•·]", " ", text)
    text = re.sub(r"[()/]", " ", text)

    replacements = {
        r"\bnodejs\b": "node.js",
        r"\bnode js\b": "node.js",
        r"\bci cd\b": "ci/cd",
        r"\bci-cd\b": "ci/cd",
        r"\bpostgres\b": "postgresql",
        r"\bjs\b": "javascript",
        r"\bts\b": "typescript",
        r"\bpy\b": "python",
        r"\breactjs\b": "react",
        r"\bnextjs\b": "next.js",
        r"\bvuejs\b": "vue",
        r"\basp net\b": "asp.net",
        r"\bdot net\b": ".net",
        r"\bgcp\b": "google cloud platform",
        r"\baws cloud\b": "aws",
        r"\bml\b": "machine learning",
        r"\bdl\b": "deep learning",
        r"\bnlp\b": "natural language processing",
        r"\bai\b": "artificial intelligence",
        r"\brestful\b": "rest api",
        r"\brest api\b": "rest api",
        r"\boops\b": "oop",
        r"\bobject oriented programming\b": "oop"
    }

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

def extract_skills(text):
    text_lower = normalize_text(text)
    doc = nlp(text_lower)

    categorized_skills = {}

    matcher = PhraseMatcher(nlp.vocab)

    for category, skills in SKILLS_DB.items():
        patterns = [nlp.make_doc(skill) for skill in skills]
        matcher.add(category, patterns)

    matches = matcher(doc)

    found_skills = {}

    for match_id, start, end in matches:
        category = nlp.vocab.strings[match_id]
        skill = doc[start:end].text

        if category not in found_skills:
            found_skills[category] = set()

        found_skills[category].add(skill)

    for category, skills in found_skills.items():
        categorized_skills[category] = sorted(list(skills))

    return categorized_skills

