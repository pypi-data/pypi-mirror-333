from abc import ABC, abstractmethod
from threading import Event, Thread
from typing import Optional

from loguru import logger

from scriptman.powers.service._models import ServiceStatus


class Service(ABC):
    """⚙ Base class for all services that can be managed by Scriptman"""

    def __init__(self, name: str):
        self.name = name
        self._stop_event = Event()
        self.status = ServiceStatus.STOPPED
        self.thread: Optional[Thread] = None

    def start(self) -> bool:
        """🚀 Start the service in a separate thread"""
        if self.status == ServiceStatus.RUNNING:
            logger.warning(f"Service {self.name} is already running")
            return False

        self.status = ServiceStatus.STARTING
        self._stop_event.clear()
        self.thread = Thread(target=self._run_service)
        self.thread.daemon = True
        self.thread.start()
        return True

    def stop(self) -> bool:
        """🛑 Stop the service"""
        if self.status != ServiceStatus.RUNNING:
            logger.warning(f"Service {self.name} is not running")
            return False

        self.status = ServiceStatus.STOPPING
        self._stop_event.set()
        return True

    def _run_service(self) -> None:
        """🔄 Internal method to run the service"""
        try:
            self.status = ServiceStatus.RUNNING
            logger.info(f"Service {self.name} started")
            self.run()
            self.status = ServiceStatus.STOPPED
        except Exception as e:
            logger.error(f"Error in service {self.name}: {e}")
            self.status = ServiceStatus.ERROR

    @abstractmethod
    def run(self) -> None:
        """🔄 Override this method in subclasses to implement service behavior"""
        raise NotImplementedError("Service subclasses must implement run method")
