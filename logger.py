import logging


class Logger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)

        