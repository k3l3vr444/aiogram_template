from dataclasses import dataclass
from pathlib import Path


@dataclass
class Paths:
    root_path: Path

    @property
    def config(self) -> Path:
        return self.root_path / 'config.yaml'
