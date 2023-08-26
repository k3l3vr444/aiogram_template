from dataclasses import dataclass


@dataclass
class LoggingConfig:
    use_file_handler: bool
