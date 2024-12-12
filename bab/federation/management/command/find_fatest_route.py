import argparse
import logging
import time

from numbers import Number
from pathlib import Path
from typing import Any
from typing import cast

import requests

from django.core.management.base import BaseCommand
from ping3 import ping


logger = logging.getLogger(__name__)


def measure_ping(host: str) -> float:
    return cast(float, ping(host).latency)


def measure_download_speed(url: str) -> float:
    start_time = time.time()

    response = requests.get(url, timeout=5)
    # Create downloads directory if it doesn't exist
    download_dir = Path("downloads")
    download_dir.mkdir(exist_ok=True)

    file_path = download_dir / "downloaded_file.bin"

    # Download the file in chunks and measure
    chunk_size = 8192
    total_size = 0

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                total_size += len(chunk)

    end_time = time.time()
    duration = end_time - start_time

    # Calculate speed in MB/s
    speed = (total_size / 1024 / 1024) / duration

    logger.info("Download completed:")
    logger.info("Total size: %.2f MB", total_size / 1024 / 1024)
    logger.info("Time taken: %.2f seconds", duration)
    logger.info("Average speed: %.2f MB/s", speed)

    return duration


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

        # Get ping and download speeds
        server_metrics = {
            server: {
                "ping": measure_ping(server),
                "download": measure_download_speed(server + "/connection_probe"),
            }
            for server in test_servers
        }

        # Sort servers by download speed (highest to lowest)
        sorted_by_download = sorted(
            server_metrics.items(),
            key=lambda x: x[1]["download"],
            reverse=True,
        )

        # Check first three servers for better combined metrics
        best_server = sorted_by_download[0][0]  # Default to fastest download
        best_download = sorted_by_download[0][1]["download"]
        best_ping = sorted_by_download[0][1]["ping"]

        for server, metrics in sorted_by_download[:3]:
            # If we find a server with better ping AND download, use it
            if metrics["ping"] < best_ping and metrics["download"] > best_download:
                best_server = server
                break

        return best_server
