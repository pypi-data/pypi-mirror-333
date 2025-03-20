from concurrent.futures import CancelledError, Future
from typing import Any, Callable, TypeVar


T = TypeVar("T")
U = TypeVar("U")

class PollingOperation(Future[U]):
    """Encapsulates the asynchronous execution of a callable.

    Supports all methods provided by the :class:`concurrent.futures.Future` class. :class:`PollingOperation` instances
    are not intended to be created directly.

    :param: transformer - a callable that is executed with the result of the delegated future as an argument.
        The result of the callable is accessible via the :func:`result` method.
    """

    def __init__(self, delegate: Future[T], transformer: Callable[[T], U]) -> None:
        self._delegate = delegate
        self._transformer = transformer
        super().__init__()
        delegate.add_done_callback(self._callback)

    def cancel(self) -> bool:
        if not self._delegate.cancel():
            return False
        return super().cancel()

    def _callback(self, _: Any) -> None:
        try:
            result = self._delegate.result()
            self.set_result(self._transformer(result))
        except CancelledError:
            return  # do nothing
        except Exception as e:
            self.set_exception(e)
