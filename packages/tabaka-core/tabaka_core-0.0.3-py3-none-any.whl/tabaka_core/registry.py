from typing import Dict, Any, List
from tabaka_core.config import (
    BaseLanguageConfig,
    PythonLanguageConfig,
    JavaScriptLanguageConfig,
    RustLanguageConfig,
    GoLanguageConfig,
    JavaLanguageConfig,
)
from docker.models.containers import Container
from typing import Set, Dict, Optional


class LanguageRegistry:
    def __init__(self):
        self.languages: Dict[str, BaseLanguageConfig] = {
            "python": PythonLanguageConfig(),
            # "javascript": JavaScriptLanguageConfig(),
            # "rust": RustLanguageConfig(),
            "go": GoLanguageConfig(),
            # "java": JavaLanguageConfig(),
        }

    def register_language(self, language: BaseLanguageConfig):
        self.languages[language.name] = language

    def get_language(self, name: str) -> BaseLanguageConfig:
        return self.languages.get(name)


class ContainerRegistry:
    def __init__(self):
        self.containers: Dict[str, Container] = {}
        self.available_containers: Set[str] = set()
        self.container_packages: Dict[str, Set[str]] = {}
        self.container_languages: Dict[str, str] = {}
        self.container_metadatas: Dict[str, Dict[str, Any]] = {}

    def register_container(
        self, container: Container, language_config: BaseLanguageConfig
    ):
        self.containers[container.id] = container
        self.available_containers.add(container.id)
        self.container_packages[container.id] = set()
        self.container_languages[container.id] = language_config.id
        self.container_metadatas[container.id] = {
            "language_config": language_config.model_dump(
                include={"id", "name", "version", "base_image", "description"}
            ),
        }

    def list_containers(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": container_id,
                "language_config": self.container_metadatas[container_id][
                    "language_config"
                ],
            }
            for container_id in self.available_containers
        ]

    def remove_container(self, container_id: str):
        del self.containers[container_id]
        self.available_containers.remove(container_id)
        del self.container_packages[container_id]
        del self.container_languages[container_id]
        del self.container_metadatas[container_id]
