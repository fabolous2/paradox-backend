from dataclasses import dataclass

@dataclass(frozen=True)
class Game:
    id: int
    name: str
    image_url: str
