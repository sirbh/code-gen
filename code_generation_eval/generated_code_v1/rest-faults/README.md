# API Server

This is a simple API server built with Node.js, Express.js, and Prisma ORM. It connects to a PostgreSQL database and is containerized using Docker and docker-compose.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository
2. Navigate to the project directory
3. Run `docker-compose up --build`
4. The server will be running at `http://localhost:8080`

### API Endpoints

- GET /z
- PUT /z
- GET /k
- PUT /k
- GET /y
- POST /y
- DELETE /y
- GET /x

### Environment Variables

- `DATABASE_URL`: Connection string for the PostgreSQL database

### Notes

- Ensure the PostgreSQL service is running and accessible.
- Prisma migrations are automatically applied when the app starts.
