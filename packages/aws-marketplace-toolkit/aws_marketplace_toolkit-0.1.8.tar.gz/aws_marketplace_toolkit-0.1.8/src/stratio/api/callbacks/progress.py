# src/stratio/api/callbacks/progress.py
from typing import Protocol

from colorama import Fore, Style
from rich.console import Console
from tqdm import tqdm


class ProgressCallback(Protocol):
    def info(self, message: str, current: int, total: int) -> None: ...

    def warn(self, message: str, current: int, total: int) -> None: ...

    def trace(self, message: str, current: int, total: int) -> None: ...


class TqdmProgressReporter:
    def __init__(self, progress_bar: tqdm, progress_label: str, console: Console):
        """
        Progress reporter for tqdm library.
        :param progress_bar:    a tqdm progress bar instance.
        :param progress_label:  a descriptive label for the progress bar.
        :param console:         a rich console instance.
        """
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        self.progress_bar.set_description_str(self.progress_label)
        self.console = console

    def info(self, message: str, current: int, total: int) -> None:
        self._progress_update(current, total)
        formatted_message = f"{Fore.WHITE}{message}{Style.RESET_ALL}"
        tqdm.write(formatted_message)

    def warn(self, message: str, current: int, total: int) -> None:
        self._progress_update(current, total)
        formatted_message = f"{Fore.YELLOW}{message}{Style.RESET_ALL}"
        tqdm.write(formatted_message)

    def trace(self, message: str, current: int, total: int) -> None:
        self._progress_update(current, total)
        formatted_message = f"{Fore.LIGHTBLACK_EX}{message}{Style.RESET_ALL}"
        tqdm.write(formatted_message)

    def _progress_update(self, current: int, total: int):
        # Update progress bar total if needed.
        if total > self.progress_bar.total:
            self.progress_bar.total = total
        self.progress_bar.n = current
        self.progress_bar.refresh()
