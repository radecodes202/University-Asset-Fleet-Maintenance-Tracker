# Team Roles and Responsibilities
## University Asset & Fleet Maintenance Tracker - Project 10

Based on the Final Requirements PDF, this document outlines the team composition, individual responsibilities, and deliverables for the 5-member development group.

---

## Team Composition & Role Distribution

Each group is composed of five members. Every member must act as the primary owner of their domain during development and must present their specific module during the live defense.

---

### Member 1: Lead Cloud & DevOps Engineer

#### Development Responsibilities:
- Manages the **PaaS deployment** (e.g., Render or Railway)
- Configures **environment variables** securely
- Provisions the **PostgreSQL database**
- Integrates **Cloudinary** for media storage

#### Presentation Responsibilities:
- **Opens the defense**
- Demonstrates the **live application**
- Explains the **cloud architecture**
- Proves the **secure handling of environment variables**

#### Grading Criteria (20% - Cloud Architecture & Deployment):
| Level | Requirements |
|-------|-------------|
| Excellent (90-100%) | Live URL is fast and flawless. Cloudinary handles all media. Environment variables are perfectly isolated. |
| Proficient (80-89%) | Live URL works well. Cloudinary is functional but has minor configuration warnings. |
| Developing (70-79%) | Deployed, but experiencing broken media links or occasional 500 server errors. |
| Needs Improvement (<70%) | Failed to deploy a functional Live URL or relies on local storage. |

---

### Member 2: API & IAM (Identity Access) Engineer

#### Development Responsibilities:
- Builds the **DRF REST API**
- Implements **JWT authentication**
- Automates **role seeding**
- Designs the **Serializer field-level masking logic**

#### Presentation Responsibilities:
- Conducts a **live Postman demonstration**
- Shows **JWT token generation**
- Demonstrates **role-based API responses**
- Shows the **masked vs. unmasked data twist**

#### Grading Criteria (20% - API Architecture & JWT):
| Level | Requirements |
|-------|-------------|
| Excellent (90-100%) | Postman demo is flawless. Field-level masking works exactly as intended based on JWT roles. |
| Proficient (80-89%) | API works and JWT is implemented. Minor issues with pagination or search filters. |
| Developing (70-79%) | API endpoints exist but lack proper JWT protection or fail to mask sensitive fields. |
| Needs Improvement (<70%) | No API implemented or API is entirely open to the public. |

---

### Member 3: Database Architect & RBAC Lead

#### Development Responsibilities:
- Designs **primary models**
- Enforces **Anti-IDOR logic**
- Builds **"Mine/All" view querysets**
- Implements **manager-only bulk update functionalities**

#### Presentation Responsibilities:
- Demonstrates **horizontal privilege escalation prevention** (attempting unauthorized ID access)
- Showcases **bulk operations executing securely**

#### Grading Criteria (20% - RBAC & Active Defense):
| Level | Requirements |
|-------|-------------|
| Excellent (90-100%) | Flawless object-level security. Lockouts (Axes), ratelimiting, and honeypots work perfectly. |
| Proficient (80-89%) | Good RBAC. Most defense layers work but show minor bugs in logging or lockouts. |
| Developing (70-79%) | Global roles work, but object-level ownership (Anti-IDOR) is flawed or missing. |
| Needs Improvement (<70%) | Severe horizontal privilege escalation vulnerabilities exist. App runs in DEBUG mode. |

---

### Member 4: Frontend UI & Component Engineer

#### Development Responsibilities:
- Designs **base templates**
- Implements **interactive dashboard filtering** (dates, statuses)
- Builds **inline formsets**
- Creates **custom template tags**

#### Presentation Responsibilities:
- Walks through the **UI/UX**
- Demonstrates **pagination persisting with active filters**
- Highlights **formset data entry** and **custom tag logic**

#### Grading Criteria (20% - UI Components & Data Handling):
| Level | Requirements |
|-------|-------------|
| Excellent (90-100%) | Elegant use of custom tags, persistent filtering, and inline formsets. Bulk actions work perfectly. |
| Proficient (80-89%) | Good UI implementation. Filters work but drop during pagination. Formsets are basic. |
| Developing (70-79%) | Basic UI with redundant templates. Formsets do not save related data correctly. |
| Needs Improvement (<70%) | UI is broken. Relies solely on the Django Admin panel for data entry. |

---

### Member 5: DevSecOps & Compliance Analyst

#### Development Responsibilities:
- Implements **active defense** (django-axes, ratelimiting, honeypots)
- Implements **NIST-aligned Python audit logging**
- Runs **Bandit/pip-audit scans**

#### Presentation Responsibilities:
- Executes **live simulated attacks** (e.g., triggering a lockout or ratelimit)
- Displays the **audit logs**
- Presents the **clean results of the check --deploy command**

#### Grading Criteria (20% - Individual Defense & Q&A):
| Level | Requirements |
|-------|-------------|
| Excellent (90-100%) | Member clearly articulates their specific domain, easily handles deep technical questions, and proves distinct contribution. |
| Proficient (80-89%) | Member explains their role adequately but struggles slightly with deeper technical inquiries. |
| Developing (70-79%) | Member relies heavily on teammates to answer questions about their assigned domain. |
| Needs Improvement (<70%) | Member shows a lack of understanding of the code they supposedly authored. |

---

## Required Deliverables

1. **Live URL**: The application must be deployed and accessible publicly (Localhost is an automatic failure).

2. **Source Code Repository**: A GitHub link with a comprehensive README.md detailing the setup process, architecture, and required environment variables.

3. **Postman Collection**: An exported `.json` file containing all API endpoints, including saved authentic and unauthenticated test requests.

4. **Security Audit Log**: A brief PDF report containing the outputs of the pip-audit, Bandit scans, and Django's `check --deploy` inspector.

5. **User Guide**: Expanded discussion on how to use the application.

6. **Documentation of the System**: Technical documentation of the system architecture and design.

7. **Curriculum Vitae of the Group**: CVs of all team members.

---

## Project 10 Specific Requirements

### Data & UI:
- Base templates with deep inheritance hierarchies for the dashboard
- Filtering by asset type, status, and maintenance date

### Security:
- Role-based access control separating standard staff, auditors (read-only), and motorpool managers

### API:
- Mobile-ready API for drivers to submit mileage and dashboard alerts
- Non-manager JWTs restrict the visibility of total fleet valuation and procurement costs

---

## Grading Rubric Summary

| Criteria | Weight |
|----------|--------|
| Cloud Architecture & Deployment (Member 1) | 20% |
| RBAC & Active Defense (Member 5) | 20% |
| API Architecture & JWT (Member 2) | 20% |
| UI Components & Data Handling (Member 4) | 20% |
| Individual Defense & Q&A (All Members) | 20% |

**Total: 100%**

---

*Document generated from Final Requirements PDF - Project 10: University Asset & Fleet Maintenance Tracker*

---

# Presentation Scripts and Step-by-Step Guides

This section provides detailed presentation scripts and step-by-step guides for each team member's defense portion.

---

## Member 1: Lead Cloud & DevOps Engineer - Presentation Guide

### Opening the Defense (3-4 minutes)

**Step 1: Introduction (30 seconds)**
> "Good [morning/afternoon], we are Team [Name] and we present FleetTrack — a centralized Django web application for managing the maintenance lifecycle of university vehicles and high-value IT equipment. I'm [Name], the Lead Cloud & DevOps Engineer, and I'll start by demonstrating our live deployment and cloud architecture."

**Step 2: Show Live URL (1 minute)**
- Open browser to the deployed URL (e.g., `https://fleettrack.onrender.com`)
- Say: "Our application is live at [URL]. As you can see, it loads quickly and is fully functional."
- Refresh the page to show responsiveness
- Say: "The application is hosted on [Render/Railway] with automatic deployments from our GitHub repository."

**Step 3: Demonstrate Cloud Architecture (1 minute)**
- Open browser DevTools → Network tab
- Navigate through a few pages
- Say: "All media files — like asset images — are stored on Cloudinary, not on our server. This ensures zero local storage risk and fast CDN delivery."
- Show an asset with an image: "Notice how the image loads from Cloudinary's CDN."

**Step 4: Prove Environment Variable Security (1 minute)**
- Say: "All sensitive configuration — database credentials, API keys, secret keys — are stored as environment variables, never in code."
- Show `.env.example` in the repository: "We provide a template for required variables."
- Show `settings.py` using `python-decouple`: "Our code reads from environment variables using python-decouple. The actual `.env` file is in `.gitignore` and never committed."
- Say: "In production, these are set in Render's environment variable dashboard, completely isolated from the codebase."

**Step 5: Handoff (15 seconds)**
> "With our cloud infrastructure established, let me hand over to [Member 2's Name] who will demonstrate our API and authentication system."

---

## Member 2: API & IAM Engineer - Presentation Guide

### Postman Demonstration (4-5 minutes)

**Step 1: Introduction (30 seconds)**
> "Thank you, [Member 1]. I'm [Name], the API & IAM Engineer. I'll now demonstrate our DRF REST API with JWT authentication and field-level masking."

**Step 2: Show Postman Collection (30 seconds)**
- Open Postman with the exported collection
- Say: "Here's our complete Postman collection with all API endpoints, including saved requests for both authenticated and unauthenticated scenarios."

**Step 3: Demonstrate JWT Token Generation (1 minute)**
- Send POST request to `/api/auth/login/` with credentials
- Say: "When a user logs in, they receive an access token and a refresh token."
- Show the response: "Notice the `access` and `refresh` tokens in the response."
- Copy the access token for subsequent requests.

**Step 3: Show Role-Based API Responses (1.5 minutes)**
- **First, as a Manager:**
  - Send GET request to `/api/assets/` with manager token
  - Say: "As a manager, I can see all assets including costs."
  - Point out: "Notice the `purchase_cost` field is visible."

- **Then, as Standard Staff:**
  - Send GET request to `/api/assets/` with staff token
  - Say: "Now, as a standard staff member, the same endpoint returns masked data."
  - Point out: "The `purchase_cost` field is either hidden or shows 'Restricted'."

**Step 4: Demonstrate Unauthenticated Request (30 seconds)**
- Send GET request to `/api/assets/` without any token
- Say: "Unauthenticated requests are rejected with a 401 Unauthorized response."

**Step 5: Show Field-Level Masking (30 seconds)**
- Send GET request to `/api/maintenance/history/` with different roles
- Say: "This masking applies to all sensitive fields — maintenance costs, procurement values — ensuring non-managers never see financial data."

**Step 6: Handoff (15 seconds)**
> "Our API is secure and role-aware. Now, [Member 3's Name] will demonstrate our database security and RBAC implementation."

---

## Member 3: Database Architect & RBAC Lead - Presentation Guide

### Security Demonstration (4-5 minutes)

**Step 1: Introduction (30 seconds)**
> "Thank you, [Member 2]. I'm [Name], the Database Architect & RBAC Lead. I'll demonstrate our Anti-IDOR implementation and bulk operations security."

**Step 2: Demonstrate Anti-IDOR (2 minutes)**
- Log in as Standard Staff user
- Navigate to Maintenance Requests page
- Say: "As a standard staff member, I can only see my own maintenance requests."
- Try to access another user's request directly via URL: `http://localhost:8000/api/maintenance/requests/999/`
- Say: "If I try to access a request that isn't mine by manipulating the ID, the system returns 404 Not Found — not 403. This prevents information leakage about the existence of other records."
- Show the code: "Our `get_queryset()` method filters by `requested_by=self.request.user`."

**Step 3: Demonstrate "Mine/All" Querysets (1 minute)**
- Log in as Manager
- Navigate to Assets page
- Say: "As a manager, I see ALL assets in the system."
- Show the query: "My queryset returns `Asset.objects.all()` for managers, but `Asset.objects.filter(created_by=user)` for staff."

**Step 4: Demonstrate Bulk Operations (1 minute)**
- As Manager, go to Maintenance Requests
- Select multiple pending requests
- Click "Bulk Approve"
- Say: "Managers can bulk-approve requests. This operation is protected — only users with `is_manager=True` can access this endpoint."
- Show the permission check: "Our `IsManager` permission class blocks non-managers."

**Step 5: Handoff (15 seconds)**
> "Our database layer enforces strict access control at every level. Now, [Member 4's Name] will walk you through our UI/UX implementation."

---

## Member 4: Frontend UI & Component Engineer - Presentation Guide

### UI/UX Demonstration (4-5 minutes)

**Step 1: Introduction (30 seconds)**
> "Thank you, [Member 3]. I'm [Name], the Frontend UI & Component Engineer. I'll demonstrate our template architecture, filtering system, and form handling."

**Step 2: Show Base Template Architecture (30 seconds)**
- View page source on any page
- Say: "All pages extend a single `base.html` template with deep inheritance. This ensures consistent navigation, styling, and behavior across the entire application."
- Point out: "The sidebar, header styles, and JavaScript are all defined once and reused everywhere."

**Step 3: Demonstrate Interactive Filtering (1.5 minutes)**
- Go to Assets page
- Type in the search box: "Notice how results filter in real-time as I type."
- Select a status filter: "The status dropdown filters instantly without page reload."
- Select a category filter: "Multiple filters combine — search + status + category."
- Paginate: "Pagination persists through active filters. If I go to page 2, my filters remain active."

**Step 4: Demonstrate Formsets (1 minute)**
- Go to a page with formsets (if available) or show the code
- Say: "Our inline formsets allow users to enter related data in a single form. For example, when creating an asset, you can add multiple categories or related records without leaving the page."
- If no formsets in current UI, show the code: "Here's our formset implementation for [specific feature]."

**Step 5: Show Custom Template Tags (30 seconds)**
- View page source
- Say: "We created custom template tags for formatting — like currency display, date formatting, and status badges."
- Point to an example: "This status badge uses our custom `status_badge` tag that applies the correct color and icon based on the status value."

**Step 6: Mobile Responsiveness (30 seconds)**
- Open browser DevTools → Device Toolbar
- Switch to mobile view
- Say: "Our templates are fully mobile-responsive. The sidebar collapses into a hamburger menu, tables scroll horizontally, and all touch targets are at least 44px."

**Step 7: Handoff (15 seconds)**
> "Our UI is intuitive, responsive, and built with reusable components. Finally, [Member 5's Name] will demonstrate our security defenses and compliance."

---

## Member 5: DevSecOps & Compliance Analyst - Presentation Guide

### Security Demonstration (4-5 minutes)

**Step 1: Introduction (30 seconds)**
> "Thank you, [Member 4]. I'm [Name], the DevSecOps & Compliance Analyst. I'll demonstrate our active defense mechanisms, audit logging, and security compliance."

**Step 2: Simulate Brute-Force Attack (1.5 minutes)**
- Open a new browser window or use a script
- Attempt to log in with wrong password 5 times
- Say: "After 5 failed login attempts, the account is locked for 10 minutes."
- Show the lockout message: "The user sees a clear lockout message."
- Check audit logs: "Every failed attempt is logged with timestamp, IP address, and username."
- Say: "This is implemented using [django-axes / custom backend] and integrated with our audit system."

**Step 3: Demonstrate Rate Limiting (1 minute)**
- Use a tool or script to send rapid API requests
- Say: "Our API implements DRF throttling — 1000 requests/hour for authenticated users, 100/hour for anonymous."
- Show the 429 Too Many Requests response: "When the limit is exceeded, the API returns a 429 response with a retry-after header."

**Step 4: Show Audit Logs (1 minute)**
- Navigate to Audit Logs page (as manager/auditor)
- Say: "Every action in the system is logged — logins, logouts, creates, updates, deletes, approvals, rejections."
- Click on a log entry: "Each entry shows the user, timestamp, IP address, action type, and before/after values."
- Say: "This NIST-aligned logging uses Python's logging module and provides a complete audit trail for compliance."

**Step 5: Present Security Scan Results (1 minute)**
- Show the security audit PDF or run live scans
- Say: "We run Bandit for static analysis and pip-audit for dependency vulnerabilities."
- Show clean results: "As you can see, we have zero security issues in our codebase and dependencies."
- Run `python manage.py check --deploy`: "Django's deployment check also passes with no warnings."

**Step 6: Conclusion (30 seconds)**
> "Our application is built with security at every layer — from active defense against attacks, to comprehensive audit logging, to clean security scans. This completes our presentation. Thank you for your time. We're ready for your questions."

---

## General Q&A Preparation Tips

1. **Know Your Code**: Every member must be able to explain and show the code they wrote.
2. **Practice Transitions**: Smooth handoffs between members show team coordination.
3. **Prepare for Common Questions**:
   - "How did you handle [specific security concern]?"
   - "What was the most challenging part of your module?"
   - "How would you scale this application?"
   - "What would you improve if you had more time?"
4. **Have Backup Plans**: If live demo fails, have screenshots or recorded videos ready.
5. **Time Management**: Keep each section within the time limit to allow for questions.

---

## Presentation Order Summary

1. **Member 1** (3-4 min): Opens defense, shows live app, cloud architecture, env vars
2. **Member 2** (4-5 min): Postman demo, JWT, role-based responses, field masking
3. **Member 3** (4-5 min): Anti-IDOR, Mine/All querysets, bulk operations
4. **Member 4** (4-5 min): UI/UX, filtering, formsets, custom tags, mobile
5. **Member 5** (4-5 min): Active defense, audit logs, security scans
6. **Q&A** (remaining time): All members answer questions about their domains

**Total Presentation Time**: ~20-25 minutes + Q&A
