import argparse
import logging

from http import HTTPStatus
from numbers import Number
from typing import Any

import requests

from django.core.management.base import BaseCommand
from ping3 import ping


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Finds the fastest node in the federation network"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--show-hops",
            action="store_true",
            help="Display intermediate nodes in the route",
        )

    def handle(self, *_args: list[Any], **_: dict[str, str | Number]) -> str:
        test_servers = [
            "http://localhost:8081",
            "http://localhost:8082",
            "http://localhost:8083",
        ]

        server_metrics = {}
        for server in test_servers:
            try:
                response = requests.get(f"{server}/healthcheck", timeout=5)
                if response.status_code == HTTPStatus.OK:
                    server_metrics[server] = {
                        "ping": ping(server.split("://")[1].split(":")[0]),
                        "health": response.json(),
                    }
            except (requests.RequestException, ValueError):
                logger.exception("Failed to get metrics from {server}")
                continue

        if not server_metrics:
            msg = "No healthy servers found"
            raise RuntimeError(msg)

        return self.select_best_server(server_metrics)
