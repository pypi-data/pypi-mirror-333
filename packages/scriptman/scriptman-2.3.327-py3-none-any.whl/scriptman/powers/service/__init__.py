from scriptman.core.config import config
from scriptman.powers.service._manager import ServiceManager
from scriptman.powers.service._models import ServiceStatus
from scriptman.powers.service._service import Service

# Add the ServiceManager singleton instance to the Config class
service_manager = ServiceManager()
object.__setattr__(config, "service_manager", service_manager)
__all__: list[str] = ["service_manager", "Service", "ServiceManager", "ServiceStatus"]
