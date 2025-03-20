from signal import SIGINT, SIGTERM, signal
from typing import Any, Optional

from loguru import logger

from scriptman.powers.service._service import Service


class ServiceManager:
    """🔄 Manages multiple services within Scriptman"""

    _initialized: bool = False
    _instance: Optional["ServiceManager"] = None

    def __new__(cls, *args: Any, **kwargs: dict[str, Any]) -> "ServiceManager":
        if cls._instance is None:
            cls._instance = super(ServiceManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        self.services: dict[str, Service] = {}
        self._initialized = True

        # Set up signal handlers for graceful shutdown
        signal(SIGINT, self._handle_shutdown)
        signal(SIGTERM, self._handle_shutdown)

    def register_service(self, service: Service) -> None:
        """🔄 Register a service with the manager"""
        if service.name in self.services:
            logger.warning(f"Service {service.name} already registered")
            return

        self.services[service.name] = service
        logger.info(f"Registered service: {service.name}")

    def start_service(self, name: str) -> bool:
        """🔄 Start a registered service by name"""
        if name not in self.services:
            logger.error(f"Service {name} not found")
            return False

        return self.services[name].start()

    def stop_service(self, name: str) -> bool:
        """🛑 Stop a registered service by name"""
        if name not in self.services:
            logger.error(f"Service {name} not found")
            return False

        return self.services[name].stop()

    def start_all(self) -> None:
        """🔄 Start all registered services"""
        for name in self.services:
            self.start_service(name)

    def stop_all(self) -> None:
        """🛑 Stop all registered services"""
        for name in self.services:
            self.stop_service(name)

    def _handle_shutdown(self, signum: int, frame: Any) -> None:
        """🔄 Handle shutdown signals"""
        logger.info("Shutdown signal received, stopping all services...")
        self.stop_all()
