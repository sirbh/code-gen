# Geocoding API

This is a simple Geocoding API built with Node.js, Express.js, and Prisma ORM. It connects to a PostgreSQL database and is containerized using Docker and docker-compose.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository
2. Navigate to the project directory
3. Run `docker-compose up --build`
4. The server will be running at `http://localhost:3000`

### API Endpoints

- GET /maps/api/geocode/json: Retrieve geocoding data

### Environment Variables

- `DATABASE_URL`: Connection string for the PostgreSQL database

### Notes

- Ensure the PostgreSQL service is running and accessible.
- Prisma migrations are automatically applied when the app starts.
