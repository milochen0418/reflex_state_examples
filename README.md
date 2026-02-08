# Reflex State Examples



## Getting Started

This project is managed with [Poetry](https://python-poetry.org/).

### Prerequisites

- Python 3.11.x
- Poetry


### Installation

1. Ensure Poetry uses Python 3.11:

```bash
poetry env use python3.11
poetry env info
```

2. Install dependencies:

```bash
poetry install
```

### Running the App

Start the development server:

```bash
poetry run ./reflex_rerun.sh
```

The application will be available at `http://localhost:3000`.

## Example 5: Redis Pub/Sub

Example 5 uses Redis Pub/Sub to sync state across sessions. You must have a Redis server running before opening the page.

### Quick start (macOS)

**Homebrew (recommended)**

```bash
brew install redis
brew services start redis
```

**Docker**

```bash
brew install --cask docker
docker run --name redis -p 6379:6379 -d redis
```

### Environment overrides

- `REDIS_URL` (default: `redis://localhost:6379/0`)
- `REDIS_CHANNEL` (default: `reflex:example5`)

## Documentation

- [docs/Reflex State Examples - Kid-Friendly Tutorials.pdf](docs/Reflex%20State%20Examples%20-%20Kid-Friendly%20Tutorials.pdf)

