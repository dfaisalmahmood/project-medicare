# Project Medicare Features

## Major Features

### User Authentication and Authorization

- Secure user registration and login using JWT tokens.

### Role-Based Access Control (RBAC)

- Roles: user, superadmin
- Superadmin can manage users and view/manage patients for any user.
- Regular users can only manage their own patient records.

### Patients Management

- Users can create and manage multiple patients (self, parents, spouse, etc).
- Patient fields: name, dob, gender, blood_group, ethnicity.
- Full CRUD endpoints under /api/patients for the current user.

### Users Management (Admin)

- Superadmin-only CRUD under /api/users.
- Endpoints: list, get by id, create, update, delete; plus /api/users/me for current user.

### CORS

- Configurable CORS via environment variables:
  - CORS_ALLOW_ORIGINS (comma-separated, default \*)
  - CORS_ALLOW_METHODS (default \*)
  - CORS_ALLOW_HEADERS (default \*)
  - CORS_ALLOW_CREDENTIALS (default true)

### Seed Script

- Script to seed an initial superadmin user.
- Run with env vars SEED_SUPERADMIN_EMAIL, SEED_SUPERADMIN_PASSWORD, SEED_SUPERADMIN_NAME.

---

## Minor Features
