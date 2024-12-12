import os

from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from django.http import JsonResponse
from django.http.request import HttpRequest


def connection_probe(_request: HttpRequest) -> JsonResponse:
    filename = "dummy_5mb.bin"
    file_path = Path(settings.MEDIA_ROOT) / filename

    size = 5 * 1024 * 1024
    file_exists = file_path.exists()

    # Create 5MB of random data
    with open(file_path, "wb") as f:
        if not file_exists:
            f.write(os.urandom(size))  # 5MB of random bytes

        return FileResponse(f, as_attachment=True, filename=filename)
