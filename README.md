# OHLC WebSocket API

This project implements a Django application with WebSocket support to provide OHLC (Open, High, Low, Close) data for a given symbol and timeframe. It uses Django Channels for WebSocket communication and integrates Redis for asynchronous task handling.

## Features

- **WebSocket API**: Real-time OHLC data retrieval via WebSocket connections.
- **Django Channels**: Asynchronous WebSocket handling.
- **Redis**: Backend for message brokering and caching.
- **DRF-yasg**: Swagger documentation for API endpoints.
- **Dockerized Environment**: Run the application and dependencies in isolated containers.

## Prerequisites

Ensure you have the following installed:

- Docker & Docker Compose
- Python 3.8+
- Redis

## Project Structure

```
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── trading
│   ├── consumers.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
└── README.md
```

## Installation

1. Clone the repository:

```bash
$ git clone https://github.com/meissasoft/ots-capital-dj.git
$ cd ots-capital-dj
```

2. Build and run the Docker containers:

```bash
$ docker-compose up --build
```

This will spin up the Django application and Redis server.

## Usage

### REST API

- **`/save_quotes/`**
  - **Method:** `POST`
  - **Description:** Saves quote data from the WebSocket.
  - **Payload Example:**
    ```json
    {
      "api_url": "wss://example.com/OnQuote?id=123"
    }
    ```
  - **Response Example:**
    ```json
    {
      "message": "Started consuming quotes"
    }
    ```

### WebSocket Endpoint

To connect to the WebSocket API, use the endpoint:

```
ws://localhost:8000/ws/ohlc/
```

#### Example WebSocket Message:

**Request:**
```json
{
  "symbol": "AAPL",
  "timeframe": "1m"
}
```

**Response:**
```json
{
  "data": [
    {
      "timestamp": "2024-12-30T12:00:00Z",
      "open": 150.0,
      "high": 155.0,
      "low": 149.5,
      "close": 154.0,
      "volume": 10000
    }
  ]
}
```

### API Documentation

Visit the Swagger UI documentation at:

```
http://localhost:8000/
```

## Development

### Environment Variables

Define environment variables in your Docker Compose file or local `.env` file. Key variables:

- `REDIS_HOST`: Redis hostname (default: `redis`)
- `REDIS_PORT`: Redis port (default: `6379`)

### Example Code

#### JavaScript Client:

```javascript
const socket = new WebSocket('ws://localhost:8000/ws/ohlc/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received OHLC data:', data);
};

socket.onopen = function(event) {
    socket.send(JSON.stringify({ symbol: 'AAPL', timeframe: '1m' }));
};
```

## Deployment

1. Build the Docker image:

```bash
$ docker-compose build
```

2. Run the containers:

```bash
$ docker-compose up
```

3. Ensure the application is accessible at `http://localhost:8000`.

