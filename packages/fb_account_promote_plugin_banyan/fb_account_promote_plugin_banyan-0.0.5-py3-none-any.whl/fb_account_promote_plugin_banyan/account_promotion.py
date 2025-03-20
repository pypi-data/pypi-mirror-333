from abc import ABC
from datetime import datetime

from .interface import PluginProtocol


class PluginA(PluginProtocol, ABC):
    def initialize(self, config: dict) -> None:
        pass

    def execute(self, *args, **kwargs) -> dict:
        return {
            "timestamp": datetime.now().isoformat(),
            "message": "Hello from demo plugin"
        }
