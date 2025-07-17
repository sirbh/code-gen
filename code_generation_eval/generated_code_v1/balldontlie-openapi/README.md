# Balldontlie API

This is a simple API built with Node.js, Express.js, and Prisma ORM. It connects to a PostgreSQL database and is containerized using Docker and docker-compose.

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

- GET /api/v1/players: Retrieve all players
- GET /api/v1/players/{playerId}: Retrieve a player by ID
- GET /api/v1/teams: Retrieve all teams
- GET /api/v1/teams/{teamId}: Retrieve a team by ID
- GET /api/v1/games: Retrieve all games
- GET /api/v1/games/{gameId}: Retrieve a game by ID
- GET /api/v1/stats: Retrieve all stats

### Environment Variables

- `DATABASE_URL`: Connection string for the PostgreSQL database

### Notes

- Ensure the PostgreSQL service is running and accessible.
- Prisma migrations are automatically applied when the app starts.
