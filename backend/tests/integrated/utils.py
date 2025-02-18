import threading


from sqlalchemy.orm import Session


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
            Session.close()

    def join(self, timeout=None):
        super(TestThread, self).join(timeout)

        if self.exc:
            raise self.exc

        return self.ret
