from enum import Enum


class ServiceStatus(Enum):
    STARTING = "starting"
    STOPPING = "stopping"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
