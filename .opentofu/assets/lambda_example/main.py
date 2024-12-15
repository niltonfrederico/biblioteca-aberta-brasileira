import json
import os

from typing import Any


def handler(event: dict, _: Any) -> dict:  # noqa: ANN401
    environment = os.environ.get("ENVIRONMENT", "development")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(
            {
                "message": f"Hello from BAB Admin ({environment} environment)!",
                "environment": environment,
                "event": event,
            },
        ),
    }
