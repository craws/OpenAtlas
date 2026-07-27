# Installing OpenAtlas with Podman (Experimental)

**Important:** The Podman setup for OpenAtlas is currently experimental and **not recommended for production environments.** It is primarily intended for local development and testing. Expect potential instability or data loss. Use at your own risk.

*Note: Commands below use Podman; Docker and `docker compose` are expected to work identically since this project follows the standard Compose Specification.*

## Prerequisites

Before you begin, ensure you have the following installed and configured:

1.  **Git:** Required to clone the OpenAtlas repository.
    * Install Git: [https://git-scm.com/book/en/v2/Getting-Started-Installing-Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2.  **Podman:**
    * Follow upstream installation instructions: [https://podman.io/docs/installation](https://podman.io/docs/installation)

## Running OpenAtlas

1.  **Clone the Repository:**
    Open your terminal or command prompt, navigate to where you want to store the project (e.g., `C:\projects` or `~/dev`), and run:
    ```bash
    git clone https://github.com/craws/OpenAtlas.git
    cd OpenAtlas # Navigate into the cloned directory
    ```

2.  **Set Environment Variables:**
    OpenAtlas requires database credentials, which are passed via a `.env` file in the project's root directory (the same directory as `compose.yaml`).

    * Windows (cmd):
        ```cmd
        (echo POSTGRES_DB=openatlas & echo POSTGRES_PASSWORD=openatlas) > .env
        ```
    * Linux/MacOS/Windows (WSL):
        ```bash
        printf "POSTGRES_DB=openatlas\nPOSTGRES_PASSWORD=openatlas\n" > .env
        ```
    * **Warning:** The password `openatlas` is insecure and only suitable for local enviroment. **Do not** use this password in any shared or production-like environment.

3.  **Pull Latest Images (Optional but Recommended):**
    Ensure you have the latest versions of pre-built images like PostGIS and Discovery (check `compose.yaml` for exact image names/tags):
    ```bash
    podman compose pull
    ```

4.  **Start the Containers:**
    In your terminal, ensure you are inside the `OpenAtlas` project directory, then run:
    ```bash
    podman compose up --detach
    ```
    * `--detach` (or `-d`) runs the containers in the background.
    * **First Run:** The first time you run this command, it will take significantly longer. Podman needs to:
        * Download base images.
        * Build the custom OpenAtlas images (`openatlas`, `initdb`, `discovery` if applicable) based on their Containerfiles.
        * Start the PostgreSQL container and wait for it to be healthy.
        * Run the `initdb` service to create the database structure and initial data (only if the database is empty).
        * Start the OpenAtlas and Discovery application containers.

5.  **Monitor Logs (Especially on First Run):**
    It's highly recommended to watch the logs during the first startup to see the progress and catch any errors:
    ```bash
    # View and follow logs from all services (press Ctrl+C to stop)
    podman compose logs -f

    # View logs from a specific service (useful for debugging)
    podman compose logs -f initdb     # Database initialization
    podman compose logs -f postgres   # PostgreSQL database logs
    podman compose logs -f openatlas  # OpenAtlas backend application logs
    podman compose logs -f discovery  # OpenAtlas Discovery frontend logs
    ```

## Gunicorn and Nginx Variant (PoC)

An additional experimental stack is available for testing OpenAtlas behind Nginx with Gunicorn instead of Apache. It uses the same PostgreSQL, database initialization, and OpenAtlas Discovery services as the default setup.

Start this variant from the project root after setting the environment variables above:

```bash
podman compose -f compose-gunicorn.yaml up --detach
```

OpenAtlas is then available at [http://localhost:8081](http://localhost:8081). To follow the application and reverse-proxy logs, run:

```bash
podman compose -f compose-gunicorn.yaml logs -f openatlas-gunicorn
podman compose -f compose-gunicorn.yaml logs -f openatlas-nginx
```

To rebuild this variant after changing its image or application code, use:

```bash
podman compose -f compose-gunicorn.yaml build
podman compose -f compose-gunicorn.yaml up -d --force-recreate
```

Stop the Gunicorn and Nginx variant with:

```bash
podman compose -f compose-gunicorn.yaml down
```

## Accessing the Applications

Once the containers are up and running (check `podman compose ps` shows services as "running" or "healthy", you can access the applications in your web browser:

* **OpenAtlas Backend/UI:** [http://localhost:8080](http://localhost:8080)
* **OpenAtlas Discovery Frontend:** [http://localhost:3000](http://localhost:3000) (If included in your `compose.yaml`, included by default)

## Stopping the Application

To stop and remove the containers and networks defined in the compose file:
```bash
podman compose down
```
This stops the application but preserves data in named volumes (`db-data`, `openatlas-uploads`, `openatlas-resized`, `openatlas-export`).

To also remove the named volumes (deletes all database and file data — irreversible):
```bash
podman compose down -v
```

## Database Management

### Fresh Install

```bash
podman compose up --detach
```

On first run, `initdb` automatically creates the schema from the SQL scripts in `./install/`.

### Resetting the Database

```bash
podman compose down
podman volume rm openatlas_db-data
podman compose up --detach
```

### Restoring from a Dump

Requires placing an SQL file at `openatlas-initdb-1:/var/www/openatlas/files/dump.sql`.

```bash
podman compose down
podman volume rm openatlas_db-data
podman compose up --no-start
podman cp ./my_dump.sql openatlas-initdb-1:/var/www/openatlas/files/dump.sql
podman compose start
```

`initdb` detects the dump automatically and restores it instead of running the install scripts.

### Verify

```bash
podman logs openatlas-initdb-1
```

Look for `Initialization verified.` at the end.

## Troubleshooting and Maintenance

* **Check Container Status:** Use `podman compose ps` to see which services are running, stopped, or unhealthy.
* **Check Logs:** Use `podman compose logs -f [SERVICE_NAME]` (e.g., `podman compose logs -f openatlas`) to view logs for specific services and diagnose issues.
* **Rebuild Custom Images:** If you modify code that requires rebuilding the custom Container images (e.g., changes in the application source code included in the Containerfile build context, or changes to the Containerfile itself):
```bash
# Rebuild images using Podman's build cache (faster)
podman compose build

# Rebuild images without using the cache (more thorough, slower)
podman compose build --no-cache
```
After rebuilding, restart the services, applying the changes and recreating containers:
```bash
podman compose up -d --force-recreate
```
