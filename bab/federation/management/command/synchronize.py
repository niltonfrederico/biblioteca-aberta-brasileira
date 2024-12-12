import argparse

from numbers import Number
from typing import Any

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Synchronizes data with dry run option"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run in dry run mode without making actual changes",
        )

    def handle(self, *_args: list[Any], **options: dict[str, str | Number]) -> None:
        dry_run = options["dry_run"]

        if dry_run:
            self.stdout.write("Running in dry run mode...")
        else:
            self.stdout.write("Running in actual mode...")
