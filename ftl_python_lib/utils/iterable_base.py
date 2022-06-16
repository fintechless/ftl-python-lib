from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class IterableBase(Base):
    __abstract__ = True

    def _init_keys(self):
        self._keys = [c.name for c in self.__table__.columns]
        self._dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_keys()

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name not in ("_dict", "_keys", "_n") and "_dict" in self.__dict__:
            self._dict[name] = value

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self):
        if self._n >= len(self._keys):
            raise StopIteration
        self._n += 1
        key = self._keys[self._n - 1]
        return (key, self._dict[key])
