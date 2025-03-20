from abc import ABC
from datetime import datetime

from .interface import PluginProtocol


class PluginA(PluginProtocol):
    def initialize(self, config: dict) -> None:
        pass

    def execute(self, *args, **kwargs) -> dict:
        return {
            "timestamp": datetime.now().isoformat(),
            "message": "Hello from demo plugin"
        }

    @property
    def metadata(self) -> dict:
        return {
            "name": "Demo Plugin",
            "version": "1.0.0",
            "author": "Dev Team"
        }
