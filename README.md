# Sales Engine API

This project provides a FastAPI-based API for ingesting and analyzing sales data. The application is designed for easy deployment and testing, using PostgreSQL as the database backend. The entire setup is containerized with Docker and managed via Docker Compose.

## Project Overview

- **Data Ingestion**: Accepts and validates sales data via an API endpoint.
- **Real-time Feedback**: Provides sales category insights without direct SQL aggregation.
- **Batch Analytics**: Includes SQL queries for deeper analysis of country contributions, top trading relationships, and repeat buyer trends.

## Data Model

The project uses two tables:

### Sales Table

```sql
CREATE TABLE sales (
    ID_ORDER STRING NOT NULL,
    ID_PRODUCT STRING NOT NULL,
    ID_BUYER STRING NOT NULL,
    ID_SELLER STRING NOT NULL,
    ID_SELLER_COUNTRY STRING NOT NULL,
    ID_BUYER_COUNTRY STRING NOT NULL,
    DATE_PAYMENT TIMESTAMP NOT NULL,
    BRAND STRING,
    CATEGORY STRING,
    REVENUE FLOAT64 NOT NULL
);
```

### Country Table

```sql
CREATE TABLE country (
    ID_COUNTRY STRING NOT NULL PRIMARY KEY,
    COUNTRY_NAME STRING NOT NULL,
    CONTINENT STRING
);
```

## API Endpoints

### 1. Data Ingestion

- **Endpoint**: `POST /ingest`
- **Description**: Accepts and validates a JSON payload representing a sales event.
- **Example Request**:

  ```json
  {
      "ID_ORDER": "34033734",
      "ID_PRODUCT": "13681706",
      "ID_BUYER": "9666775",
      "ID_SELLER": "6723223",
      "ID_SELLER_COUNTRY": "203",
      "ID_BUYER_COUNTRY": "170",
      "DATE_PAYMENT": "2021-01-07 00:09:24",
      "BRAND": "Dsquared2",
      "CATEGORY": "clothing",
      "REVENUE": 57.27
  }
  ```

### 2. Real-time Feedback

- **Endpoint**: `GET /feedback`
- **Description**: Returns the total revenue per sales category for the top three most common sales categories.
- **Note**: Aggregation is done without using direct SQL queries.

## Batch Analytics (SQL Queries)

Stored in the `queries/` directory:

1. **`country_contribution.sql`**: Computes each country's percentage contribution to total sales and item count.
2. **`top_country_relationships.sql`**: Identifies the two countries with the highest combined revenue.
3. **`repeat_buyer_revenue.sql`**: Compares total revenue from repeat buyers between the first and second weeks of January 2021.

## Setup and Deployment

### Prerequisites

Ensure the following are installed:

- Docker
- Docker Compose

### Running the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/kkuznets/sales-engine-api.git
   cd sales-engine-api
   ```

2. Create a `.env` file with the necessary environment variables:

   ```env
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=sales
    DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/sales
    PGADMIN_DEFAULT_EMAIL=admin@pgadmin.org
    PGADMIN_DEFAULT_PASSWORD=admin
   ```

3. Build and run the Docker containers:

   ```bash
   docker-compose up --build
   ```

   This will:
   - Start the FastAPI application
   - Initialize a PostgreSQL database
   - Apply database migrations (Alembic)

4. Access the API:
   - FastAPI Docs: [Swagger UI](http://0.0.0.0:8000/docs) | [ReDoc](http://0.0.0.0:8000/redoc)

### Miscellaneous Commands

- Initialize the virtual environment:

   ```bash
    uv sync && source .venv/bin/activate
   ```

- Add new Alembic migrations:

   ```bash
    docker-compose run web uv run alembic revision --autogenerate -m "migration message"
   ```

    This will create a new migration file based on the current database schema and apply the changes.

## Design Decisions

- **PostgreSQL**: Chosen for scalability and reliability.
- **FastAPI & SQLModel**: Used for performance and ease of schema management.
- **Docker**: Ensures consistent development and deployment environments.
- **Alembic**: Handles database migrations.
- **Input Validation**: Implemented using SQLModel. Added extra validation for sale category field to accept only predefined values.

## Future Enhancements

- Implement authentication and authorization.
- Add unit and integration tests.
- Improve logging and monitoring.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
