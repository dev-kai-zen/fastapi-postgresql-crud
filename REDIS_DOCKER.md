# Redis with Docker (custom host port)

Redis listens on **6379** inside the container by default. If something on your machine already uses **6379** (another Redis, another container mapping, etc.), publish Redis on a **different host port** (for example **6380**).

Mapping is always: **`<host_port>:<container_port>`** → typically **`6380:6379`**.

---

## Step 1 — Pick a free host port

To see which ports are listening:

_Terminal_

```
# On Linux or macOS:
sudo lsof -iTCP -sTCP:LISTEN -Pn

# On Windows (Command Prompt):
netstat -ano | findstr LISTENING

# Check the default Redis port on the host (change command for your OS):

# On Linux:
sudo ss -ltnp | grep ':6379'

# On macOS:
sudo lsof -iTCP:6379 -sTCP:LISTEN -Pn

# On Windows (Command Prompt):
netstat -ano | findstr :6379
```

Choose an unused port, for example:

- `6380`

The examples below use **`6380`**. Replace it if that port is taken.

---

## Step 2 — Run Redis in Docker

The **container** listens on **6379**; your **host** uses **6380**.

```bash
docker run --name app-redis \
  -p 6380:6379 \
  -d redis:7-alpine
```

| Flag / arg         | Purpose                                   |
| ------------------ | ----------------------------------------- |
| `--name app-redis` | Stable name for start/stop/logs           |
| `-p 6380:6379`     | **Host 6380** → **container 6379**        |
| `-d`               | Run in background                         |
| `redis:7-alpine`   | Official image (adjust tag if you prefer) |

This starts Redis **without a password** (fine for **local dev only**). See [Optional: password](#optional-password-local-dev-or-staging) for `--requirepass`.

---

## Step 3 — Confirm (and start if needed) the container

```bash
docker ps --filter name=app-redis
```

If it is stopped:

```bash
docker start app-redis
docker ps --filter name=app-redis
```

You should see something like `0.0.0.0:6380->6379/tcp`.

---

## Step 4 — Test a connection

**Inside the container** (always works if Redis is up):

```bash
docker exec -it app-redis redis-cli ping
```

Expected:

```text
PONG
```

**From the host** (same port your FastAPI app will use), if `redis-cli` is installed:

```bash
redis-cli -h127.0.0.1 -p 6380 ping
```

Expected: `PONG`.

---

## Step 5 — Application URL (`.env`)

Most Python clients use a URL like:

```text
redis://HOST:PORT/DB_INDEX
```

With the run command above, in `.env`:

```env
REDIS_URL=redis://localhost:6380/0
```

- **`6380`** is the **host** side of `-p 6380:6379`.
- **`/0`** is logical database index `0` (default).

Read this value in FastAPI with Pydantic `BaseSettings` (or similar) as a **plain string**; do not rely on `${VAR}` expansion inside `REDIS_URL` unless your loader supports it (same idea as `DATABASE_URL` in [POSTGRES_DOCKER.md](POSTGRES_DOCKER.md)).

---

### How to use it from FastAPI (overview)

1. Install a client, for example: `pip install redis`.
2. On startup or per request, create a client with the URL from settings, for example `redis.from_url(settings.redis_url)`.
3. Call `ping()` or `get` / `set` as needed.

---

## Step 6 — Stop and start later

```bash
docker stop app-redis
docker start app-redis
```

Logs:

```bash
docker logs -f app-redis
```

---

## Step 7 — Remove the container

**Data in memory is lost** when the container is removed unless you used persistence (volume + AOF/RDB below).

```bash
docker stop app-redis
docker rm app-redis
```

### Optional: persistence (named volume)

Keep data across container recreation. Use your `.env` file values for ports, for example `${REDIS_PUBLISH_PORT}`.

```bash
docker run --name app-redis \
  -p ${REDIS_PUBLISH_PORT: -6380}:6379 \
  -v fastapi_redisdata:/data \
  redis:7-alpine \
  redis-server --appendonly yes
```

The `:-default` syntax applies only if the variable is unset or empty; override everything in `.env` for a single source of truth.

Make sure your `.env` file (next to your compose file or in your shell session) contains:

```env
REDIS_PUBLISH_PORT=6380
REDIS_URL=redis://localhost:6380/0
```

This way, you can reuse the same port number everywhere by changing it in one place.

---

## Optional: password (local dev or staging)

The official image has no `REDIS_PASSWORD` env like Postgres. Pass a config flag:

```bash
docker run --name app-redis \
  -p ${REDIS_PUBLISH_PORT: -6380}:6379 \
  -d redis:7-alpine \
  redis-server --requirepass yoursecret
```

URL form:

```text
redis://:yoursecret@localhost:6380/0
```

(URL-encode the password if it contains special characters.)

---

## Optional: `docker compose` with `.env`

Add a **second service** next to your Postgres service in `docker-compose.yaml`, or use a dedicated compose file.

### Variables (in `.env`, next to the compose file)

Compose substitutes `${VAR}` in the YAML when you run `docker compose` from that directory.

| Variable             | Purpose                                                      |
| -------------------- | ------------------------------------------------------------ |
| `REDIS_PUBLISH_PORT` | **Host** port mapped to container **6379** (example: `6380`) |

Example `.env` entries (copy from [.env.example](.env.example) and edit):

```env
REDIS_PUBLISH_PORT=6380
REDIS_URL=redis://localhost:6380/0
```

### Example `docker-compose.yaml` fragment

```yaml
services:
  redis:
    image: redis:7-alpine
    container_name: app-redis
    ports:
      - "${REDIS_PUBLISH_PORT:-6380}:6379"
    volumes:
      - fastapi_redisdata:/data
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD:-yoursecret}

volumes:
  fastapi_redisdata:
```

If no password, just remove (`--requirepass ${REDIS_PASSWORD:-yoursecret}`):

- command: redis-server --appendonly yes

/\*

- To use a password, set REDIS_PASSWORD in your `.env`:
  REDIS_PASSWORD=yourpassword
- Compose will substitute it into the container start command.
  \*/

If this `volumes:` block duplicates an existing top-level `volumes:` from Postgres, **merge** them under one `volumes:` key at the bottom of the file.

### Commands

```bash
docker compose up -d
```

Start only Redis:

```bash
docker compose up -d redis
```

---

## Quick reference

| Where            | Port                               |
| ---------------- | ---------------------------------- |
| Inside container | `6379` (default Redis)             |
| On your machine  | Whatever you chose (e.g. `6380`)   |
| In `REDIS_URL`   | **Host** port (`6380`), not `6379` |

If connection fails, check: container is running, `-p` mapping, firewall, and that your app uses **`localhost` + host port** when running **on the host** (not `6379` unless you published that).
