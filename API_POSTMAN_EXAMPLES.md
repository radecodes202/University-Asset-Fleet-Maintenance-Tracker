# FleetTrack API Documentation with Postman Examples

Complete API reference with Postman request examples for the University Asset & Fleet Maintenance Tracker.

---

## Base URL
```
http://localhost:8000/api/
```
(Replace with your deployed URL in production, e.g., `https://fleettrack.onrender.com/api/`)

---

## Table of Contents

1. [Authentication Endpoints](#authentication-endpoints)
2. [Assets Endpoints](#assets-endpoints)
3. [Maintenance Endpoints](#maintenance-endpoints)
4. [Dashboard Endpoints](#dashboard-endpoints)
5. [Accounts Endpoints](#accounts-endpoints)
6. [Audit Endpoints](#audit-endpoints)

---

## Authentication Endpoints

### 1. Login (Obtain JWT Tokens)

**Endpoint:** `POST /api/auth/login/`

**Description:** Authenticate user and obtain access/refresh tokens. Uses email-based authentication.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "manager@university.edu.ph",
  "password": "password123"
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Postman Example:**
- Method: POST
- URL: `{{base_url}}/auth/login/`
- Body (raw JSON):
```json
{
  "email": "manager@university.edu.ph",
  "password": "password123"
}
```

> **Note:** The login endpoint uses email-based authentication. Make sure the user exists in the database and the credentials are correct. If you get a 401 error, verify that:
> 1. The email address is exactly as created (case-sensitive)
> 2. The password is correct
> 3. The user account is active (`is_active=True`)
> 4. The account is not locked due to failed login attempts

---

### 2. Refresh Token

**Endpoint:** `POST /api/auth/refresh/`

**Description:** Obtain a new access token using a valid refresh token.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Postman Example:**
- Method: POST
- URL: `{{base_url}}/auth/refresh/`
- Body (raw JSON):
```json
{
  "refresh": "{{refresh_token}}"
}
```

---

### 3. Logout (Blacklist Token)

**Endpoint:** `POST /api/auth/logout/`

**Description:** Blacklist a refresh token, effectively logging out the user.

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {{access_token}}
```

**Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response (200 OK):**
```json
{
  "detail": "Token blacklisted successfully"
}
```

**Postman Example:**
- Method: POST
- URL: `{{base_url}}/auth/logout/`
- Headers: `Authorization: Bearer {{access_token}}`
- Body (raw JSON):
```json
{
  "refresh": "{{refresh_token}}"
}
```

---

## Assets Endpoints

### 4. List All Assets

**Endpoint:** `GET /api/assets/`

**Description:** Retrieve a paginated list of all assets. Accessible by all authenticated users.

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Query Parameters (Optional):**
- `search` - Search by asset name, category, or serial number
- `status` - Filter by status (ACTIVE, UNDER_MAINTENANCE, RETIRED)
- `category` - Filter by category name
- `ordering` - Order by field (e.g., `asset_name`, `-purchase_date`)
- `page` - Page number for pagination

**Success Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/assets/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "asset_name": "Toyota Vios 2024",
      "serial_number": "SN-2024-0001",
      "category": {
        "id": 1,
        "name": "Sedan",
        "description": "Passenger vehicle"
      },
      "purchase_date": "2024-01-15",
      "purchase_cost": 850000.00,
      "current_status": "ACTIVE",
      "asset_image": "https://res.cloudinary.com/...",
      "notes": "Regular maintenance every 5000km",
      "date_added": "2024-01-15T08:30:00Z",
      "created_by": "admin@university.edu.ph"
    }
  ]
}
```

**Note:** Non-managers will NOT see `purchase_cost` field (field-level masking).

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/assets/?status=ACTIVE&ordering=asset_name`
- Headers: `Authorization: Bearer {{access_token}}`

---

### 5. Create New Asset

**Endpoint:** `POST /api/assets/`

**Description:** Create a new asset. **Manager only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body:**
```json
{
  "asset_name": "Honda Civic 2023",
  "serial_number": "SN-2023-0045",
  "category_id": 1,
  "purchase_date": "2023-12-01",
  "purchase_cost": 920000.00,
  "current_status": "ACTIVE",
  "notes": "Newly acquired vehicle for faculty use"
}
```

**Success Response (201 Created):**
```json
{
  "id": 26,
  "asset_name": "Honda Civic 2023",
  "serial_number": "SN-2023-0045",
  "category": {
    "id": 1,
    "name": "Sedan",
    "description": "Passenger vehicle"
  },
  "purchase_date": "2023-12-01",
  "purchase_cost": 920000.00,
  "current_status": "ACTIVE",
  "asset_image": null,
  "notes": "Newly acquired vehicle for faculty use",
  "date_added": "2024-06-03T10:15:00Z",
  "created_by": "manager@university.edu.ph"
}
```

**Postman Example:**
- Method: POST
- URL: `{{base_url}}/assets/`
- Headers: `Authorization: Bearer {{access_token}}`
- Body (raw JSON):
```json
{
  "asset_name": "Honda Civic 2023",
  "serial_number": "SN-2023-0045",
  "category_id": 1,
  "purchase_date": "2023-12-01",
  "purchase_cost": 920000.00,
  "current_status": "ACTIVE",
  "notes": "Newly acquired vehicle for faculty use"
}
```

---

### 6. Retrieve Asset Detail

**Endpoint:** `GET /api/assets/<id>/`

**Description:** Get detailed information about a specific asset.

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "asset_name": "Toyota Vios 2024",
  "serial_number": "SN-2024-0001",
  "category": {
    "id": 1,
    "name": "Sedan",
    "description": "Passenger vehicle"
  },
  "purchase_date": "2024-01-15",
  "purchase_cost": 850000.00,
  "current_status": "ACTIVE",
  "asset_image": "https://res.cloudinary.com/...",
  "notes": "Regular maintenance every 5000km",
  "date_added": "2024-01-15T08:30:00Z",
  "created_by": "admin@university.edu.ph"
}
```

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/assets/1/`
- Headers: `Authorization: Bearer {{access_token}}`

---

### 7. Update Asset

**Endpoint:** `PATCH /api/assets/<id>/`

**Description:** Update an existing asset. **Manager only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (partial update):**
```json
{
  "current_status": "UNDER_MAINTENANCE",
  "notes": "Scheduled for engine repair"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "asset_name": "Toyota Vios 2024",
  "serial_number": "SN-2024-0001",
  "category": {
    "id": 1,
    "name": "Sedan",
    "description": "Passenger vehicle"
  },
  "purchase_date": "2024-01-15",
  "purchase_cost": 850000.00,
  "current_status": "UNDER_MAINTENANCE",
  "asset_image": "https://res.cloudinary.com/...",
  "notes": "Scheduled for engine repair",
  "date_added": "2024-01-15T08:30:00Z",
  "created_by": "admin@university.edu.ph"
}
```

**Postman Example:**
- Method: PATCH
- URL: `{{base_url}}/assets/1/`
- Headers: `Authorization: Bearer {{access_token}}`
- Body (raw JSON):
```json
{
  "current_status": "UNDER_MAINTENANCE"
}
```

---

### 8. Delete Asset

**Endpoint:** `DELETE /api/assets/<id>/`

**Description:** Delete an asset. **Manager only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Success Response (204 No Content):**
```
(No response body)
```

**Postman Example:**
- Method: DELETE
- URL: `{{base_url}}/assets/1/`
- Headers: `Authorization: Bearer {{access_token}}`

---

### 9. List Asset Categories

**Endpoint:** `GET /api/assets/categories/`

**Description:** Retrieve all asset categories.

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Success Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Sedan",
      "description": "Passenger vehicle"
    },
    {
      "id": 2,
      "name": "SUV",
      "description": "Sport Utility Vehicle"
    },
    {
      "id": 3,
      "name": "Laptop",
      "description": "Portable computer"
    }
  ]
}
```

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/assets/categories/`
- Headers: `Authorization: Bearer {{access_token}}`

---

### 10. Create Asset Category

**Endpoint:** `POST /api/assets/categories/`

**Description:** Create a new asset category. **Manager only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body:**
```json
{
  "name": "Printer",
  "description": "Office printing equipment"
}
```

**Success Response (201 Created):**
```json
{
  "id": 6,
  "name": "Printer",
  "description": "Office printing equipment"
}
```

**Postman Example:**
- Method: POST
- URL: `{{base_url}}/assets/categories/`
- Headers: `Authorization: Bearer {{access_token}}`
- Body (raw JSON):
```json
{
  "name": "Printer",
  "description": "Office printing equipment"
}
```

---

## Maintenance Endpoints

### 11. List Maintenance Requests

**Endpoint:** `GET /api/maintenance/requests/`

**Description:** Retrieve maintenance requests. Staff see only their own; managers/auditors see all.

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Query Parameters (Optional):**
- `search` - Search by asset name, requester, or problem
- `status` - Filter by status (PENDING, APPROVED, REJECTED, COMPLETED)
- `asset` - Filter by asset ID
- `ordering` - Order by field (e.g., `date_requested`, `-status`)
- `page` - Page number

**Success Response (200 OK):**
```json
{
  "count": 12,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "asset": {
        "id": 1,
        "asset_name": "Toyota Vios 2024",
        "serial_number": "SN-2024-0001"
      },
      "problem_description": "Engine overheating during long drives",
      "date_requested": "2024-06-01",
      "status": "PENDING",
      "requested_by": "staff@university.edu.ph"
    }
  ]
}
```

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/maintenance/requests/?status=PENDING`
- Headers: `Authorization: Bearer {{access_token}}`

---

### 12. Submit Maintenance Request

**Endpoint:** `POST /api/maintenance/requests/`

**Description:** Submit a new maintenance request. All authenticated users except auditors.

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body:**
```json
{
  "asset_id": 1,
  "problem_description": "Brake pads are worn out, producing squeaking sound when braking"
}
```

**Success Response (201 Created):**
```json
{
  "id": 13,
  "asset": {
    "id": 1,
    "asset_name": "Toyota Vios 2024",
    "serial_number": "SN-2024-0001"
  },
  "problem_description": "Brake pads are worn out, producing squeaking sound when braking",
  "date_requested": "2024-06-03",
  "status": "PENDING",
  "requested_by": "staff@university.edu.ph"
}
```

**Postman Example:**
- Method: POST
- URL: `{{base_url}}/maintenance/requests/`
- Headers: `Authorization: Bearer {{access_token}}`
- Body (raw JSON):
```json
{
  "asset_id": 1,
  "problem_description": "Brake pads are worn out, producing squeaking sound when braking"
}
```

---

### 13. Update Maintenance Request

**Endpoint:** `PATCH /api/maintenance/requests/<id>/`

**Description:** Update a maintenance request (approve/reject). **Manager only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body:**
```json
{
  "status": "APPROVED"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "asset": {
    "id": 1,
    "asset_name": "Toyota Vios 2024",
    "serial_number": "SN-2024-0001"
  },
  "problem_description": "Engine overheating during long drives",
  "date_requested": "2024-06-01",
  "status": "APPROVED",
  "requested_by": "staff@university.edu.ph"
}
```

**Postman Example:**
- Method: PATCH
- URL: `{{base_url}}/maintenance/requests/1/`
- Headers: `Authorization: Bearer {{access_token}}`
- Body (raw JSON):
```json
{
  "status": "APPROVED"
}
```

---

### 14. Bulk Update Maintenance Requests

**Endpoint:** `POST /api/maintenance/requests/bulk-update/`

**Description:** Bulk approve or reject multiple requests. **Manager only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body:**
```json
{
  "request_ids": [1, 2, 3],
  "status": "APPROVED"
}
```

**Success Response (200 OK):**
```json
{
  "updated_count": 3,
  "details": [
    {"id": 1, "status": "APPROVED"},
    {"id": 2, "status": "APPROVED"},
    {"id": 3, "status": "APPROVED"}
  ]
}
```

**Postman Example:**
- Method: POST
- URL: `{{base_url}}/maintenance/requests/bulk-update/`
- Headers: `Authorization: Bearer {{access_token}}`
- Body (raw JSON):
```json
{
  "request_ids": [1, 2, 3],
  "status": "APPROVED"
}
```

---

### 15. List Work Orders

**Endpoint:** `GET /api/maintenance/workorders/`

**Description:** Retrieve work orders. **Manager only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Query Parameters (Optional):**
- `status` - Filter by status (OPEN, IN_PROGRESS, COMPLETED, CANCELLED)
- `asset` - Filter by asset ID
- `technician` - Filter by technician user ID
- `ordering` - Order by field

**Success Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "maintenance_request": {
        "id": 1,
        "asset_name": "Toyota Vios 2024",
        "problem_description": "Engine overheating"
      },
      "asset": {
        "id": 1,
        "asset_name": "Toyota Vios 2024"
      },
      "technician": {
        "id": 5,
        "email": "technician@university.edu.ph",
        "full_name": "Juan Dela Cruz"
      },
      "work_description": "Inspect and repair engine cooling system",
      "status": "IN_PROGRESS",
      "date_assigned": "2024-06-02"
    }
  ]
}
```

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/maintenance/workorders/?status=IN_PROGRESS`
- Headers: `Authorization: Bearer {{access_token}}`

---

### 16. Create Work Order

**Endpoint:** `POST /api/maintenance/workorders/`

**Description:** Create a new work order. **Manager only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body:**
```json
{
  "request_id": 1,
  "technician_id": 5,
  "work_description": "Replace brake pads and inspect braking system"
}
```

**Success Response (201 Created):**
```json
{
  "id": 6,
  "maintenance_request": {
    "id": 1,
    "asset_name": "Toyota Vios 2024",
    "problem_description": "Brake pads worn out"
  },
  "asset": {
    "id": 1,
    "asset_name": "Toyota Vios 2024"
  },
  "technician": {
    "id": 5,
    "email": "technician@university.edu.ph",
    "full_name": "Juan Dela Cruz"
  },
  "work_description": "Replace brake pads and inspect braking system",
  "status": "OPEN",
  "date_assigned": "2024-06-03"
}
```

**Postman Example:**
- Method: POST
- URL: `{{base_url}}/maintenance/workorders/`
- Headers: `Authorization: Bearer {{access_token}}`
- Body (raw JSON):
```json
{
  "request_id": 1,
  "technician_id": 5,
  "work_description": "Replace brake pads and inspect braking system"
}
```

---

### 17. Update Work Order

**Endpoint:** `PATCH /api/maintenance/workorders/<id>/`

**Description:** Update work order status. **Manager only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body:**
```json
{
  "status": "COMPLETED"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "maintenance_request": {
    "id": 1,
    "asset_name": "Toyota Vios 2024",
    "problem_description": "Engine overheating"
  },
  "asset": {
    "id": 1,
    "asset_name": "Toyota Vios 2024"
  },
  "technician": {
    "id": 5,
    "email": "technician@university.edu.ph",
    "full_name": "Juan Dela Cruz"
  },
  "work_description": "Inspect and repair engine cooling system",
  "status": "COMPLETED",
  "date_assigned": "2024-06-02"
}
```

**Postman Example:**
- Method: PATCH
- URL: `{{base_url}}/maintenance/workorders/1/`
- Headers: `Authorization: Bearer {{access_token}}`
- Body (raw JSON):
```json
{
  "status": "COMPLETED"
}
```

---

### 18. List Maintenance History

**Endpoint:** `GET /api/maintenance/history/`

**Description:** Retrieve completed maintenance records. Non-managers see masked costs.

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Query Parameters (Optional):**
- `asset` - Filter by asset ID
- `date_from` - Filter from date (YYYY-MM-DD)
- `date_to` - Filter to date (YYYY-MM-DD)
- `search` - Search by asset name or description
- `ordering` - Order by field

**Success Response (200 OK):**
```json
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "asset": {
        "id": 2,
        "asset_name": "Dell OptiPlex 7090",
        "serial_number": "SN-2022-0015"
      },
      "maintenance_cost": 4500.00,
      "technician": {
        "id": 5,
        "email": "technician@university.edu.ph",
        "full_name": "Juan Dela Cruz"
      },
      "work_description": "Replaced thermal paste and cleaned cooling fans",
      "remarks": "System now running at normal temperatures",
      "date_completed": "2024-05-28",
      "timestamp": "2024-05-28T16:30:00Z"
    }
  ]
}
```

**Note:** Non-managers will see `"maintenance_cost": "Restricted"` instead of the actual value.

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/maintenance/history/?asset=1`
- Headers: `Authorization: Bearer {{access_token}}`

---

### 19. Export Maintenance History as CSV

**Endpoint:** `GET /api/maintenance/history-export-csv/`

**Description:** Export maintenance history as CSV file.

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Success Response (200 OK):**
```
Content-Type: text/csv
Content-Disposition: attachment; filename="maintenance_history.csv"

Asset Name,Serial Number,Cost,Technician,Work Description,Date Completed
"Dell OptiPlex 7090","SN-2022-0015",4500.00,"Juan Dela Cruz","Replaced thermal paste","2024-05-28"
```

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/maintenance/history-export-csv/`
- Headers: `Authorization: Bearer {{access_token}}`

---

### 20. List Technicians

**Endpoint:** `GET /api/maintenance/technicians/`

**Description:** Retrieve list of users with technician role. **Manager only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Success Response (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "email": "technician@university.edu.ph",
      "full_name": "Juan Dela Cruz",
      "role": "STANDARD_STAFF"
    },
    {
      "id": 7,
      "email": "mechanic@university.edu.ph",
      "full_name": "Pedro Santos",
      "role": "STANDARD_STAFF"
    }
  ]
}
```

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/maintenance/technicians/`
- Headers: `Authorization: Bearer {{access_token}}`

---

## Dashboard Endpoints

### 21. Dashboard Summary

**Endpoint:** `GET /api/dashboard/summary/`

**Description:** Get KPI summary for dashboard. All authenticated users.

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Success Response (200 OK):**
```json
{
  "total_assets": 25,
  "pending_requests": 8,
  "completed_repairs": 42,
  "under_maintenance": 3,
  "total_maintenance_cost": 125000.00
}
```

**Note:** `total_maintenance_cost` is only included for managers.

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/dashboard/summary/`
- Headers: `Authorization: Bearer {{access_token}}`

---

### 22. Recent Activity

**Endpoint:** `GET /api/dashboard/recent-activity/`

**Description:** Get recent maintenance requests, work orders, and completed repairs.

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Success Response (200 OK):**
```json
{
  "recent_requests": [
    {
      "id": 13,
      "asset_name": "Toyota Vios 2024",
      "status": "PENDING",
      "date_requested": "2024-06-03"
    }
  ],
  "recent_workorders": [
    {
      "id": 6,
      "asset_name": "Honda Civic 2023",
      "status": "IN_PROGRESS",
      "date_assigned": "2024-06-02"
    }
  ],
  "recent_completed": [
    {
      "id": 1,
      "asset_name": "Dell OptiPlex 7090",
      "maintenance_cost": 4500.00,
      "date_completed": "2024-05-28"
    }
  ]
}
```

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/dashboard/recent-activity/`
- Headers: `Authorization: Bearer {{access_token}}`

---

## Accounts Endpoints

### 23. List Users

**Endpoint:** `GET /api/accounts/users/list/`

**Description:** Retrieve list of all users. **Manager only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Query Parameters (Optional):**
- `search` - Search by email or name
- `role` - Filter by role (STANDARD_STAFF, MOTORPOOL_MANAGER, AUDITOR)
- `page` - Page number

**Success Response (200 OK):**
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "admin@university.edu.ph",
      "full_name": "Admin User",
      "role": "MOTORPOOL_MANAGER",
      "is_active": true,
      "date_joined": "2024-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "email": "staff@university.edu.ph",
      "full_name": "Staff User",
      "role": "STANDARD_STAFF",
      "is_active": true,
      "date_joined": "2024-02-15T00:00:00Z"
    }
  ]
}
```

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/accounts/users/list/?role=STANDARD_STAFF`
- Headers: `Authorization: Bearer {{access_token}}`

---

### 24. Create User

**Endpoint:** `POST /api/accounts/users/list/`

**Description:** Create a new user. **Manager only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body:**
```json
{
  "email": "newstaff@university.edu.ph",
  "password": "TempPass123!",
  "full_name": "Maria Clara",
  "role": "STANDARD_STAFF"
}
```

**Success Response (201 Created):**
```json
{
  "id": 16,
  "email": "newstaff@university.edu.ph",
  "full_name": "Maria Clara",
  "role": "STANDARD_STAFF",
  "is_active": true,
  "date_joined": "2024-06-03T10:30:00Z"
}
```

**Postman Example:**
- Method: POST
- URL: `{{base_url}}/accounts/users/list/`
- Headers: `Authorization: Bearer {{access_token}}`
- Body (raw JSON):
```json
{
  "email": "newstaff@university.edu.ph",
  "password": "TempPass123!",
  "full_name": "Maria Clara",
  "role": "STANDARD_STAFF"
}
```

---

## Audit Endpoints

### 25. List Audit Logs

**Endpoint:** `GET /api/audit/`

**Description:** Retrieve audit logs. **Manager and Auditor only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Query Parameters (Optional):**
- `action` - Filter by action (CREATE, UPDATE, DELETE, STATUS_CHANGE, APPROVE, REJECT, LOGIN, LOGOUT)
- `model_name` - Filter by model (Asset, MaintenanceRequest, WorkOrder, etc.)
- `date_from` - Filter from date (YYYY-MM-DD)
- `search` - Search by user email, object ID, or IP address
- `ordering` - Order by field (default: `-timestamp`)
- `page` - Page number

**Success Response (200 OK):**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/audit/?page=2",
  "previous": null,
  "results": [
    {
      "id": 245,
      "timestamp": "2024-06-03T10:15:30Z",
      "user_email": "manager@university.edu.ph",
      "user_name": "Manager User",
      "action": "APPROVE",
      "action_display": "Approved",
      "model_name": "MaintenanceRequest",
      "object_id": 1,
      "object_display": "Maintenance Request #1 - Toyota Vios 2024",
      "ip_address": "192.168.1.100",
      "old_values": {
        "status": "PENDING"
      },
      "new_values": {
        "status": "APPROVED"
      }
    }
  ]
}
```

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/audit/?action=APPROVE&model_name=MaintenanceRequest`
- Headers: `Authorization: Bearer {{access_token}}`

---

### 26. Retrieve Audit Log Detail

**Endpoint:** `GET /api/audit/<id>/`

**Description:** Get detailed information about a specific audit log entry. **Manager and Auditor only.**

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Success Response (200 OK):**
```json
{
  "id": 245,
  "timestamp": "2024-06-03T10:15:30Z",
  "user_email": "manager@university.edu.ph",
  "user_name": "Manager User",
  "action": "APPROVE",
  "action_display": "Approved",
  "model_name": "MaintenanceRequest",
  "object_id": 1,
  "object_display": "Maintenance Request #1 - Toyota Vios 2024",
  "ip_address": "192.168.1.100",
  "old_values": {
    "status": "PENDING"
  },
  "new_values": {
    "status": "APPROVED"
  }
}
```

**Postman Example:**
- Method: GET
- URL: `{{base_url}}/audit/245/`
- Headers: `Authorization: Bearer {{access_token}}`

---

## Postman Environment Variables

To use these examples efficiently in Postman, set up the following environment variables:

| Variable | Example Value | Description |
|----------|---------------|-------------|
| `base_url` | `http://localhost:8000/api` | Base API URL |
| `access_token` | `eyJhbGci...` | JWT access token |
| `refresh_token` | `eyJhbGci...` | JWT refresh token |
| `manager_email` | `manager@university.edu.ph` | Manager test account |
| `staff_email` | `staff@university.edu.ph` | Staff test account |
| `password` | `password123` | Test password |

---

## Testing Field-Level Masking

To demonstrate field-level masking for Member 2's presentation:

### Test as Manager (Can See Costs)

1. Login as manager:
```json
POST /api/auth/login/
{
  "email": "manager@university.edu.ph",
  "password": "password123"
}
```

2. Get assets with manager token:
```
GET /api/assets/
Authorization: Bearer {{manager_access_token}}
```

Response will include `purchase_cost` field.

### Test as Staff (Cannot See Costs)

1. Login as staff:
```json
POST /api/auth/login/
{
  "email": "staff@university.edu.ph",
  "password": "password123"
}
```

2. Get assets with staff token:
```
GET /api/assets/
Authorization: Bearer {{staff_access_token}}
```

Response will have `purchase_cost` field removed or showing "Restricted".

---

## Common Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 429 Too Many Requests
```json
{
  "detail": "Request was throttled."
}
```

### 400 Bad Request (Validation Error)
```json
{
  "asset_name": ["This field is required."],
  "purchase_cost": ["Ensure this value is greater than 0."]
}
```

---


