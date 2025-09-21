---
description: "This document provides an overview of the backend app's folder hierarchy. Individual files are omitted; each folder is described by the types of files it contains."
---

# Project Structure

This backend is organized in NestJS-style modules for easy future extraction into microservices.

```text
project-root/apps/backend/
├── app/
│   ├── api/
│   │   [aggregate API router(s) that include module routers]
│   ├── core/
│   │   [shared configuration, database setup, and security utilities]
│   ├── modules/
│   │   ├── auth/
│   │   │   [auth module: router (controller), schemas (dto), dependencies]
│   │   └── users/
│   │       [users module: model, router (controller), service, schemas (dto)]
│   └── main.py
│       [application factory and FastAPI app wiring]
└── docs/
    [project documentation and task management CSVs]
```

Notes:

- Modules encapsulate controller/router, service, model(s), and DTO schemas.
- Database is configured via `DATABASE_URL` environment variable.
- JWT settings are controlled by `JWT_SECRET_KEY`, `JWT_ALGORITHM`, and `ACCESS_TOKEN_EXPIRE_MINUTES`.
