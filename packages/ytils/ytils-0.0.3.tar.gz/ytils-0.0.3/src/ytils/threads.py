import threading


class StoppableThread(threading.Thread):

    def __init__(
        self,
        group=None,
        target: callable = None,
        name: str = None,
        args: iter = (),
        kwargs: dict = None,
        *,
        daemon: bool = None,
    ):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._stop_event = threading.Event()

    def run(self):
        if self._target is not None:
            self._target(self, *self._args, **self._kwargs)
        else:
            raise Exception("Missing target")

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()


class ThreadWithResult(threading.Thread):

    def __init__(
        self,
        group=None,
        target: callable = None,
        name: str = None,
        args: iter = (),
        kwargs: dict = None,
        *,
        daemon: bool = None,
    ) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._result = None

    def run(self):
        if self._target is not None:
            self._result = self._target(*self._args, **self._kwargs)
        else:
            raise Exception("Missing target")

    def result(self, start=False, join=False):
        if start:
            self.start()
        if join:
            self.join()
        return self._result


if __name__ == "__main__":
    import time
    t = ThreadWithResult(target=lambda x: x if time.sleep(5) else x * 2, args=(7,))
    t.start()
    t.join()
    result = t.result()
    print(result)
