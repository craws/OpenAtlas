# Installing OpenAtlas with Docker (Experimental)

**Important:** The Docker setup for OpenAtlas is currently experimental and **not recommended for production environments.** It is primarily intended for local development and testing. Expect potential instability or data loss. Use at your own risk.

## Prerequisites

Before you begin, ensure you have the following installed and configured:

1.  **Git:** Required to clone the OpenAtlas repository.
    * Install Git: [https://git-scm.com/book/en/v2/Getting-Started-Installing-Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2.  **Docker and Docker Compose:**
    * **Linux:** Docker Engine and the Docker Compose plugin (V2 command `docker compose`). See Linux installation steps below.
    * **Windows:** Docker Desktop. See Windows installation steps below.
3.  **Operating System:**
    * **Linux:** A modern distribution (e.g., Debian 11+,).
    * **Windows:** Windows 10/11 64-bit: Pro, Enterprise, or Education. Windows Home edition *requires* WSL 2 to be enabled and used as the Docker Desktop backend.

## Docker Installation

Follow the instructions for your operating system.

### Linux

1.  **Install Docker Engine:** Follow the official Docker guide for your specific distribution. **Using the official Docker repository is highly recommended** over default distribution packages (like `docker.io` on Debian/Ubuntu).
    * Debian: [https://docs.docker.com/engine/install/debian/](https://docs.docker.com/engine/install/debian/)
    * Other distributions: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
2.  **Install Docker Compose Plugin:** The `docker compose` V2 command (without a hyphen) is required. It's usually included when installing `docker-ce` from the official repository. Verify with `docker compose version`. If not present, follow the Docker Compose installation guide: [https://docs.docker.com/compose/install/linux/](https://docs.docker.com/compose/install/linux/)
3.  **!!! Manage Docker as a non-root user (CRITICAL POST-INSTALL STEP) !!!**
    * To run Docker commands without `sudo` and avoid permission errors when interacting with the Docker daemon socket, add your user to the `docker` group:
        ```bash
        sudo usermod -aG docker ${USER}
        ```
    * **IMPORTANT:** You **must log out and log back in** (or restart your system) for this group change to take effect! You can verify group membership with the `groups` command after logging back in.
4.  **Start and Enable Docker Service:**
    ```bash
    sudo systemctl start docker
    sudo systemctl enable docker # Optional: Start Docker automatically on system boot
    ```
5.  **Verify Installation:** Check that Docker Engine and Compose are installed correctly:
    ```bash
    docker --version
    docker compose version
    # Test running a simple container (should run without sudo after login/logout)
    docker run hello-world
    ```

### Windows

1.  **Install Docker Desktop:** Download and install Docker Desktop for Windows from the official website:
    * [https://docs.docker.com/desktop/install/windows-install/](https://docs.docker.com/desktop/install/windows-install/)
2.  **Enable WSL 2 Backend (Recommended):** Docker Desktop works best with the Windows Subsystem for Linux version 2 (WSL 2). It's the default for new installations, but ensure it's enabled in Docker Desktop settings (Settings > General > "Use the WSL 2 based engine").
    * If you need to install or enable WSL 2 itself, follow Microsoft's guide: [https://learn.microsoft.com/en-us/windows/wsl/install](https://learn.microsoft.com/en-us/windows/wsl/install)
3.  **Docker Compose Included:** Docker Desktop includes the `docker compose` command. No separate installation is needed.
4.  **Verify Installation:** Check the Docker Desktop dashboard shows it's running ("Docker Desktop is running"). You can also open a terminal (Command Prompt, PowerShell, or a WSL terminal) and run:
    ```powershell
    docker --version
    docker compose version
    docker run hello-world
    ```

## Running OpenAtlas

1.  **Clone the Repository:**
    Open your terminal or command prompt, navigate to where you want to store the project (e.g., `C:\projects` or `~/dev`), and run:
    ```bash
    git clone https://github.com/craws/OpenAtlas.git
    cd OpenAtlas # Navigate into the cloned directory
    ```

2.  **Set Environment Variables:**
    OpenAtlas requires database credentials, which are passed via a `.env` file in the project's root directory (the same directory as `docker-compose.yaml`).

    * Windows (Cmd):
        ```cmd
        (echo POSTGRES_DB=openatlas & echo POSTGRES_PASSWORD=openatlas) > .env
        ```
    * Linux or Windows (PowerShell/Git Bash):
        ```bash
        printf "POSTGRES_DB=openatlas\nPOSTGRES_PASSWORD=openatlas\n" > .env
        ```
    * **Warning:** The password `openatlas` is insecure and only suitable for local enviroment. **Do not** use this password in any shared or production-like environment.

3.  **Pull Latest Images (Optional but Recommended):**
    Ensure you have the latest versions of pre-built images like PostGIS and Discovery (check `docker-compose.yaml` for exact image names/tags):
    ```bash
    docker compose pull
    ```

4.  **Start the Docker Containers:**
    In your terminal, ensure you are inside the `OpenAtlas` project directory, then run:
    ```bash
    docker compose up --detach
    ```
    * `--detach` (or `-d`) runs the containers in the background.
    * **First Run:** The first time you run this command, it will take significantly longer. Docker needs to:
        * Download base images.
        * Build the custom OpenAtlas images (`openatlas`, `initdb`, `discovery` if applicable) based on their Dockerfiles.
        * Start the PostgreSQL container and wait for it to be healthy.
        * Run the `initdb` service to create the database structure and initial data (only if the database is empty).
        * Start the OpenAtlas and Discovery application containers.

5.  **Monitor Logs (Especially on First Run):**
    It's highly recommended to watch the logs during the first startup to see the progress and catch any errors:
    ```bash
    # View and follow logs from all services (press Ctrl+C to stop)
    docker compose logs -f

    # View logs from a specific service (useful for debugging)
    docker compose logs -f initdb     # Database initialization
    docker compose logs -f postgres   # PostgreSQL database logs
    docker compose logs -f openatlas  # OpenAtlas backend application logs
    docker compose logs -f discovery  # OpenAtlas Discovery frontend logs
    ```

## Accessing the Applications

Once the containers are up and running (check `docker compose ps` shows services as "running" or "healthy", you can access the applications in your web browser:

* **OpenAtlas Backend/UI:** [http://localhost:8080](http://localhost:8080)
* **OpenAtlas Discovery Frontend:** [http://localhost:3000](http://localhost:3000) (If included in your `docker-compose.yaml`)

## Initial Login and Setup

* Log into the OpenAtlas UI ([http://localhost:8080](http://localhost:8080)) using the default administrator credentials:
    * Username: `OpenAtlas`
    * Password: `change_me_PLEASE!`
* **IMPORTANT: Change the default administrator password immediately** in your user profile settings for security. Follow any other initial setup steps prompted by the application.

## Stopping the Application

* To stop and remove the containers, networks, and volumes defined in the compose file, navigate to the `OpenAtlas` project directory in your terminal and run:
    ```bash
    docker compose down
    ```
    This stops the application but preserves persistent data stored in bind mounts (like `./data/db`).
* To also remove *named* Docker volumes if any were defined (check your `docker-compose.yaml`):
    ```bash
    docker compose down -v
    ```
    **Note:** This command does **not** delete data in host *bind mounts* like the `./data/db` directory used by default for PostgreSQL data.

## Troubleshooting and Maintenance

* **Permission Denied (Linux):** If you encounter `permission denied while trying to connect to the Docker daemon socket` errors, double-check that you have added your user to the `docker` group and **logged out and back in** (see Linux installation Step 3).
* **Check Container Status:** Use `docker compose ps` to see which services are running, stopped, or unhealthy.
* **Check Logs:** Use `docker compose logs -f [SERVICE_NAME]` (e.g., `docker compose logs -f openatlas`) to view logs for specific services and diagnose issues.
* **Rebuild Custom Images:** If you modify code that requires rebuilding the custom Docker images (e.g., changes in the application source code included in the Dockerfile build context, or changes to the Dockerfile itself):
    ```bash
    # Rebuild images using Docker's build cache (faster)
    docker compose build

    # Rebuild images without using the cache (more thorough, slower)
    docker compose build --no-cache
    ```
    After rebuilding, restart the services, applying the changes and recreating containers:
    ```bash
    docker compose up -d --force-recreate
    ```
* **Reset the Database:** To completely wipe the database and force re-initialization using the `initdb` service or a dump file on the next startup:
    1.  **Stop the services:** `docker compose down`
    2.  **Manually delete the database directory on your host machine:**
        ```bash
        # WARNING: This permanently deletes all database data!
        rm -rf ./data/db # Linux/macOS/Git Bash
        ```
    3.  Restart the services: `docker compose up -d`. The `postgres` container will start with an empty data directory, triggering the initialization process.

## Restoring a Database Dump

To initialize the database from an existing SQL dump file (`.sql`) instead of using the default `initdb` scripts provided in `./install/`:

1.  **Stop Containers:** Ensure services are stopped:
    ```bash
    docker compose down
    ```
2.  **Clean Database Directory:** Make sure no previous database exists, as the PostgreSQL entrypoint scripts only run initialization procedures when the data directory is empty. **Delete the host directory:**
    ```bash
    # WARNING: Permanently deletes any existing DB data! Use with caution.
    rm -rf ./data/db # Linux/macOS/Git Bash
    # or delete manually/use rmdir/Remove-Item on Windows (see "Reset" section)
    ```
3.  **Place Dump File:** Copy or move your `.sql` dump file to a location accessible by the Docker build context, for example, inside the project directory like `./files/export/my_database_dump.sql`.
4.  **Modify `docker-compose.yaml`:**
    * Open the `docker-compose.yaml` file in a text editor.
    * Locate the `postgres` service definition.
    * Inside its `volumes:` section:
        * **Ensure the database data volume is present:** `- ./data/db:/var/lib/postgresql/data`
        * **Comment out** any lines that mount individual SQL files from `./install/` into `/docker-entrypoint-initdb.d/`. For example:
            ```yaml
            # - ./install/0_extensions.sql:/docker-entrypoint-initdb.d/0_extensions.sql
            # - ./install/1_structure.sql:/docker-entrypoint-initdb.d/1_structure.sql
            # - ./install/2_data_model.sql:/docker-entrypoint-initdb.d/2_data_model.sql
            # ... etc ...
            ```
        * **Add or uncomment** a line to mount your *single dump file* into the init directory. Adjust the *host path* (before the colon) to point to your actual dump file:
            ```yaml
            volumes:
              - ./data/db:/var/lib/postgresql/data
              # Ensure lines like the ones above are commented out
              # Mount your dump file:
              - ./files/export/my_database_dump.sql:/docker-entrypoint-initdb.d/dump.sql
            ```
            *(Replace `./files/export/my_database_dump.sql` with the actual path to your dump file relative to the `docker-compose.yaml` file, or provide an absolute path)*. The name inside the container (`dump.sql`) doesn't matter as much as long as it ends with `.sql`, `.sql.gz`, or `.sh`.
5.  **Start Docker Compose:**
    Start the services. The PostgreSQL container will detect the empty data directory and execute the script(s) found in `/docker-entrypoint-initdb.d/` alphabetically.
    ```bash
    docker compose up -d
    ```
    Monitor the PostgreSQL logs (`docker compose logs -f postgres`) to check the import progress and watch for any errors during the restore process. This might take a while for large dump files.
