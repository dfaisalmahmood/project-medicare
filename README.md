# Project Medicare

This is the monorepo for Project Medicare, which includes both the backend and frontend applications, alongside any libs and scripts shared between them.

## Apps

- **Backend**: Located in `apps/backend`, this is the FastAPI backend service.
- **Frontend**: Located in `apps/web`, this is the React/NextJS frontend application (coming soon).

## Development

### Prerequisites

- Node.js (v22+ recommended)
- pnpm (v10+ recommended)
- astral uv
- Docker & Docker Compose (for local development with PostgreSQL)

### Setup

1. Install dependencies:

   ```bash
   pnpm install
   ```

   This will automatically run the post-install script to set up backend virtual environment and install Python dependencies.

2. Start the Docker containers (PostgreSQL, Redis, etc):

   ```bash
   pnpm docker:env
   ```

3. Start the development servers:

   ```bash
   pnpm dev
   ```
