import logging

from abc import ABC
from typing import Annotated, get_type_hints

from kaya_module_sdk.src.utils.metadata.display_description import DisplayDescription
from kaya_module_sdk.src.utils.metadata.display_name import DisplayName

log = logging.getLogger(__name__)


class Args(ABC):
    _errors: Annotated[
        list,
        DisplayName("Errors"),
        DisplayDescription("Collection of things that went very, very wrong."),
    ]

    def __init__(self):
        self._errors = []

    @property
    def errors(self) -> list[Exception]:
        return self._errors

    def set_errors(self, *values: Exception) -> None:
        self._errors += list(values)

    def metadata(self):
        return get_type_hints(self, include_extras=True)
