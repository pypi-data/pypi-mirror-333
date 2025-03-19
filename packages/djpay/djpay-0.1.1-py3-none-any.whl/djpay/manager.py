# dj
from django.utils.functional import classproperty

# internal
from .backends.base import BaseBackend
from .errors import PaymentBackendDoesNotExistError


class PayManager(object):
    """PayManager"""

    def __init__(self) -> None:
        self._configs = {
            "zarinpal": {
                "currency": "",
                "merchant_id": "",
                "callback_view_name": "",
            },
        }

    @classproperty
    def backends(cls) -> list:
        from .backends import BACKENDS

        return BACKENDS

    @classproperty
    def backends_as_choices(cls):
        return ((backend.identifier, backend.label) for backend in cls.backends)

    @classmethod
    def get_backend_class(cls, identifier: str):
        for backend in cls.backends:
            if identifier == backend.identifier:
                return backend
        raise PaymentBackendDoesNotExistError

    @property
    def zarinpal_currency(self) -> str:
        return self._configs["zarinpal"]["currency"]

    @zarinpal_currency.setter
    def zarinpal_currency(self, value: str) -> None:
        self._configs["zarinpal"]["currency"] = value

    @property
    def zarinpal_merchant_id(self) -> str:
        return self._configs["zarinpal"]["merchant_id"]

    @zarinpal_merchant_id.setter
    def zarinpal_merchant_id(self, value: str) -> None:
        self._configs["zarinpal"]["merchant_id"] = value

    @property
    def zarinpal_callback_view_name(self):
        return self._configs["zarinpal"]["callback_view_name"]

    @zarinpal_callback_view_name.setter
    def zarinpal_callback_view_name(self, value: str) -> None:
        self._configs["zarinpal"]["callback_view_name"] = value

    def get_backend(self, identifier: str, config: dict | None = None) -> BaseBackend:
        # get backend class
        backend_class = self.get_backend_class(identifier)
        # get manager_config by given identifier
        manager_config = self._configs.get(identifier, {})
        # update manager_config by given config if any
        if config:
            manager_config.update(config)

        return backend_class(manager_config)
