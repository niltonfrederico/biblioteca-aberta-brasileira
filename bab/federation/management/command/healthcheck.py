import logging

from numbers import Number
from typing import Any

import psutil

from django.core.management.base import BaseCommand
from ping3 import ping

from bab.core.dataclass import ServerNode


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fetch heathcheck data"

    def handle(self, *_args: list[Any], **_: dict[str, str | Number]) -> ServerNode:
        """
        Will return this dataclass

        @dataclass
        class ServerNode:
            id: str
            ping_ms: float
            download_speed_mbps: float
            current_load_percent: float
            priority_rank: int  # 1 is highest priority
            active_connections: int
            file_hashes: dict[str, str]
        """

        # Get local machine metrics
        ping_ms = ping("localhost", unit="ms")
        if ping_ms is None:
            ping_ms = 0.0

        # Simulate download speed test (would need actual implementation)
        download_speed_mbps = 100.0  # Example value

        # Get CPU load
        cpu_load = psutil.cpu_percent()

        # Get Django active connections using psutil
        active_conns = len(p for p in psutil.Process().children())

        # Create server node instance
        return ServerNode(
            id="localhost",
            ping_ms=float(ping_ms),
            download_speed_mbps=download_speed_mbps,
            current_load_percent=cpu_load,
            priority_rank=1,
            active_connections=active_conns,
            file_hashes={},
        )
