from bab.core.dataclass import ServerNode


class ServerSelector:
    def __init__(
        self,
        ping_weight: float = 0.4,
        download_weight: float = 0.6,
        connection_impact: float = 0.1,
    ) -> None:
        self.ping_weight = ping_weight
        self.download_weight = download_weight
        self.connection_impact = connection_impact

    def normalize_ping(self, ping_ms: float) -> float:
        """Convert ping to a score where lower ping = higher score"""
        return 1000 / (ping_ms + 1)  # Adding 1 to avoid division by zero

    def normalize_speed(self, speed_mbps: float, max_speed: float) -> float:
        """Normalize download speed to a 0-1 scale"""
        return speed_mbps / max_speed

    def calculate_hash_integrity(
        self,
        server_hashes: dict[str, str],
        reference_hashes: dict[str, str],
    ) -> float:
        """Check if all file hashes match the reference"""
        if not server_hashes or not reference_hashes:
            return 0.0

        matches = sum(
            1 for k, v in server_hashes.items() if reference_hashes.get(k) == v
        )
        return matches / len(reference_hashes)

    def calculate_load_factor(self, load_percent: float) -> float:
        """Convert load to a factor where higher load = higher denominator"""
        return 1 + (load_percent / 50)  # Load factor grows linearly

    def calculate_priority_factor(self, rank: int) -> float:
        """Convert priority rank to a multiplier"""
        return 1 + (1 / rank)

    def select_best_server(
        self,
        servers: list[ServerNode],
        reference_hashes: dict[str, str],
    ) -> ServerNode:
        max_speed = max(s.download_speed_mbps for s in servers)
        scores = {}

        for server in servers:
            # Calculate normalized metrics
            ping_score = self.normalize_ping(server.ping_ms)
            speed_score = self.normalize_speed(server.download_speed_mbps, max_speed)

            # Calculate factors
            hash_integrity = self.calculate_hash_integrity(
                server.file_hashes,
                reference_hashes,
            )
            load_factor = self.calculate_load_factor(server.current_load_percent)
            priority_factor = self.calculate_priority_factor(server.priority_rank)

            # Calculate final score using our equation
            network_score = (
                self.ping_weight * ping_score + self.download_weight * speed_score
            )

            score = (
                network_score
                * hash_integrity
                * priority_factor
                / (
                    load_factor
                    * (1 + self.connection_impact * server.active_connections)
                )
            )

            scores[server.id] = score

        # Return the server with the highest score
        best_server_id = max(scores, key=scores.get)
        return next(s for s in servers if s.id == best_server_id)
