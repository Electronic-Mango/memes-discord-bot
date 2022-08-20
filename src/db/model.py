class LanguageModel:
    """DB model used for storing languages per Discord channel"""

    def __init__(self, channel_id: int, language: str) -> None:
        self.channel_id = str(channel_id)
        self.language = language

    def __str__(self) -> str:
        return f"{self.channel_id} {self.language}"
