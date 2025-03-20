from typing import Any, Dict, List
from bedrocked.reporting.reported import logger


class Extension:
    """
    Base class for extensions.
    Implements lifecycle methods and dependency injection.
    """

    def __init__(self, name: str, version: str, dependencies: List[str] = None, config: Dict[str, Any] = None):
        self.name = name
        self.version = version
        self.dependencies = dependencies or []
        self.config = config or {}
        self.active = False

    def register(self):
        """
        Register the extension.
        This method can be overridden to perform setup tasks.
        """
        logger.info(f"Registering extension {self.name} (v{self.version})")
        # Dependency injection stub: load required dependencies.
        self.inject_dependencies()

    def inject_dependencies(self):
        """
        Stub for dependency injection. Validate that dependencies are met.
        """
        if self.dependencies:
            logger.info(f"Injecting dependencies for {self.name}: {self.dependencies}")
        # TODO: integrate with a dependency resolver.

    def activate(self):
        """Activate the extension."""
        self.active = True
        logger.info(f"Activating extension {self.name}")

    def deactivate(self):
        """Deactivate the extension."""
        self.active = False
        logger.info(f"Deactivating extension {self.name}")

    def execute(self, *args, **kwargs):
        """
        The main execution method for the extension.
        This should be overridden by subclasses.
        """
        raise NotImplementedError("Extensions must implement the execute method.")
