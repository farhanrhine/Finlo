# Security Review: Add New Expenses Feature (Step 7)

## Summary
The add-new-expenses feature demonstrates **strong foundational security practices** with parameterized queries and authentication guards. However, there are important gaps in CSRF protection and session security configuration that should be addressed.

---

## Strengths ✅

1. **SQL Injection Prevention**: Uses parameterized queries with `?` placeholders throughout. The `create_expense()` function properly binds all user inputs, preventing SQL injection attacks.

2. **Authentication Guard**: Both GET and POST routes check `session.get('user_id')` and redirect to login if missing. Unauthorized users cannot access the form or submit expenses.

3. **Input Validation (Defense-in-Depth)**:
   - Amount: Converted to float with try/catch, validated as positive number
   - Category: Whitelist validation against `ALLOWED_CATEGORIES`
   - Date: Validated against `%Y-%m-%d` format
   - All inputs `.strip()` to prevent whitespace bypasses

4. **XSS Protection**: Jinja2 templates auto-escape by default. Form values like `{{ amount }}` are safely escaped, preventing script injection.

5. **Error Handling**: Proper use of `ValueError` exceptions with user-friendly messages; no raw database errors exposed.

---

## Risks & Recommendations ⚠️

### 1. **CSRF (Cross-Site Request Forgery)** — **HIGH PRIORITY**
**Issue**: Form lacks CSRF token. Attacker can forge POST requests on behalf of logged-in users.
```html
<!-- Add to form: -->
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```
**Action**: Enable Flask-WTF or implement manual CSRF token validation.

### 2. **Hardcoded Session Secret Key** — **HIGH PRIORITY**
```python
app.secret_key = 'your-secret-key-change-in-production'  # ❌ Insecure
```
**Issue**: Hardcoded secret allows session tampering if code is exposed.
**Action**: Load from environment variable:
```python
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-only')
```

### 3. **Rate Limiting** — **MEDIUM**
No rate limiting on POST /expenses/add. Attackers could spam expenses.
**Action**: Implement Flask-Limiter or check request frequency per user.

### 4. **Date Validation** — **MINOR**
Date format validated but not bounds-checked. Users can enter year 9999 or 1900.
**Action**: Validate `date >= '2000-01-01' and date <= today`.

---

## Verdict
**Safe for production with CSRF and secret key fixes.** The feature correctly prevents SQL injection and enforces authentication. Priority: implement CSRF tokens and environment-based secret key immediately.

