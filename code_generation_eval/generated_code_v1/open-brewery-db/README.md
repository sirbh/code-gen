# OpenBreweryDB API

This is a simple OpenBreweryDB API built with Node.js, Express.js, and Prisma ORM. It connects to a PostgreSQL database and is containerized using Docker and docker-compose.

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

- GET /breweries: Retrieve all breweries
- GET /breweries/{id}: Retrieve a brewery by ID
- GET /breweries/search: Search for breweries
- GET /breweries/autocomplete: Autocomplete brewery names
- GET /breweries/random: Retrieve a random brewery

### Environment Variables

- `DATABASE_URL`: Connection string for the PostgreSQL database

### Notes

- Ensure the PostgreSQL service is running and accessible.
- Prisma migrations are automatically applied when the app starts.
