import threading


class ReadWriteLockManager:
    def __init__(self):
        self._readers = 0
        self._writer = False
        self._lock = threading.Condition()

    def acquire_read_lock(self):
        with self._lock:
            while self._writer:
                self._lock.wait()
            self._readers += 1

    def release_read_lock(self):
        with self._lock:
            self._readers -= 1
            if self._readers == 0:
                self._lock.notify_all()

    def acquire_write_lock(self):
        with self._lock:
            while self._readers > 0:
                self._lock.wait()
            self._writer = True

    def release_write_lock(self):
        with self._lock:
            self._writer = False
            self._lock.notify_all()


