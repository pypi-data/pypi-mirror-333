from scriptman.powers.service import Service


class ScriptService(Service):
    """Service for running a Python script as a background service"""

    def __init__(self, name: str, script_path: Path, **kwargs):
        """
        Initialize a script service

        Args:
            name: Service name
            script_path: Path to the Python script
        """
        super().__init__(name, **kwargs)
        self.script_path = script_path

    def run(self) -> None:
        """Run the script in a separate module namespace"""
        try:
            # Add the script's directory to the Python path
            script_dir = str(self.script_path.parent)
            if script_dir not in sys.path:
                sys.path.insert(0, script_dir)

            # Load the script as a module
            spec = importlib.util.spec_from_file_location(
                f"scriptman_service_{self.name}", self.script_path
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Check if the module has a run_as_service function
                if hasattr(module, "run_as_service"):
                    module.run_as_service(stop_event=self._stop_event)
                else:
                    # If no run_as_service function is defined, wait until the stop event is set
                    logger.warning(
                        f"No run_as_service function found in {self.script_path}"
                    )
                    while not self._stop_event.is_set():
                        time.sleep(1)
            else:
                raise ImportError(f"Could not load module from {self.script_path}")

        except Exception as e:
            logger.error(f"Error running script service {self.name}: {e}")
            raise


class SchedulerService(Service):
    """Service for running the APScheduler scheduler"""

    def __init__(self, name: str, **kwargs):
        """Initialize a scheduler service"""
        super().__init__(name, **kwargs)

    def run(self) -> None:
        """Run the scheduler service"""
        try:
            from scriptman.core.config import config

            # The scheduler is already started when imported, just wait until stop event
            logger.info(f"Scheduler service {self.name} is running")
            while not self._stop_event.is_set():
                time.sleep(1)

            # Shutdown gracefully
            config.scheduler.__scheduler.shutdown()

        except Exception as e:
            logger.error(f"Error in scheduler service {self.name}: {e}")
            raise


__all__: list[str] = ["FastAPIService", "ScriptService", "SchedulerService"]
