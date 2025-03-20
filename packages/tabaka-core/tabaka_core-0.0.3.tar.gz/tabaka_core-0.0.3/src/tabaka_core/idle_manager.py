import time
from typing import Dict, Set
from docker.models.containers import Container
from threading import Lock


class ContainerIdleManager:
    def __init__(self, idle_timeout: int):
        self.idle_timeout = idle_timeout
        self.container_activities: Dict[str, float] = {}
        self.idle_containers: Set[str] = set()
        self._lock = Lock()

    def add_container(self, container: Container):
        with self._lock:
            self.container_activities[container.id] = time.time()

    def record_activity(self, container_id: str) -> None:
        with self._lock:
            self.container_activities[container_id] = time.time()

    def check_idle(self) -> bool:
        """
        Check if any container has been idle for more than the idle timeout

        Returns:
            bool: True if any container has been idle for more than the idle timeout, False otherwise
        """
        with self._lock:
            for container_id, last_activity in self.container_activities.items():
                if time.time() - last_activity > self.idle_timeout:
                    self.idle_containers.add(container_id)

        return False

    def check_container_idle(self, container_id: str) -> bool:
        """
        Check if a container is idle

        Args:
            container_id (str): The ID of the container to check

        Returns:
            bool: True if the container is idle, False otherwise
        """
        with self._lock:
            return container_id in self.idle_containers
