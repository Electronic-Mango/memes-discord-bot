class LanguageModel:
    """DB model used for storing languages per Discord channel"""

    def __init__(self, channel_id: int, language: str) -> None:
        self.channel_id = channel_id
        self.language = language

    def __str__(self) -> str:
        return f"{self.channel_id} {self.language}"


class PeriodicModel:
    """DB model used for storing periodic media data per Discord channel"""

    def __init__(self, channel_id: int, interval: int) -> None:
        self.channel_id = channel_id
        self.interval = interval

    def __str__(self) -> str:
        return f"{self.channel_id} {self.interval}"
