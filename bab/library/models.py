from django.contrib.postgres.indexes import BrinIndex
from django.db import models

from bab.core.models import BaseModel


class Works(BaseModel):
    class WorkType(models.TextChoices):
        BOOK = "book"
        MANUSCRIPT = "manuscript"
        PUBLICATION = "publication"
        MAGAZINE = "magazine"

    state = models.ForeignKey("federation.State", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    published_date = models.DateField(null=True)
    type = models.CharField(max_length=11, choices=WorkType.choices)
    description = models.TextField(blank=True)
    registration_id = models.CharField(max_length=255, blank=True)  # ISBN and others
    publisher = models.CharField(max_length=255, blank=True)
    pages = models.IntegerField(default=1)
    file = models.CharField(max_length=255, blank=True)
    cover = models.CharField(max_length=255, blank=True)
    last_synced_at = models.DateTimeField(null=True)
    last_sync_data = models.JSONField(default=dict)

    class Meta:
        indexes = (
            models.Index(fields=["state"], name="idx_state_id"),
            models.Index(fields=["author"], name="idx_author"),
            BrinIndex(fields=["published_date"], name="idx_published_date"),
            models.Index(fields=["type"], name="idx_type"),
        )
