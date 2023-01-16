from __future__ import annotations

import abc
from typing import Any


class Record(abc.ABC):
    def dict(self) -> dict[str, Any]:
        raise NotImplementedError

    @staticmethod
    def from_dict(*args, **kwargs) -> Record:
        raise NotImplementedError

    @staticmethod
    def new(*args, **kwargs) -> Record:
        raise NotImplementedError
