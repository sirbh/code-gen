# Quartz Scheduler API

This is a Quartz Scheduler API built with Node.js, Express.js, and Prisma ORM. It connects to a PostgreSQL database and is containerized using Docker and docker-compose.

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

- POST /quartz/mail/create: Create a mail schedule
- DELETE /quartz/mail/delete/{id}: Delete a mail schedule
- GET /quartz/mail/list: Get all mail schedules created by user
- GET /quartz/mail/list/{id}: Get mail schedule by ID
- POST /quartz/mail/update/{id}: Update mail schedule

### Environment Variables

- `DATABASE_URL`: Connection string for the PostgreSQL database

### Notes

- Ensure the PostgreSQL service is running and accessible.
- Prisma migrations are automatically applied when the app starts.
