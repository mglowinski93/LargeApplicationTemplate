import threading

from sqlalchemy.orm import session

from modules.common.time import (
    convert_timestamp_to_utc_timestamp,
    get_current_timestamp,
)


def get_current_utc_timestamp():
    return convert_timestamp_to_utc_timestamp(get_current_timestamp())


class TestThread(threading.Thread):
    __test__ = False

    def run(self):
        self.exc = None

        try:
            if hasattr(self, "_Thread__target"):
                self.ret = self._Thread__target(
                    *self._Thread__args, **self._Thread__kwargs
                )
            else:
                self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as err:
            self.exc = err
        finally:
            session.close_all_sessions()

    def join(self, timeout=None):
        super(TestThread, self).join(timeout)

        if self.exc:
            raise self.exc

        return self.ret
