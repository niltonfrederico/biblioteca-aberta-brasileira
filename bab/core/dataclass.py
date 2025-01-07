from dataclasses import dataclass


@dataclass
class ServerNode:
    id: str
    ping_ms: float
    download_speed_mbps: float
    current_load_percent: float
    priority_rank: int  # 1 is highest priority
    active_connections: int
    file_hashes: dict[str, str]
