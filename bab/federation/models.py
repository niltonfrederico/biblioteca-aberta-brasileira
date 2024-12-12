import uuid

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import BrinIndex
from django.db import models

from bab.core.models import BaseModel


class Federation(BaseModel):
    last_active_node_count = models.IntegerField(default=0)
    total_publications = models.IntegerField(default=0)
    main_host = models.CharField(max_length=255)
    standby_hosts = ArrayField(models.CharField(max_length=255), default=list)
    last_healthcheck = models.JSONField(default=dict)
    last_update_checksum = models.JSONField(default=dict)
    public_key = models.TextField(unique=True)


class State(BaseModel):
    federation = models.ForeignKey(Federation, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    main_host = models.CharField(max_length=255)
    standby_hosts = ArrayField(models.CharField(max_length=255), default=list)
    last_healthcheck = models.DateTimeField(null=True)
    last_update_checksum = models.JSONField(default=dict)
    public_key = models.TextField(unique=True)

    class Meta:
        indexes = (
            models.Index(fields=["is_active"], name="idx_is_active"),
            BrinIndex(fields=["last_healthcheck"], name="idx_last_healthcheck"),
            models.Index(
                fields=["last_update_checksum"],
                name="idx_last_update_checksum",
            ),
        )


class StateSync(BaseModel):
    class SyncStatus(models.TextChoices):
        SCHEDULED = "scheduled"
        ONGOING = "ongoing"
        FAILURE = "failure"
        SUCCESS = "success"
        DELAYED = "delayed"

    state = models.ForeignKey(State, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=SyncStatus.choices,
        default=SyncStatus.SCHEDULED,
    )
    status_details = models.TextField(blank=True)
    scheduled_for = models.DateTimeField()
    completed_at = models.DateTimeField(null=True)
    last_state = models.JSONField(default=dict)
    current_state = models.JSONField(default=dict)

    class Meta:
        indexes = (
            models.Index(fields=["state"], name="idx_state_id"),
            models.Index(fields=["status"], name="idx_status"),
        )


class StateHealthcheck(BaseModel):
    class HealthcheckStatus(models.TextChoices):
        UNHEALTHY = "unhealthy"
        HEALTHY = "healthy"
        UNREACHABLE = "unreachable"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=HealthcheckStatus.choices)
    duration = models.DateTimeField()
    last_state = models.JSONField(default=dict)
    current_state = models.JSONField(default=dict)

    class Meta:
        indexes = (
            models.Index(fields=["state"], name="idx_state_id"),
            models.Index(fields=["status"], name="idx_status"),
        )
