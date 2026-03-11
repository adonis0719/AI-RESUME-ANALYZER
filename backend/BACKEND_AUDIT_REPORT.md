# Backend Audit Report — Resume Analyzer ATS

**Audit Date:** March 2025  
**Scope:** analyzer/, matching/, jobs/, resumes/, accounts/, recruiter/, core/

---

## 1️⃣ Backend Health Score: **72/100**

| Category           | Score  | Notes                                      |
|--------------------|--------|--------------------------------------------|
| Architecture       | 80/100 | Clean separation; minor PDF extraction inconsistency |
| Function Integrity | 85/100 | All critical paths verified                 |
| Skill Extraction   | 75/100 | skills.json aligned; domain mapping fixed   |
| Matching Logic     | 85/100 | Weights corrected; hybrid formula validated |
| Domain Detection   | 90/100 | Full skills.json → domain_weights mapping   |
| AI Semantic        | 80/100 | Model caching added; scoring correct        |
| Pipeline           | 85/100 | End-to-end flow working                     |
| Recruiter Flow     | 75/100 | Safety checks added; temp cleanup added     |
| Performance        | 70/100 | Caching in place; large PDF risk remains    |
| Security           | 60/100 | User scoping fixed; credentials/CORS need env-based config |

---

## 2️⃣ Critical Bugs (Fixed)

| # | Issue | Location | Fix Applied |
|---|-------|----------|-------------|
| 1 | **Domain detection never matched** — `domain_detector` used old category names (`frontend`, `backend`) while `skills.json` uses `frontend_frameworks_libraries`, `backend_frameworks`. Domain weights were never applied. | `domain_detector.py` | Rewrote CATEGORY_TO_DOMAIN to map all skills.json categories to domain_weights keys |
| 2 | **domain_weights.json never used** — `domain_detector` returned `"IT"`, `"DATA_SCIENCE"` but domain_weights uses `IT_SOFTWARE_DEVELOPMENT`, `DATA_SCIENCE_AI`. `_load_domain_weights` always returned None. | `domain_detector.py` | Updated to return domain_weights keys |
| 3 | **Auth bypass in compare view** — `Resume.objects.get(id=resume_id)` did not filter by `user=request.user`; users could compare others' resumes/jobs. | `matching/views.py` | Added `user=request.user` filter |
| 4 | **Unmapped categories inflated score** — `use_weights.get(category, 5)` gave default 5 to all unmapped categories. | `matcher.py` | Changed default to 0 so unmapped categories do not affect score |
| 5 | **WEIGHTS fallback mismatch** — Fallback used `frameworks`, `databases` (not in skills.json). | `matcher.py` | Updated WEIGHTS to use skills.json category names |

---

## 3️⃣ Logical Errors (Fixed)

| # | Issue | Fix |
|---|-------|-----|
| 1 | Hybrid formula uses `max(rule_score, hybrid_score)` — does not penalize perfect rule match, but hybrid can still dominate. | Left as-is per design: `final_score = max(rule_score, hybrid_score)` |
| 2 | Recruiter: empty job_description, no resumes, non-PDF files could cause failures. | Added validation and try/except for PDF extraction |
| 3 | Temp recruiter files never deleted. | Added `os.remove(file_path)` after processing each file |

---

## 4️⃣ Performance Risks

| Risk | Location | Mitigation |
|------|----------|------------|
| SentenceTransformer loaded per call | `ai_matcher.py` | **Fixed** — Model cached in module-level `_model` |
| domain_weights.json loaded per call | `matcher.py` | **Fixed** — Cached in `_DOMAIN_WEIGHTS_CACHE` |
| Large PDF in memory | `pdf_extractor.py`, recruiter | Full PDF loaded; consider streaming for very large files |
| Large skills.json | `skill_extractor.py` | Loaded once at import; acceptable |
| Recruiter bulk — many files | `recruiter/views.py` | Sequential; consider async or batch limits for 50+ resumes |

---

## 5️⃣ Security Risks

| Risk | Severity | Status |
|------|----------|--------|
| Compare view auth bypass | High | **Fixed** |
| send_interview_email — any user can send to arbitrary emails | Medium | Requires business rule: restrict to recruiter-owned candidates |
| CORS_ALLOW_ALL_ORIGINS = True | Medium | Set in settings; move to env-based whitelist for production |
| EMAIL_HOST_PASSWORD in settings | Medium | Use environment variables in production |
| OTP / forgot-password — no rate limiting | Low | Add throttle in production |
| File upload — no extension/size validation | Low | Add validation for production |

---

## 6️⃣ Recommended Refactors

1. **Unify PDF/DOCX extraction** — `resumes/views.py` uses pdfplumber+docx; serializer and recruiter use PyPDF2. Create shared `extract_text(file_path)` that supports PDF and DOCX.
2. **Move credentials to env** — `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, CORS origins.
3. **Rate limiting** — Add throttling for OTP, forgot-password, send_interview_email.
4. **File upload validation** — Validate extension (PDF/DOCX), max size (e.g., 10MB), content-type.
5. **Interview email authorization** — Restrict emails to those from resumes the user has access to.
6. **question_generator** — Extend to support all skills.json categories; many categories get no interview questions today.

---

## Architecture Summary

```
Resume PDF → pdf_extractor → text
                              ↓
                    skill_extractor (skills.json)
                              ↓
                    skill_expander (optional, embeddings)
                              ↓
Job description → skill_extractor → job_skills
                              ↓
                    domain_detector → domain key
                              ↓
                    _load_domain_weights(domain) → category weights
                              ↓
                    calculate_match(resume_skills, job_skills, weights)
                              ↓
                    semantic_similarity(resume_text, job_text)  [optional]
                              ↓
                    final_score = max(rule_score, 0.6*rule + 0.4*ai)
```

---

## Files Modified

- `analyzer/domain_detector.py` — Full category→domain mapping
- `analyzer/ai_matcher.py` — Model caching
- `matching/matcher.py` — WEIGHTS update, domain_weights cache, default weight 0, fallback domain
- `matching/views.py` — User-scoped compare
- `recruiter/views.py` — Safety checks, temp file cleanup, error handling
