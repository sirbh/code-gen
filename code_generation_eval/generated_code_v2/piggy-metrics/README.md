# Piggy Metrics API

This is a simple financial advisor app API built with Node.js, Express.js, and Prisma ORM. It connects to a PostgreSQL database and is containerized using Docker and docker-compose.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository
2. Navigate to the project directory
3. Run `docker-compose up --build`
4. The server will be running at `http://localhost:8000`

### API Endpoints

- GET /accounts/{account}: Retrieve specified account data
- GET /accounts/current: Retrieve current account data
- PUT /accounts/current: Save current account data
- GET /accounts/demo: Retrieve demo account data
- POST /accounts/: Register new account
- GET /statistics/{account}: Retrieve specified account statistics
- PUT /statistics/{account}: Create or update time series datapoint for specified account
- GET /statistics/current: Retrieve current account statistics
- GET /statistics/demo: Retrieve demo account statistics
- GET /notifications/settings/current: Retrieve current account notification settings
- PUT /notifications/settings/current: Save current account notification settings

### Environment Variables

- `DATABASE_URL`: Connection string for the PostgreSQL database

### Notes

- Ensure the PostgreSQL service is running and accessible.
- Prisma migrations are automatically applied when the app starts.
