import threading
import time
from typing import Any

from loguru import logger

from scriptman.powers.service._service import Service


class FastAPIService(Service):
    """⚙️ Service for running a FastAPI application"""

    def __init__(
        self,
        name: str,
        app_path: str,
        host: str = "0.0.0.0",
        port: int = 8000,
        workers: int = 1,
        **kwargs: dict[str, Any],
    ):
        """
        Initialize a FastAPI service

        Args:
            name: Service name
            app_path: Path to the FastAPI application (e.g., "myapp.main:app")
            host: Host to bind the server to
            port: Port to bind the server to
            workers: Number of worker processes
        """
        super().__init__(name, **kwargs)
        self.app_path = app_path
        self.host = host
        self.port = port
        self.workers = workers
        self._process = None

    def run(self) -> None:
        """Run the FastAPI application using uvicorn"""
        try:
            # Import inside the method to avoid dependency issues if uvicorn isn't installed
            import uvicorn

            # Run the server
            config = uvicorn.Config(
                app=self.app_path,
                host=self.host,
                port=self.port,
                workers=self.workers,
                log_level="info",
            )
            server = uvicorn.Server(config)

            # Set up a function to monitor the stop event
            def check_stop():
                while not self._stop_event.is_set():
                    time.sleep(1)
                server.should_exit = True

            monitor_thread = threading.Thread(target=check_stop)
            monitor_thread.daemon = True
            monitor_thread.start()

            # Start the server
            server.run()

        except Exception as e:
            logger.error(f"Error starting FastAPI service {self.name}: {e}")
            raise
