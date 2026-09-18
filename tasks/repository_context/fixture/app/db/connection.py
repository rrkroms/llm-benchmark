from contextlib import contextmanager


class Database:
    def __init__(self, url):
        self.url = url

    @contextmanager
    def transaction(self):
        try:
            yield self
        except Exception:
            self.rollback()
            raise
        else:
            self.commit()

    def commit(self):
        pass

    def rollback(self):
        pass
